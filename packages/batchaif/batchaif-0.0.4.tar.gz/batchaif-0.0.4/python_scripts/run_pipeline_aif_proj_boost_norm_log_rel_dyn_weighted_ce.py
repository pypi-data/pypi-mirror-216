# Import useful system libraries
import os
import distutils.util
import argparse

# Import data useful libraries
import pandas as pd
import numpy as np
import anndata

# Import useful functions
from batchaif.training_functions import run_batch_effect_pipeline
from batchaif.models import CVAE, Discriminator, Auxiliary

# Retrieving useful environments variables
work_dir = os.environ.get('WORKDIR', os.getcwd())  # Working directory where the data is stored
file_name = os.environ.get('dataset_name', 'dataset_1')  # Dataset name
model_name = os.environ.get('model_name', 'aif_proj_boost_norm_log_rel_dyn_weighted_ce')  # Model name

# Creating a parser for hyperparameters given as arguments
parser = argparse.ArgumentParser()
parser.add_argument("--batch_size", type=int, default=32, help="Batch size for dataloaders")
parser.add_argument("--epochs", type=int, default=100, help="Number of epochs for training")
parser.add_argument("--learning_rate", type=float, default=1e-3, help="Learning rate for ADAM optimizer")
parser.add_argument("--beta_1", type=float, default=0.9, help="Beta 1 for ADAM optimizer")
parser.add_argument("--beta_2", type=float, default=0.99, help="Beta 2 for ADAM optimizer")
parser.add_argument("--alpha", type=float, default=0.2, help="Weight for KL loss")
parser.add_argument("--rho", type=float, default=0.1, help="Weight for classification loss")
parser.add_argument("--delta", type=float, default=0.1, help="Weight for generator loss")
parser.add_argument("--beta", type=float, default=0.0, help="Weight for classification after reconstruction loss")
parser.add_argument("--gamma", type=float, default=1, help="Weight for aux encoder loss")
parser.add_argument("--mu", type=float, default=0.1, help="Weight for projection loss")
parser.add_argument("--test", type=lambda x: bool(distutils.util.strtobool(x)), default=False,
                    help="Whether to evaluate on the test set")

# Parsing arguments
args = parser.parse_args()

# Training hyperparameters
epochs = args.epochs            # Epochs
lr = args.learning_rate         # Learning rate
batch_size = args.batch_size    # Batch size
beta_1 = args.beta_1            # Beta 1 for ADAM optimizer
beta_2 = args.beta_2            # Beta 2 for ADAM optimizer

# Loss hyperparameters
losses_weights_names = {'kl': 'alpha', 'class': 'rho', 'class_rec': 'beta', 'aux': 'gamma', 'gen': 'delta',
                        'proj': 'mu'}
losses_enc_weights = dict(zip(['mse'] + list(losses_weights_names.keys()),
                              [1] + [getattr(args, losses_weights_names[weight_key]) for weight_key
                                     in losses_weights_names.keys()]))

# Defining the model's specifications
nz = 100                            # Dimension of latent space

# CVAE
cvae_hidden_units = [800, 800]      # CVAE layers' hidden units
sigma = 1                           # Latent space variance for normal distribution
cvae_activation = 'ReLU'            # CVAE activation functions
norm = True                         # Adding batch normalization layers

# Discriminator
dis_hidden_units = [800, 800]       # Discriminator layers' hidden units
dis_activation = 'ReLU'             # Discriminator activation functions

# Auxiliary
aux_hidden_units = [800, 800]       # Auxiliary layers' hidden units
aux_activation = 'ReLU'             # Auxiliary activation functions

# Defining other useful variables
cell_type_key = 'cell_type'         # Cell type key in adata
batch_key = 'batch'                 # Batch key in adata
label_projection = 0                # Batch label used for projection
test = args.test                    # Whether to evaluate the model on the test set
seed = 42                           # Seed to set the randomness
plot = True                         # Whether to plot the losses evolution
save = {'cvae': True,               # Saving specifications
        'aux': False,
        'dis': False,
        'loss': True,
        'corrected_data': False,
        'time': True}
