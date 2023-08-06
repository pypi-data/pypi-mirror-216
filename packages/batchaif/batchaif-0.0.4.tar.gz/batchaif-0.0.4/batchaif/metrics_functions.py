# Import array and dataframe libraries
import anndata

# Import plotting libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc

# Import ML algorithms
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, SpectralClustering
from sklearn.neighbors import NearestNeighbors
from sknetwork.clustering import Louvain, modularity

# Import metrics
from sklearn.metrics import adjusted_rand_score
from sklearn.metrics import silhouette_score
from harmonypy.lisi import compute_simpson


# Function to find optimal mapping
def find_optimal_mapping(labels_map, n_labels_map):
    """
    Function to find the optimal mapping between 2 labels list.
    Args:
        labels_map:
        n_labels_map:

    Returns:

    """
    # Initialization of results
    results = []

    # If labels left, do the same procedure recursively
    if len(np.unique(labels_map[:, 1])) > 0:
        # Retrieving maximum occurrences label mapping
        i_max = n_labels_map.argmax()
        label_max = labels_map[i_max, 0]

        # Adding the results to the list
        results.append(labels_map[i_max].tolist())

        # Removing label from labels map and n_labels_map
        i_keep = (labels_map[:, 0] != label_max)
        labels_map = labels_map[i_keep, :]
        n_labels_map = n_labels_map[i_keep]

        # Recursively finding optimal mapping and adding it to results
        results += find_optimal_mapping(labels_map=labels_map, n_labels_map=n_labels_map)

    # Returning the results
    return results


# Function to compute dimensionality reduction algorithm
def compute_dim_reduction(data, data_embedding='pca', n_components=20, seed=42, prior_pca=False):
    """
    Function to compute dimensionality reduction algorithm among 'pca', 'tsne' or 'umap'.
    Args:
        data:               array of size (N_samples, N_features), data on which to compute dimensionality reduction.
        data_embedding:     str, embedding method to use ('pca', 'tsne', 'umap'), default='pca'.
        n_components:       int, number of components to use in the PCA, default=20.
        seed:               int, seed used to set the randomness, default=42.
        prior_pca:          bool, whether to use pca prior to the embedding algorithm, default=False.
    Returns: array of size (N_samples, N_features_red), the dimensionally reduced features.
    """

    # Principal Component Analysis (PCA)
    if data_embedding.casefold() == 'pca'.casefold():
        pca = PCA(n_components=n_components, random_state=seed)
        embedded_data = pca.fit_transform(data)

    # t-SNE embedding
    elif data_embedding.casefold() == 'tsne'.casefold():
        adata = anndata.AnnData(data)
        if prior_pca:
            sc.tl.tsne(adata, random_state=seed)
        else:
            sc.tl.tsne(adata, use_rep='X', random_state=seed)
        embedded_data = adata.obsm['X_tsne']

    # UMAP embedding
    elif data_embedding.casefold() == 'umap'.casefold():
        adata = anndata.AnnData(data)
        if prior_pca:
            sc.pp.neighbors(adata)
        else:
            sc.pp.neighbors(adata, use_rep='X')
        sc.tl.umap(adata, random_state=seed, n_components=n_components)
        embedded_data = adata.obsm['X_umap']

    # No embedding
    else:
        embedded_data = data

    # Returning the embedded data
    return embedded_data


# Function to compute K-means algorithm for either cell type or batch label
def compute_km(data, true_clusters, percent_samples=0.8, seed=42):
    """
    Function to compute KMeans algorithm for either the cell type or the batch label.
    Args:
        data:               array of size (N_samples, N_features), data on which to compute KMeans.
        true_clusters:      array of size (N_samples), true clusters labels.
        percent_samples:    float, percentage of the data to use to compute KMeans, default=0.8.
        seed:               int, seed used to set the randomness, default=42.
    Returns: (results, samples_id), the predicted labels and the id of the samples used.
    """
    # Setting randomness by initializing a random generator
    rng = np.random.default_rng(seed)

    # Determining number of samples to use
    n_samples = int(percent_samples * data.shape[0])

    # Extracting samples
    samples_id = rng.choice(data.shape[0], n_samples, replace=False)
    samples = data[samples_id]

    # Creating the KMeans model and fitting it to the samples chosen
    model = KMeans(n_clusters=len(np.unique(true_clusters)),
                   random_state=seed).fit(samples)
    clusters = model.labels_

    # Concatenating the samples, the clusters attributed and the true clusters
    results = np.concatenate([samples, np.array(clusters).reshape(-1, 1),
                              np.array(true_clusters[samples_id]).reshape(-1, 1)],
                             axis=1)

    # Returning the results and the samples id
    return results, samples_id


