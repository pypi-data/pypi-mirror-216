# Importing useful data libraries
import math

# Importing system management libraries
import os as os

# Importing plotting libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Defining a function to parse useful information (weights and hyperparameters) in the title
def parse_title(model_name, title_hyp_dict, title_hyp_names, label_hyp_index, label_hyp_names,
                additional_info="'s robustness evaluated on the training losses"):
    """
    Function to parse useful information (weights and hyperparameters) in the figure's title.
    Args:
        model_name:         str, model name.
        title_hyp_dict:     dict, hyperparameters name and value to add in the title.
        title_hyp_names:    dict, hyperparameters name to display (e.g. math formula) in the title.
        label_hyp_index:    pd.Index, hyperparameters combinations values to add in the axis labels.
        label_hyp_names:    dict, hyperparameters name to display (e.g. math formula) in the axis labels.
        additional_info:    str, info to add in the title, default=''s robustness evaluated on the training losses'.
    Returns:    str, parsed title and hyperparameters dropped in the axis labels (unique value) and added in
    the title info.
    """

    # Creating the title
    title = f"{model_name}" + additional_info + "\n"

    # Adding hyperparameters information in title
    count = 0
    for key in title_hyp_dict.keys():
        title += title_hyp_names[key] + f'={title_hyp_dict[key]}'
        if count < len(title_hyp_dict.keys()) - 1:
            title += ', '
        count += 1

    # Creating dictionary to store index names and levels
    index_dict = dict(zip(label_hyp_index.names, label_hyp_index.levels))

    # Adding fixed label hyperparameters information to title
    hyp_dropped = []
    count = 0
    count_added = 0
    for index_name in label_hyp_names:
        if label_hyp_index.levshape[count] == 1:
            if count_added == 0:
                title += ' ('
            else:
                title += ', '
            title += label_hyp_names[index_name] + f'={index_dict[index_name][0]}'
            hyp_dropped += [index_name]
            count_added += 1
        count += 1
    if count_added != 0:
        title += ')'

    # Returning the title and the hyperparameters dropped
    return title, hyp_dropped


# Defining a function to parse hyperparameters information in the labels
def parse_labels(hyp_names, hyp_dropped, hyp_tuple_values, add_break=True):
    """
    Function to parse hyperparameters information in the axis labels.
    Args:
        hyp_names:          dict, hyperparameters name to display (e.g. math formula).
        hyp_dropped:        list, hyperparameters name to drop in the axis labels.
        hyp_tuple_values:   tuple, hyperparameters combinations values.
        add_break:          bool, whether to add a break between hyperparameters values.
    Returns:    list, parsed labels.
    """

    # Retrieving hyperparameters to keep in the label
    i_kept = [k for k in range(len(hyp_names.keys())) if list(hyp_names.keys())[k] not in hyp_dropped]
    hyp_kept = [list(hyp_names.keys())[i] for i in i_kept]

    # Creating a dictionary matching hyperparameters keys and values
    labels_dict = [dict(zip(hyp_kept * len(hyp_tuple_values[k]), [hyp_tuple_values[k][i] for i in i_kept])) for k in
                   range(len(hyp_tuple_values))]

    # Initialization of a list to store the labels
    labels = []

    # Parse each label
    for k in range(len(labels_dict)):

        # Initialization of a string for the label and a count
        label = ''
        count = 0

        # For each hyperparameter, add its name and value to the label
        for key in labels_dict[k].keys():
            label += hyp_names[key] + f'={labels_dict[k][key]}'
            if count < len(labels_dict[k].keys()) - 1:
                if add_break:
                    label += '\n'
                else:
                    label += ', '
            count += 1

        # Add the label to the labels list
        labels += [label]

    # Returning the labels list
    return labels


