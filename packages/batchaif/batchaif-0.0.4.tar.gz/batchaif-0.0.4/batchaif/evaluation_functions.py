# Import file managing library
import os

# Import numpy and pandas
import pandas as pd
import numpy as np

# Import useful functions
from batchaif.metrics_functions import compute_and_plot_best_clustering
from batchaif.batch_removal_functions import batch_removal_conditional_robust


# Function to run the evaluation pipeline
def run_evaluation_pipeline(cvae, adata, model_path, hyp=None,
                            label_projection=0.5, n_samplings=20, seed=42,
                            n_repetitions=20, save_plot=True, data_embedding='tsne',
                            prior_pca=False, n_components=None, clustering_method='kmeans',
                            metric_names=None, metric_best=None, norm_metrics=False,
                            range_batch=None, range_ct=None, shared_ct=None, add_pred=True,
                            percent_samples=0.8, cell_type_key='cell_type', batch_key='batch', perplexity=30,
                            colors_batch=None, colors_cell_types=None,
                            colors_clusters=None, remove_outliers=False, title_info='',
                            show_plot=True, percent_load=1, device='cpu', test_index=None,
                            min_cell_cluster=0, additional_info=None, add_to_previous=False,
                            save_metrics=True, model_file_name='cvae_params', *args, **kwargs):
    """
     Function to perform the evaluation pipeline on the corrected data.
     Args:
         cvae:                  CVAE model.
         adata:                 AnnData object, original data containing gene expression and observations.
         model_path:            str, path to the model's directory where to save the results.
         hyp:                   str, directory name for a specified combination of training hyperparameters,
                                default=None.
         label_projection:      float, batch label used for batches' distribution projection, default=0.5.
         n_samplings:           int, number of samples to draw from the latent distribution during batch effect
                                correction, default=20.
         seed:                  int, seed used to set the randomness, default=42.
         n_repetitions:         int, number of trainings to perform, default=20.
         save_plot:             bool, whether to save clustering plot, default=True.
         data_embedding:        str, embedding method on which to perform the KMeans, default='tsne'.
         prior_pca:             bool, whether to use pca prior to embedding algorithm, default=False.
         n_components:          int, number of components to use during the embedding of the data, default=None.
         clustering_method:     str, clustering method to use ('kmeans', 'louvain' or 'spectral_clustering'),
                                default='kmeans'.
         metric_names:          list, metrics to compute, default=None.
         metric_best:           str, metric to use to determine best clustering results, default=None.
         norm_metrics:          bool, whether to normalize the metrics before computing the F1 score, default=False.
         range_batch:           dict, ranges to use for normalization of the batch metrics, default=None.
         range_ct:              dict, ranges to use for normalization of the cell type metrics, default=None.
         shared_ct:             dict of bools, whether to use only shared cell types for each metric.
         add_pred:              bool, whether to add ASW metric using predicted labels, default=True.
         n_repetitions:         int, number of KMeans repetitions to run, default=20.
         percent_samples:       float, percentage of the data to use for the KMeans, default=0.8.
         cell_type_key:         str, key for cell type labels in adata, default='cell_type'.
         batch_key:             str, key for batch labels in adata, default='batch'.
         perplexity:            int, perplexity for LISI metric.
         colors_batch:          dict, colors for the batches, default=None.
         colors_cell_types:     dict, colors for the cell types, default=None.
         colors_clusters:       dict, colors for the KMeans clusters, default=None.
         remove_outliers:       bool, whether to remove the outliers in the clustering plots, default=False.
         title_info:            str, info for title in clustering plot, default=''.
         show_plot:             bool, whether to show plot, default=True.
         percent_load:          float, percent of data to load for batch effect correction step, default=1.
         device:                str, device to use ('cpu' or 'cuda'), default='cpu'.
         test_index:            list of int, list of index for test samples, default=None.
         min_cell_cluster:      int, minimum of cells for cluster to be taken into account in the metrics computation,
                                default=0.
         additional_info:       str, additional info for this experiment when saving files, default=None.
         add_to_previous:       bool, whether to add metrics to previous metrics dataframe, default=False.
         save_metrics:          bool, whether to save the metrics, default=True.
         model_file_name:       str, file name containing the model's parameters, default='cvae_params'.
     """

    # Parsing file name
    file_name = f'metrics_{clustering_method}'
    if additional_info is not None:
        file_name += '_' + additional_info

    # Copying colors dictionary
    colors_batch_copy = colors_batch.copy()
    colors_cell_types_copy = colors_cell_types.copy()
    colors_clusters_copy = colors_clusters.copy()

    # Retrieving training hyperparameters
    if hyp is None:
        training_hyp = [hyp for hyp in os.listdir(model_path) if 'bs' in hyp]
        training_hyp.sort()
    elif not isinstance(hyp, list):
        training_hyp = [hyp]
    else:
        training_hyp = hyp

    # Initialization of a dataframe to store the metrics
    if add_to_previous:
        metrics_df = pd.read_csv(f'{model_path}/{file_name}.csv', index_col=0)
        if test_index is not None:
            metrics_df_train = pd.read_csv(f'{model_path}/{file_name}_train.csv', index_col=0)
    else:
        metrics_df = pd.DataFrame()
        if test_index is not None:
            metrics_df_train = pd.DataFrame()

    # Removing small cell type clusters
    if min_cell_cluster > 0:
        ct_labels, counts = np.unique(adata.obs['cell_type'], return_counts=True)
        ct_labels = ct_labels[counts > min_cell_cluster]
        adata = adata[adata.obs['cell_type'].isin(ct_labels)]
        i_ct_removed = [i for i, key in enumerate(colors_cell_types_copy.keys()) if key in ct_labels]
        colors_ct_removed = list(map(colors_cell_types_copy.pop, list(set(colors_cell_types_copy.keys()) -
                                                                      set(ct_labels))))
        colors_clusters_removed = list(map(colors_clusters_copy.pop, i_ct_removed))

    # Computing the metrics
    for hyp_key_name in training_hyp:

        try:

            # Updating title info
            title_info_hyp = title_info + '\n' + hyp_key_name.replace('_', ' ')

            # Retrieving trained model
            cvae.load_params(f'{model_path}/{hyp_key_name}/', name=model_file_name)

            # Correcting data using robust batch removal based on conditional sampling
            corrected_data = batch_removal_conditional_robust(adata=adata, cvae=cvae,
                                                              label_projection=label_projection,
                                                              device=device, seed=seed,
                                                              n_samplings=n_samplings,
                                                              percent_load=percent_load)

            # Computing the metrics on the overall dataset
            results = compute_and_plot_best_clustering(corrected_data=corrected_data.X,
                                                       adata=adata, metric_names=metric_names,
                                                       data_embedding=data_embedding,
                                                       prior_pca=prior_pca,
                                                       clustering_method=clustering_method,
                                                       shared_ct=shared_ct,
                                                       n_components=n_components,
                                                       n_repetitions=n_repetitions,
                                                       percent_samples=percent_samples, seed=seed,
                                                       metric_best=metric_best, norm=norm_metrics,
                                                       range_batch=range_batch, range_ct=range_ct,
                                                       cell_type_key=cell_type_key, batch_key=batch_key,
                                                       colors_batch=colors_batch_copy,
                                                       colors_cell_types=colors_cell_types_copy,
                                                       colors_clusters=colors_clusters_copy,
                                                       remove_outliers=remove_outliers,
                                                       title_info=title_info_hyp,
                                                       save_plot=save_plot,
                                                       saving_path=f'{model_path}/{hyp_key_name}/',
                                                       add_pred=add_pred, perplexity=perplexity,
                                                       show_plot=show_plot, additional_info=additional_info,
                                                       *args, **kwargs)

            # Storing the metrics
            metrics_df = pd.concat([metrics_df, pd.DataFrame(results, columns=[hyp_key_name]).T], axis=0)

            # Computing the metrics on the training set and storing the results
            if test_index is not None:

                # Parsing additional info
                if additional_info is not None:
                    clustering_add_info = f'{additional_info}_train'
                else:
                    clustering_add_info = 'train'

                # Retrieving index for train dataset
                train_index = [i for i in range(0, len(corrected_data.X)) if i not in test_index]

                # Computing the metrics on the training set
                results_train = compute_and_plot_best_clustering(corrected_data=corrected_data.X[train_index, :],
                                                                 adata=adata[train_index], metric_names=metric_names,
                                                                 data_embedding=data_embedding,
                                                                 prior_pca=prior_pca,
                                                                 clustering_method=clustering_method,
                                                                 shared_ct=shared_ct,
                                                                 n_components=n_components,
                                                                 n_repetitions=n_repetitions,
                                                                 percent_samples=percent_samples, seed=seed,
                                                                 metric_best=metric_best, norm=norm_metrics,
                                                                 range_batch=range_batch, range_ct=range_ct,
                                                                 cell_type_key=cell_type_key, batch_key=batch_key,
                                                                 colors_batch=colors_batch_copy,
                                                                 colors_cell_types=colors_cell_types_copy,
                                                                 colors_clusters=colors_clusters_copy,
                                                                 remove_outliers=remove_outliers,
                                                                 title_info=title_info_hyp,
                                                                 save_plot=save_plot,
                                                                 saving_path=f'{model_path}/{hyp_key_name}/',
                                                                 add_pred=add_pred, perplexity=perplexity,
                                                                 show_plot=show_plot,
                                                                 additional_info=clustering_add_info,
                                                                 *args, **kwargs)

                # Storing the metrics
                metrics_df_train = pd.concat([metrics_df_train, pd.DataFrame(results_train,
                                                                             columns=[hyp_key_name]).T], axis=0)

        except:
            print(f"Evaluation failed for {model_path.split('/')[-1]} and {hyp_key_name}")

    # Saving metrics as csv file
    if save_metrics:
        metrics_df.to_csv(f'{model_path}/{file_name}.csv')
        if test_index is not None:
            metrics_df_train.to_csv(f'{model_path}/{file_name}_train.csv')

    # Returning the metrics
    if test_index is None:
        return metrics_df
    else:
        return metrics_df, metrics_df_train
