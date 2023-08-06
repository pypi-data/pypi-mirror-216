# Import useful system libraries
import os
import argparse
import distutils.util

# Import data useful libraries
import pandas as pd
import numpy as np
import anndata

# Import plotting libraries
import matplotlib.pyplot as plt

# Import useful functions
from batchaif.training_functions import robust_grid_search
from batchaif.models import CVAE, Discriminator, Auxiliary

# Retrieving useful environments variables
work_dir = os.environ.get('WORKDIR', os.getcwd())               # Working directory where the data is stored
file_name = os.environ.get('dataset_name', 'dataset_2')         # Dataset name
model_name = os.environ.get('model_name', 'aif_proj_boost_rel_dyn_aux_dis_delayed')        # Model name

# Dataset path, file's name and outputs directory name
root = f'{work_dir}/batch_effects_biomed/attribute-cVAEGAN/InData'
data_file = f'{work_dir}/batch_effects_biomed/data_preprocessed/{file_name}.csv'
experiment_path = f'{work_dir}/batch_effects_biomed/attribute-cVAEGAN/Experiments'
results_path = f'{experiment_path}/{file_name}'
out_dir = f'{results_path}/multi_run_analysis'
hyperparameters_file = f'{out_dir}/robust_proj_hyperparameters_set.csv'

# Creating outputs directory
if not os.path.isdir(experiment_path):
    os.mkdir(experiment_path)
if not os.path.isdir(results_path):
    os.mkdir(results_path)
if not os.path.isdir(out_dir):
    os.mkdir(out_dir)

# Creating a parser for hyperparameters given as arguments
parser = argparse.ArgumentParser()
parser.add_argument("--job_index", type=int, help="SLURM array task id")
parser.add_argument("--batch_size_list", type=int, nargs='+', default=[32], help="Batch size for dataloaders")
parser.add_argument("--epochs", type=int, default=100, help="Number of epochs for training")
parser.add_argument("--learning_rate_list", type=float, nargs='+', default=[1e-3],
                    help="Learning rate for ADAM optimizer")
parser.add_argument("--beta_1_list", type=float, nargs='+', default=[0.9], help="Beta 1 for ADAM optimizer")
parser.add_argument("--beta_2_list", type=float, nargs='+', default=[0.99], help="Beta 2 for ADAM optimizer")
parser.add_argument("--test", type=lambda x: bool(distutils.util.strtobool(x)), default=False,
                    help="Whether to evaluate on the test set")

# Parsing arguments
args = parser.parse_args()

# Retrieving job index
job_index = args.job_index  # Job index, e.g. index corresponding to the set of hyperparameters to try

# Retrieving the corresponding set of hyperparameters
hyperparameters = pd.read_csv(hyperparameters_file).iloc[job_index - 1, :]

# Training hyperparameters
epochs = args.epochs                    # Epochs
lr_list = args.learning_rate_list       # Learning rate
batch_size_list = args.batch_size_list  # Batch size
beta_1_list = args.beta_1_list          # Beta 1 for ADAM optimizer
beta_2_list = args.beta_2_list          # Beta 2 for ADAM optimizer

# Loss hyperparameters
losses_weights_names = {'kl': 'alpha', 'class': 'rho', 'class_rec': 'beta', 'aux': 'gamma', 'gen': 'delta',
                        'proj': 'mu'}
losses_enc_weights = dict(zip(['mse'] + list(losses_weights_names.keys()),
                              [1] + list(hyperparameters.loc[losses_weights_names.values()])))

# Renaming the model to add the information of the weights
for loss_key in losses_weights_names.keys():
    model_name += f'_{losses_weights_names[loss_key]}_{losses_enc_weights[loss_key]}'

# Defining the model's specifications
nz = 100                        # Dimension of latent space

# CVAE
cvae_hidden_units = [800, 800]  # CVAE layers' hidden units
sigma = 1                       # Latent space variance for normal distribution
cvae_activation = 'ReLU'        # CVAE activation functions
norm = True                     # Adding batch normalization layers

# Discriminator
dis_hidden_units = [800, 800]   # Discriminator layers' hidden units
dis_activation = 'ReLU'         # Discriminator activation functions

# Auxiliary
aux_hidden_units = [800, 800]   # Auxiliary layers' hidden units
aux_activation = 'ReLU'         # Auxiliary activation functions


# Defining other useful variables
cell_type_key = 'cell_type'         # Cell type key in adata
batch_key = 'batch'                 # Batch key in adata
label_projection = 0                # Batch label used for projection
test = args.test                    # Whether to evaluate the model on the test set
seed = 42                           # Seed to set the randomness
plot = True                         # Whether to plot the losses evolution
n_repetitions = 10                  # Number of trainings to run for robustness
n_samplings = 20                    # Number of samplings to draw for batch effect correction
save = {'cvae': {'median': True,    # Saving specifications
                 'min': True},
        'loss': True,
        'time': True,
        'metrics': True,
        'metrics_viz': True}
verbose = False                     # Verbosity
print_every = 1                     # Frequency of prints
device = 'cpu'                      # Device to use (e.g. 'cpu' or 'cuda')
add_to_previous = False             # Whether to add the results to previous results
seed_list = None                    # List of seeds to use
exp_names = None                    # Name of the experiments

# Defining optimization parameters
norm_data = False               # Whether to use normalized data
log_transfo = False             # Whether to perform log1p transformation
early_stopping = True           # Whether to perform early stopping
min_epochs = int(0.9 * epochs)  # Minimum number of epochs for early stopping
losses_norm = {}                # Normalization strategy for each loss
weighting_strategy = 'rel'      # Whether to use relative weighting
dynamic_ratio = 0.1             # Percentage of the data to use for dynamic reweighting
grad_clip = None                # Value to use for grad clipping
update_aux_freq = 1/300         # Frequency at which to update the auxiliary network
update_dis_freq = 1/300         # Frequency at which to update the GAN network
projection_constraint = {'random': True,    # Projection constraint to use
                         'avg': True}