# Defining a function to plot the best losses or metrics distribution
def plot_best_distribution(best_losses, loss_names, model_name, weights_dict, weights_names, hyp_names,
                           colors=None, n_cols=3, y_label='Loss value',
                           additional_info="'s robustness evaluated on the training losses",
                           remove_outliers=True, additional_data=None):
    """
    Function to plot the best distribution for the losses or the metrics.
    Args:
        best_losses:        pd.DataFrame, array containing all the best losses.
        loss_names:         list, losses names.
        model_name:         str, model name to display.
        weights_dict:       dict, weights name and values tried.
        weights_names:      dict, weights name to display (e.g. math formula).
        hyp_names:          dict, hyperparameters name to display (e.g. math formula).
        colors:             list, colors for each model, default=None.
        n_cols:             int, number of columns in the plot, default=3.
        y_label:             str, label for the y-axis, default='Loss value'.
        additional_info:    str, info to add in the title, default=None.
        remove_outliers:    bool, whether to remove the outliers in the plot, default=True.
        additional_data:    str, additional data (e.g. 'max', 'min' etc.) to add in the plot, default=None.
    """

    # Parsing the title
    title, hyp_dropped = parse_title(model_name=model_name, title_hyp_dict=weights_dict, title_hyp_names=weights_names,
                                     label_hyp_index=best_losses.index, label_hyp_names=hyp_names,
                                     additional_info=additional_info)

    # Creating a figure
    n_rows = len(loss_names) // n_cols + math.ceil(len(loss_names) % n_cols / n_cols)
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(10 * n_cols, 8 * n_rows))
    plt.subplots_adjust(hspace=0.25)

    # Adding title
    fig.suptitle(title, x=0.55, y=0.98, fontsize=24, fontweight='bold')

    for k in range(len(loss_names)):

        # Extracting this loss data and preparing the dataframe for the plot
        loss_df = best_losses[[loss_names[k]]].copy()
        loss_df.loc[:, 'hyperparameter'] = loss_df[[loss_names[k]]].index.droplevel(['experiment']).to_flat_index()
        loss_df = loss_df.reset_index().set_index('experiment')
        loss_df = loss_df[[loss_names[k], 'hyperparameter']]
        loss_df = pd.pivot_table(loss_df, index='experiment',
                                 values=loss_names[k], columns='hyperparameter')

        # Defining the row and column index in the plot
        i_row = k // 3
        i_col = k % 3

        # Parsing labels
        labels = parse_labels(hyp_names=hyp_names, hyp_dropped=hyp_dropped, hyp_tuple_values=loss_df.columns)

        # Plotting boxplot
        bplot = ax[i_row, i_col].boxplot(loss_df, labels=loss_df.columns, notch=True, patch_artist=True,
                                         showfliers=not remove_outliers)

        # Adding maximum value
        if additional_data is not None:
            ax[i_row, i_col].scatter(range(1, len(loss_df.columns) + 1),
                                     getattr(loss_df, additional_data)(),
                                     c=colors, marker='*', s=200, label=additional_data)
            ax[i_row, i_col].legend()

        # Adding colors
        if colors is not None:
            for patch, color in zip(bplot['boxes'], colors):
                patch.set_facecolor(color)

        # Setting axis labels and figure's title
        ax[i_row, i_col].set_title(f'{loss_names[k].replace("_", " ")}', fontsize=22, fontweight='bold')
        ax[i_row, i_col].set_xticklabels(labels, rotation=90)
        if i_row == n_rows - 1:
            ax[i_row, i_col].set_xlabel('Hyperparameters values', fontsize=18, fontweight='bold')
        ax[i_row, i_col].set_ylabel(y_label, fontsize=18, fontweight='bold')

    # Show figure
    plt.show()


