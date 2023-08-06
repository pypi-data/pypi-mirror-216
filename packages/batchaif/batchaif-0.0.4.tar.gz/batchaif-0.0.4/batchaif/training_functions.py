# Import file managing library
import os
import random

# Import time and random
import time

# Import numpy and pandas
import numpy as np
import pandas as pd
import torch
from torch import nn
from torch.nn import functional as F
from torch import optim
from torch.autograd import Variable
from torch.backends import cudnn
from torch.utils.data import DataLoader

# Import useful functions
from batchaif.dataload import Biodataset
from batchaif.weighting_functions import update_losses_weights
from batchaif.metrics_functions import compute_and_plot_best_clustering
from batchaif.model_auxiliary_functions import plot_losses_panel, plot_weights_panel, sample_z
from batchaif.batch_removal_functions import batch_removal_conditional_robust


# Function to reset weights of a model
def reset_weights(model, seed=42):
    """
    Function to reset the weights of each layer of a Neural Network model.
    Args:
        model:      torch Neural Network, model whose weights need to be reinitialized.
        seed:       int, seed used for setting the randomness when resetting the model's parameters, default=42.

    """

    # Setting randomness
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)

    for m in list(model.children()):
        if isinstance(m, nn.Conv2d) or isinstance(m, nn.Linear):
            m.reset_parameters()
        elif hasattr(m, 'children'):
            reset_weights(m)
        elif isinstance(m, nn.Sequential):
            reset_weights(m)


# Function to get default weights
def get_default_weights(model, weighting_strategy=None, projection_constraint=False, variance_constraint=False,
                        mse_rel=False):
    """
    Function to get the default initialization of the losses' weights.
    Args:
        model:                  dictionary containing torch Neural Network blocks for AIF model (CVAE, Auxiliary,
                                Discriminator).
        weighting_strategy:     str, weighting strategy to use for losses' weights, default=None.
        projection_constraint:  dictionary, whether to use average and random projection constraints, default=None.
        variance_constraint:    bool, whether to use variance constraint, default=False.
        mse_rel:                bool, whether to use MSE on genes' relative expression, default=False.

    Returns:    losses_weights, dictionary containing the initial losses' weights.

    """

    # Setting default weights
    if weighting_strategy in ['rel', 'norm']:
        losses_enc_weights = {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1, 'class_rec': 0.1, 'aux': 1, 'gen': 0.1}
    else:
        losses_enc_weights = {'mse': 1, 'kl': 1, 'mmd': 1, 'class': 1, 'class_rec': 1, 'aux': 1, 'gen': 1}

    # Removing unused latent loss
    if 'cvae' in model.keys() and not model['cvae'].variational or 'kl' not in model['cvae'].latent_loss:
        losses_enc_weights.pop('kl')
    if 'cvae' in model.keys() and not model['cvae'].variational or 'mmd' not in model['cvae'].latent_loss:
        losses_enc_weights.pop('mmd')

    # Adding other constraints
    if projection_constraint is not None:
        losses_enc_weights.update({'proj': 0.1})
    if variance_constraint:
        losses_enc_weights.update({'var': 0.1})
    if mse_rel:
        losses_enc_weights.update({'mse_rel': 0.2})

    # Returning default weights
    return losses_enc_weights


# Function to print training info
def print_training_info(losses, n_samples, elapsed_time, e=None, end_epoch=None):
    """
    Function to print training information.
    Args:
        losses:         dictionary containing losses values.
        n_samples:      int, total number of samples.
        elapsed_time:   float, elapsed time.
        e:              int, current epoch, default=None.
        end_epoch:      int, ending epoch, default=None.

    """

    # Retrieving the losses' name to display info on
    losses_not_display = ['auxEnc', 'gen', 'total_no_rel', 'total_no_rel_scaled']
    losses_name = [name for name in losses.keys() if name not in losses_not_display]

    # Creating the message's
    if e is not None and end_epoch is not None:
        msg = '[%d, %d] '
        msg_info = (e, end_epoch)
    else:
        msg = ''
        msg_info = ()
    for name in losses_name:
        msg += f'{name}: %0.5f, '
        msg_info = (*msg_info, losses[name] / n_samples)
    msg += 'time: %0.3f'
    msg_info = (*msg_info, elapsed_time)

    # Printing message
    print(msg % msg_info)


# Function to compute the losses
def compute_loss(model, x, y, x_rec, mu, log_var, y_pred, y_rec, losses_name, projection_constraint=None,
                 variance_constraint=False, mse_rel=False, device='cuda'):
    """
    Function to compute the losses: MSE, KL and / or MMD, classification losses, projection loss, variance loss, MSE on
    gens' relative expression.
    Args:
        model:                      dictionary containing torch Neural Network blocks for AIF model (CVAE, Auxiliary,
                                    Discriminator).
        x:                          torch.Tensor,size (batch_size, n_features), original data.
        y:                          torch.Tensor, size (batch_size, 1), original batch labels.
        x_rec:                      torch.Tensor, size (batch_size, n_features), reconstructed data.
        mu:                         torch.Tensor, size (batch_size, n_z), encoded mean of latent space.
        log_var:                    torch.Tensor, size (batch_size, n_z), encoded log variance of latent space.
        y_pred:                     torch.Tensor, size (batch_size, n_labels), predicted one hot encoded batch labels.
        y_rec:                      torch.Tensor, size (batch_size, n_labels), predicted one hot encoded batch labels
                                    using reconstruction.
        losses_name:                list of str, list of losses' name.
        projection_constraint:      dictionary of bool, whether to use average and random projection constraints,
                                    default=None.
        variance_constraint:        bool, whether to use variance constraint, default=False.
        mse_rel:                    bool, whether to use MSE on genes' relative expression, default=False.
        device:                     str, device to use, default='cuda'.

    Returns:   losses, dictionary containing all the losses.

    """

    # Initialization of losses dictionary to store the results
    losses = dict(zip(losses_name, [0 for _ in range(len(losses_name))]))

    # Compute encoder's losses (MSE, KL and or MMD, classification and classification after reconstruction losses)
    (losses['mse'], losses['kl'], losses['mmd'],
     losses['class'], losses['class_rec']) = model['cvae'].loss(x_rec=x_rec, x=x, y_pred=y_pred,
                                                                y=y, y_rec=y_rec, mu=mu, log_var=log_var)

    # Compute auxiliary classification loss for the cvae loss and for auxiliary network
    # To train the encoder to fool the auxiliary network
    if 'aux' in model.keys():
        z = model['cvae'].re_param(mu=mu, log_var=log_var)
        losses['auxEnc'] = model['aux'].loss(model['aux'](z), y.to(device))  # For encoder loss
        losses['aux'] = model['aux'].loss(model['aux'](z.detach()),
                                          y.to(device))  # Detaching z to update only aux network

    # Compute the discriminator classification loss
    if 'dis' in model.keys():
        # Compute loss for discriminator network
        p_xreal = model['dis'](x)
        p_xfake_rec = model['dis'](x_rec.detach())  # Detaching reconstruction to update only discriminator
        z_rand = sample_z(x.size(0), mu.size(1), device)
        y_rand = y
        p_xfake_rand = model['dis'](model['cvae'].decoder(y_rand, z_rand).detach())
        fake_label = Variable(torch.Tensor(p_xreal.size()).zero_()).type_as(p_xreal).to(device)
        real_label = Variable(torch.Tensor(p_xreal.size()).fill_(1)).type_as(p_xreal).to(device)
        losses['dis'] = 0.3 * (
                model['dis'].loss(pred=p_xreal, target=real_label) +  # BCE between reconstruction and true labels
                model['dis'].loss(pred=p_xfake_rec, target=fake_label) +  # BCE between reconstruction and fake labels
                model['dis'].loss(pred=p_xfake_rand, target=fake_label))  # BCE between random reconstruction and fake

        # Compute the generator loss for the cvae total loss
        p_xfake_rec = model['dis'](x_rec)
        p_xfake_rand = model['dis'](model['cvae'].decoder(y_rand, z_rand))
        losses['gen'] = 0.5 * (
                model['dis'].loss(p_xfake_rec, real_label) +  # BCE between reconstruction and real labels
                model['dis'].loss(p_xfake_rand, real_label))  # BCE between random reconstruction and real labels

    # Compute projection constraint
    if projection_constraint is not None:
        proj_loss = 0
        z = model['cvae'].re_param(mu=mu, log_var=log_var)

        # Projection on average batch label
        if 'avg' in projection_constraint.keys() and projection_constraint['avg']:
            y_avg = (torch.ones(y.size()) /
                     y.size(1)).to(device)  # Generating average batch label
            x_avg = model['cvae'].decoder(y_avg, z)  # Reconstructing data for average batch
            proj_loss += F.cosine_similarity(x, x_avg).sum()  # Computing cosine similarity

        # Projection on a randomly chosen batch
        if 'random' in projection_constraint.keys() and projection_constraint['random']:
            y_ind_rand = (torch.where(y > 0)[1] +
                          torch.randint(1, model['cvae'].n_labels,  # Generating random batch label
                                        (y.shape[0],),
                                        device=device)) % model['cvae'].n_labels
            y_rand = torch.zeros(y.shape, device=device)
            y_rand[range(y.shape[0]), y_ind_rand] = 1
            x_rand = model['cvae'].decoder(y_rand, z)  # Reconstructing data for random batch
            proj_loss += F.cosine_similarity(x, x_rand).sum()  # Computing cosine similarity

        # Storing projection loss
        losses['proj'] = proj_loss

    # Compute variance constraint
    if variance_constraint:
        losses['var'] = F.mse_loss(x_rec.std(dim=-1), x.std(dim=-1))

    # Compute MSE on genes relative expression
    if mse_rel:
        losses['mse_rel'] = F.mse_loss(F.softmax(x_rec, dim=-1), F.softmax(x, dim=-1))

    # Returning the losses
    return losses


