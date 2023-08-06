from os.path import join
import numpy as np
import math
import torch
from torch.autograd import Variable
from matplotlib import pyplot as plt


# Function to plot the losses evolution
def plot_losses(losses, ex_dir, title='Losses evolution throughout training', colors=None):
    """
    Function to plot the losses' evolution.
    Args:
        losses:     dict, dictionary containing all the losses' evolution stored in a list.
        ex_dir:     str, path to the directory where to save the plots.
        title:      str, title in the plot, default='Losses evolution throughout training'.
        colors:     dict, colors for the losses, default=None.
    """

    # Retrieving losses names
    loss_names = [loss_name for loss_name in losses.keys() if 'norm' not in loss_name]
    loss_norm_names = [loss_name for loss_name in losses.keys() if 'norm' in loss_name]

    # Retrieving the number of epochs
    epochs = len(list(losses.values())[0])

    # Verifying that the training has started
    assert epochs > 0

    # Setting default 
    if (len(loss_names) > 0) & (len(loss_norm_names) > 0):
        n_cols = 2
        width_ratios = n_cols * [5, 1]
    else:
        n_cols = 1
        width_ratios = n_cols * [5, 1]
    if colors is None:
        cmap = plt.get_cmap('tab20')
        colors = dict(zip(loss_names, [cmap(i) for i in range(0, 20, 2)] + [cmap(i) for i in range(1, 20, 2)]))

    # Creating the figure
    fig1, ax = plt.subplots(ncols=2 * n_cols, figsize=(7 * n_cols, 5),
                            gridspec_kw={'width_ratios': width_ratios})

    # Plotting the losses evolution
    for key in losses.keys():
        if 'norm' not in key:
            i_ax = 0
        else:
            i_ax = 2
        nb_points = len(losses[key])
        factor = float(nb_points) / epochs
        ax[i_ax].plot(np.arange(len(losses[key])) / factor, losses[key], label=key, c=colors[key.split('_')[0]])

    # Adding axis legend and titles
    for i in range(n_cols):
        ax[2 * i].set_xlabel('Epochs')
        ax[2 * i].set_ylabel('Loss')
        h, labels = ax[2 * i].get_legend_handles_labels()
        ax[2 * i + 1].legend(h, labels, borderaxespad=0, handlelength=1)
        ax[2 * i + 1].axis('off')

    # Adding figure's title and specifications
    fig1.suptitle(title, x=0.5, y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], w_pad=1)

    # Saving the figure
    fig1.savefig(join(ex_dir, 'loss_plt.png'))
    plt.close(fig1)


# Function to plot the normalized losses
def plot_norm_losses(losses, ex_dir, title='Normalized losses evolution throughout training', colors=None):
    """
    Function to plot the normalized losses' evolution.
    Args:
        losses:     dict, dictionary containing all the losses' evolution stored in a list.
        ex_dir:     str, path to the directory where to save the plots.
        title:      str, title in the plot, default='Normalized losses evolution throughout training'.
        colors:     dict, colors for the losses, default=None.
    """

    # Retrieving losses names
    loss_names = [loss_name for loss_name in losses.keys() if 'norm' not in loss_name]

    # Retrieving the number of epochs
    epochs = len(list(losses.values())[0])

    # Verifying that the training has started
    assert epochs > 0

    # Setting the defaults
    if colors is None:
        cmap = plt.get_cmap('tab20')
        colors = dict(zip(loss_names, [cmap(i) for i in range(0, 20, 2)] + [cmap(i) for i in range(1, 20, 2)]))

    # Creating the figure
    fig1, ax = plt.subplots(ncols=2, figsize=(10, 5),
                            gridspec_kw={'width_ratios': [5, 1]})

    # Plotting the losses evolution
    for key in losses.keys():
        nb_points = len(losses[key])
        factor = float(nb_points) / epochs
        ax[0].plot(np.arange(len(losses[key])) / factor, losses[key], label=key, c=colors[key.split('_')[0]])

    # Adding axis legend and titles
    ax[0].set_xlabel('Epochs')
    ax[0].set_ylabel('Loss')
    h, labels = ax[0].get_legend_handles_labels()
    ax[1].legend(h, labels, borderaxespad=0, handlelength=1)
    ax[1].axis('off')

    # Adding figure's title and specifications
    fig1.suptitle(title, x=0.5, y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95], w_pad=1)

    # Saving the figure
    fig1.savefig(join(ex_dir, 'norm_loss_plt.png'))
    plt.close(fig1)