# Defining a function to plot the best losses or metrics distribution
def plot_best_distribution_per_hyperparameter(best_losses, loss_names, model_name, hyp_dict, hyp_names, weights_names,
                                              axis_spec=None, colors=None, y_label='Loss value', additional_info='loss',
                                              remove_outliers=True, additional_data=None):
    """
    Function to plot the best distribution per hyperparameter's value for the losses or the metrics.
    Args:
        best_losses:        pd.DataFrame, array containing all the best losses.
        loss_names:         list, losses names.
        model_name:         str, model name to display.
        hyp_dict:           dict, hyperparameters name and values tried.
        hyp_names:          dict, hyperparameters name to display (e.g. math formula).
        weights_names:      dict, weights name to display (e.g. math formula).
        axis_spec:          dict, axis specification for where to display each weight, default=None.
        colors:             list, colors for each model, default=None.
        y_label:             str, label for the y-axis, default='Loss value'.
        additional_info:    str, info to add in the title, default=None.
        remove_outliers:    bool, whether to remove the outliers in the plot, default=True.
        additional_data:    str, additional data (e.g. 'max', 'min' etc.) to add in the plot, default=None.
    """

    # Defining the default axes specifications
    if axis_spec is None:
        axis_spec = dict(zip(['fig_ax_x', 'fig_ax_y'], weights_names.keys()))

    # Retrieving weights values for figure axes
    fig_ax_x_values = best_losses.index.get_level_values(level=axis_spec['fig_ax_x']).unique().sort_values()
    fig_ax_y_values = best_losses.index.get_level_values(level=axis_spec['fig_ax_y']).unique().sort_values()
    n_cols = len(fig_ax_x_values)
    n_rows = len(fig_ax_y_values)

    # For each loss, plot the influence of the losses weights
    for k in range(len(loss_names)):

        # Parsing the title
        title, hyp_dropped = parse_title(model_name=model_name, title_hyp_dict=hyp_dict, title_hyp_names=hyp_names,
                                         label_hyp_index=best_losses.index, label_hyp_names=weights_names,
                                         additional_info="'s robustness evaluated on the training " +
                                                         loss_names[k].replace('_', ' ') + " " + additional_info)

        # Creating a figure
        fig, ax = plt.subplots(len(fig_ax_y_values), len(fig_ax_x_values),
                               figsize=(8 * n_cols, 7 * n_rows), sharey=True)
        plt.subplots_adjust(hspace=0.25)

        # Adding title
        fig.suptitle(title, x=0.55, y=0.98, fontsize=24, fontweight='bold')

        # For each value in the figure x-axis and y-axis
        for i_row in range(n_rows):
            for i_col in range(n_cols):

                # Extracting this loss data and preparing the dataframe for the plot
                loss_df = best_losses.loc[
                          best_losses.index.get_loc_level(key=fig_ax_x_values[i_col], level=axis_spec['fig_ax_x'])[0] &
                          best_losses.index.get_loc_level(key=fig_ax_y_values[i_row], level=axis_spec['fig_ax_y'])[0],
                          :].copy()
                loss_df.loc[:, 'weights'] = loss_df[[loss_names[k]]].index.droplevel(
                    hyp_dropped + ['experiment']).to_flat_index()
                loss_df = loss_df.reset_index().set_index('experiment')
                loss_df = loss_df[[loss_names[k], 'weights']]
                loss_df = pd.pivot_table(loss_df, index='experiment',
                                         values=loss_names[k], columns='weights')

                # Parsing labels
                labels = parse_labels(hyp_names=weights_names,
                                      hyp_dropped=hyp_dropped + [axis_spec['fig_ax_x'], axis_spec['fig_ax_y']],
                                      hyp_tuple_values=loss_df.columns)

                # Plotting boxplot
                bplot = ax[i_row, i_col].boxplot(loss_df, labels=loss_df.columns, notch=True, patch_artist=True,
                                                 showfliers=not remove_outliers)

                # Adding colors
                if colors is not None:
                    for patch, color in zip(bplot['boxes'], colors):
                        patch.set_facecolor(color)

                # Adding maximum value
                if additional_data is not None:
                    ax[i_row, i_col].scatter(range(1, len(loss_df.columns) + 1),
                                             getattr(loss_df, additional_data)(),
                                             c=colors, marker='*', s=200, label=additional_data)
                    ax[i_row, i_col].legend()

                # Setting axis labels and figure's title
                ax[i_row, i_col].set_title(weights_names[axis_spec['fig_ax_x']] + f'={fig_ax_x_values[i_col]}',
                                           fontsize=22, fontweight='bold')
                ax[i_row, i_col].yaxis.set_tick_params(labelleft=True)
                ax[i_row, i_col].set_xticklabels(labels, rotation=90)
                if i_row == n_rows - 1:
                    ax[i_row, i_col].set_xlabel('Losses weights values', fontsize=18, fontweight='bold')
                ax[i_row, i_col].set_ylabel(
                    y_label + ' (' + weights_names[axis_spec['fig_ax_y']] + f'={fig_ax_y_values[i_row]})', fontsize=18,
                    fontweight='bold')

        # Show figure
        plt.show()