# Function to train the model
def train_model(model, optimizer, train_loader, end_epoch, start_epoch=0,
                out_dir_name='./results', plot=True, losses_enc_weights=None, weighting_strategy=None,
                losses_norm=None, save=None, verbose=True, print_every=1, device='cpu', early_stopping=True,
                min_epochs=10, dynamic_ratio=1.0, class_weights=None, grad_clip=None, scheduler=None,
                decay_factor=0.999, start_decay=0, end_decay=-1, projection_constraint=None, variance_constraint=False,
                mse_rel=False, update_dis_freq=None, update_aux_freq=None, seed=42, best_total_loss=None,
                *args, **kwargs):
    """
    Function to train the AIF model (cVAE + GAN + Auxiliary network).
    Args:
        model:                 dictionary containing torch Neural Networks (CVAE, Auxiliary and Discriminator).
        optimizer:             dictionary containing torch optimizers for CVAE, Auxiliary and Discriminator models.
        train_loader:          torch dataloader, train dataloader created based on the Biodataset class.
        end_epoch:             int, ending epoch number.
        start_epoch:           int, starting epoch number, default=0.
        out_dir_name:          str, path to the directory where to save the results, default='./results'.
        plot:                  bool, whether to plot the losses' evolution, default=True.
        losses_enc_weights:    dict, weights for each of the encoder's loss in the overall encoder's loss,
                               default=None, corresponding to {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1,
                                                               'class_rec': 0.1, 'aux': 1, 'gen': 0.1}.
        weighting_strategy:    str, weighting strategy to use for encoder's losses' weights, default=None.
        losses_norm:           dict, normalization coefficient or method for each loss to normalize, default=None.
        save:                  dict, saving specifications, default=None,
                               corresponding to {'cvae': True, 'aux': True, 'dis': True, 'loss': True, 'time': True}.
        verbose:               bool, whether to print useful info during training, default=True.
        print_every:           int, frequency of printed info (i.e. number of epochs), default=1.
        device:                str, device used ('cuda' or 'cpu'), default='cpu'.
        early_stopping:        bool, whether to perform early stopping, default=True.
        min_epochs:            int, minimum number of epochs before using early stopping, default=10.
        dynamic_ratio:         float, percentage of data to take into account while reweighing, default=1.
        class_weights:         array, weights for each batch label in case of unbalanced classes, default=None.
        grad_clip:             float, upper bound for gradient clipping, default=None.
        scheduler:             str, lr scheduler to use for encoder, default=None.
        decay_factor:          float, decay factor to use for lr scheduler, default=0.999.
        start_decay:           int, epoch when to start lr scheduler decay, default=0.
        end_decay:             int, epoch when to end lr scheduler decay, default=-1.
        projection_constraint: dict of bools, whether to use projection constraint losses, default=None.
        variance_constraint:   bool, whether to use variance constraint loss, default=False.
        mse_rel:               bool, whether to add MSE loss on genes' relative expression, default=False.
        update_dis_freq:       float, frequency at which to update discriminator network's parameters, default=None.
        update_aux_freq:       float, frequency at which to update auxiliary network's parameters, default=None.
        seed:                  int, seed for setting randomness, default=42.
        best_total_loss:       float, best total loss to compare it to for early stopping, default=None.

    Returns:    (loss, weight), losses and losses' weights history during training stored in a dictionary.

    """

    # Setting randomness
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    torch.set_anomaly_enabled(True)

    # Create a new folder to save results
    if not os.path.isdir(out_dir_name):
        os.mkdir(out_dir_name)

    # Parsing default arguments
    if losses_enc_weights is None:
        losses_enc_weights = get_default_weights(model=model, projection_constraint=projection_constraint,
                                                 variance_constraint=variance_constraint, mse_rel=mse_rel,
                                                 weighting_strategy=weighting_strategy)
    if losses_norm is None:
        losses_norm = {}
    if save is None:
        save = {'cvae': True, 'aux': True, 'dis': True, 'loss': True, 'time': True}
        if weighting_strategy is not None:
            save.update({'weights': True})
    if end_decay == -1:
        end_decay = end_epoch

    # Parsing scheduler arguments
    if scheduler == 'exponential':
        scheduler_enc = torch.optim.lr_scheduler.LambdaLR(
            optimizer['cvae'],
            lambda x: 1 if x + start_epoch < start_decay else (decay_factor ** (x + start_epoch - start_decay)))
    elif scheduler == 'cosine':
        scheduler_enc = torch.optim.lr_scheduler.LambdaLR(
            optimizer['cvae'],
            lambda x: (1 if x + start_epoch < start_decay else
                       (1 - decay_factor * (1 - np.cos((x + start_epoch - start_decay) /
                                                       (end_decay - start_decay - 1) * np.pi / 2)))), last_epoch=-1)
    else:
        scheduler_enc = None

    # Converting the class weights and storing them as models' attribute
    if class_weights is not None:
        model['cvae'].class_weights = torch.Tensor(class_weights).to(device)
        model['aux'].class_weights = torch.Tensor(class_weights).to(device)

    # Initialization of dictionary of losses and defining loss for stopping criterion
    losses_name = ['total'] + list(losses_enc_weights.keys()) + ['auxEnc', 'dis']
    if weighting_strategy is not None:
        losses_name += ['total_no_rel']
        if train_loader.dataset.norm or train_loader.dataset.scaled:
            losses_name += ['total_no_rel_scaled']
            loss_comparison = 'total_no_rel_scaled'
        else:
            loss_comparison = 'total_no_rel'
    else:
        loss_comparison = 'total'
    if (weighting_strategy == 'norm') and (losses_norm is not None) and (len(losses_norm) > 0):
        losses_name += [f'{loss}_norm' if loss != 'aux' else f'{loss}Enc_norm' for loss in losses_norm.keys()]
    losses = dict(zip(losses_name, [[] for _ in range(len(losses_name))]))

    # Converting losses adversarial weights
    losses_enc_weights_copy = losses_enc_weights.copy()
    if 'aux' in losses_enc_weights_copy.keys():
        losses_enc_weights_copy['auxEnc'] = -abs(losses_enc_weights_copy['aux'])
        losses_enc_weights_copy.pop('aux')
    if 'proj' in losses_enc_weights_copy.keys():
        losses_enc_weights_copy['proj'] = -abs(losses_enc_weights_copy['proj'])

    # Initialization of a variable to store best total loss
    if best_total_loss is None:
        best_total_loss = np.inf

    # Starting timer
    start_time = time.time()

    # Parsing the models to the right processor and specifying training step of model
    for key in model.keys():
        model[key] = model[key].to(device)
        model[key].train()

    # Initialization of norm coefficients for the losses during optimization
    if len(losses_norm) > 0:
        losses_norm_copy = losses_norm.copy()
        if 'aux' in losses_norm.keys():
            losses_norm_copy['auxEnc'] = losses_norm_copy['aux']
            losses_norm_copy.pop('aux')
        norm_coef = dict(zip(list(losses_norm_copy.keys()) +
                             list((set(losses_enc_weights_copy.keys()) - set(losses_norm_copy.keys()))),
                             [losses_norm_copy[key] if (isinstance(losses_norm_copy[key], float) or
                                                        isinstance(losses_norm_copy[key], int))
                              else 1 for key in losses_norm_copy.keys()] +
                             [1 for _ in set(losses_enc_weights_copy.keys()) - set(losses_norm_copy.keys())]))
    else:
        norm_coef = dict(zip(list(losses_enc_weights_copy.keys()), [1 for _ in losses_enc_weights_copy.keys()]))

    # Initialization of a dictionary to store the weights
    if weighting_strategy is not None:
        weights_history = dict(zip(norm_coef.keys(), [[norm_coef[key]] for key in norm_coef.keys()]))

    # Initialization of final norm coefficients for determining best model
    if loss_comparison.casefold() == 'total_no_rel_scaled'.casefold():
        final_norm_coef = dict(zip(list(losses_enc_weights_copy.keys()), [1 for _ in losses_enc_weights_copy.keys()]))
    else:
        final_norm_coef = None

    # Training the model
    for e in range(start_epoch, end_epoch):

        # Initialization of the number of samples
        n_samples = 0

        # Initialization of losses for this epoch
        epoch_losses = dict(zip(losses_name, [0 for _ in range(len(losses_name))]))

        # For each, batch train the models
        for i, data in enumerate(train_loader):

            # Retrieving the data and the label
            x = data[0].view(data[0].size(0), -1).to(device)
            y = data[1].view(data[1].size(0), -1).type(torch.FloatTensor).to(device)

            # Forward propagating the input through the encoder and decoder
            x_rec, mu, log_var, y_pred = model['cvae'](x)
            _, _, y_rec = model['cvae'].encoder(x_rec)

            # Computing the losses
            batch_losses = compute_loss(model=model, x=x, y=y, x_rec=x_rec, mu=mu, log_var=log_var,
                                        y_pred=y_pred, y_rec=y_rec, losses_name=losses_name,
                                        projection_constraint=projection_constraint,
                                        variance_constraint=variance_constraint, mse_rel=mse_rel,
                                        device=device)

            # Compute total encoder's loss
            for loss_name in losses_enc_weights_copy.keys():
                batch_losses['total'] += (losses_enc_weights_copy[loss_name] * batch_losses[loss_name] *
                                          norm_coef[loss_name])
                if weighting_strategy is not None:
                    if weighting_strategy in ['rel', 'norm']:
                        batch_losses['total_no_rel'] += losses_enc_weights_copy[loss_name] * batch_losses[loss_name]
                        if loss_comparison.casefold() == 'total_no_rel_scaled'.casefold():
                            batch_losses['total_no_rel_scaled'] += (
                                    losses_enc_weights_copy[loss_name] * batch_losses[loss_name] *
                                    final_norm_coef[loss_name])
                    else:
                        batch_losses['total_no_rel'] += batch_losses[loss_name]
                        if loss_comparison.casefold() == 'total_no_rel_scaled'.casefold():
                            batch_losses['total_no_rel_scaled'] += (batch_losses[loss_name] *
                                                                    final_norm_coef[loss_name])

            # Optimizer step
            for key in optimizer.keys():
                optimizer[key].zero_grad()
                if key == 'cvae':
                    batch_losses['total'].backward()
                elif ((key == 'aux' and not (update_aux_freq is None or
                                             (e + 1) % int(update_aux_freq * end_epoch) == 0)) or
                      (key == 'dis' and not (update_dis_freq is None or
                                             (e + 1) % int(update_dis_freq * end_epoch) == 0))):
                    continue
                else:
                    batch_losses[key].backward()
                if grad_clip is not None:
                    torch.nn.utils.clip_grad_norm_(model['key'].parameters(), max_norm=grad_clip)
                optimizer[key].step()

            # Add loss to epoch's loss
            for key in losses_name:
                if 'norm' not in key:
                    epoch_losses[key] += batch_losses[key].item()

            # Updating the number of samples
            n_samples += data[0].size(0)

        # Updating lr scheduler decay
        if (scheduler_enc is not None) and (e <= end_decay):
            scheduler_enc.step()

        # Printing verbose
        if verbose:
            if (e == 1) | ((e + 1) % print_every == 0):
                print_training_info(e=e, end_epoch=end_epoch, losses=epoch_losses, n_samples=n_samples,
                                    elapsed_time=(time.time() - start_time))

        # Adding epoch's loss to losses history
        for key in losses.keys():

            # Adding normalized epoch's loss to losses history
            if 'norm' in key:
                losses[key].append(epoch_losses['_'.join(key.split('_')[0:-1])] /
                                   n_samples * norm_coef['_'.join(key.split('_')[0:-1])])

            # Adding unnormalized epoch's loss to losses history
            else:
                losses[key].append(epoch_losses[key] / n_samples)

        # Updating the normalization weights using weighting strategy and storing its value
        if weighting_strategy is not None:
            if e > start_epoch:
                norm_coef = update_losses_weights(losses_history=losses,
                                                  weighting_strategy=weighting_strategy,
                                                  losses_included=norm_coef.keys(),
                                                  dynamic_ratio=dynamic_ratio, *args, **kwargs)
            for key in weights_history.keys():
                weights_history[key].append(norm_coef[key])

        # Updating the final normalization weights median at min epoch
        if (loss_comparison.casefold() == 'total_no_rel_scaled'.casefold()) and e == max(start_epoch, min_epochs - 1):
            for key in losses_enc_weights_copy.keys():
                if np.median(losses[key]) != 0:
                    final_norm_coef[key] = np.median(losses['mse']) / (np.median(losses[key]))
                else:
                    final_norm_coef[key] = 1

        # Saving models parameters
        if early_stopping and (e >= max(start_epoch, min_epochs)):
            if losses[loss_comparison][-1] < best_total_loss:
                best_total_loss = losses[loss_comparison][-1]
                for key in model.keys():
                    if save[key]:
                        model[key].save_params(ex_dir=out_dir_name)
        else:
            for key in model.keys():
                if save[key]:
                    model[key].save_params(ex_dir=out_dir_name)

    # Plotting losses evolution
    if plot:
        plot_losses_panel(losses, ex_dir=out_dir_name)
        if weighting_strategy is not None:
            plot_weights_panel(weights=weights_history, ex_dir=out_dir_name)

    # Adding time information
    if save['time']:
        losses['time'] = time.time() - start_time

    # Saving losses
    if save['loss']:
        pd.DataFrame(losses).to_csv(f'{out_dir_name}/losses.csv', index=False)

    # Saving weights
    if weighting_strategy is not None and 'weights' in save.keys() and save['weights']:
        pd.DataFrame(weights_history).to_csv(f'{out_dir_name}/weights.csv', index=False)

    # Returning trained cvae and losses
    return losses, norm_coef