# Function to plot the losses' evolution in a panel
def plot_losses_panel(losses, n_cols=4, color=None, remove_outliers_losses=None, losses_names=None,
                      q=0.999, start_index=0, title_info='', save_fig=True, ex_dir='./'):
    """
    Function to plot the losses' evolution in a panel: each loss in a different subplot.
    Args:
        losses:                     dict of lists, losses' evolution.
        n_cols:                     int, number of columns in the plot, default=4.
        color:                      str, color to use, default=None.
        remove_outliers_losses:     dict of bool, whether to remove the outliers for each loss, default=None.
        losses_names:                list, losses' names to plot, default=None.
        q:                          float, quantile to use for determining the outliers, default=0.999.
        start_index:                int, starting index for determining the outliers, default=0.
        title_info:                 str, additional info for title, default=''.
        save_fig:                   bool, whether to save the figure in a png file, default=True.
        ex_dir:                     str, path where to save the plot, default='./'.
    """

    # Retrieving the losses names
    if losses_names is None:
        losses_names = list(losses.keys())

    # Parsing default arguments
    if remove_outliers_losses is None:
        remove_outliers = dict(zip(losses_names, [False for _ in range((len(losses_names)))]))
    else:
        remove_outliers = dict(zip(remove_outliers_losses + [loss_name for loss_name in losses_names if
                                                             loss_name not in remove_outliers_losses],
                                   [True for _ in range(len(remove_outliers_losses))] + [False for _ in range(
                                       len(losses_names) - len(remove_outliers_losses))]))

    # Initialization of a dictionary to store the quantiles
    quantiles = dict(zip(losses_names,
                         [{'min': np.inf, 'max': -np.inf} for _ in range(len(losses_names))]))

    # Defining the title
    title = 'Losses evolution during training' + title_info

    # Computing the number of rows
    n_rows = math.ceil(len(losses_names) / n_cols)

    # Initialization of a figure
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols * 7.5, n_rows * 5.5),
                           gridspec_kw={'hspace': 0.25, 'wspace': 0.2})

    # Defining background color of figure
    fig.patch.set_facecolor('white')

    # Adding title to the figure
    fig.suptitle(title, x=0.55, y=0.95,
                 ha='center', va='center', fontsize=25, fontweight='bold')

    # Plot each loss evolution for each combination of hyperparameters
    for i in range(len(losses_names)):

        # Retrieving the index of the figure
        i_row, i_col = i // n_cols, i % n_cols

        # Plotting the loss evolution
        ax[i_row, i_col].plot(losses[losses_names[i]][start_index:], c=color)

        # Computing the quantiles for plot's limits
        if remove_outliers[losses_names[i]]:
            quantiles[losses_names[i]]['max'] = max(quantiles[losses_names[i]]['max'],
                                                    losses[losses_names[i]][start_index:].quantile(q=q))
            quantiles[losses_names[i]]['min'] = min(quantiles[losses_names[i]]['min'],
                                                    losses[losses_names[i]][start_index:].quantile(q=1 - q))

        # Setting the axis labels and figure's title, adding legend
        ax[i_row, i_col].set_title(f'{losses_names[i].replace("_", " ")} loss evolution', fontsize=18,
                                   fontweight='bold')
        ax[i_row, i_col].set_ylabel(f'{losses_names[i].replace("_", " ")} loss', fontsize=15, fontweight='bold')
        ax[i_row, i_col].set_xlabel('Number of epochs', fontsize=15, fontweight='bold')

        # Setting the plot's y-axis limits
        if remove_outliers[losses_names[i]]:
            ax[i_row, i_col].set_ylim(quantiles[losses_names[i]]['min'],
                                      quantiles[losses_names[i]]['max'])

    # Remove unused axis
    for k in range(len(losses_names), n_rows * n_cols):
        # Retrieving the index of the figure
        i_row, i_col = k // n_cols, k % n_cols

        # Removing the axis
        ax[i_row, i_col].axis('off')

    # Saving the figure
    if save_fig:
        fig.savefig(join(ex_dir, 'loss_plt.png'))
        plt.close(fig)

    # Showing the figure
    else:
        plt.show()


# Function to plot the weights' evolution in a panel
def plot_weights_panel(weights, n_cols=4, color=None, title_info='', save_fig=True, ex_dir='./'):
    """
    Function to plot the losses' evolution in a panel: each loss in a different subplot.
    Args:
        weights:                    dict of lists, weights' evolution.
        n_cols:                     int, number of columns in the plot, default=4.
        color:                      str, color to use, default=None.
        title_info:                 str, additional info for title, default=''.
        save_fig:                   bool, whether to save the figure in a png file, default=True.
        ex_dir:                     str, path where to save the plot, default='./'.
    """

    # Retrieving the losses names
    weights_names = list(weights.keys())

    # Defining the title
    title = 'Weights evolution during training' + title_info

    # Computing the number of rows
    n_rows = math.ceil(len(weights_names) / n_cols)

    # Initialization of a figure
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols * 7.5, n_rows * 5.5),
                           gridspec_kw={'hspace': 0.25, 'wspace': 0.2})

    # Defining background color of figure
    fig.patch.set_facecolor('white')

    # Adding title to the figure
    fig.suptitle(title, x=0.55, y=0.95,
                 ha='center', va='center', fontsize=25, fontweight='bold')

    # Plot each loss evolution for each combination of hyperparameters
    for i in range(len(weights_names)):

        # Retrieving the index of the figure
        if n_rows > 1:
            i_fig = i // n_cols, i % n_cols
        else:
            i_fig = i

        # Plotting the loss evolution
        ax[i_fig].plot(weights[weights_names[i]], c=color)

        # Setting the axis labels and figure's title, adding legend
        ax[i_fig].set_title(f'{weights_names[i].replace("_", " ")} loss evolution', fontsize=18,
                            fontweight='bold')
        ax[i_fig].set_ylabel(f'{weights_names[i].replace("_", " ")} loss', fontsize=15, fontweight='bold')
        ax[i_fig].set_xlabel('Number of epochs', fontsize=15, fontweight='bold')

    # Remove unused axis
    for k in range(len(weights_names), n_rows * n_cols):

        # Retrieving the index of the figure
        if n_rows > 1:
            i_fig = k // n_cols, k % n_cols
        else:
            i_fig = k

        # Removing the axis
        ax[i_fig].axis('off')

    # Saving the figure
    if save_fig:
        fig.savefig(join(ex_dir, 'weights_plt.png'))
        plt.close(fig)

    # Showing the figure
    else:
        plt.show()


# Sampling z function
def sample_z(batch_size, nz, device):
    """
    Function to sample z from an N(0,I) distribution.
    Args:
        batch_size:     int, batch size.
        nz:             int, dimension of the latent space.
        device:         str, device used ('cpu' or 'cuda').
    Returns:    tensor of size (batch_size, nz), the samples drawn from the N(0,I) distribution.
    """
    return Variable(torch.randn(batch_size, nz).to(device))
