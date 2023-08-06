# Importing useful libraries
import os
from os.path import join
import numpy as np
import pandas as pd
import torch
from torch.utils import data as data_module


# Class for biological dataset
class Biodataset(data_module.Dataset):
    """
    Class to create the biodatasets to work with the data loaders from pytorch.
    """

    # Dataset constructor
    def __init__(self, root, train=True, norm=False, scaled=False, log_transfo=False,
                 filename='dataset_1', n_labels=2):
        """
        Constructor function of the biodataset class.
        Args:
            root:        str, path to the preprocessed data.
            train:       bool, whether it is the training or testing set, default=True.
            norm:        bool, whether to use the normalized data or not, default=False.
            scaled:      bool, whether to scale the data per batch or not, default=False.
            log_transfo: bool, whether to use log1p transformation on data, default=False.
            filename:    str, file's name, default='dataset_1'.
            n_labels:    int, number of batch labels, default=2.
        """
        # Storing useful attributes
        self.root = os.path.expanduser(root)  # Root directory
        self.train = train                    # Training or test
        self.norm = norm                      # Whether to get normalized data
        self.scaled = scaled                  # Whether to get scaled data
        self.log_transfo = log_transfo        # Whether to use log1p transformation
        self.filename = filename              # File name
        self.n_labels = n_labels              # Number of batch labels

        # Defining data suffix
        data_suffix = ''
        if self.norm:
            data_suffix += '_norm'
        if self.scaled:
            data_suffix += '_scaled'
        if self.log_transfo:
            data_suffix += '_log'

        # Loading the data and the labels
        if self.train:
            self.data = torch.from_numpy(np.array(pd.read_csv(join(self.root, self.filename,
                                                                   f'xTrain{data_suffix}.csv'))))
            self.labels = torch.from_numpy(np.array(pd.read_csv(join(self.root, self.filename,
                                                                     'yTrain.csv'))))

        else:
            self.data = torch.from_numpy(np.array(pd.read_csv(join(self.root, self.filename,
                                                                   f'xTest{data_suffix}.csv'))))
            self.labels = torch.from_numpy(np.array(pd.read_csv(join(self.root, self.filename,
                                                                     'yTest.csv'))))
        self.shape = self.data.shape

    # Function to extract an item corresponding to the specified index
    def __getitem__(self, index):
        """
        Function to extract an item corresponding to the specified index.
        Args:
            index:  int, index.
        Returns: (data, target) where target is the one-hot vector corresponding to the index of the target class.
        """
        # Retrieving data
        data, target = self.data[index], torch.eye(self.n_labels)[self.labels[index]]

        # Parsing target and data types
        target = target.type(torch.int)
        data = data.type(torch.float)

        # Returning data and target
        return data, target

    # Function to retrieve the length of the dataset
    def __len__(self):
        """
        Function to return the length of the dataset.
        Returns: int, length of the dataset.
        """
        return len(self.data)

    # Function to check if the directory exists
    def _check_dir_exist(self):
        """
        Function to check if the directory exists.
        Returns: bool, whether the directory exists or not.
        """
        in_dir = join(self.root, self.filename)
        assert os.path.isdir(in_dir)
        data_suffix = ''
        if self.norm:
            data_suffix += '_norm'
        if self.scaled:
            data_suffix += '_scaled'
        if self.log_transfo:
            data_suffix += '_log'
        if self.train:
            assert os.path.exists(join(in_dir, f'xTrain{data_suffix}.csv'))
            assert os.path.exists(join(in_dir, f'yTrain.csv'))
        else:
            assert os.path.exists(join(in_dir, f'xTest{data_suffix}.csv'))
            assert os.path.exists(join(in_dir, f'yTest.csv'))
