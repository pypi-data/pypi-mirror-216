# Importing useful libraries
import pandas as pd
import torch
import torch.nn.functional as F
import numpy as np


# Function to compute relative normalization weighting strategy
def compute_relative_weights(losses_history, losses_included, dynamic_ratio=1.0, *args, **kwargs):
    # Parsing losses history to a dataframe
    if isinstance(losses_history, dict):
        losses_df = pd.DataFrame.from_dict(losses_history).loc[:, losses_included]
    elif isinstance(losses_history, pd.DataFrame):
        losses_df = losses_history.loc[:, losses_included]

    # Computing starting index
    start_index = 0
    if 0 < dynamic_ratio < 1:
        start_index = - min(len(losses_df), int(dynamic_ratio * len(losses_df)))

    # Computing relative normalization weights
    losses_weights = (losses_df.loc[start_index:, 'mse'].median(axis=0) /
                      losses_df.loc[start_index:, :].median(axis=0).replace(0, 1))

    # Returning losses weights dictionary
    return losses_weights.to_dict()


# Function to compute Dynamic Average Weighting strategy
def compute_dwa_weights(losses_history, losses_included, dynamic_ratio=0, T=1, weights_sum=1, *args, **kwargs):
    # Parsing losses history to a dataframe
    if isinstance(losses_history, dict):
        losses_df = pd.DataFrame.from_dict(losses_history).loc[:, losses_included]
    elif isinstance(losses_history, pd.DataFrame):
        losses_df = losses_history.loc[:, losses_included]

    # Computing starting index
    start_index = - 2
    if 0 < dynamic_ratio < 1:
        start_index = - min(len(losses_df), int(dynamic_ratio * len(losses_df)))

    # Computing descending rates for each loss
    desc_rates = losses_df.iloc[-1, :] / losses_df.iloc[start_index:-1, :].median().replace(0, 1)

    # Computing DWA weights using softmax
    losses_weights = dict(zip(desc_rates.index,
                              (weights_sum * F.softmax(torch.Tensor(desc_rates.to_numpy() / T),
                                                       dim=0).detach().numpy())))

    # Returning losses weights dictionary
    return losses_weights


# Function to compute relative DWA weights
def compute_relative_dwa_weights(losses_history, losses_included, rel_dynamic_ratio=1.0,
                                 dwa_dynamic_ratio=0, T=1, weights_sum=1, *args, **kwargs):
    # Parsing losses history to a dataframe
    losses_df = pd.DataFrame.from_dict(losses_history).loc[:, losses_included]

    # Computing relative normalization weights
    rel_weights = compute_relative_weights(losses_history=losses_df, losses_included=losses_included,
                                           dynamic_ratio=rel_dynamic_ratio)

    # Computing DWA weights
    dwa_weights = compute_dwa_weights(losses_history=losses_df, losses_included=losses_included,
                                      dynamic_ratio=dwa_dynamic_ratio,
                                      T=T, weights_sum=weights_sum)

    # Combining both weights
    losses_weights = (pd.Series(rel_weights) * pd.Series(dwa_weights))

    # Returning losses weights dict
    return losses_weights.to_dict()


# Function to compute user defined normalization weights
def compute_normalized_weights(losses_history, losses_included, losses_norm, dynamic_ratio=1.0, *args, **kwargs):
    # Parsing losses history to a dataframe
    if isinstance(losses_history, dict):
        losses_df = pd.DataFrame.from_dict(losses_history).loc[:, losses_included]
    elif isinstance(losses_history, pd.DataFrame):
        losses_df = losses_history.loc[:, losses_included]

    # Computing starting index
    start_index = 0
    if 0 < dynamic_ratio < 1:
        start_index = - min(len(losses_df), int(dynamic_ratio * len(losses_df)))

    # Computing normalization weights
    losses_weights = losses_norm.copy()
    for key in losses_norm.keys():
        if isinstance(losses_norm[key], str) and hasattr(np, losses_norm[key]):
            losses_weights[key] = 1 / getattr(np, losses_norm[key])(losses_df[key][start_index:]).replace(0, 1)

    # Returning losses weights dictionary
    return losses_weights


# Function to update losses weights
def update_losses_weights(losses_history, weighting_strategy, losses_included, *args, **kwargs):
    # Relative normalization weighting strategy
    if weighting_strategy == 'rel':
        losses_weights = compute_relative_weights(losses_history=losses_history,
                                                  losses_included=losses_included, *args, **kwargs)

    # Dynamic Weighting Average (DWA) strategy
    elif weighting_strategy == 'dwa':
        losses_weights = compute_dwa_weights(losses_history=losses_history,
                                             losses_included=losses_included, *args, **kwargs)

    # Dynamic Weighting Average (DWA) and relative normalization strategy
    elif weighting_strategy == 'rel_dwa':
        losses_weights = compute_relative_dwa_weights(losses_history=losses_history,
                                                      losses_included=losses_included, *args, **kwargs)

    # User defined normalization
    elif weighting_strategy == 'norm':
        losses_weights = compute_normalized_weights(losses_history=losses_history,
                                                    losses_included=losses_included, *args, **kwargs)

    # Otherwise None
    else:
        losses_weights = None

    # Returning updated losses weights
    return losses_weights