# Function to compute spectral clustering algorithm for either cell type or batch label
def compute_spectral_clustering(data, true_clusters, percent_samples=0.8, seed=42,
                                affinity='nearest_neighbors', n_neighbors=20,
                                gamma=None, *args, **kwargs):
    """
    Function to compute spectral clustering algorithm for either the cell type or the batch label.
    Args:
        data:               array of size (N_samples, N_features), data on which to compute KMeans.
        true_clusters:      array of size (N_samples), true clusters labels.
        percent_samples:    float, percentage of the data to use to compute KMeans, default=0.8.
        affinity:           string, affinity method to use, default='nearest_neighbors'.
        n_neighbors:        int, number of neighbors to use in kNN, default=20.
        seed:               int, seed used to set the randomness, default=42.
    Returns: (results, samples_id), the predicted labels and the id of the samples used.
    """
    # Setting randomness by initializing a random generator
    rng = np.random.default_rng(seed)

    # Determining number of samples to use
    n_samples = int(percent_samples * data.shape[0])

    # Extracting samples
    samples_id = rng.choice(data.shape[0], n_samples, replace=False)
    samples = data[samples_id]

    # Creating the Spectral Clustering model and fitting it to the samples chosen
    model = SpectralClustering(n_clusters=len(np.unique(true_clusters)),
                               affinity=affinity, n_neighbors=n_neighbors,
                               gamma=gamma, random_state=seed).fit(samples)
    clusters = model.labels_

    # Concatenating the samples, the clusters attributed and the true clusters
    results = np.concatenate([samples, np.array(clusters).reshape(-1, 1),
                              np.array(true_clusters[samples_id]).reshape(-1, 1)],
                             axis=1)

    # Returning the results and the samples id
    return results, samples_id


# Function to compute Louvain algorithm for either cell type or batch label
def compute_louvain(data, percent_samples=0.8, seed=42, n_neighbors=20, resolution=1,
                    modularity_method='newman', init_graph='knn', weighted_graph=False,
                    radius=1, tol=1e-3, prune=0, *args, **kwargs):
    """
    Function to compute KMeans algorithm for either the cell type or the batch label.
    Args:
        data:               array of size (N_samples, N_features), data on which to compute KMeans.
        percent_samples:    float, percentage of the data to use to compute KMeans, default=0.8.
        seed:               int, seed used to set the randomness, default=42.
        n_neighbors:        int, number of neighbors for kNN graph, default=20.
        resolution:         float, resolution for Louvain algorithm, default=1.
        modularity_method:  str, modularity for Louvain algorithm, default='newman'.
        init_graph:         str, method to compute initial graph, default='knn'.
        weighted_graph:     bool, whether to use weighted graph or not, default=False.
        radius:             float, radius used for Nearest Neighbor, default=1.
        tol:                float, minimum increase for optimization and aggregation passes, default=1e-3.
        prune:              float, jaccard index threshold when computing Shared Neighborhood Graph, default=0.
    Returns: (results, samples_id), the predicted labels and the id of the samples used.
    """
    # Setting randomness by initializing a random generator
    rng = np.random.default_rng(seed)

    # Determining number of samples to use
    n_samples = int(percent_samples * data.shape[0])

    # Extracting samples
    samples_id = rng.choice(data.shape[0], n_samples, replace=False)
    samples = data[samples_id]

    # Creating the original graph
    neighbors = NearestNeighbors(n_neighbors=n_neighbors, radius=radius).fit(samples)
    if init_graph.casefold() == 'knn'.casefold():
        if weighted_graph:
            adj = neighbors.kneighbors_graph(samples, mode='connectivity').toarray()
            distances = neighbors.kneighbors_graph(samples, mode='distance').toarray()
            adj[(adj == 1) & (distances > 0)] = 1 / distances[(adj == 1) & (distances > 0)]
            adj = adj * np.apply_along_axis(lambda x: x[x > 0].min(), 1, distances)
            adj[np.eye(adj.shape[0]) == 1] = 1
        else:
            adj = neighbors.kneighbors_graph(samples, mode='connectivity').toarray()
    elif init_graph.casefold() == 'rad_nn'.casefold():
        if weighted_graph:
            adj = neighbors.radius_neighbors_graph(radius=radius, mode='connectivity').toarray()
            distances = neighbors.radius_neighbors_graph(radius=radius, mode='distance').toarray()
            adj[(adj == 1) & (distances > 0)] = 1 / distances[(adj == 1) & (distances > 0)]
            adj = adj * np.apply_along_axis(lambda x: x[x > 0].min(), 1, distances)
            adj[np.eye(adj.shape[0]) == 1] = 1
        else:
            adj = neighbors.radius_neighbors_graph(radius=radius, mode='connectivity').toarray()
    elif init_graph.casefold() == 'snn'.casefold():
        knn_adj = neighbors.kneighbors_graph(n_neighbors=n_neighbors, mode='connectivity').toarray()
        knn_adj += np.eye(knn_adj.shape[0])
        count_shared_neighbors = knn_adj.dot(knn_adj.T)
        adj = count_shared_neighbors / (2 * (n_neighbors + 1) - count_shared_neighbors)
        adj[adj < prune,] = 0

    # Creating Louvain model and fitting it to the samples chosen
    louvain = Louvain(resolution=resolution, modularity=modularity_method,
                      tol_aggregation=tol, tol_optimization=tol)
    clusters = louvain.fit_transform(adj)

    # Computing final modularity
    modularity_ = modularity(adjacency=adj,
                             labels=clusters,
                             resolution=resolution)

    # Returning the clusters and the samples id
    return clusters, samples_id, modularity_