# Function to test the model
def test_model(model, test_loader, out_dir_name='./results', norm_coef=None,
               losses_enc_weights=None, weighting_strategy=None, projection_constraint=None,
               variance_constraint=False, mse_rel=False, save=None, verbose=True, device='cpu',
               *args, **kwargs):
    """
    Function to evaluate the AIF model (cVAE + GAN + Auxiliary network) on the test dataset.
    Args:
        model:                  dictionary containing torch Neural Networks for AIF model (CVAE, Auxiliary,
                                Discriminator).
        test_loader:            torch dataloader, test dataloader created based on the Biodataset class.
        out_dir_name:           str, path to the directory where to save the results, default='./results'.
        norm_coef:              dict, norm coefficient for each loss to normalize, default=None.
        losses_enc_weights:     dict, weights for each of the encoder's loss in the overall encoder's loss,
                                default=None, corresponding to {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1,
                                                                'class_rec': 0.1, 'aux': 1, 'gen': 0.1}.
        weighting_strategy:     str, weighting_strategy to use for the losses' weights, default=None.
        projection_constraint:  dict of bools, whether to use projection constraint losses, default=None.
        variance_constraint:    bool, whether to use variance constraint loss, default=False.
        mse_rel:                bool, whether to use MSE loss on genes' relative expression, default=False.
        save:                   dict, saving specifications, default=None, corresponding to {'loss': True,
                                'time': True}.
        verbose:                bool, whether to print useful info during training, default=True.
        device:                 str, device used ('cuda' or 'cpu'), default='cpu'.

    Returns:    loss, losses evaluated on the test set stored in a dictionary.

    """

    # Create a new folder to save results
    if not os.path.isdir(out_dir_name):
        os.mkdir(out_dir_name)

    # Parsing default arguments
    if losses_enc_weights is None:
        losses_enc_weights = get_default_weights(model=model, weighting_strategy=weighting_strategy,
                                                 projection_constraint=projection_constraint,
                                                 variance_constraint=variance_constraint, mse_rel=mse_rel)
    if save is None:
        save = {'cvae': True, 'aux': True, 'dis': True, 'loss': True, 'time': True}

    # Initialization of dictionary of losses
    losses_name = ['total'] + list(losses_enc_weights.keys()) + ['auxEnc', 'dis']
    if weighting_strategy is not None:
        losses_name += ['total_no_rel']
    if norm_coef is not None:
        losses_name += [f'{loss}_norm' if loss != 'aux' else f'{loss}Enc_norm' for loss in norm_coef.keys()]
    else:
        norm_coef = {}
    losses = dict(zip(losses_name, [[] for _ in range(len(losses_name))]))

    # Converting losses adversarial weights
    losses_enc_weights_copy = losses_enc_weights.copy()
    losses_enc_weights_copy['auxEnc'] = -abs(losses_enc_weights_copy['aux'])
    losses_enc_weights_copy.pop('aux')
    if projection_constraint is not None:
        losses_enc_weights_copy['proj'] = -abs(losses_enc_weights_copy['proj'])

    # Initialization of the number of samples
    n_samples = 0

    # Starting timer
    start_time = time.time()

    # Parsing the models to the right processor and specifying evaluation step
    for key in model.keys():
        model[key] = model[key].to(device)
        model[key].eval()

    # Initialization of losses for this epoch
    epoch_losses = dict(zip(losses_name, [0 for _ in range(len(losses_name))]))

    # Evaluating the model
    with torch.no_grad():

        # For each batch, feedforward the samples to the model
        for i, data in enumerate(test_loader):

            # Retrieving the data and the label
            x = data[0].view(data[0].size(0), -1).to(device)
            y = data[1].view(data[1].size(0), -1).type(torch.FloatTensor).to(device)

            # Forward propagating the input throughout the encoder and the decoder
            x_rec, mu, log_var, y_pred = model['cvae'](x)
            _, _, y_rec = model['cvae'].encoder(x_rec)

            # Computing losses
            batch_losses = compute_loss(model, x=x, y=y, x_rec=x_rec, mu=mu, log_var=log_var, y_pred=y_pred,
                                        y_rec=y_rec, losses_name=losses_name,
                                        projection_constraint=projection_constraint,
                                        variance_constraint=variance_constraint, mse_rel=mse_rel, device=device)

            # Compute total encoder's loss
            for loss_name in losses_enc_weights_copy.keys():
                batch_losses['total'] += (losses_enc_weights_copy[loss_name] * batch_losses[loss_name] *
                                          norm_coef[loss_name])
                if weighting_strategy is not None:
                    if weighting_strategy in ['rel', 'norm']:
                        batch_losses['total_no_rel'] += losses_enc_weights_copy[loss_name] * batch_losses[loss_name]
                    else:
                        batch_losses['total_no_rel'] += batch_losses[loss_name]

            # Add loss to epoch's loss
            for key in losses_name:
                if 'norm' not in key:
                    epoch_losses[key] += batch_losses[key].item()

            # Adding the samples to the number of samples
            n_samples += data[0].size(0)

    # Printing verbose
    if verbose:
        print_training_info(losses=epoch_losses, n_samples=n_samples,
                            elapsed_time=(time.time() - start_time))

    # Adding epoch's loss to losses history
    for key in losses.keys():
        if 'norm' not in key:
            losses[key].append(epoch_losses[key] / n_samples)

        # Adding normalized epoch's loss to losses history
        else:
            losses[key].append(epoch_losses['_'.join(key.split('_')[0:-1])] /
                               n_samples * norm_coef['_'.join(key.split('_')[0:-1])])

    # Saving losses
    if save['loss']:
        if save['time']:
            losses['time'] = time.time() - start_time
        pd.DataFrame(losses).to_csv(f'{out_dir_name}/losses_test.csv', index=False)

    # Returning losses
    return losses