# Function to extract the losses' evolution per hyperparameter and experiment and aggregate the losses
# throughout the experiments
def extract_losses_evolution(hyperparameters, model_path, agg_func=None):
    """
    Function to extract the losses' evolution per hyperparameters and experiment and aggregate the losses
    throughout experiments.
    Args:
        hyperparameters:    dict, hyperparameters name and values.
        model_path:         str, path where the models are stored.
        agg_func:           list, aggregation function to compute, default=None.
    Returns:    pd.DataFrame, aggregated losses throughout experiment.
    """

    # Parsing default argument
    if agg_func is None:
        agg_func = ['median', 'std']

    # Initialization of a dataframe to store the losses evolution
    losses = pd.DataFrame()

    # For each hyperparameter, retrieve the losses for each experiment and aggregate the losses
    for hyp_key in hyperparameters:

        # Retrieve the experiments directories
        experiments = [file for file in os.listdir(f'{model_path}/{hyp_key}') if file.startswith('experiment_')]

        # Initialization of a dataframe to store all experiments losses 
        losses_exp = pd.DataFrame()

        # For each experiment, add the losses to the dataframe
        for experiment in experiments:
            # Retrieve the losses evolution
            loss = pd.read_csv(f'{model_path}/{hyp_key}/{experiment}/losses.csv')

            # Add useful columns
            loss['hyperparameter'] = hyp_key
            loss['experiment'] = experiment
            loss['epoch'] = loss.index

            # Add this experiment losses to the overall dataframe
            losses_exp = pd.concat([losses_exp, loss], axis=0)

        # Compute median and standard deviation
        losses_exp = pd.pivot_table(losses_exp, index=['epoch'], aggfunc=agg_func)

        # Add useful column
        losses_exp['hyperparameter'] = hyp_key

        # Aggregate information to overall dataframe
        losses = pd.concat([losses, losses_exp], axis=0)

    # Returning the overall dataframe
    return losses


# Function to extract the losses' evolution aggregated on training hyperparameters and throughout the experiments
def extract_losses_evolution_aggregated(model_names, model_parent_path, general_model_name, agg_func=None,
                                        hyp_fixed=None):
    """
    Function to extract the losses' evolution for each hyperparameter and experiment and aggregate the losses throughout
    the experiments and the hyperparameters combinations.
    Args:
        model_names:        list, model names to explore.
        model_parent_path:  str, path where to find the parent directory containing the models.
        general_model_name: str, general model name.
        agg_func:           list, aggregation function to compute (e.g. 'max', 'min' etc.), default=None.
        hyp_fixed:          dict, hyperparameters name and value that are fixed, default=None.
    Returns:    pd.DataFrame, aggregated losses.
    """

    # Parsing default argument
    if agg_func is None:
        agg_func = ['median', 'std']

    # Initialization of a dataframe to store the losses evolution
    losses = pd.DataFrame()

    # For each model and hyperparameter, retrieve the losses for each experiment and aggregate the losses
    for model_name in model_names:

        # Retrieve the hyperparameters
        hyperparameters = [file for file in os.listdir(f'{model_parent_path}/{model_name}/')
                           if '_'.join(
                hyp_name + '_' + str(hyp_value) for hyp_name, hyp_value in hyp_fixed.items()) in file]

        # For each hyperparameter, aggregate the losses throughout the experiments
        for hyp_key in hyperparameters:

            # Retrieve the experiments directories
            experiments = [file for file in os.listdir(f'{model_parent_path}/{model_name}/{hyp_key}') if
                           file.startswith('experiment_')]

            # Initialization of a dataframe to store all experiments losses 
            losses_exp = pd.DataFrame()

            # For each experiment, add the losses to the dataframe
            for experiment in experiments:
                # Retrieve the losses evolution
                loss = pd.read_csv(f'{model_parent_path}/{model_name}/{hyp_key}/{experiment}/losses.csv')

                # Add useful column on which to aggregate data
                loss['epoch'] = loss.index

                # Add this experiment losses to the overall dataframe
                losses_exp = pd.concat([losses_exp, loss], axis=0)

        # Compute median and standard deviation
        losses_exp = pd.pivot_table(losses_exp, index=['epoch'], aggfunc=agg_func)

        # Add useful weights information columns
        losses_exp[model_name.split('_')[len(general_model_name.split('_'))::2]] = pd.DataFrame(
            [list(map(float, model_name.split('_')[len(general_model_name.split('_')) + 1::2]))],
            index=losses_exp.index)

        # Aggregate information to overall dataframe
        losses = pd.concat([losses, losses_exp], axis=0)

    # Adding information to index
    losses = losses.reset_index().set_index(model_names[-1].split('_')[len(general_model_name.split('_'))::2])

    # Returning the overall dataframe
    return losses


