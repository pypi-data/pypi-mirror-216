# Importing useful libraries
from os.path import join
import torch
import torch.nn.functional as F
from torch import nn
from torch.autograd import Variable


# Class for encoder block
class Encoder(nn.Module):
    """
    Class for the Encoder block.
    """

    # Model constructor function
    def __init__(self, nz, input_size, hidden_units,
                 n_labels=2, norm=True, activation='ReLU', variational=True):
        """
        Function to create an instance from this class.
        Args:
            nz:             int, dimension of the latent space.
            input_size:     int, features space dimension.
            hidden_units:   list, hidden units to use for each layer.
            n_labels:       int, number of batch labels, default=2.
            norm:           bool, whether to use batch normalization, default=True.
            activation:     str, activation function to use, default='ReLU'.
            variational:    bool, whether to use variational formulation, default=True.
        """

        super(Encoder, self).__init__()

        # Storing useful attributes
        self.nz = nz
        self.input_size = input_size
        self.n_labels = n_labels
        self.variational = variational

        # Defining encoder's layers
        self.layers = []
        for i in range(len(hidden_units)):
            if i == 0:
                self.layers.append(nn.Linear(self.input_size,
                                             hidden_units[i]))  # 1st Linear layer
            else:
                self.layers.append(nn.Linear(hidden_units[i - 1],
                                             hidden_units[i]))  # Middle Linear layer
            if norm:
                self.layers.append(nn.BatchNorm1d(hidden_units[i],  # Normalization layer
                                                  affine=False))
            if activation is not None:
                if hasattr(torch.nn, activation):
                    self.layers.append(getattr(torch.nn, activation)())  # Activation layer
        self.layers = nn.Sequential(*self.layers)

        # Defining encoder's last layers
        if self.variational:
            self.logvar_layer = nn.Linear(hidden_units[-1], self.nz)  # No activation
        self.mu_layer = nn.Linear(hidden_units[-1], self.nz)  # No activation
        if self.n_labels <= 2:
            self.y_layer = nn.Sequential(nn.Linear(hidden_units[-1], self.n_labels),
                                         nn.Sigmoid())  # Sigmoid activation
        else:
            self.y_layer = nn.Sequential(nn.Linear(hidden_units[-1], self.n_labels),
                                         nn.Softmax(dim=1))  # Softmax activation

    # Forward propagation function
    def forward(self, x):
        """
        Forward propagation function.
        Args:
            x:      array of size (batch_size, n_features)
        Returns:    (mu, logvar, y), estimated parameters of the latent space distribution (mean and log variance)
        and probabilities for the batch label.
        """
        # Forward propagating the input
        x = self.layers(x)  # Linear layers with batch normalization and activation
        mu = self.mu_layer(x)  # Encoding the mean
        if self.variational:
            log_var = self.logvar_layer(x)  # Encoding the log variance
        else:
            log_var = None
        y = self.y_layer(x.detach())  # Encoding the batch label

        # Returning the encoded distribution parameters
        return mu, log_var, y

    # Function to save model's parameters
    def save_params(self, ex_dir, name='encoder_params'):
        """
        Function to save the network's parameters.
        Args:
            ex_dir:     str, path where to save the network's parameters.
            name:       str, file's name, default='encoder_params'.
        """
        torch.save(self.state_dict(), join(ex_dir, name))

    # Function to load model's parameters
    def load_params(self, ex_dir, device='cpu', name='encoder_params'):
        """
        Function to load the network's parameters.
        Args:
            ex_dir:     str, path where the network's parameters are stored.
            device:     str, device used ('cpu' or 'cuda').
            name:       str, file's name, default='encoder_params'.
        """
        self.load_state_dict(torch.load(join(ex_dir, name),
                                        map_location=device))