# Function to compute Louvain with known number of clusters
def compute_best_louvain(data, true_clusters, percent_samples=0.8, seed=42, modularity_method='newman',
                         max_iter=10, n_neighbors=20, tol=1e-3, best_criteria=None,
                         init_graph='knn', weighted_graph=False, radius=1, prune=0, *args, **kwargs):
    """
    Function to compute best-matching Louvain clustering knowing the number of clusters, using resolution parameter's
    dichotomy search.
    Args:
        data:               array of size (N_samples, N_features), data on which to compute the clustering.
        true_clusters:      array of size (N_samples), true clusters labels.
        modularity_method:  str, clustering method to use ('kmeans' or 'louvain'), default='kmeans'.
        percent_samples:    float, percentage of samples on which to compute the clustering, default=0.8.
        seed:               int, seed for setting the split's randomness, default=42.
        modularity_method:  str, modularity method to use for Louvain, default='newman'.
        max_iter:           int, maximum number of iterations, default=10.
        n_neighbors:        int, number of neighbors for computing initial graph for Louvain, default=20.
        tol:                float, minimum increase for optimization and aggregation passes, default=1e-3.
        best_criteria:      str, criteria to use to retain best louvain clustering, default=None.
        init_graph:         str, method to compute initial graph, default='knn'.
        weighted_graph:     bool, whether to use weighted graph or not, default=False.
        radius:             float, radius used for Nearest Neighbor, default=1.
        prune:              float, jaccard index threshold when computing Shared Neighborhood Graph, default=0.
    Returns:    (clusters, samples_id), the best predicted labels and the id of the samples used.
    """

    # Initialization of useful variables
    resolution = 1
    step = 0.5
    i_iter = 0
    n_clusters_pred = 0
    n_clusters = len(np.unique(true_clusters))
    best_metric = - np.inf
    best_clusters = None
    best_samples_id = None

    # Dichotomy on resolution parameter
    while (i_iter < max_iter) and (n_clusters_pred != n_clusters):

        # Computing clusters
        clusters, samples_id, metric = compute_louvain(data=data, percent_samples=percent_samples,
                                                       seed=seed, modularity_method=modularity_method,
                                                       n_neighbors=n_neighbors, resolution=resolution,
                                                       tol=tol, weighted_graph=weighted_graph,
                                                       init_graph=init_graph, radius=radius, prune=prune,
                                                       *args, **kwargs)

        # Updating the best criteria and clustering
        if best_criteria is not None:
            if best_criteria.casefold() == 'modularity'.casefold():
                condition_best = (metric >= best_metric)
            elif best_criteria.casefold() == 'ari'.casefold():
                metric = compute_ari(true_clusters=true_clusters[samples_id],
                                     clusters=clusters)
                condition_best = (metric >= best_metric)
        else:
            condition_best = True
        if condition_best:
            best_metric = metric
            best_clusters = clusters
            best_samples_id = samples_id

        # Updating n_clusters predicted
        n_clusters_pred = len(np.unique(clusters))

        # Updating resolution
        if n_clusters_pred > n_clusters:
            resolution -= step
        else:
            resolution += step

        # Decreasing step
        step = step / 2

        # Updating count
        i_iter += 1

    # Processing output
    results = np.concatenate([data[best_samples_id],
                              np.array(best_clusters).reshape(-1, 1),
                              np.array(true_clusters[best_samples_id]).reshape(-1, 1)],
                             axis=1)

    # Returning results and samples id
    return results, best_samples_id


# Function to compute clusters
def compute_clustering(data, true_clusters, method='kmeans', percent_samples=0.8, seed=42, *args, **kwargs):
    """
    Function to compute clustering.
    Args:
        data:            array of size (N_samples, N_features), data on which to compute the clustering.
        true_clusters:   array of size (N_samples), true clusters labels.
        method:          str, clustering method to use ('kmeans', 'louvain' or 'spectral_clustering'),
                         default='kmeans'.
        percent_samples: float, percentage of samples on which to compute the clustering, default=0.8.
        seed:            int, seed for setting the split's randomness, default=42.
    Returns:    (clusters, samples_id), the predicted clusters labels vector and the corresponding samples' id vector.
    """

    # Computing KMeans clustering
    if method.casefold() == 'kmeans'.casefold():
        clusters, samples_id = compute_km(data=data, true_clusters=true_clusters, percent_samples=percent_samples,
                                          seed=seed)

    # Computing Louvain clustering
    elif method.casefold() == 'louvain'.casefold():
        clusters, samples_id = compute_best_louvain(data=data, true_clusters=true_clusters,
                                                    percent_samples=percent_samples,
                                                    seed=seed, *args, **kwargs)

    # Computing Spectral Clustering
    elif method.casefold() == 'spectral_clustering'.casefold():
        clusters, samples_id = compute_spectral_clustering(data=data, true_clusters=true_clusters,
                                                           percent_samples=percent_samples,
                                                           seed=seed, *args, **kwargs)

    # Returning clustering
    return clusters, samples_id