# Function to extract the losses' evolution per hyperparameter and experiment
# and aggregate the losses throughout the experiments
def extract_losses_evolution_per_hyperparameter(model_names, model_parent_path, hyp_key, general_model_name,
                                                agg_func=None):
    """
    Function to extract the losses' evolution per hyperparameter and experiment and aggregate the losses
    throughout the experiments and the weights.
    Args:
        model_names:        list, model names to explore.
        model_parent_path:  str, path to the parent directory where the models are stored.
        hyp_key:            str, folder name corresponding to this hyperparameter combination.
        general_model_name: str, general model name.
        agg_func:           list, aggregation function to compute (e.g. 'max', 'min' etc.), default=None.
    Returns:    pd.DataFrame,   aggregated losses.
    """

    # Parsing default argument
    if agg_func is None:
        agg_func = ['median', 'std']

    # Initialization of a dataframe to store the losses evolution
    losses = pd.DataFrame()

    # For each model, retrieve the losses for each experiment and aggregate the losses
    for model_name in model_names:

        # Retrieve the experiments directories
        experiments = [file for file in os.listdir(f'{model_parent_path}/{model_name}/{hyp_key}') if
                       file.startswith('experiment_')]

        # Initialization of a dataframe to store all experiments losses
        losses_exp = pd.DataFrame()

        # For each experiment, add the losses to the dataframe
        for experiment in experiments:
            # Retrieve the losses evolution
            loss = pd.read_csv(f'{model_parent_path}/{model_name}/{hyp_key}/{experiment}/losses.csv')

            # Add useful column on which to aggregate data
            loss['epoch'] = loss.index

            # Add this experiment losses to the overall dataframe
            losses_exp = pd.concat([losses_exp, loss], axis=0)

        # Compute median and standard deviation
        losses_exp = pd.pivot_table(losses_exp, index=['epoch'], aggfunc=agg_func)

        # Add useful weights information columns
        losses_exp[model_names[-1].split('_')[len(general_model_name.split('_'))::2]] = pd.DataFrame(
            [list(map(float, model_names[-1].split('_')[len(general_model_name.split('_')) + 1::2]))],
            index=losses_exp.index)

        # Aggregate information to overall dataframe
        losses = pd.concat([losses, losses_exp], axis=0)

    # Adding information to index
    losses = losses.reset_index().set_index(model_names[-1].split('_')[len(general_model_name.split('_'))::2])

    # Returning the overall dataframe
    return losses