# Class for decoder block
class Decoder(nn.Module):
    """
    Class for the decoder block.
    """

    # Model constructor function
    def __init__(self, nz, input_size, hidden_units,
                 n_labels=2, norm=True, activation='ReLU',
                 last_activation=None):
        """
        Constructor function.
        Args:
            nz:                int, dimension of the latent space.
            input_size:        int, dimension of the features space.
            hidden_units:      list, hidden units to use for each layer.
            n_labels:          int, number of batch labels, default=2.
            norm:              bool, whether to use batch  normalization, default=True.
            activation:        str, activation function to use, default='ReLU'.
            last_activation:   str, last activation function to use, default=None.

        """

        super(Decoder, self).__init__()

        # Storing useful attributes
        self.nz = nz
        self.input_size = input_size
        self.n_labels = n_labels

        # Defining decoder's layers
        self.layers = []
        for i in range(0, len(hidden_units)):
            if i == 0:
                self.layers.append(nn.Linear(self.nz + self.n_labels,
                                             hidden_units[i]))  # 1st Linear layer
            else:
                self.layers.append(nn.Linear(hidden_units[i - 1],
                                             hidden_units[i]))  # Middle Linear layer
            if norm:
                self.layers.append(nn.BatchNorm1d(hidden_units[i],  # Normalization layer
                                                  affine=False))
            if activation is not None:
                if hasattr(torch.nn, activation):
                    self.layers.append(getattr(torch.nn, activation)())  # Activation layer
        self.layers = nn.Sequential(*self.layers)

        # Defining decoder's last layers
        if last_activation is not None:
            self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1], self.input_size),
                                            getattr(torch.nn, last_activation)())  # Linear layer
        else:
            self.last_layer = nn.Linear(hidden_units[-1], self.input_size)  # Linear layer, no activation

    # Forward propagation function
    def forward(self, y, z):
        """
        Forward propagation function.
        Args:
            y:      array of size (batch_size, n_labels), vector containing the predicted batch label probabilities.
            z:      array of size (batch_size, nz), array containing the latent vectors.
        Returns:    array of size (batch_size, n_features), reconstructed data.
        """
        # Forward propagating the input
        z = torch.cat([y, z], dim=1)
        z = self.layers(z)
        z = self.last_layer(z)

        # Returning the decoded distribution
        return z

    # Function to save model's parameters
    def save_params(self, ex_dir, name='decoder_params'):
        """
        Function to save the parameters of the network.
        Args:
            ex_dir:     str, path where to save the network's parameters.
            name:       str, name of the file, default='decoder_params'.
        """
        torch.save(self.state_dict(), join(ex_dir, name))

    # Function to load model's parameters
    def load_params(self, ex_dir, device='cpu', name='decoder_params'):
        """
        Function to load the parameters of the network.
        Args:
            ex_dir:     str, path where the network's parameters are store.
            device:     str, device used ('cpu' or 'cuda'), default='cpu'.
            name:       str, name of the file, default='decoder_params'.
        """
        self.load_state_dict(torch.load(join(ex_dir, name),
                                        map_location=device))