# Function to compute the ARI metric
def compute_ari(clusters, true_clusters, *args, **kwargs):
    """
    Function to compute the Adjusted Rand Index between the predicted and the true labels.
    Args:
        clusters:       array of size (N_samples), predicted clusters labels.
        true_clusters:  array of size (N_samples), true clusters labels.

    Returns:    float, ARI between predicted and true clusters labels.

    """
    # Returning the adjusted rand index score
    return adjusted_rand_score(clusters, true_clusters)


# Function to compute the silhouette score
def compute_asw(data, clusters, *args, **kwargs):
    """
    Function to compute the silhouette score on the data using the clusters labels.
    Args:
        data:       array of size (N_samples, N_features), data on which to compute the ASW.
        clusters:   array of size (N_samples), clusters labels.
    Returns:    float, silhouette score computed on the data using the clusters labels.
    """
    # Returning the silhouette score
    return silhouette_score(data, clusters)


# Function to compute the Local Inverse Simpson Index (LISI)
def compute_lisi(data, clusters, perplexity=30, eps=1e-12, *args, **kwargs):
    """
    Function to compute the median Local Inverse Simpson Index over the samples using the clusters labels.
    Args:
        data:        array of size (N_samples, N_features), data on which to compute the LISI.
        clusters:    array of size (N_samples), clusters labels.
        perplexity:  float, perplexity for neighborhood definition, default=30.
        eps:         float, safety for division by 0, default=1e-12.
    Returns:    list, Local Inverse Simpson Index computed for each sample using the clusters labels.
    """

    # Retrieving number of labels
    n_labels = len(np.unique(clusters))

    # Computing the nearest neighbors
    neighbors = NearestNeighbors(n_neighbors=3 * perplexity).fit(data)
    distances, indices = neighbors.kneighbors(data)

    # Removing itself from neighbors
    distances = distances[:, 1:]
    indices = indices[:, 1:]

    # Compute Simpson Index based on local neighborhood
    simpson_index = compute_simpson(distances=distances.T, indices=indices.T,
                                    labels=pd.Categorical(clusters),
                                    n_categories=n_labels, perplexity=perplexity)

    # Returning the median LISI score
    return np.median(1 / (simpson_index + eps))


# Function to compute the appropriate metric based on the metric name given
def compute_metric(metric_name, clusters, true_clusters, *args, **kwargs):
    """
    Function to compute a clustering metric among ARI, ASW and LISI.
    Args:
        metric_name:    str, name of the metric among ('ARI', 'ASW', 'LISI').
        clusters:       vector of size (N_samples), predicted clustering labels.
        true_clusters:  vector of size (N_samples), true clusters labels.
    Returns:    float, corresponding computed metric.
    """
    # Computing ARI
    if metric_name.casefold() == 'ARI'.casefold():
        return compute_ari(clusters=clusters, true_clusters=true_clusters, *args, **kwargs)

    # Computing ASW
    elif metric_name.casefold() == 'ASW'.casefold():
        return compute_asw(clusters=true_clusters, *args, **kwargs)

    # Computing LISI
    elif metric_name.casefold() == 'LISI'.casefold():
        return compute_lisi(clusters=true_clusters, *args, **kwargs)


# Function to compute the F1 score : batch mixing and cell type purity
def compute_f1_score(metric_batch, metric_ct, norm=False, range_batch=None, range_ct=None):
    """
    Function to compute the F1 score between the batch ARI and cell type ARI.
    Args:
        metric_batch:  float, batch metric.
        metric_ct:     float, cell type metric.
        norm:          bool, whether to normalize the metrics before computing the F1 score, default=False.
        range_batch:   list of floats, range for the batch metric, default=None.
        range_ct:      list of floats, range for the cell type metric, default=None.
    Returns:    float, F1 score between batch and cell type metrics.
    """

    # Normalizing the metrics so that they range from 0 to 1
    if norm:
        if range_batch is not None:
            metric_batch = (metric_batch - min(range_batch)) / (max(range_batch) - min(range_batch))
        if range_ct is not None:
            metric_ct = (metric_ct - min(range_ct)) / (max(range_ct) - min(range_ct))

    # Returning the F1 score for the metrics
    return (2 * metric_batch * metric_ct) / (metric_batch + metric_ct)