# Function to plot losses evolution for multi run analysis
def plot_losses_evolution_multi(losses, hyp_names, weights_dict, weights_names, loss_names, model_name,
                                colors=None, n_cols=3, y_label='Loss value', q=0.999, plot_std=True,
                                remove_outliers=True):
    """
    Function to plot the losses' evolution throughout the epochs for a multi-run analysis.
    Args:
        losses:             pd.DataFrame, losses values throughout training.
        hyp_names:          dict, hyperparameters names to display (e.g. math formula).
        weights_dict:       dict, weights names and values to explore.
        weights_names:      dict, weights names to display (e.g. math formula).
        loss_names:         list, losses names.
        model_name:         str, model name.
        colors:             dict, colors for each loss, default=None.
        n_cols:             int, number of columns in the plot, default=3.
        y_label:            str, y-axis label, default='Loss value'.
        q:                  float, quantile value for the outliers, default=0.999.
        plot_std:           bool, whether to add the standard deviation to the plot, default=True.
        remove_outliers:    bool, whether to remove the outliers in the plot, default=True.
    """

    # Retrieving the hyperparameters
    hyperparameters = np.sort(losses['hyperparameter'].unique())

    # Parsing hyperparameters string to list
    hyp = [[hyp_key.split('_')[0::2], hyp_key.split('_')[1::2]] for hyp_key in hyperparameters]

    # Parsing hyperparameters list to multiindex
    hyp_index = pd.MultiIndex.from_arrays(np.array(hyp)[:, 1, :].T, names=hyp[0][0])

    # Parsing title
    title, hyp_dropped = parse_title(model_name=model_name, title_hyp_dict=weights_dict, title_hyp_names=weights_names,
                                     label_hyp_index=hyp_index, label_hyp_names=hyp_names,
                                     additional_info="'s robustness evaluated on the training losses evolution")
    # Creating a figure
    n_rows = len(loss_names) // n_cols + math.ceil(len(loss_names) % n_cols / n_cols)
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(11 * n_cols, 9 * n_rows))
    plt.subplots_adjust(wspace=0.3)

    # Adding title
    fig.suptitle(title, x=0.55, y=0.97, fontsize=24, fontweight='bold', ha='center', va='center')

    # Colors
    if colors is None:
        colors = [None] * len(hyperparameters)

    # Plotting each loss evolution
    for k in range(len(loss_names)):

        # Defining the row and column index in the plot
        i_row = k // n_cols
        i_col = k % n_cols

        # Parsing labels
        labels = parse_labels(hyp_names=hyp_names, hyp_dropped=hyp_dropped, hyp_tuple_values=hyp_index.to_flat_index())

        # Plotting each loss evolution for each hyperparameter
        for j in range(len(hyperparameters)):

            # Plotting median
            ax[i_row, i_col].plot(losses.loc[losses['hyperparameter'] == hyperparameters[j], ('median', loss_names[k])],
                                  label=labels[j], color=colors[j])

            # Plotting standard deviation
            if plot_std:
                ax[i_row, i_col].fill_between(x=losses.loc[losses['hyperparameter'] == hyperparameters[j], :].index,
                                              y1=(losses.loc[losses['hyperparameter'] == hyperparameters[j],
                                                             ('median', loss_names[k])] -
                                                  losses.loc[losses['hyperparameter'] == hyperparameters[j],
                                                             ('std', loss_names[k])]),
                                              y2=(losses.loc[losses['hyperparameter'] == hyperparameters[j],
                                                             ('median', loss_names[k])] +
                                                  losses.loc[losses['hyperparameter'] == hyperparameters[j],
                                                             ('std', loss_names[k])]),
                                              alpha=0.3, color=colors[j])

        # Setting the limits of the plot
        if plot_std and remove_outliers:
            ax[i_row, i_col].set_ylim((losses.loc[:, ('median', loss_names[k])] -
                                       losses.loc[:, ('std', loss_names[k])]).quantile(q=1 - q),
                                      (losses.loc[:, ('median', loss_names[k])] +
                                       losses.loc[:, ('std', loss_names[k])]).quantile(q=q))

        # Setting axis labels and figure's title
        ax[i_row, i_col].set_title(f'{loss_names[k].replace("_", " ")}',
                                   fontsize=22, fontweight='bold')
        ax[i_row, i_col].set_xlabel('Number of epochs', fontsize=18, fontweight='bold')
        ax[i_row, i_col].set_ylabel(y_label, fontsize=18, fontweight='bold')
        legend = ax[i_row, i_col].legend(bbox_to_anchor=(1, 0.5), loc='center left', handlelength=1.1)
        for line in legend.get_lines():
            line.set_linewidth(4.0)

    # Removing unused graphs
    for i in range(len(loss_names), n_cols * n_rows):
        # Defining the row and column index in the plot
        i_row = i // n_cols
        i_col = i % n_cols

        # Removing the axis
        ax[i_row, i_col].axis('off')

        # Show figure
    plt.show()