# Class for conditional variational auto-encoder (cVAE) block
class CVAE(nn.Module):
    """
    Class for the conditional Variational Auto-Encoder block.
    """

    # Model constructor function
    def __init__(self, nz, input_size, hidden_units, sigma=1,
                 n_labels=2, norm=True, activation='ReLU', device='cpu', norm_loss=True,
                 class_weights=None, last_activation=None, latent_loss='kl', var_kernel=None,
                 variational=True):
        """
        Constructor function.
        Args:
            nz:             int, dimension of the latent space.
            input_size:     int, dimension of the features space.
            hidden_units:   list, hidden units to use for each layer.
            sigma:          float, sigma for the N(0,sigma) distribution in the latent space, default=1.
            n_labels:       int, number of batch labels, default=2.
            norm:           bool, whether to use batch normalization, default=True.
            activation:     str, activation function to use, default='ReLU'.
            device:         str, device used ('cpu' or 'cuda'), default='cpu'.
            norm_loss:      bool, whether to normalize the MSE and KL losses by the number of features,
                            default=True.
            class_weights:  tensor of size number of labels, weights for each batch label, default=None.
            latent_loss:    str, loss to use for constraining latent space distribution, default='kl'.
            var_kernel:     float, variance to use when computing gaussian kernel, default=None.
            variational:    bool, whether to use variational formulation, default=True.
        """
        super(CVAE, self).__init__()

        # Storing useful attributes
        self.nz = nz                        # Latent representation dimension
        self.input_size = input_size        # Input size
        self.sigma = sigma                  # Sigma for gaussian distribution of latent representation
        self.device = device                # Device to use
        self.n_labels = n_labels            # Number of labels to use
        self.norm_loss = norm_loss          # Whether to normalize the loss
        self.class_weights = class_weights  # Weights for each batch label
        self.variational = variational      # Whether to use variational formulation
        self.var_kernel = var_kernel        # Variance to use when computing gaussian kernel
        if self.variational:
            self.latent_loss = latent_loss  # Latent loss to use
        else:
            self.latent_loss = None

        # Defining encoder's block
        self.encoder = Encoder(nz=self.nz, input_size=self.input_size,
                               hidden_units=hidden_units, norm=norm,
                               activation=activation, n_labels=self.n_labels,
                               variational=self.variational)

        # Defining decoder's block
        self.decoder = Decoder(nz=self.nz, input_size=self.input_size,
                               hidden_units=hidden_units, norm=norm,
                               activation=activation, n_labels=self.n_labels,
                               last_activation=last_activation)

    # Function to parse the model on specified device
    def to(self, device, *args, **kwargs):
        """
        Function to parse the model on the specified device.
        Args:
            device:     str, device used ('cpu' or 'cuda').
            *args:
            **kwargs:
        Returns:    model on specified device.
        """
        self = super().to(device, *args, **kwargs)
        self.device = device
        if self.class_weights is not None:
            self.class_weights = self.class_weights.to(device, copy=True)
        return self

    # Function to sample from latent representation
    def sample_z(self, nb_samples, sigma=None):
        """
        Function to sample z from the latent distribution.
        Args:
            nb_samples:      int, number of samples.
            sigma:           float, sigma of the theoretical N(0,sigma) latent distribution, default=None.
        Returns:    array of size (nb_samples, nz), samples from the latent distribution.
        """
        # Storing sigma in attributes
        if sigma is not None:
            self.sigma = sigma

        # Sampling from N(0,sigma)
        z = self.sigma * torch.randn(nb_samples, self.nz)

        # Returning the samples
        return Variable(z).to(self.device)

    # Re parameterization trick function
    def re_param(self, mu, log_var, sigma=None):
        """
        Function to do the re parameterization trick.
        Args:
            mu:         array of size (batch_size, nz), estimated mean vector from the encoder block.
            log_var:    array of size (batch_size, nz), estimated log variance from the encoder block.
            sigma:      float, sigma for theoretical N(0,sigma) latent distribution, default=None.
        Returns:    array of size (batch_size, nz), samples from the latent distribution.
        """

        # Storing sigma in attributes
        if sigma is not None:
            self.sigma = sigma

        # Returning mu if non-variational formulation
        if not self.variational:
            return mu

        else:
            # Re parameterization trick
            std = torch.exp(log_var / 2).to(self.device)
            eps = self.sample_z(nb_samples=std.size(0), sigma=sigma)

            # Return the latent representation distribution obtained
            return Variable(mu).to(self.device) + std * eps

    # Function to forward propagate the input through the encoder and decoder
    def forward(self, x):
        """
        Forward propagation function.
        Args:
            x:      array of size (batch_size, N_features)
        Returns:    (reconstruction, mu, logvar, y), reconstructed samples as well as the estimated parameters of the
        latent distribution and the estimated batch label probabilities.
        """
        # Encoding the data into the latent representation distribution
        mu, log_var, y = self.encoder(x)

        # Sampling z from latent distribution
        z = self.re_param(mu, log_var)

        # Reconstructing the data conditionally to the label
        reconstruction = self.decoder(y=y, z=z)

        # Returning all outputs
        return reconstruction, mu, log_var, y

    # Function to save model's parameters
    def save_params(self, ex_dir, name='cvae_params'):
        """
        Function to save the network's parameters.
        Args:
            ex_dir:     str, path where to save the network's parameters.
            name:       str, file name.
        """
        torch.save(self.state_dict(), join(ex_dir, name))

    # Function to load model's parameters
    def load_params(self, ex_dir, name='cvae_params'):
        """
        Function to load the network's parameters.
        Args:
            ex_dir:     str, path where the network's parameters are stored.
            name:       str, file name.
        """
        self.load_state_dict(torch.load(join(ex_dir, name),
                                        map_location=self.device))

    # Function to compute gaussian kernel
    def compute_gaussian_kernel(self, x, y, var_kernel=None):
        """
        Function to compute gaussian kernel.
        Args:
            x:              array of size (n_samples in x, n_features).
            y:              array of size (n_samples in y, n_features).
            var_kernel:     float, sigma**2 to use for computing gaussian kernel, default=None.
        """
        # Parsing variance kernel default value
        if var_kernel is None:
            if self.var_kernel is None:
                var_kernel = x.shape[1] / 2
            else:
                var_kernel = self.var_kernel

        # Creating matrices to compute distances on each pair of vector
        x = x.view(x.shape[0], 1, x.shape[1]).expand(x.shape[0], y.shape[0], x.shape[1])
        y = y.view(1, y.shape[0], y.shape[1]).expand(x.shape[0], y.shape[0], y.shape[1])

        # Returning gaussian kernel between each vector in x and y
        return torch.exp(- torch.pow(x - y, 2).sum(-1) / 2 / var_kernel)

    # Function to compute the corresponding loss: MSE + latent space
    def loss(self, x_rec, x, y_pred, y, y_rec, mu, log_var, eps=1e-12, class_weights=None, var_kernel=None):
        """
        Function to compute the VAE loss: MSE and KL.
        Args:
            x_rec:          array of size (batch_size, N_features), reconstructed samples.
            x:              array of size (batch_size, N_features), original samples.
            y_pred:         array of size (batch_size, n_labels), predicted probabilities of the batch label.
            y:              array of size (batch_size, n_labels), one-hot vector containing the true batch labels.
            y_rec:          array of size (batch_size, n_labels), predicted probabilities of the batch label after
                            reconstruction.
            mu:             array of size (batch_size, nz), estimated mean vector.
            log_var:        array of size (batch_size, nz), estimated log variance.
            eps:            float, safety for log computation, default=1e-12.
            class_weights:  tensor of size number of labels, weights for each batch label, default=None.
            var_kernel:     float, sigma**2 to use for computing gaussian kernel, default=None.
        Returns:    (mse, latent_loss, class, class_rec), reconstruction, latent, classification and classification after
        reconstruction losses.
        """

        # Adding class weights to attribute
        if class_weights is not None:
            self.class_weights = class_weights

        # Computing MSE term
        mse = F.mse_loss(x_rec.reshape(x.shape), x, reduction='sum')

        # Computing latent loss term
        kl_loss, mmd_loss = 0, 0
        if self.variational and 'kl' in self.latent_loss:
            if self.sigma == 1:
                kl_loss = 0.5 * torch.sum(mu ** 2 + torch.exp(log_var) - 1. - log_var)
            else:
                sigma_th = Variable(torch.Tensor([self.sigma])).to(self.device)
                log_var_th = torch.log(sigma_th ** 2)
                kl_loss = torch.sum(
                    0.5 * (log_var_th - log_var) + (torch.exp(log_var) + mu ** 2) / 2 / sigma_th ** 2 - 0.5)
        if self.variational and 'mmd' in self.latent_loss:
            z_prior = self.re_param(mu=torch.zeros(mu.shape),
                                    log_var=torch.log(torch.ones(log_var.shape) * self.sigma ** 2))
            z = self.re_param(mu=mu, log_var=log_var)
            mmd_loss = ((self.compute_gaussian_kernel(x=z_prior, y=z_prior, var_kernel=var_kernel).sum() +
                         self.compute_gaussian_kernel(x=z, y=z, var_kernel=var_kernel).sum() -
                         2 * self.compute_gaussian_kernel(x=z_prior, y=z, var_kernel=var_kernel).sum()) /
                         z_prior.shape[0])

        # Computing classification term
        if self.n_labels <= 2:
            class_loss = F.binary_cross_entropy(y_pred, torch.clamp(y, 0, 1), reduction='sum',
                                                weight=self.class_weights)
        else:
            class_loss = F.nll_loss(torch.log(y_pred + eps), y.type(torch.LongTensor).argmax(dim=1).to(self.device),
                                    reduction='sum', weight=self.class_weights)

        # Computing classification after reconstruction term
        if self.n_labels <= 2:
            class_rec_loss = F.binary_cross_entropy(y_rec, torch.clamp(y, 0, 1), reduction='sum',
                                                    weight=self.class_weights)
        else:
            class_rec_loss = F.nll_loss(torch.log(y_rec + eps), y.type(torch.LongTensor).argmax(dim=1).to(self.device),
                                        reduction='sum', weight=self.class_weights)

        # Norming the losses
        if self.norm_loss:
            mse = mse / (x.size(1) ** 2)
            if self.variational and 'kl' in self.latent_loss:
                kl_loss = kl_loss / mu.size(1)
            if self.variational and 'mmd' in self.latent_loss:
                mmd_loss = mmd_loss / (mu.size(1) ** 2)

        # Returning the losses
        return mse, kl_loss, mmd_loss, class_loss, class_rec_loss