# Function to compute all the metrics
def compute_metrics(corrected_data, adata, n_components=20, n_repetitions=20, percent_samples=0.8,
                    seed=42, cell_type_key='cell_type', batch_key='batch', metric_names=None, shared_ct=None,
                    clustering_method='kmeans', data_embedding='pca', prior_pca=False, add_pred=False,
                    return_best=False, metric_best=None, norm=False, range_batch=None, range_ct=None, perplexity=30,
                    *args, **kwargs):
    """
    Function to compute all the clustering metrics on the corrected data.
    Args:
        corrected_data:     array of size (N_samples, N_features), corrected data.
        adata:              AnnData object, original data (gene expression and observations).
        n_components:       int, number of components to use in the PCA, default=20.
        n_repetitions:      int, number of repetitions for KMeans, default=20.
        percent_samples:    float, percentage of the data to use for each KMeans, default=0.8.
        seed:               int, seed used to set the randomness, default=42.
        cell_type_key:      str, key for cell type label in original data, default='cell_type'.
        batch_key:          str, key for batch label in original data, default='batch'.
        metric_names:       list of str, names of the metrics to compute, default=None.
        shared_ct:          dict of bools, whether to use only shared cell types for each metric, default=None.
        clustering_method:  str, clustering method to use, default='kmeans'.
        data_embedding:     str, embedding method to use, default='pca'.
        prior_pca:          bool, whether to use PCA prior to the embedding method, default=False.
        add_pred:           bool, whether to add the metrics computed based on the KMeans predictions, default=False.
        return_best:        bool, whether to return the best KMeans clusters, default=False.
        metric_best:        str, metric to use to determine the best KMeans clusters, default=None.
        norm:               bool, whether to normalize the metrics, default=False.
        range_batch:        dict, batch metrics ranges to use to normalize the metrics, default=None.
        range_ct:           dict, cell type metrics ranges to use to normalize the metrics, default=None.
        perplexity:         int, perplexity to determine the neighborhood for LISI, default=30.
        *args:              list of parameters for clustering method.
        **kwargs:           named list of parameters for clustering method.
    Returns:    pd.Series, array containing all the metrics median and maximum values.
    """

    # Parsing default argument
    if metric_names is None:
        metric_names = ['ARI', 'ASW']
        shared_ct = {'ARI': True, 'ASW': False}
    if metric_best is None:
        metric_best = f'F1_{metric_names[0]}'
    if shared_ct is None:
        shared_ct = dict(zip(metric_names, [True for _ in range(len(metric_names))]))
    if norm:
        if range_batch is None:
            range_batch = dict(zip(['ARI', 'ASW', 'LISI'],
                                   [[-1, 1], [0, 2], [1, len(np.unique(adata.obs[batch_key]))]]))
        if range_ct is None:
            range_ct = dict(zip(['ARI', 'ASW', 'LISI'],
                                [[-1, 1], [0, 2], [0, -len(np.unique(adata.obs[cell_type_key]))]]))
    else:
        range_batch = dict(zip(['ARI', 'ASW', 'LISI'],
                               [None, None, None]))
        range_ct = dict(zip(['ARI', 'ASW', 'LISI'],
                            [None, None, None]))

    # Storing all metrics names
    all_metrics = []
    for metric in metric_names:
        if metric in ['ARI', 'ASW']:
            all_metrics += [f'{metric}_CT', f'1-{metric}_B', f'F1_{metric}']
            if metric.casefold() == 'ASW'.casefold() and add_pred:
                all_metrics += [f'{metric}_CT_pred', f'F1_{metric}_pred']
        elif metric.casefold() == 'LISI'.casefold():
            all_metrics += [f'1-{metric}_CT', f'{metric}_B', f'F1_{metric}']
        else:
            all_metrics += [f'{metric}_CT', f'{metric}_B', f'F1_{metric}']

    # Initialization of a dictionary to store the results
    metrics_results = dict(zip(all_metrics,
                               [np.zeros(n_repetitions) for _ in range(len(all_metrics))]))

    # Initialization of useful variables to return best results
    best_metric = - np.inf
    best_results = None
    best_samples_id = None

    # Initialization of a list to store shared cell types
    shared_cell_types = []

    # Retrieving shared cell types
    for CT in np.unique(adata.obs[cell_type_key]):
        if len(np.unique(adata.obs[batch_key][adata.obs[cell_type_key] == CT])) > 1:
            shared_cell_types.append(CT)

    # Compute dimensionality reduction algorithm
    embedded_data = compute_dim_reduction(data=corrected_data, data_embedding=data_embedding,
                                          n_components=n_components,
                                          seed=seed, prior_pca=prior_pca)

    # For each repetition, compute KMeans on a subset of the embedded data
    for j in range(n_repetitions):

        # Compute clustering for cell types
        results, samples_id = compute_clustering(data=embedded_data, true_clusters=adata.obs[cell_type_key],
                                                 percent_samples=percent_samples, seed=int(seed + j),
                                                 method=clustering_method, *args, **kwargs)

        # Compute KMeans clustering for batches considering only shared cell types
        results_shared_ct, samples_id_shared_ct = compute_clustering(
            data=embedded_data[np.isin(adata.obs[cell_type_key], shared_cell_types)],
            true_clusters=adata.obs[batch_key][np.isin(adata.obs[cell_type_key], shared_cell_types)],
            percent_samples=percent_samples, seed=int(seed + j), method=clustering_method,
            *args, **kwargs)

        # Compute each metric on the cell types and the batches
        for metric in metrics_results.keys():

            # Cell type metric
            if '_CT' in metric:
                metric_name = metric.split('-')[-1].split('_')[0]
                opposite = (len(metric.split('-')) > 1)
                if '_pred' in metric:
                    metrics_results[metric][j] = compute_metric(metric_name=metric_name, true_clusters=results[:, -2],
                                                                clusters=results[:, -2], data=embedded_data[samples_id],
                                                                perplexity=perplexity)
                else:
                    if opposite:
                        metrics_results[metric][j] = 1 - compute_metric(metric_name=metric_name,
                                                                        clusters=results[:, -2],
                                                                        true_clusters=results[:, -1],
                                                                        data=embedded_data[samples_id],
                                                                        perplexity=perplexity)
                    else:
                        metrics_results[metric][j] = compute_metric(metric_name=metric_name, clusters=results[:, -2],
                                                                    true_clusters=results[:, -1],
                                                                    data=embedded_data[samples_id],
                                                                    perplexity=perplexity)

            # Batch metric
            elif '_B' in metric:
                metric_name = metric.split('-')[-1].split('_')[0]
                opposite = (len(metric.split('-')) > 1)
                if shared_ct[metric_name]:
                    batch_clusters = adata.obs[batch_key][np.isin(adata.obs[cell_type_key],
                                                                  shared_cell_types)][samples_id_shared_ct]
                    clusters = results_shared_ct[:, -2]
                    data = embedded_data[samples_id_shared_ct]
                else:
                    batch_clusters = adata.obs[batch_key][samples_id]
                    clusters = results[:, -2]
                    data = embedded_data[samples_id]
                if opposite:
                    metrics_results[metric][j] = 1 - compute_metric(metric_name=metric_name, clusters=clusters,
                                                                    true_clusters=batch_clusters, data=data,
                                                                    perplexity=perplexity)
                else:
                    metrics_results[metric][j] = compute_metric(metric_name=metric_name, clusters=clusters,
                                                                true_clusters=batch_clusters, data=data,
                                                                perplexity=perplexity)

            # F1 Score
            elif 'F1' in metric:
                metric_name = metric.split('_')[1]
                if metric_name in ['ASW', 'ARI']:
                    if '_pred' not in metric:
                        metrics_results[metric][j] = compute_f1_score(
                            metric_batch=metrics_results[f'1-{metric_name}_B'][j],
                            metric_ct=metrics_results[f'{metric_name}_CT'][j],
                            norm=norm, range_batch=range_batch[metric_name], range_ct=range_ct[metric_name])
                    else:
                        metrics_results[metric][j] = compute_f1_score(
                            metric_batch=metrics_results[f'1-{metric_name}_B'][j],
                            metric_ct=metrics_results[f'{metric_name}_CT_pred'][j],
                            norm=norm, range_batch=range_batch[metric_name], range_ct=range_ct[metric_name])
                elif metric_name.casefold() == 'LISI'.casefold():
                    metrics_results[metric][j] = compute_f1_score(metric_batch=metrics_results[f'{metric_name}_B'][j],
                                                                  metric_ct=metrics_results[f'1-{metric_name}_CT'][j],
                                                                  norm=norm, range_batch=range_batch[metric_name],
                                                                  range_ct=range_ct[metric_name])
                else:
                    metrics_results[metric][j] = compute_f1_score(metric_batch=metrics_results[f'{metric_name}_B'][j],
                                                                  metric_ct=metrics_results[f'1-{metric_name}_CT'][j],
                                                                  norm=norm, range_batch=range_batch[metric_name],
                                                                  range_ct=range_ct[metric_name])

            # Comparing to previous metric to save best results
            if best_metric < metrics_results[metric_best][j]:
                best_metric = metrics_results[metric_best][j]
                best_results = results
                best_samples_id = samples_id

    # Extracting median and max values from the results
    results_df = pd.DataFrame(metrics_results, columns=metrics_results.keys())
    median_df = results_df.median(axis=0)
    max_df = results_df.max(axis=0)
    max_df.index = [f'max_{index}' for index in max_df.index]

    # Returning all metrics statistics (median and maximum values)
    if not return_best:
        return pd.concat([median_df, max_df], axis=0)
    else:
        return pd.concat([median_df, max_df], axis=0), best_results, best_samples_id


