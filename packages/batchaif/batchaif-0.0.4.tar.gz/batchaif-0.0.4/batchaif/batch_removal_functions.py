# Import torch useful libraries
import anndata
import numpy as np
import torch


# Function to remove batch effect
def batch_removal(adata, cvae, cell_label_key='cell_type', batch_key='batch',
                  device='cpu'):
    """
    Function to remove batch effect based on latent space arithmetic: normalization of the latent space distribution by
    cell type x batch.
    Args:
        adata:          AnnData object containing the data (gene expression and observations).
        cvae:           trained CVAE model.
        cell_label_key: str, key for cell type information in adata, default='cell_type'.
        batch_key:      str, key for batch information in adata, default='batch'.
        device:         str, device to use ('cuda' or 'cpu'), default='cpu'.

    Returns: Corrected data in AnnData object using the batch x cell type normalization in the latent space.
    """

    # Specifying eval mode
    cvae.eval()

    # Specifying no gradient required
    with torch.no_grad():

        # Retrieving latent representation of data and associated Y
        out_rec, out_mu, out_log_var, pred_y = cvae(torch.tensor(adata.X).to(device))
        z = cvae.re_param(out_mu, out_log_var)

    # Creating AnnData object for latent representation
    adata_latent = anndata.AnnData(z.detach().cpu().numpy())
    adata_latent.obs = adata.obs

    # Computing shared cell types and normalizing by cell type x batch
    unique_cell_types = np.unique(adata_latent.obs[cell_label_key])
    shared_ct = []
    not_shared_ct = []
    for cell_type in unique_cell_types:
        temp_cell = adata_latent[adata_latent.obs[cell_label_key] == cell_type]
        if len(np.unique(temp_cell.obs[batch_key])) < 2:
            cell_type_ann = adata_latent[adata_latent.obs[cell_label_key] == cell_type]
            not_shared_ct.append(cell_type_ann)
            continue
        temp_cell = adata_latent[adata_latent.obs[cell_label_key] == cell_type]
        batch_list = {}
        batch_ind = {}
        max_batch = 0
        max_batch_ind = ""
        batches = np.unique(temp_cell.obs[batch_key])
        for i in batches:
            temp = temp_cell[temp_cell.obs[batch_key] == i]
            temp_ind = temp_cell.obs[batch_key] == i
            if max_batch < len(temp):
                max_batch = len(temp)
                max_batch_ind = i
            batch_list[i] = temp
            batch_ind[i] = temp_ind
        max_batch_ann = batch_list[max_batch_ind]
        for study in batch_list:
            delta = np.average(max_batch_ann.X, axis=0) - np.average(batch_list[study].X, axis=0)
            batch_list[study].X = delta + batch_list[study].X
            temp_cell[batch_ind[study]].X = batch_list[study].X
        shared_ct.append(temp_cell)
    all_shared_ann = anndata.AnnData.concatenate(*shared_ct, batch_key="concat_batch", index_unique=None)

    # Removing concat_batch column
    if "concat_batch" in all_shared_ann.obs.columns:
        del all_shared_ann.obs["concat_batch"]

    # If all cell types are shared
    if len(not_shared_ct) < 1:
        corrected = anndata.AnnData(cvae.decoder(y=pred_y[all_shared_ann.obs.index.astype(int)].to(device),
                                                 z=torch.tensor(all_shared_ann.X).to(device)).detach().cpu().numpy(),
                                    obs=all_shared_ann.obs)
        corrected.var_names = adata.var_names.tolist()
        corrected = corrected[adata.obs_names]

        if adata.raw is not None:
            adata_raw = anndata.AnnData(X=adata.raw.X, var=adata.raw.var)
            adata_raw.obs_names = adata.obs_names
            corrected.raw = adata_raw
        corrected.obsm["latent"] = all_shared_ann.X
        return corrected

    # If some cell types are not shared
    else:
        all_not_shared_ann = anndata.AnnData.concatenate(*not_shared_ct, batch_key="concat_batch", index_unique=None)
        all_corrected_data = anndata.AnnData.concatenate(all_shared_ann, all_not_shared_ann, batch_key="concat_batch",
                                                         index_unique=None)
        if "concat_batch" in all_shared_ann.obs.columns:
            del all_corrected_data.obs["concat_batch"]
        corrected = anndata.AnnData(
            cvae.decoder(y=pred_y[all_corrected_data.obs.index.astype(int)].to(device),
                         z=torch.tensor(all_corrected_data.X).to(device)).detach().cpu().numpy(),
            obs=all_corrected_data.obs)
        corrected.var_names = adata.var_names.tolist()
        corrected = corrected[adata.obs_names]
        if adata.raw is not None:
            adata_raw = anndata.AnnData(X=adata.raw.X, var=adata.raw.var)
            adata_raw.obs_names = adata.obs_names
            corrected.raw = adata_raw
        corrected.obsm["latent"] = all_corrected_data.X
        return corrected