# Class for the auxiliary block
class Auxiliary(nn.Module):
    """
    Class for the auxiliary block.
    """

    # Module constructor function
    def __init__(self, nz, hidden_units, n_labels=2,
                 activation='ReLU', last_activation=None, device='cpu', class_weights=None):
        """
        Constructor function.
        Args:
            nz:                 int, dimension of the latent space.
            hidden_units:       list, hidden units to use for each layer.
            n_labels:           int, number of batch labels, default=2.
            activation:         str, activation function to use, default='ReLU'.
            last_activation:    str, last activation function, default=None.
            device:             str, device used ('cpu' or 'cuda'), default='cpu'.
            class_weights:      tensor of size number of labels, weights for each batch label, default=None.
        """

        super(Auxiliary, self).__init__()

        # Storing useful attributes
        self.nz = nz  # Latent space dimension
        self.n_labels = n_labels  # Number of labels
        self.device = device  # Device to use
        self.class_weights = class_weights  # Weights for each batch label.

        # Defining model's layers
        self.layers = []
        for i in range(len(hidden_units)):
            if i == 0:
                self.layers.append(nn.Linear(self.nz,
                                             hidden_units[i]))  # 1st linear layer
            else:
                self.layers.append(nn.Linear(hidden_units[i - 1],
                                             hidden_units[i]))  # Middle linear layer
            if activation is not None:
                if hasattr(torch.nn, activation):
                    self.layers.append(getattr(torch.nn, activation)())  # Activation layer
        self.layers = nn.Sequential(*self.layers)

        # Defining the model's last layer
        if last_activation is None:
            if self.n_labels <= 2:
                self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1],
                                                          self.n_labels),
                                                nn.Sigmoid())  # Sigmoid activation
            else:
                self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1],
                                                          self.n_labels),
                                                nn.Softmax(dim=1))  # Softmax activation
        else:
            self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1],
                                                      self.n_labels),
                                            getattr(torch.nn, last_activation))

    # Function to parse the model on specified device
    def to(self, device, *args, **kwargs):
        """
        Function to parse the model on the specified device.
        Args:
            device:     str, device used ('cpu' or 'cuda').
            *args:
            **kwargs:
        Returns:    model on specified device.
        """
        self = super().to(device, *args, **kwargs)
        self.device = device
        if self.class_weights is not None:
            self.class_weights = self.class_weights.to(device)
        return self

    # Function to forward propagate the input through the auxiliary network
    def forward(self, z):
        """
        Forward propagation function.
        Args:
            z:      array of size (batch_size, nz), latent vector for each sample.
        Returns:    array of size (batch_size, n_batches), probabilities for the batch label.
        """
        z = self.layers(z)
        z = self.last_layer(z)
        return z

    # Function to compute the loss
    def loss(self, pred, target, eps=1e-12, class_weights=None):
        """
        Function to compute the auxiliary's loss.
        Args:
            pred:           array of size (batch_size, n_batches), probabilities of batch labels.
            target:         array of size (batch_size, n_batches), true batch labels in one-hot vector.
            eps:            float, safety for log computation, default=1e-12.
            class_weights:  tensor of size number of labels, weights for each batch label, default=None.
        Returns:    float, cross entropy between prediction and target.
        """
        # Adding class weights in model's attributes
        if class_weights is not None:
            self.class_weights = class_weights

        # Computing the Cross Entropy
        if self.n_labels <= 2:
            return F.binary_cross_entropy(pred, torch.clamp(target, 0, 1), weight=self.class_weights)
        else:
            return F.nll_loss(torch.log(pred + eps), target.type(torch.LongTensor).argmax(dim=1).to(self.device),
                              reduction='sum', weight=self.class_weights)

    # Function to save the model's parameters
    def save_params(self, ex_dir, name='aux_params'):
        """
        Function to save the network's parameters.
        Args:
            ex_dir:     str, path where to save the network's parameters.
            name:       str, file name, default='aux_params'.
        """
        torch.save(self.state_dict(), join(ex_dir, name))

    # Function to load the model's parameters
    def load_params(self, ex_dir, device='cpu', name='aux_params'):
        """
        Function to load the network's parameters.
        Args:
            ex_dir:     str, path where the network's parameters are stored.
            device:     str, device used ('cpu' or 'cuda'), default='cpu'.
            name:       str, file name, default='aux_params'.
        """
        self.load_state_dict(torch.load(join(ex_dir, name),
                                        map_location=device))