# Function to plot clustering results
def plot_clustering_results(results, batch_vector, title,
                            colors_batch=None, colors_cell_types=None, colors_clusters=None,
                            batch_key='batch', cell_type_key='cell_type', label='C', remove_outliers=True,
                            save_plot=True, saving_path='./', additional_info=None,
                            clustering_method='kmeans', show_plot=True):
    """
    Function to plot the KMeans clusters.
    Args:
        results:            array of size (N_samples,2), array containing the true clusters and the predicted clusters.
        batch_vector:       array of size (N_samples), array containing the true batch labels.
        title:              str, title for the plot.
        colors_batch:       dict, colors for each batch, default=None.
        colors_cell_types:  dict, colors for each cell type, default=None.
        colors_clusters:    dict, colors for each cluster, default=None.
        batch_key:          str, key for batch label, default='batch'.
        cell_type_key:      str, key for cell type, default='cell_type'.
        label:              str, axis labels, default='C'.
        remove_outliers:    bool, whether to remove outliers from the plot, default=True.
        save_plot:          bool, whether to save the plot, default=True.
        saving_path:        str, path indicating where to save the plot, default='./'.
        additional_info:    str, info to add in the title, default=None.
        clustering_method:  str, clustering method used, default=kmeans.
        show_plot:          bool, whether to show the plot, default=True.
        """
    # Retrieving cell types, batches and clusters labels
    cell_types = np.unique(results[:, -1])
    batches = np.unique(batch_vector)
    clusters = np.unique(results[:, -2])

    # Parsing marker size
    if len(results) > 1000:
        marker_size = 5
        marker_scale = 2
    else:
        marker_size = None
        marker_scale = 1

    # Parsing legend specifications
    if len(cell_types) > 8:
        legend_out_plot = True
    else:
        legend_out_plot = False

    # Parsing colors
    if colors_batch is None:
        colors_batch_copy = dict(zip(batches, [None] * len(batches)))
    else:
        colors_batch_copy = colors_batch.copy()
    if colors_cell_types is None:
        colors_cell_types_copy = dict(zip(cell_types, [None] * len(cell_types)))
    else:
        colors_cell_types_copy = colors_cell_types.copy()
    if colors_clusters is None:
        colors_clusters_copy = dict(zip(clusters, [None] * len(clusters)))
    elif len(colors_clusters) < len(clusters):
        if len(clusters) >= 5:
            cmap = plt.cm.get_cmap('Spectral')
        else:
            cmap = plt.cm.get_cmap('viridis')
        colors_clusters_copy = dict(zip(clusters,
                                        [cmap(i / len(clusters)) for i in clusters]))
    elif len(colors_clusters) > len(clusters):
        i_selected = [i for i in range(len(colors_clusters))][::round(len(colors_clusters) / len(clusters))]
        if len(i_selected) < len(clusters):
            i_selected += list(np.random.choice(list(set(colors_clusters.keys()) - set(i_selected)),
                                                int(len(clusters) - len(i_selected)), replace=False))
        colors_clusters_copy = dict(zip(clusters,
                                        list(zip(*np.array(list(colors_clusters.values())).T[:, i_selected]))))
    else:
        colors_clusters_copy = colors_clusters.copy()

    # Preparing a dataframe
    df = pd.DataFrame(results[:, :-2])
    df[batch_key] = np.array(batch_vector)
    df[cell_type_key] = results[:, -1]
    df[f'{cell_type_key}_{clustering_method}'] = results[:, -2]

    # Preparing figure
    if legend_out_plot:
        n_cols = 5
        gridspec_kw = {'width_ratios': [7, 7, 2, 7, 1]}
    else:
        n_cols = 3
        gridspec_kw = None
    fig, ax = plt.subplots(1, n_cols, figsize=(5 * n_cols, 6),
                           sharey=True, sharex=True, gridspec_kw=gridspec_kw)
    fig.suptitle(title, x=0.55, y=0.97)

    # Batch mixing
    for i in batches:
        ax[0].scatter(df.loc[df[batch_key] == i, 0],
                      df.loc[df[batch_key] == i, 1],
                      color=colors_batch_copy[i],
                      label=i, s=marker_size)
    ax[0].set_title('Batch mixing')
    ax[0].legend(markerscale=marker_scale)
    ax[0].set_xlabel(f'{label}1')
    ax[0].set_ylabel(f'{label}2')

    # Real cell types
    for i in cell_types:
        ax[1].scatter(df.loc[df[cell_type_key] == i, 0],
                      df.loc[df[cell_type_key] == i, 1],
                      color=colors_cell_types_copy[i],
                      label=i, s=marker_size)
    ax[1].set_title('Cell Type')
    if legend_out_plot:
        handles, labels = ax[1].get_legend_handles_labels()
        ax[2].legend(handles, labels, markerscale=marker_scale)
        ax[2].axis('off')
        i_next = 3
    else:
        ax[1].legend(markerscale=marker_scale)
        i_next = 2
    ax[1].set_xlabel(f'{label}1')
    ax[1].set_ylabel(f'{label}2')

    # KMeans clustering
    for i in clusters:
        ax[i_next].scatter(df.loc[df[f'{cell_type_key}_{clustering_method}'] == i, 0],
                           df.loc[df[f'{cell_type_key}_{clustering_method}'] == i, 1],
                           color=colors_clusters_copy[i],
                           label=i, s=marker_size)
    if legend_out_plot:
        handles, labels = ax[i_next].get_legend_handles_labels()
        ax[i_next + 1].legend(handles, labels, markerscale=marker_scale)
        ax[i_next + 1].axis('off')
    else:
        ax[i_next].legend(markerscale=marker_scale)
    ax[i_next].set_title(f'{clustering_method.replace("_", " ").replace("clustering", "")} clustering')
    ax[i_next].set_xlabel(f'{label}1')
    ax[i_next].set_ylabel(f'{label}2')

    # Setting figure's parameters
    if remove_outliers:
        ax[i_next].set_xlim(-3 * df.iloc[:, 0].std(), 3 * df.iloc[:, 0].std())
        ax[i_next].set_ylim(-3 * df.iloc[:, 1].std(), 3 * df.iloc[:, 1].std())
    ax[i_next].set_xticks([])
    ax[i_next].set_yticks([])

    # Adjusting top of plot for title
    plt.subplots_adjust(top=0.8)

    # Saving the plot
    if save_plot:
        if additional_info is None:
            fig.savefig(f'{saving_path}/clustering_{clustering_method}.png')
        else:
            fig.savefig(f'{saving_path}/clustering_{clustering_method}_{additional_info}.png')

    # Displaying the plot
    if show_plot:
        plt.show()

    # Closing the plot
    plt.close(fig)