# Function to remove batch effect using conditional sampling
def batch_removal_conditional(adata, cvae, label_projection=0.5, device='cpu', seed=42, deterministic=False):
    """
    Function to remove batch effect based on projection of the batches' distribution using conditional reconstruction
    of the cVAE.
    Args:
        adata:              AnnData object containing the data (gene expression and observations).
        cvae:               trained CVAE model.
        label_projection:   float, batch label used for projection, default=0.5.
        device:             str, device to use ('cpu' or 'cuda'), default='cpu'.
        seed:               int, seed used to set the randomness, default=42.
        deterministic:      bool, whether to use a deterministic approach or not, default=False.

    Returns: Corrected data in AnnData object using conditional reconstruction to project the batches' distribution.
    """

    # Setting randomness
    torch.manual_seed(seed)

    # Retrieving index and labels of projection
    i_proj = label_projection // 1  # Classes between which to project (integer part)
    l_proj = label_projection % 1   # Label of projection (decimal part)

    # Specifying eval mode
    cvae.eval()

    # Specifying no gradient required
    with torch.no_grad():

        # Retrieving latent representation of data and associated Y
        out_rec, out_mu, out_log_var, pred_y = cvae(torch.Tensor(adata.X).to(device))
        if deterministic:
            z = out_mu
        else:
            z = cvae.re_param(out_mu, out_log_var)

        # Creating projection labels array
        y_proj = np.zeros((adata.X.shape[0], cvae.n_labels))
        try:
            if i_proj < cvae.n_labels - 1:
                y_proj[:, [int(i_proj), int(i_proj + 1)]] = np.ones((adata.X.shape[0], 2)) * np.array(
                    [1 - l_proj, l_proj])
            else:
                y_proj[:, int(i_proj)] = np.ones(adata.X.shape[0]) * (1 - l_proj)
        except IndexError:
            print('Please provide a valid label of projection: any float from 0 to the number of batches.')

        # Decoding latent representation conditionally to only one batch and storing in a AnnData object
        corrected_adata = anndata.AnnData(cvae.decoder(y=torch.Tensor(y_proj).to(device),
                                                       z=z.detach().to(device)).detach().cpu().numpy())

    # Adding original observations
    corrected_adata.obs = adata.obs.astype('category')
    corrected_adata.uns = adata.uns

    # Return corrected AnnData
    return corrected_adata


# Function to remove batch effect using conditional sampling
def batch_removal_conditional_robust(adata, cvae, label_projection=0.5, device='cpu', seed=42, n_samplings=20,
                                     percent_load=1.0):
    """
    Function to remove the batch effect based on projection of the batches' distribution using a robust conditional
    reconstruction of the cVAE.
    Args:
        adata:              AnnData object containing the data (gene expression and observations).
        cvae:               trained CVAE model.
        label_projection:   float, batch label used for projection, default=0.5.
        device:             str, device to use ('cpu' or 'cuda'), default='cpu'.
        seed:               int, seed used to set the randomness, default=42.
        n_samplings:        int, number of samples to draw from latent distribution.
        percent_load:       float, percent of data to load simultaneously, default=1.0.
    Returns: Corrected data in AnnData object using robust conditional reconstruction to project the batches'
    distribution.
    """

    # Retrieving the stopping index
    n_per_load = int(len(adata) * percent_load)
    stop_index_list = [k for k in range(len(adata))][::n_per_load]
    if max(stop_index_list) < len(adata):
        stop_index_list += [len(adata)]

    # Correcting batch effect for each load of data
    for k in range(len(stop_index_list) - 1):

        # Initialization of a list to store each repetition
        corrected_data = []

        # Retrieving start and stop indices
        i_start = stop_index_list[k]
        i_stop = stop_index_list[k + 1]
        index = [l for l in range(i_start, i_stop)]

        # For each repetition, correct batch effect
        for i in range(n_samplings):
            corrected_data.append(
                batch_removal_conditional(adata=adata[index], cvae=cvae, label_projection=label_projection,
                                          device=device, seed=seed + i, deterministic=False).X)

        # Averaging corrected data and adding to overall corrected data
        if k == 0:
            all_corrected_data = np.array(corrected_data).mean(axis=0)
        else:
            all_corrected_data = np.concatenate([all_corrected_data,
                                                 np.array(corrected_data).mean(axis=0)], axis=0)

    # Creating anndata object and adding original observations
    corrected_adata = anndata.AnnData(all_corrected_data)
    corrected_adata.obs = adata.obs.astype('category')
    corrected_adata.uns = adata.uns

    # Return corrected AnnData
    return corrected_adata