# Function to plot losses evolution for a certain hyperparameter's value for multi-run analysis
def plot_losses_evolution_per_hyperparameter(losses, hyp_names, hyp_dict, weights_names, loss_names, model_name,
                                             axis_spec=None, colors=None, y_label='Loss value',
                                             additional_info='loss', q=0.999, plot_std=True, remove_outliers=True):
    """
    Function to plot the losses' evolution throughout the epochs for a certain hyperparameter value for a multi run
    analysis.
    Args:
        losses:             pd.DataFrame, losses values throughout training.
        hyp_names:          dict, hyperparameters names to display (e.g. math formula).
        hyp_dict:           dict, hyperparameters names and values to explore.
        weights_names:      dict, weights names to display (e.g. math formula).
        loss_names:         list, losses names.
        model_name:         str, model name.
        axis_spec:          dict, axis specification for where to place the hyperparameters on the plot, default=None.
        colors:             dict, colors for each loss, default=None.
        y_label:            str, y-axis label, default='Loss value'.
        additional_info:    str, info to add to the title, default='loss'.
        q:                  float, quantile value for the outliers, default=0.999.
        plot_std:           bool, whether to add the standard deviation to the plot, default=True.
        remove_outliers:    bool, whether to remove the outliers in the plot, default=True.
    """

    # Defining the default axes specifications
    if axis_spec is None:
        axis_spec = dict(zip(['fig_ax_x', 'fig_ax_y'], weights_names.keys()))

    # Sorting index
    losses = losses.reset_index().set_index(list(weights_names.keys()))
    losses = losses.sort_index(axis=0)

    # Retrieving weights values for figure axes
    fig_ax_x_values = losses.index.get_level_values(level=axis_spec['fig_ax_x']).unique()
    fig_ax_y_values = losses.index.get_level_values(level=axis_spec['fig_ax_y']).unique()
    n_cols = len(fig_ax_x_values)
    n_rows = len(fig_ax_y_values)

    # Defining the default colors
    if colors is None:
        colors = [None] * len(weights_names)

    # For each loss, plot the influence of the losses weights
    for k in range(len(loss_names)):

        # Parsing the title
        title, hyp_dropped = parse_title(model_name=model_name, title_hyp_dict=hyp_dict, title_hyp_names=hyp_names,
                                         label_hyp_index=losses.index, label_hyp_names=weights_names,
                                         additional_info="'s robustness evaluated on the training " +
                                                         loss_names[k].replace('_', ' ') + " " + additional_info)

        # Creating a figure
        fig, ax = plt.subplots(len(fig_ax_y_values), len(fig_ax_x_values),
                               figsize=(10 * n_cols, 7 * n_rows), sharey=True)
        plt.subplots_adjust(wspace=0.4)

        # Adding title
        fig.suptitle(title, x=0.55, y=0.98, fontsize=24, fontweight='bold')

        # For each value in the figure x-axis and y-axis
        for i_row in range(n_rows):
            for i_col in range(n_cols):

                # Creating a filter for this model
                model_filter = np.ones(len(losses)).astype(bool)
                if isinstance(losses.index.get_loc_level(key=fig_ax_x_values[i_col], level=axis_spec['fig_ax_x'])[0],
                              slice):
                    model_filter[np.r_[
                        losses.index.get_loc_level(key=fig_ax_x_values[i_col], level=axis_spec['fig_ax_x'])[0]]] = True
                else:
                    model_filter &= losses.index.get_loc_level(key=fig_ax_x_values[i_col], level=axis_spec['fig_ax_x'])[
                        0]
                if isinstance(losses.index.get_loc_level(key=fig_ax_y_values[i_row], level=axis_spec['fig_ax_y'])[0],
                              slice):
                    model_filter[np.r_[
                        losses.index.get_loc_level(key=fig_ax_y_values[i_row], level=axis_spec['fig_ax_y'])[0]]] = True
                else:
                    model_filter &= losses.index.get_loc_level(key=fig_ax_y_values[i_row], level=axis_spec['fig_ax_y'])[
                        0]

                # Retrieving the index without duplicates
                unique_index = losses.loc[model_filter, :].index.drop_duplicates()

                # Parsing labels
                labels = parse_labels(hyp_names=weights_names,
                                      hyp_dropped=hyp_dropped + [axis_spec['fig_ax_x'], axis_spec['fig_ax_y']],
                                      hyp_tuple_values=unique_index.to_flat_index())

                # Setting default colors
                if colors is None:
                    colors = [None] * len(labels)

                # For each remaining weight, plot the median and standard deviation
                for j in range(len(np.unique(labels))):

                    # Plotting median
                    ax[i_row, i_col].plot(losses.loc[unique_index[j], ('median', loss_names[k])].values,
                                          label=labels[j], color=colors[j])

                    # Plotting standard deviation
                    if plot_std:
                        ax[i_row, i_col].fill_between(x=losses.loc[unique_index[j], 'epoch'].values,
                                                      y1=(losses.loc[
                                                              unique_index[j], ('median', loss_names[k])].values -
                                                          losses.loc[unique_index[j], ('std', loss_names[k])].values),
                                                      y2=(losses.loc[
                                                              unique_index[j], ('median', loss_names[k])].values +
                                                          losses.loc[unique_index[j], ('std', loss_names[k])].values),
                                                      alpha=0.3, color=colors[j])

                # Setting the limits of the plot
                if plot_std & remove_outliers:
                    ax[i_row, i_col].set_ylim((losses.loc[:, ('median', loss_names[k])] -
                                               losses.loc[:, ('std', loss_names[k])]).quantile(q=1 - q),
                                              (losses.loc[:, ('median', loss_names[k])] +
                                               losses.loc[:, ('std', loss_names[k])]).quantile(q=q))

                # Setting axis labels and figure's title
                ax[i_row, i_col].set_title(weights_names[axis_spec['fig_ax_x']] + f'={fig_ax_x_values[i_col]}',
                                           fontsize=22, fontweight='bold')
                ax[i_row, i_col].yaxis.set_tick_params(labelleft=True)
                ax[i_row, i_col].set_xlabel('Number of epochs', fontsize=18, fontweight='bold')
                ax[i_row, i_col].set_ylabel(
                    y_label + '(' + weights_names[axis_spec['fig_ax_y']] + f'={fig_ax_y_values[i_row]})',
                    fontsize=18, fontweight='bold')
                legend = ax[i_row, i_col].legend(bbox_to_anchor=(1, 0.5), loc='center left', handlelength=1.1)
                for line in legend.get_lines():
                    line.set_linewidth(4.0)

        # Show figure
        plt.show()