# Function to compute all metrics and plot the best KMeans clustering
def compute_and_plot_best_clustering(corrected_data, adata, metric_names=None, shared_ct=None, data_embedding='pca',
                                     clustering_method='kmeans', prior_pca=False, n_components=20, n_repetitions=20,
                                     percent_samples=0.8, seed=42, cell_type_key='cell_type', batch_key='batch',
                                     add_pred=False, metric_best=None, norm=False,
                                     range_batch=None, range_ct=None, perplexity=30, colors_batch=None,
                                     colors_cell_types=None, colors_clusters=None, remove_outliers=True, title_info='',
                                     save_plot=True, saving_path='./', additional_info=None,
                                     show_plot=True, *args, **kwargs):
    """
    Function to compute and plot the best clustering, as well as compute the clustering metrics.
    Args:
        corrected_data:     array of size (N_samples, N_features), corrected data.
        adata:              AnnData object, original data (gene expression and observations).
        metric_names:       list of str, names of the metrics to compute, default=None.
        shared_ct:          dict of bools, whether to use only shared cell types for each metric.
        data_embedding:     str, embedding method to use ('pca', 'tsne', 'umap'), default='pca'.
        clustering_method:  str, clustering method to use ('kmeans', 'louvain'), default='louvain'.
        prior_pca:          bool, whether to compute PCA prior to the embedding algorithm, default=False.
        n_components:       int, number of components to use in the PCA, default=20.
        n_repetitions:      int, number of repetitions for KMeans, default=20.
        percent_samples:    float, percentage of the data to use for each clustering repetition, default=0.8.
        seed:               int, seed used to set the randomness, default=42.
        cell_type_key:      str, key for cell type label in original data, default='cell_type'.
        batch_key:          str, key for batch label in original data, default='batch'.
        add_pred:           bool, whether to add the metrics computed based on the KMeans predictions, default=False.
        metric_best:        str, metric to use to determine the best KMeans clusters, default=None.
        norm:               bool, whether to normalize the metrics before computing the F1 score, default=False.
        range_batch:        dict, batch metrics ranges to use to normalize the metrics, default=None.
        range_ct:           dict, cell type metrics ranges to use to normalize the metrics, default=None.
        perplexity:         int, perplexity to determine the neighborhood for LISI, default=30.
        colors_batch:       dict, colors for the batches, default=None.
        colors_cell_types:  dict, colors for the cell types, default=None.
        colors_clusters:    dict, colors for the clusters, default=None.
        remove_outliers:    bool, whether to remove the outliers in the plot, default=True.
        title_info:         str, title information for the plot, default=''.
        save_plot:          bool, whether to save the plot or not, default=True.
        saving_path:        str, path where to save the plot, default='./'.
        additional_info:    str, info to add when saving files, default=None.
        show_plot:          bool, whether to show the plot, default=True.
        *args:              list of parameters for clustering method.
        **kwargs:           list of named parameters for clustering method.
    Returns:    pd.Series, array containing the metrics median and maximum values.
    """

    # Labels for axes plot
    if data_embedding.casefold() == 'pca'.casefold():
        label = 'PC'
    else:
        label = 'C'

    # Computing metrics and best clustering
    metrics, results, samples_id = compute_metrics(corrected_data=corrected_data, adata=adata,
                                                   n_components=n_components, n_repetitions=n_repetitions,
                                                   percent_samples=percent_samples, seed=seed,
                                                   cell_type_key=cell_type_key, batch_key=batch_key,
                                                   metric_names=metric_names, shared_ct=shared_ct,
                                                   data_embedding=data_embedding, prior_pca=prior_pca,
                                                   clustering_method=clustering_method,
                                                   add_pred=add_pred, return_best=True,
                                                   metric_best=metric_best, norm=norm, range_batch=range_batch,
                                                   range_ct=range_ct, perplexity=perplexity, *args, **kwargs)

    # Plotting best results
    plot_clustering_results(results=results,
                            batch_vector=adata[samples_id].obs[batch_key],
                            title=f'Clustering on corrected {data_embedding}\n' + title_info,
                            colors_batch=colors_batch, colors_cell_types=colors_cell_types,
                            colors_clusters=colors_clusters, batch_key=batch_key, cell_type_key=cell_type_key,
                            label=label, remove_outliers=remove_outliers, save_plot=save_plot,
                            saving_path=saving_path, additional_info=additional_info,
                            clustering_method=clustering_method, show_plot=show_plot)

    # Returning the metrics
    return metrics