# Class for the discriminator block
class Discriminator(nn.Module):
    """
    Class for the discriminator block.
    """

    # Module constructor function
    def __init__(self, input_size, hidden_units,
                 activation='ReLU', last_activation=None):
        """
        Constructor function.
        Args:
            input_size:         int, dimension of the features space.
            hidden_units:       list, hidden units to use for each layer.
            activation:         str, activation function to use, default='ReLU'.
            last_activation:    str, last activation function to use, default=None.
        """

        super(Discriminator, self).__init__()

        # Storing useful attributes
        self.input_size = input_size  # Input size
        self.n_labels = 2  # Number of labels

        # Defining the model's layers
        self.layers = []
        for i in range(len(hidden_units)):
            if i == 0:
                self.layers.append(nn.Linear(input_size,
                                             hidden_units[i]))  # 1st linear layer
            else:
                self.layers.append(nn.Linear(hidden_units[i - 1],
                                             hidden_units[i]))  # Middle linear layer
            if activation is not None:
                if hasattr(torch.nn, activation):
                    self.layers.append(getattr(torch.nn, activation)())  # Activation layer
        self.layers = nn.Sequential(*self.layers)

        # Defining the model's last layer
        if last_activation is None:
            self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1],
                                                      self.n_labels - 1),
                                            nn.Sigmoid())
        else:
            self.last_layer = nn.Sequential(nn.Linear(hidden_units[-1],
                                                      self.n_labels - 1),
                                            getattr(torch.nn, last_activation))

    # Function to forward propagate the input through the discriminator
    def forward(self, x):
        """
        Forward propagation function.
        Args:
            x:      array of size (batch_size, N_features), original samples.
        Returns:    array of size (batch_size), probabilities for the 'real' class
        """
        x = self.layers(x)
        x = self.last_layer(x)
        return x

    # Function to save model's parameters
    def save_params(self, ex_dir, name='dis_params'):
        """
        Function to save the network's parameters.
        Args:
            ex_dir:     str, path where to save the network's parameters.
            name:       str, file name, default='dis_params'.
        """
        torch.save(self.state_dict(), join(ex_dir, name))

    # Function to load model's parameters
    def load_params(self, ex_dir, device='cpu', name='dis_params'):
        """
        Function to load the network's parameters.
        Args:
            ex_dir:     str, path where the network's parameters are stored.
            device:     str, device used ('cpu' or 'cuda'), default='cpu'
            name:       str, file name, default='dis_params'.
        """
        self.load_state_dict(torch.load(join(ex_dir, name),
                                        map_location=device))

    # Function to compute the loss
    @staticmethod
    def loss(pred, target):
        """
        Function to compute the discriminator's loss: binary cross entropy between the prediction and the target.
        Args:
            pred:       array of size (batch_size), probabilities for the 'real' class.
            target:     array of size (batch size), true labels.

        Returns:    float, binary cross entropy between the prediction and the target.
        """
        return F.binary_cross_entropy(pred, target, reduction='sum')