# Parameters related to the metrics
n_components = 20                           # Number of components to use in PCA
n_repetitions_kmeans = 20                   # Number of KMeans to run
percent_samples = 0.8                       # Percent of dataset to use for computing the metrics
data_embedding = 'tsne'                     # Embedding algorithm to use (e.g. tsne, umap or pca)
remove_outliers = False                     # Whether to remove the outliers in clustering visualization
metric_names = ['ARI', 'ASW', 'LISI']       # Metric names
shared_ct = {'LISI': True, 'ARI': True,     # Whether to use the shared cell types for the batch metrics
             'ASW': False}
metric_best = 'F1_ARI'                      # Metric to use to determine the best clustering
perplexity = 30                             # Perplexity to use to determine the neighborhood for LISI
add_pred = True                             # Whether to add cell type ASW computed on predicted clusters
norm_metrics = False                        # Whether to normalize the metrics prior to computing F1 score
class_weights = None

# Importing original data
data = pd.read_csv(data_file, index_col=0, header=0)
# Creating annotated matrix in AnnData format with expression matrix
adata = anndata.AnnData(X=np.array(data.iloc[:, 0:-2]))
# Adding cell type and batch as observations
adata.obs[cell_type_key] = data[cell_type_key].tolist()
adata.obs[batch_key] = data[batch_key].tolist()

# Retrieving the number of batch labels and the input size
n_labels = len(data[batch_key].unique())
input_size = len(data.columns) - 2

# Defining colors vectors
colors_batch = ['#24bca8', '#448ee4', '#cb0162', '#fc824a', '#ffda03']
colors_cell_types = ['tab:blue', '#75bbfd', '#24bca8',
                     'tab:orange', '#ffda03', '#d5ab09',
                     'tab:green', '#99cc04', '#9be5aa',
                     'tab:red', '#8c0034', '#fc86aa',
                     '#ac1db8', '#c48efd', '#758da3']
cmap = plt.cm.get_cmap('viridis')

# Retrieving unique batch labels and cell type labels
batch_labels = data[batch_key].unique()
batch_labels.sort()
cell_type_labels = data[cell_type_key].unique().tolist()
cell_type_labels.sort(key=lambda y: y.lower())

# Defining dictionary for cell types and batches and clusters colors
colors_cell_types_dict = dict(zip(cell_type_labels, colors_cell_types[::int(len(colors_cell_types) /
                                                                            len(cell_type_labels))]))
colors_batch_dict = dict(zip(batch_labels, colors_batch[::int(len(colors_batch) / len(batch_labels))]))
colors_clusters = dict(zip(range(len(cell_type_labels)),
                           [cmap(i / len(cell_type_labels)) for i in range(len(cell_type_labels))]))

# Defining ranges for normalizing the metrics prior to computing F1 score
range_batch = {'ARI': [0, 2],               # Range for batch metrics
               'ASW': [0, 2],
               'LISI': [1, len(np.unique(adata.obs[batch_key]))]}
range_ct = {'ARI': [-1, 1],                 # Range for batch metrics
            'ASW': [-1, 1],
            'LISI': [1, -len(np.unique(adata.obs[cell_type_key]))]}

# Creating the model
model = {'cvae': CVAE(nz=nz, input_size=input_size, hidden_units=cvae_hidden_units, sigma=sigma,
                      activation=cvae_activation, norm=norm, n_labels=n_labels),
         'dis': Discriminator(input_size=input_size, hidden_units=dis_hidden_units, activation=dis_activation),
         'aux': Auxiliary(nz=nz, hidden_units=aux_hidden_units,
                          activation=aux_activation, n_labels=n_labels)}

# Running a robust grid search
robust_grid_search(model=model, lr_list=lr_list, batch_size_list=batch_size_list,
                   beta_1_list=beta_1_list, beta_2_list=beta_2_list, adata=adata,
                   root=root, file_name=file_name, model_name=model_name, results_path=out_dir,
                   losses_enc_weights=losses_enc_weights, weighting_strategy=weighting_strategy, losses_norm=losses_norm,
                   max_epochs=epochs, projection_constraint=projection_constraint, update_dis_freq=update_dis_freq,
                   update_aux_freq=update_aux_freq, label_projection=label_projection, n_samplings=n_samplings, n_labels=n_labels,
                   seed=seed, n_repetitions=n_repetitions, seed_list=seed_list, exp_names=exp_names, plot=plot,
                   norm_data=norm_data, log_transfo=log_transfo, save=save, verbose=verbose, print_every=print_every,
                   device=device, early_stopping=early_stopping, min_epochs=min_epochs, data_embedding=data_embedding,
                   n_components=n_components, metric_names=metric_names, metric_best=metric_best, shared_ct=shared_ct,
                   norm_metrics=norm_metrics, range_batch=range_batch, range_ct=range_ct,
                   n_repetitions_kmeans=n_repetitions_kmeans, add_to_previous=add_to_previous,
                   percent_samples=percent_samples, cell_type_key=cell_type_key, batch_key=batch_key,
                   colors_batch=colors_batch_dict, colors_cell_types=colors_cell_types_dict,
                   colors_clusters=colors_clusters, remove_outliers=remove_outliers, test=test,
                   dynamic_ratio=dynamic_ratio, class_weights=class_weights, grad_clip=grad_clip)