# Function to run the batch effect pipeline : train the cvae-gan model and remove the batch effect
def run_batch_effect_pipeline(model, adata, batch_size, epochs, lr, beta_1, beta_2, root, results_path,
                              file_name, model_name, losses_enc_weights=None, weighting_strategy=None,
                              losses_norm=None, label_projection=0.5, n_samplings=20, seed=42,
                              norm_data=False, scaled_data=False, log_transfo=False,
                              n_labels=2, save=None, plot=True, saving_path=None, verbose=True,
                              print_every=1, device='cpu', early_stopping=True, min_epochs=10, test=False,
                              dynamic_ratio=1.0, class_weights=None, grad_clip=None, scheduler=None,
                              decay_factor=0.999, start_decay=0, end_decay=-1, projection_constraint=None,
                              variance_constraint=False, mse_rel=False, update_dis_freq=None, update_aux_freq=None,
                              *args, **kwargs):
    """
    Function to run the batch effect pipeline on the AIF model (cVAE + GAN + Auxiliary network):
    training the model, evaluation on the test set, correction of the batch effect.
    Args:
        model:                  dictionary containing torch Neural Networks blocks for AIF model (CVAE, auxiliary,
                                discriminator).
        adata:                  AnnData object, original data containing gene expression and observations.
        batch_size:             int, batch size to use for the data loaders.
        epochs:                 int, number of epochs to run during training.
        lr:                     float, learning rate for the ADAM optimizers.
        beta_1:                 float, beta_1 coefficient in ADAM optimizers.
        beta_2:                 float, beta_2 coefficient in ADAM optimizers.
        root:                   str, path to the preprocessed data directory for the AIF model.
        results_path:           str, path to the parent directory where to save the results.
        file_name:              str, dataset name.
        model_name:             str, model name.
        losses_enc_weights:     dict, weights for each of the encoder's loss in the overall encoder's loss,
                                default=None, corresponding to {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1,
                                                                'class_rec': 0.1, 'aux': 1, 'gen': 0.1}.
        weighting_strategy:     str, weighting strategy to use for the losses' weights, default=None.
        losses_norm:            dict, normalization coefficient or method for the losses to normalize, default=None.
        label_projection:       float, batch label used for batches' distribution projection, default=0.5.
        n_samplings:            int, number of samples to draw from the latent distribution during batch effect
                                correction, default=20.
        seed:                   int, seed used to set the randomness, default=42.
        norm_data:              bool, whether to use the normalized data, default=False.
        scaled_data:            bool, whether to use the scaled data, default=False.
        log_transfo:            bool, whether to apply log1p transformation on the data, default=False.
        n_labels:               int, number of batch labels.
        save:                   dict, saving specifications, default=None,
                                corresponding to {'cvae': True, 'aux': True, 'dis': True, 'loss': True,
                                'corrected_data': True, 'time': True}.
        plot:                   bool, whether to plot the losses evolution or not, default=True.
        verbose:                bool, whether to print useful info during training, default=True.
        saving_path:            str, path where to save the results, default=None.
        verbose:                bool, whether to print useful info during training, default=True.
        print_every:            int, frequency of printed info (e.g. number of epochs), default=1.
        device:                 str, device used ('cuda' or 'cpu'), default='cpu'.
        early_stopping:         bool, whether to perform early stopping, default=True.
        min_epochs:             int, minimum number of epochs before early stopping, default=10.
        test:                   bool, whether to use evaluate the model on the test set, default=False.
        dynamic_ratio:          float, percentage of data to take into account while reweighing, default=1.
        class_weights:          array of size n_labels, weights for each batch label, default=None.
        grad_clip:              float, upper bound for gradient clipping, default=None.
        scheduler:              str, lr scheduler to use for encoder, default=None.
        decay_factor:           float, decay factor to use for lr scheduler, default=0.999.
        start_decay:            int, epoch when to start lr scheduler decay, default=0.
        end_decay:              int, epoch when to end lr scheduler decay, default=-1.
        projection_constraint:  dict of bools, whether to use projection constraint losses, default=None.
        variance_constraint:    bool, whether to use variance constraint loss, default=False.
        mse_rel:                bool, whether to use MSE loss on genes' relative expression, default=False.
        update_dis_freq:        float, frequency at which to update discriminator network's parameters, default=None.
        update_aux_freq:        float, frequency at which to update auxiliary network's parameters, default=None.

    Returns:    AnnData object, batch effect corrected data.

    """

    # Setting randomness
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.enabled = False
    cudnn.deterministic = True

    # Parsing default arguments
    if losses_enc_weights is None:
        losses_enc_weights = get_default_weights(model=model, weighting_strategy=weighting_strategy,
                                                 projection_constraint=projection_constraint,
                                                 variance_constraint=variance_constraint, mse_rel=mse_rel)
    if losses_norm is None:
        losses_norm = {}
    if save is None:
        save = {'cvae': True, 'aux': True, 'dis': True, 'loss': True, 'corrected_data': True, 'time': True}
        if weighting_strategy is not None:
            save.update({'weights': True})

    # Defining loss name for comparison
    if weighting_strategy is not None:
        if norm_data or scaled_data:
            loss_comparison = 'total_no_rel_scaled'
        else:
            loss_comparison = 'total_no_rel'
    else:
        loss_comparison = 'total'

    # Creating corresponding train loader
    print('Prepare data loaders ...')
    train_dataset = Biodataset(root=root, train=True, norm=norm_data, scaled=scaled_data,
                               log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    if test:
        test_dataset = Biodataset(root=root, train=False, norm=norm_data, scaled=scaled_data,
                                  log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
        test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    else:
        test_loader = None
    print('Data loaders ready.\n')

    # Creating corresponding outputs' directory name
    print(f'Trying batch size={batch_size}, lr={lr}, beta1={beta_1}, beta2={beta_2}')
    if saving_path is None:
        out_dir_name = f'{results_path}/{model_name}/bs_{batch_size}_lr_{lr}_beta1_{beta_1}_beta2_{beta_2}/'
    else:
        out_dir_name = saving_path

    # Resetting model's weights
    print('Resetting weights ...')
    for key in model.keys():
        reset_weights(model[key])

    # Creating corresponding optimizers
    print('Creating optimizers ...')
    optimizer = {}
    for key in model.keys():
        optimizer.update({key: optim.Adam(model[key].parameters(), lr=lr, betas=(beta_1, beta_2))})

    # Training the model
    print('Training model ...')
    loss, norm_coef = train_model(model=model, optimizer=optimizer, train_loader=train_loader, end_epoch=epochs,
                                  losses_enc_weights=losses_enc_weights, weighting_strategy=weighting_strategy,
                                  losses_norm=losses_norm, out_dir_name=out_dir_name, plot=plot,
                                  save=save, verbose=verbose, print_every=print_every, device=device,
                                  early_stopping=early_stopping, min_epochs=min_epochs,
                                  dynamic_ratio=dynamic_ratio, class_weights=class_weights,
                                  grad_clip=grad_clip, scheduler=scheduler, decay_factor=decay_factor,
                                  start_decay=start_decay, end_decay=end_decay,
                                  projection_constraint=projection_constraint,
                                  variance_constraint=variance_constraint,
                                  mse_rel=mse_rel, update_dis_freq=update_dis_freq,
                                  update_aux_freq=update_aux_freq, seed=seed, *args, **kwargs)

    # Printing total loss
    print(f'Final total loss:     {loss[loss_comparison][-1]}')

    # Retrieving best model's parameters
    if early_stopping:
        print(f'Best total loss:     {min(loss[loss_comparison][max(0, min_epochs - 1):])}')
    print('Retrieving best model ...')
    model['cvae'].load_params(out_dir_name)

    # Removing batch effect from data
    print('Removing batch effect ...')
    corrected_data = batch_removal_conditional_robust(adata, cvae=model['cvae'],
                                                      label_projection=label_projection,
                                                      device=device, n_samplings=n_samplings,
                                                      seed=seed)

    # Saving corrected data
    if save['corrected_data']:
        print('Saving corrected data...')
        corrected_data.write(f'{out_dir_name}/corrected_data.h5ad')

    # Running model on test data
    if test:
        print('Evaluating model on test data ...')
        _, _ = test_model(model=model, test_loader=test_loader,
                          losses_enc_weights=losses_enc_weights, norm_coef=norm_coef,
                          out_dir_name=out_dir_name, device=device, verbose=verbose,
                          save={'loss': save['loss'], 'time': save['time']},
                          projection_constraint=projection_constraint,
                          variance_constraint=variance_constraint, mse_rel=mse_rel,
                          weighting_strategy=weighting_strategy)

    # Returning corrected data
    return corrected_data


# Function to run a grid search
def grid_search(model, lr_list, batch_size_list, beta_1_list, beta_2_list, adata,
                root, file_name, model_name, results_path='./Experiments', losses_enc_weights=None,
                weighting_strategy=None, losses_norm=None, max_epochs=100, label_projection=0.5,
                n_samplings=20, seed=42, plot=True, norm_data=False, scaled_data=False, log_transfo=False,
                n_labels=2, save=None, verbose=True, print_every=1, device='cpu', early_stopping=True,
                min_epochs=10, test=False, dynamic_ratio=1.0, class_weights=None, grad_clip=None,
                scheduler=None, decay_factor=0.999, start_decay=0, end_decay=-1, projection_constraint=None,
                variance_constraint=False, mse_rel=False, update_dis_freq=None, update_aux_freq=None,
                lr_aux=None, lr_dis=None, *args, **kwargs):
    """
     Function to perform a grid search on the training hyperparameters of the AIF model (cVAE + GAN + Auxiliary):
     training the model, evaluation on the test set, correction of the batch effect.
     Args:
         model:                  dict, AIF model (cVAE, auxiliary, discriminator) from the classes defined in models.
         lr_list:                list, learning rates to explore.
         batch_size_list:        list, batch sizes to explore.
         beta_1_list:            list, beta 1 coefficients in ADAM optimizer to explore.
         beta_2_list:            list, beta 2 coefficients in ADAM optimizer to explore.
         adata:                  AnnData object, original data containing gene expression and observations.
         root:                   str, path to the preprocessed data directory for the AIF model.
         file_name:              str, dataset name.
         model_name:             str, model name.
         results_path:           str, path to the directory where to save the results, default='./Experiments'.
         losses_enc_weights:     dict, weights for each of the encoder's loss in the overall encoder's loss,
                                 default=None, corresponding to {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1,
                                                                 'class_rec': 0.1, 'aux': 1, 'gen': 0.1}.
         weighting_strategy:      bool, weighting strategy to use for the losses' weights, default=None.
         losses_norm:            dict, normalization coefficient or method for the losses to normalize, default=None.
         max_epochs:             int, maximum number of epochs to run, default=100.
         label_projection:       float, batch label used for batches' distribution projection, default=0.5.
         n_samplings:            int, number of samples to draw from the latent distribution during batch effect
                                 correction, default=20.
         seed:                   int, seed used to set the randomness, default=42.
         norm_data:              bool, whether to use the normalized data, default=False.
         scaled_data:            bool, whether to use the scaled data, default=False.
         log_transfo:            bool, whether to use log1p transformation on the data, default=False.
         n_labels:               int, number of batch labels.
         save:                   dict, saving specifications, default=None,
                                 corresponding to {'cvae': True, 'aux': True, 'dis': True, 'loss': True,
                                                   'corrected_data': True, 'time': True}.
         plot:                   bool, whether to plot the losses evolution or not, default=True.
         verbose:                bool, whether to print useful info during training, default=True.
         verbose:                bool, whether to print useful info during training, default=True.
         print_every:            int, frequency of printed info (e.g. number of epochs), default=1.
         device:                 str, device used ('cuda' or 'cpu'), default='cpu'.
         early_stopping:         bool, whether to perform early stopping, default=True.
         min_epochs:             int, minimum number of epochs before early stopping, default=10.
         test:                   bool, whether to use evaluate the model on the test set, default=False.
         dynamic_ratio:          float, percentage of data to take into account while reweighing, default=1.
         class_weights:          array of size n_labels, weights for each batch label, default=None.
         grad_clip:              float, upper bound for gradient clipping, default=None.
         scheduler:              str, lr scheduler to use for encoder, default=None.
         decay_factor:           float, decay factor to use for lr scheduler, default=0.999.
         start_decay:            int, epoch when to start lr scheduler decay, default=0.
         end_decay:              int, epoch when to end lr scheduler decay, default=-1.
         projection_constraint:  dict of bools, whether to use projection constraint losses, default=None.
         variance_constraint:    bool, whether to use variance constraint loss, default=False.
         mse_rel:                bool, whether to use MSE loss on genes' relative expression, default=False.
         update_dis_freq:        float, frequency at which to update discriminator network's parameters, default=None.
         update_aux_freq:        float, frequency at which to update auxiliary network's parameters, default=None.
         lr_aux:                 float, learning rate for auxiliary network, default=None.
         lr_dis:                 float, learning rate for discriminator network, default=None.
         args:                   list, ordered list of arguments for update weights function.
         kwargs:                 dict, named arguments for update weights function.

     """

    # Setting randomness
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    cudnn.enabled = False
    cudnn.deterministic = True

    # Parsing default arguments
    if losses_enc_weights is None:
        losses_enc_weights = get_default_weights(model=model, weighting_strategy=weighting_strategy,
                                                 projection_constraint=projection_constraint,
                                                 variance_constraint=variance_constraint,
                                                 mse_rel=mse_rel)
    if losses_norm is None:
        losses_norm = {}
    if save is None:
        save = {'cvae': True, 'aux': True, 'dis': True, 'loss': True, 'corrected_data': True, 'time': True}
        if weighting_strategy is not None:
            save.update({'weights': True})

    # Defining loss name for comparison
    if weighting_strategy is not None:
        if norm_data or scaled_data:
            loss_comparison = 'total_no_rel_scaled'
        else:
            loss_comparison = 'total_no_rel'
    else:
        loss_comparison = 'total'

    # Creating model's directory
    if not os.path.isdir(f'{results_path}/{model_name}'):
        os.mkdir(f'{results_path}/{model_name}')

    print(f'--------- Running a grid search for {model_name} ---------')

    # For all combination of hyperparameters train the model
    for batch_size in batch_size_list:

        # Creating corresponding train loader
        print('Prepare data loaders ...')
        train_dataset = Biodataset(root=root, train=True, norm=norm_data, scaled=scaled_data,
                                   log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        if test:
            test_dataset = Biodataset(root=root, train=False, norm=norm_data, scaled=scaled_data,
                                      log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
            test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        else:
            test_loader = None
        print('Data loaders ready.\n')

        for lr in lr_list:
            for beta_1 in beta_1_list:
                for beta_2 in beta_2_list:

                    print(f'Trying batch size={batch_size}, lr={lr}, beta1={beta_1}, beta2={beta_2}')

                    # Resetting model's weights
                    for key in model.keys():
                        reset_weights(model[key])

                    # Creating corresponding optimizers
                    optimizer = {}
                    for key in model.keys():
                        if key == 'dis' and lr_dis is not None:
                            optimizer.update({key: optim.Adam(model[key].parameters(),
                                                              lr=lr_dis, betas=(beta_1, beta_2))})
                        elif key == 'aux' and lr_aux is not None:
                            optimizer.update({key: optim.Adam(model[key].parameters(),
                                                              lr=lr_aux, betas=(beta_1, beta_2))})
                        else:
                            optimizer.update({key: optim.Adam(model[key].parameters(),
                                                              lr=lr, betas=(beta_1, beta_2))})

                    # Creating corresponding outputs' directory name
                    out_dir_name = f'{results_path}/{model_name}/bs_{batch_size}_lr_{lr}_beta1_{beta_1}_beta2_{beta_2}/'

                    try:

                        # Training the model
                        loss, norm_coef = train_model(model=model, optimizer=optimizer, train_loader=train_loader,
                                                      end_epoch=max_epochs, losses_enc_weights=losses_enc_weights,
                                                      weighting_strategy=weighting_strategy, losses_norm=losses_norm,
                                                      out_dir_name=out_dir_name, plot=plot, save=save, verbose=verbose,
                                                      print_every=print_every, device=device,
                                                      early_stopping=early_stopping, min_epochs=min_epochs,
                                                      dynamic_ratio=dynamic_ratio, class_weights=class_weights,
                                                      grad_clip=grad_clip, scheduler=scheduler,
                                                      decay_factor=decay_factor, start_decay=start_decay,
                                                      end_decay=end_decay, projection_constraint=projection_constraint,
                                                      variance_constraint=variance_constraint, mse_rel=mse_rel,
                                                      update_dis_freq=update_dis_freq, update_aux_freq=update_aux_freq,
                                                      *args, **kwargs)

                        # Printing total loss
                        print(f'Final total loss:     {loss[loss_comparison][-1]}')

                        # Retrieving best model's parameters
                        if early_stopping:
                            print(f'Best total loss:     {min(loss[loss_comparison][max(0, min_epochs - 1):])}')
                            print('Retrieving best model ...')
                            model['cvae'].load_params(out_dir_name)

                        # Removing batch effect from data
                        if save['corrected_data']:
                            print('Removing batch effect ...')
                            corrected_data = batch_removal_conditional_robust(adata, cvae=model['cvae'],
                                                                              label_projection=label_projection,
                                                                              device=device, n_samplings=n_samplings,
                                                                              seed=seed)

                            # Saving corrected data
                            print('Saving corrected data ...')
                            corrected_data.write(f'{out_dir_name}/corrected_data.h5ad')

                        # Evaluating the model on the test dataset
                        if test:
                            print('Evaluating model on test data ...')
                            _, _ = test_model(model=model, test_loader=test_loader, out_dir_name=out_dir_name,
                                              losses_enc_weights=losses_enc_weights, norm_coef=norm_coef,
                                              save={'loss': save['loss'], 'time': save['time']},
                                              verbose=verbose, device=device,
                                              projection_constraint=projection_constraint,
                                              variance_constraint=variance_constraint,
                                              mse_rel=mse_rel, weighting_strategy=weighting_strategy)

                        # Adding tab for logs
                        print('\n')

                    except RuntimeError:

                        print('Failed to converge ...')


# Function to run a robust grid search
def robust_grid_search(model, lr_list, batch_size_list, beta_1_list, beta_2_list, adata,
                       root, file_name, model_name, results_path='./Experiments', losses_enc_weights=None,
                       weighting_strategy=None, losses_norm=None, max_epochs=100, label_projection=0.5,
                       n_samplings=20, seed=42, n_repetitions=20, seed_list=None, exp_names=None, plot=True,
                       norm_data=False, scaled_data=False, log_transfo=False, n_labels=2, save=None,
                       verbose=True, print_every=1, device='cpu', early_stopping=True, min_epochs=10,
                       data_embedding='tsne', n_components=None, metric_names=None, metric_best=None,
                       norm_metrics=False, range_batch=None, range_ct=None, shared_ct=None, n_repetitions_kmeans=20,
                       add_to_previous=False, percent_samples=0.8, cell_type_key='cell_type',
                       batch_key='batch', colors_batch=None, colors_cell_types=None,
                       colors_clusters=None, remove_outliers=False, test=False, dynamic_ratio=1.0,
                       class_weights=None, grad_clip=None, scheduler=None, decay_factor=0.999,
                       start_decay=0, end_decay=-1, projection_constraint=None, mse_rel=False,
                       variance_constraint=False, update_aux_freq=None, update_dis_freq=None,
                       lr_aux=None, lr_dis=None):
    """
     Function to perform a robust grid search on the training hyperparameters of the AIF model (cVAE + GAN + Auxiliary):
     training the model, evaluation on the test set, correction of the batch effect.
     Args:
         model:                  dict, AIF model (cVAE, auxiliary, discriminator) from the classes defined in models.
         lr_list:                list, learning rates to explore.
         batch_size_list:        list, batch sizes to explore.
         beta_1_list:            list, beta 1 coefficients in ADAM optimizer to explore.
         beta_2_list:            list, beta 2 coefficients in ADAM optimizer to explore.
         adata:                  AnnData object, original data containing gene expression and observations.
         root:                   str, path to the preprocessed data directory for the AIF model.
         file_name:              str, dataset name.
         model_name:             str, model name.
         results_path:           str, path to the directory where to save the results, default='./Experiments'.
         losses_enc_weights:     dict, weights for each of the encoder's loss in the overall encoder's loss,
                                 default=None, corresponding to {'mse': 1, 'kl': 0.2, 'mmd': 0.2, 'class': 0.1,
                                                                 'class_rec': 0.1, 'aux': 1, 'gen': 0.1}.
         weighting_strategy:     str, weighting strategy to use for losses' weights, default=None.
         losses_norm:            dict, normalization coefficient or method for the losses to normalize, default=None.
         max_epochs:             int, maximum number of epochs to run, default=100.
         label_projection:       float, batch label used for batches' distribution projection, default=0.5.
         n_samplings:            int, number of samples to draw from the latent distribution during batch effect
                                 correction, default=20.
         seed:                   int, seed used to set the randomness, default=42.
         n_repetitions:          int, number of trainings to perform, default=20.
         seed_list:              list, seeds to use for each training, default=None.
         exp_names:              list, experiments name, default=None.
         norm_data:              bool, whether to use the normalized data, default=False.
         scaled_data:            bool, whether to use the scaled data, default=False.
         log_transfo:            bool, whether to use log1p transformation on the data, default=False.
         n_labels:               int, number of batch labels.
         save:                   dict, saving specifications, default=None,
                                 corresponding to {'cvae': {'median': True, 'min': True}, 'loss': True, 'time': True,
                                                   'metrics': True, 'metrics_viz': True}.
         plot:                   bool, whether to plot the losses evolution or not, default=True.
         verbose:                bool, whether to print useful info during training, default=True.
         verbose:                bool, whether to print useful info during training, default=True.
         print_every:            int, frequency of printed info (e.g. number of epochs), default=1.
         device:                 str, device used ('cuda' or 'cpu'), default='cpu'.
         early_stopping:         bool, whether to perform early stopping, default=True.
         min_epochs:             int, minimum number of epochs before early stopping, default=10.
         data_embedding:         str, embedding method on which to perform the KMeans, default='tsne'.
         n_components:           int, number of components to use during the embedding of the data, default=None.
         metric_names:           list, metrics to compute, default=None.
         metric_best:            str, metric to use to determine best clustering results, default=None.
         norm_metrics:           bool, whether to normalize the metrics before computing the F1 score, default=False.
         range_batch:            dict, ranges to use for normalization of the batch metrics, default=None.
         range_ct:               dict, ranges to use for normalization of the cell type metrics, default=None.
         shared_ct:              dict of bools, whether to use only shared cell types for each metric, default=None.
         n_repetitions_kmeans:   int, number of KMeans repetitions to run, default=20.
         add_to_previous:        bool, whether to add the results to a previous analysis, default=False.
         percent_samples:        float, percentage of the data to use for the KMeans, default=0.8.
         cell_type_key:          str, key for cell type labels in adata, default='cell_type'.
         batch_key:              str, key for batch labels in adata, default='batch'.
         colors_batch:           dict, colors for the batches, default=None.
         colors_cell_types:      dict, colors for the cell types, default=None.
         colors_clusters:        dict, colors for the KMeans clusters, default=None.
         remove_outliers:        bool, whether to remove the outliers in the clustering plots, default=False.
         test:                   bool, whether to use evaluate the model on the test set, default=False.
         dynamic_ratio:          float, percentage of data to take into account while reweighing, default=1.
         class_weights:          array of size n_labels, weights for each batch label, default=None.
         grad_clip:              float, upper bound for gradient clipping, default=None.
         scheduler:              str, lr scheduler to use for encoder, default=None.
         decay_factor:           float, decay factor to use for lr scheduler, default=0.999.
         start_decay:            int, epoch when to start lr scheduler decay, default=0.
         end_decay:              int, epoch when to end lr scheduler decay, default=-1.
         projection_constraint:  dict of bools, whether to use projection constraint losses, default=None.
         variance_constraint:    bool, whether to use variance constraint loss, default=False.
         mse_rel:                bool, whether to use MSE on genes' relative expression, default=False.
         update_dis_freq:        float, frequency at which to update discriminator network's parameters, default=None.
         update_aux_freq:        float, frequency at which to update auxiliary network's parameters, default=None.
         lr_aux:                 float, learning rate for auxiliary network, default=None.
         lr_dis:                 float, learning rate for discriminator network, default=None.

     """

    # Parsing default arguments
    if losses_enc_weights is None:
        losses_enc_weights = get_default_weights(model=model, weighting_strategy=weighting_strategy,
                                                 projection_constraint=projection_constraint,
                                                 variance_constraint=variance_constraint, mse_rel=mse_rel)
    if losses_norm is None:
        losses_norm = {}
    if save is None:
        save = {'cvae': {'median': True, 'min': True}, 'loss': True, 'time': True, 'metrics': True, 'metrics_viz': True}
        if weighting_strategy is not None:
            save.update({'weights': True})

    # Creating model's directory
    if not os.path.isdir(f'{results_path}/{model_name}'):
        os.mkdir(f'{results_path}/{model_name}')

    # Defining loss name to use for comparison
    if weighting_strategy is not None:
        if norm_data or scaled_data:
            loss_comparison = 'total_no_rel_scaled'
            final_loss_comparison = f'final_{loss_comparison}'
            final_norm_coef = dict(zip(losses_enc_weights.keys(), [1 for _ in range(len(losses_enc_weights.keys()))]))
        else:
            loss_comparison = 'total_no_rel'
            final_loss_comparison = loss_comparison
            final_norm_coef = None
    else:
        loss_comparison = 'total'
        final_loss_comparison = loss_comparison
        final_norm_coef = None

    print(f'--------- Running a grid search for {model_name} ---------')

    # Initialization of dataframes to store the best losses and metrics
    if add_to_previous:
        best_losses_df = pd.read_csv(f'{results_path}/{model_name}/best_losses.csv', index_col=[k for k in range(5)])
        best_metrics_df = pd.read_csv(f'{results_path}/{model_name}/best_metrics.csv', index_col=[k for k in range(5)])
        best_median = best_losses_df[loss_comparison].median(level=[k for k in range(4)]).min()
        overall_best_loss = best_losses_df[loss_comparison].min(level=[k for k in range(4)]).min()

        if test:
            best_losses_test = pd.read_csv(f'{results_path}/{model_name}/best_losses_test.csv',
                                           index_col=[k for k in range(5)])
            best_metrics_train = pd.read_csv(f'{results_path}/{model_name}/best_metrics_train.csv',
                                             index_col=[k for k in range(5)])
            best_metrics_test = pd.read_csv(f'{results_path}/{model_name}/best_metrics_test.csv',
                                            index_col=[k for k in range(5)])

        else:
            best_losses_test = None
            best_metrics_train = None
            best_metrics_test = None

    else:
        best_losses_df = pd.DataFrame(index=pd.MultiIndex.from_product([batch_size_list, lr_list,
                                                                        beta_1_list, beta_2_list,
                                                                        range(n_repetitions)],
                                                                       names=['bs', 'lr', 'beta_1',
                                                                              'beta_2', 'experiment']))
        best_metrics_df = pd.DataFrame(index=best_losses_df.index)
        best_median = np.inf
        overall_best_loss = np.inf

        if test:
            best_losses_test = pd.DataFrame(index=pd.MultiIndex.from_product([batch_size_list, lr_list,
                                                                              beta_1_list, beta_2_list,
                                                                              range(n_repetitions)],
                                                                             names=['bs', 'lr', 'beta_1',
                                                                                    'beta_2', 'experiment']))
            best_metrics_train = pd.DataFrame(index=best_losses_df.index)
            best_metrics_test = pd.DataFrame(index=best_losses_df.index)

        else:
            best_losses_test = None
            best_metrics_train = None
            best_metrics_test = None

    # Retrieving index corresponding to test dataset
    if test:
        test_index = pd.read_csv(f'{root}/{file_name}/test_index.csv').iloc[:, 0].values.tolist()
    else:
        test_index = pd.DataFrame()

    # Default setting for seeds
    if seed_list is None:
        seed_list = [seed + k for k in range(n_repetitions)]

    # Default setting for experiments name
    if exp_names is None:
        exp_names = ['experiment_' + str(k) for k in range(n_repetitions)]

    # Initialization of a count variable
    count = 0

    # Initialization of a variable to store the best CVAE
    best_cvae = model['cvae']

    # For all combination of hyperparameters train the model
    for batch_size in batch_size_list:

        # Creating corresponding train loader
        print('Prepare data loaders ...')
        train_dataset = Biodataset(root=root, train=True, norm=norm_data, scaled=scaled_data,
                                   log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
        if test:
            test_dataset = Biodataset(root=root, train=False, norm=norm_data, scaled=scaled_data,
                                      log_transfo=log_transfo, filename=file_name, n_labels=n_labels)
            test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
        else:
            test_loader = None
        print('Data loaders ready.\n')

        for lr in lr_list:
            for beta_1 in beta_1_list:
                for beta_2 in beta_2_list:

                    print(f'Trying batch size={batch_size}, lr={lr}, beta1={beta_1}, beta2={beta_2}')

                    # Creating corresponding outputs' directory name
                    out_dir_name = f'{results_path}/{model_name}/bs_{batch_size}_lr_{lr}_beta1_{beta_1}_beta2_{beta_2}/'
                    if not os.path.isdir(out_dir_name):
                        os.mkdir(out_dir_name)

                    # Initialization of a variable to store the best loss
                    best_loss = np.inf

                    # Training the model for n_repetitions times
                    for i in range(len(seed_list)):

                        # Setting randomness
                        torch.manual_seed(seed_list[i])
                        torch.cuda.manual_seed(seed_list[i])
                        np.random.seed(seed_list[i])
                        random.seed(seed_list[i])
                        cudnn.enabled = False
                        cudnn.deterministic = True

                        print(f'Running {exp_names[i].replace("_", " ")} ...')

                        # Creating model info for figures
                        title_info = model_name + '/n' + f'(bs={batch_size},lr={lr},beta1={beta_1},beta2={beta_2})'

                        # Creating an output directory for this experiment
                        out_dir_name_exp = f'{out_dir_name}/{exp_names[i]}'

                        # Resetting model's weights
                        for key in model.keys():
                            reset_weights(model[key])

                        # Creating corresponding optimizers
                        optimizer = {}
                        for key in model.keys():
                            if key == 'dis' and lr_dis is not None:
                                optimizer.update({key: optim.Adam(model[key].parameters(),
                                                                  lr=lr_dis, betas=(beta_1, beta_2))})
                            elif key == 'aux' and lr_aux is not None:
                                optimizer.update({key: optim.Adam(model[key].parameters(),
                                                                  lr=lr_aux, betas=(beta_1, beta_2))})
                            else:
                                optimizer.update({key: optim.Adam(model[key].parameters(),
                                                                  lr=lr, betas=(beta_1, beta_2))})

                        try:
                            # Training the model
                            loss, norm_coef = train_model(model=model, optimizer=optimizer, train_loader=train_loader,
                                                          end_epoch=max_epochs, losses_enc_weights=losses_enc_weights,
                                                          weighting_strategy=weighting_strategy,
                                                          losses_norm=losses_norm, out_dir_name=out_dir_name_exp,
                                                          save={'cvae': False, 'aux': False, 'dis': False,
                                                                'loss': save['loss'], 'time': save['time']},
                                                          plot=plot, verbose=verbose, print_every=print_every,
                                                          device=device, early_stopping=early_stopping,
                                                          min_epochs=min_epochs, dynamic_ratio=dynamic_ratio,
                                                          class_weights=class_weights, grad_clip=grad_clip,
                                                          scheduler=scheduler, decay_factor=decay_factor,
                                                          start_decay=start_decay, end_decay=end_decay,
                                                          projection_constraint=projection_constraint,
                                                          variance_constraint=variance_constraint,
                                                          mse_rel=mse_rel,
                                                          update_dis_freq=update_dis_freq,
                                                          update_aux_freq=update_aux_freq)

                            # Printing total loss
                            print(f'Final total loss:     {loss[loss_comparison][-1]}')

                            # Updating final normalization coefficients for determining best models
                            if count == 0:
                                for key in final_norm_coef.keys():
                                    final_norm_coef[key] = norm_coef[key]

                            # Evaluating the model on test data
                            if test:
                                print('Evaluating model on test data ...')
                                cvae, test_loss = test_model(model=model, test_loader=test_loader,
                                                             out_dir_name=out_dir_name,
                                                             losses_enc_weights=losses_enc_weights, norm_coef=norm_coef,
                                                             save={'loss': save['loss'], 'time': save['time']},
                                                             verbose=verbose, device=device,
                                                             projection_constraint=projection_constraint,
                                                             variance_constraint=variance_constraint,
                                                             mse_rel=mse_rel, weighting_strategy=weighting_strategy)
                            else:
                                test_loss = None

                            # Adding column names
                            if len(best_losses_df.columns) == 0:
                                best_losses_df = best_losses_df.reindex(best_losses_df.columns.union(loss.keys()),
                                                                        axis=1)
                                if test:
                                    best_losses_test = best_losses_test.reindex(
                                        best_losses_test.columns.union(loss.keys()),
                                        axis=1)
                                else:
                                    best_losses_test = None
                                if early_stopping:
                                    best_losses_df = best_losses_df.reindex(
                                        best_losses_df.columns.union(['min_epochs']), axis=1)
                                    if test:
                                        best_losses_test = best_losses_test.reindex(
                                            best_losses_test.columns.union(['min_epochs']), axis=1)

                            # Storing the best loss on train dataset for this experiment
                            if early_stopping:
                                print(f'Best total loss:     {min(loss[loss_comparison][max(0, min_epochs - 1):])}')
                                loss_df = pd.DataFrame.from_dict(loss, orient='columns')
                                index = (batch_size, lr, beta_1, beta_2, int(exp_names[i].split('_')[-1]))
                                best_losses_df.loc[index, :] = (
                                    loss_df.loc[loss_df[loss_comparison][max(0, min_epochs - 1):].argmin() +
                                                min_epochs - 1, :].append(
                                        pd.Series(max(min_epochs - 1,
                                                      loss_df[loss_comparison][max(0, min_epochs - 1):].argmin() +
                                                      min_epochs - 1), index=['min_epochs'])))
                            else:
                                index = (batch_size, lr, beta_1, beta_2, int(exp_names[i].split('_')[-1]))
                                best_losses_df.loc[index, :] = pd.DataFrame.from_dict(loss,
                                                                                      orient='columns').iloc[-1, :]

                            # Computing final loss for further comparison
                            if loss_comparison.casefold() == 'total_no_rel_scaled'.casefold():
                                if final_loss_comparison not in best_losses_df.columns:
                                    best_losses_df = best_losses_df.reindex(
                                        best_losses_df.columns.union(final_loss_comparison),
                                        axis=1)
                                for key in losses_enc_weights.keys():
                                    best_losses_df.loc[index, final_loss_comparison] += (
                                            best_losses_df.loc[index, key] * final_norm_coef[key])

                            # Storing corresponding losses on test dataset
                            if test:
                                best_losses_test.loc[index, :] = pd.DataFrame.from_dict(test_loss,
                                                                                        orient='columns').iloc[0, :]

                            # Computing and saving the metrics on entire dataset
                            if save['metrics']:

                                # Correcting data using robust batch removal based on conditional sampling
                                corrected_data = batch_removal_conditional_robust(adata=adata, cvae=model['cvae'],
                                                                                  label_projection=label_projection,
                                                                                  device=device, seed=seed,
                                                                                  n_samplings=n_samplings)

                                # Computing the metrics on the overall dataset
                                metrics = compute_and_plot_best_clustering(corrected_data=corrected_data.X,
                                                                           adata=adata, metric_names=metric_names,
                                                                           data_embedding=data_embedding,
                                                                           n_components=n_components,
                                                                           n_repetitions=n_repetitions_kmeans,
                                                                           percent_samples=percent_samples, seed=seed,
                                                                           metric_best=metric_best, norm=norm_metrics,
                                                                           range_batch=range_batch, range_ct=range_ct,
                                                                           shared_ct=shared_ct,
                                                                           cell_type_key=cell_type_key,
                                                                           batch_key=batch_key,
                                                                           colors_batch=colors_batch,
                                                                           colors_cell_types=colors_cell_types,
                                                                           colors_clusters=colors_clusters,
                                                                           remove_outliers=remove_outliers,
                                                                           title_info=title_info,
                                                                           save_plot=save['metrics_viz'],
                                                                           saving_path=out_dir_name_exp)

                                # Computing the metrics on the train dataset
                                if test:
                                    # Retrieving index for train dataset
                                    train_index = [i for i in range(0, len(corrected_data.X)) if i not in test_index]

                                    # Computing the metrics on the train dataset
                                    metrics_train = compute_and_plot_best_clustering(
                                        corrected_data=corrected_data.X[train_index, :],
                                        adata=adata[train_index], metric_names=metric_names,
                                        data_embedding=data_embedding,
                                        n_components=n_components, n_repetitions=n_repetitions_kmeans,
                                        percent_samples=percent_samples, seed=seed,
                                        metric_best=metric_best, norm=norm_metrics,
                                        range_batch=range_batch, range_ct=range_ct, shared_ct=shared_ct,
                                        cell_type_key=cell_type_key, batch_key=batch_key,
                                        colors_batch=colors_batch,
                                        colors_cell_types=colors_cell_types,
                                        colors_clusters=colors_clusters,
                                        remove_outliers=remove_outliers,
                                        title_info=title_info, save_plot=save['metrics_viz'],
                                        saving_path=out_dir_name_exp, additional_info='train')

                                    # Computing the metrics on the test dataset
                                    metrics_test = compute_and_plot_best_clustering(
                                        corrected_data=corrected_data.X[test_index, :],
                                        adata=adata[test_index], metric_names=metric_names,
                                        data_embedding=data_embedding,
                                        n_components=n_components, n_repetitions=n_repetitions_kmeans,
                                        percent_samples=percent_samples, seed=seed,
                                        metric_best=metric_best, norm=norm_metrics,
                                        range_batch=range_batch, range_ct=range_ct, shared_ct=shared_ct,
                                        cell_type_key=cell_type_key, batch_key=batch_key,
                                        colors_batch=colors_batch,
                                        colors_cell_types=colors_cell_types,
                                        colors_clusters=colors_clusters,
                                        remove_outliers=remove_outliers,
                                        title_info=title_info, save_plot=save['metrics_viz'],
                                        saving_path=out_dir_name_exp, additional_info='test')

                                else:
                                    metrics_train = pd.DataFrame()
                                    metrics_test = pd.DataFrame()

                                # Adding metric names
                                if len(best_metrics_df.columns) == 0:
                                    best_metrics_df = best_metrics_df.reindex(
                                        best_metrics_df.columns.union(metrics.keys()),
                                        axis=1)
                                if test:
                                    if len(best_metrics_train.columns) == 0:
                                        best_metrics_train = best_metrics_train.reindex(
                                            best_metrics_train.columns.union(metrics_train.keys()), axis=1)
                                    if len(best_metrics_test.columns) == 0:
                                        best_metrics_test = best_metrics_test.reindex(
                                            best_metrics_test.columns.union(metrics_test.keys()), axis=1)

                                # Store metrics
                                index = (batch_size, lr, beta_1, beta_2, int(exp_names[i].split('_')[-1]))
                                best_metrics_df.loc[index, :] = metrics
                                if test:
                                    best_metrics_train.loc[index, :] = metrics_train
                                    best_metrics_test.loc[index, :] = metrics_test

                            # Checking if it is the best model across experiments
                            if best_loss >= min(loss[final_loss_comparison][max(0, min_epochs - 1):]):
                                best_loss = min(loss[final_loss_comparison][max(0, min_epochs - 1):])
                                best_cvae = model['cvae']

                            print('\n')

                        except RuntimeError:
                            print('Fail to converge ...')

                        # Comparing the median across experiments
                        if best_losses_df.loc[(batch_size, lr, beta_1, beta_2,),
                                              final_loss_comparison].median() < best_median:
                            if save['cvae']['median']:
                                print('Saving best loss median model ...')
                                best_cvae.save_params(f'{results_path}/{model_name}',
                                                      name='best_median_cvae_params')
                            best_median = best_losses_df.loc[
                                (batch_size, lr, beta_1, beta_2,), final_loss_comparison].median()

                        # Comparing the minimum across experiments
                        if best_losses_df.loc[(batch_size, lr, beta_1, beta_2,),
                                              final_loss_comparison].min() < overall_best_loss:
                            if save['cvae']['min']:
                                print('Saving best loss model ...')
                                best_cvae.save_params(f'{results_path}/{model_name}',
                                                      name='best_loss_cvae_params')
                            overall_best_loss = best_losses_df.loc[
                                (batch_size, lr, beta_1, beta_2,), final_loss_comparison].min()

                        print('\n')

                        # Saving best losses dataframe
                        if save['loss']:
                            best_losses_df.to_csv(f'{results_path}/{model_name}/best_losses.csv', index=True)
                            if test:
                                best_losses_test.to_csv(f'{results_path}/{model_name}/best_losses_test.csv', index=True)

                        # Saving metrics dataframe
                        if save['metrics']:
                            best_metrics_df.to_csv(f'{results_path}/{model_name}/best_metrics.csv', index=True)
                            if test:
                                best_metrics_train.to_csv(f'{results_path}/{model_name}/best_metrics_train.csv',
                                                          index=True)
                                best_metrics_test.to_csv(f'{results_path}/{model_name}/best_metrics_test.csv',
                                                         index=True)