verbose = False                     # Verbosity
print_every = 1                     # Frequency of prints
device = 'cuda'                     # Device to use

# Defining optimization parameters
norm_data = True                    # Whether to use normalized data
log_transfo = True                  # Whether to use log1p transformation
early_stopping = True               # Whether to perform early stopping
min_epochs = int(0.9 * epochs)      # Minimum number of epochs for early stopping
losses_norm = {'mse': 'median',     # Normalization strategy for each loss
               'gen': 1 / 100,
               'dis': 1 / 100,
               'aux': 1 / 100}
weighting_strategy = 'rel'          # Weighting strategy to use
class_weights = None                # Weights for weighted cross entropy in case of unbalanced dataset
dynamic_ratio = 0.1                 # Percentage of the data to use for dynamic reweighting
grad_clip = None                    # Value to use for grad clipping
projection_constraint = {'random': True,    # Projection constraint to use
                         'avg': True}

# Dataset path, file's name and outputs directory name
root = f'{work_dir}/InData'
data_file = f'{work_dir}/data_preprocessed/{file_name}_norm_log.csv'
experiment_path = f'{work_dir}/Experiments'
results_path = f'{experiment_path}/{file_name}'
out_dir = f'{results_path}/single_run_analysis'

# Creating outputs directory
if not os.path.isdir(experiment_path):
    os.mkdir(experiment_path)
if not os.path.isdir(results_path):
    os.mkdir(results_path)
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)
if not (os.path.isdir(f'{out_dir}/{model_name}')):
    os.mkdir(f'{out_dir}/{model_name}')

# Importing original data
data = pd.read_csv(data_file, index_col=0, header=0)
# Creating annotated matrix in AnnData format with expression matrix
adata = anndata.AnnData(X=np.array(data.iloc[:, :-2]))
# Adding cell type and batch as observations
adata.obs[cell_type_key] = data[cell_type_key].tolist()
adata.obs[batch_key] = data[batch_key].tolist()

# Retrieving the number of batch labels and the input size
n_labels = len(data[batch_key].unique())
input_size = len(data.columns) - 2

# Defining class weights for weighted cross entropy as proportional to their inverse frequency
batch_labels, batch_counts = np.unique(adata.obs[batch_key], return_counts=True)
class_weights = batch_counts.sum() / batch_counts
class_weights = torch.Tensor(class_weights / class_weights.sum())

# Creating the model
model = {'cvae': CVAE(nz=nz, input_size=input_size, hidden_units=cvae_hidden_units, sigma=sigma,
                      activation=cvae_activation, norm=norm, n_labels=n_labels),
         'dis': Discriminator(input_size=input_size, hidden_units=dis_hidden_units, activation=dis_activation),
         'aux': Auxiliary(nz=nz, hidden_units=aux_hidden_units,
                          activation=aux_activation, n_labels=n_labels)}

# Running the batch effect removal pipeline
run_batch_effect_pipeline(model=model, adata=adata, batch_size=batch_size, epochs=epochs, lr=lr, beta_1=beta_1,
                          beta_2=beta_2, root=root, results_path=out_dir, file_name=file_name, model_name=model_name,
                          losses_enc_weights=losses_enc_weights, weighting_strategy=weighting_strategy,
                          losses_norm=losses_norm,
                          seed=seed, norm_data=norm_data, log_transfo=log_transfo, label_projection=label_projection,
                          n_labels=n_labels,
                          plot=plot, save=save, verbose=verbose, print_every=print_every, device=device,
                          early_stopping=early_stopping, min_epochs=min_epochs,
                          test=test, dynamic_ratio=dynamic_ratio, class_weights=class_weights, grad_clip=grad_clip,
                          projection_constraint=projection_constraint)