# Function to plot the losses' evolution for single run analysis
def plot_losses_evolution_single(losses_list, hyperparameters, n_cols=4, colors=None, remove_outliers_losses=None,
                                 q=0.999, start_index=0):
    """
    Function to plot the losses' evolution for a single run analysis.
    Args:
        losses_list:                list of list, losses evolution for each hyperparameter combination.
        hyperparameters:            list of dict, hyperparameters combinations.
        n_cols:                     int, number of columns in the plot, default=4.
        colors:                     list of str, colors to use, default=None.
        remove_outliers_losses:     dict of bools, whether to remove the outliers for each loss, default=None.
        q:                          float, quantile to use for determining the outliers, default=0.999.
        start_index:                int, starting index for computing the quantile, default=0.
    """

    # Retrieving the losses names
    losses_names = list(losses_list[0].columns)

    # Parsing default arguments
    if colors is None:
        colors = [colors] * len(hyperparameters)
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
    title = 'Losses evolution during training'

    # Retrieving fixed hyperparameters and add them to title info
    hyp_fixed = dict(
        pd.DataFrame(hyperparameters).apply(lambda x: x.unique() if len(x.unique()) == 1 else None
                                            ).dropna(axis=1).loc[0, :])
    if len(hyp_fixed) > 0:
        title += ' (' + ', '.join([f'{key}={hyp_fixed[key]}' for key in hyp_fixed.keys()]) + ')'

    # Retrieving hyperparameters key for labels
    hyp_label_keys = list(set(hyperparameters[0].keys()) - set(hyp_fixed.keys()))

    # Computing the number of rows
    n_rows = math.ceil(len(losses_names) / n_cols)

    # Initialization of a figure
    fig, ax = plt.subplots(n_rows, n_cols, figsize=(n_cols * 7.5, n_rows * 5.5),
                           gridspec_kw={'hspace': 0.25, 'wspace': 0.2})

    # Adding title to the figure
    fig.suptitle(title, x=0.55, y=0.95,
                 ha='center', va='center', fontsize=25, fontweight='bold')

    # Plot each loss evolution for each combination of hyperparameters
    for i in range(len(losses_names)):

        # Retrieving the index of the figure
        i_row, i_col = i // n_cols, i % n_cols

        # Plotting the loss evolution for each hyperparameter combination
        for j in range(len(hyperparameters)):

            # Parsing labels
            label = ''
            for k in range(len(hyp_label_keys)):
                label += f'{hyp_label_keys[k]}={hyperparameters[j][hyp_label_keys[k]]}'
                if k < len(hyp_label_keys) - 1:
                    label += '\n'

            # Plotting the loss evolution
            ax[i_row, i_col].plot(losses_list[j][losses_names[i]][start_index:], label=label, c=colors[j])

            # Computing the quantiles for plot's limits
            if remove_outliers[losses_names[i]]:
                quantiles[losses_names[i]]['max'] = max(quantiles[losses_names[i]]['max'],
                                                        losses_list[j][losses_names[i]][start_index:].quantile(q=q))
                quantiles[losses_names[i]]['min'] = min(quantiles[losses_names[i]]['min'],
                                                        losses_list[j][losses_names[i]][start_index:].quantile(q=1 - q))

        # Setting the axis labels and figure's title
        ax[i_row, i_col].set_title(f'{losses_names[i].replace("_", " ")} loss evolution', fontsize=18,
                                   fontweight='bold')
        ax[i_row, i_col].set_ylabel(f'{losses_names[i].replace("_", " ")} loss', fontsize=15, fontweight='bold')
        ax[i_row, i_col].set_xlabel('Number of epochs', fontsize=15, fontweight='bold')

        # Adding legend
        if len(hyperparameters) > 1:
            ax[i_row, i_col].legend()

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

    # Showing the figure
    plt.show()
