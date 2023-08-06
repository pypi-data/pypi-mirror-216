Batch-effects correction with Adversarial Information Factorization
===================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
Single cell sequencing is a recent technology that suffers from important batch effects related to the experimental conditions, thus contaminating any downstream analysis with an experimental bias, in particular for scRNA-seq data. 

The Adversarial Information Factorization (AIF) method, originally developped by Creswell et al. [1], relies on the conditional sampling of images with respect to an attribute: from smiling and unsmiling faces of celebrities, the model is able to generate any celberity's face under any of those 2 conditions. 

In this repository, we adapted this method to the batch-effect correction problem in scRNA-seq data and incorporated a projection constraint to add some regularization and cross-over between the batches' distribution.
The model is trained to accurately reconstruct samples with respect to their batch label, by learning a shared latent space distribution, as it supposed to be deprived from any batch-effect. Once the model is trained, the batch-effect correction relies on the projection of one batch's cell distributions onto the other ones. To do so, we use the same batch label for all cells to reconstruct the samples. 

To evaluate the model, we borrowed the evaluation framework proposed in [2].

## Architecture

The AIF's architecture is presented bellow, as well as the different blocks' optimization objective. 

<img src="images/AIF_architecture.png" width="500" height="200">
<img src="images/aif_losses.png" width="400" height="350">


## Repository structure
This repository is composed of the following folders:
- **`batchaif`**: useful functions to create and train the AIF model, correct batch effects and evaluate the model.
- **`data`**: directory containing raw data in csv or txt format.
- **`data_preprocessed`**: directory containing pre-processed data in csv format.
- **`Experiments`**: directory containing the results (trained model, losses, metrics) after calling one of the 
training functions.
- **`images`**: useful images for documentation.
- **`InData`**: directory containing pre-processed data in the right format for creating the dataset to work with 
pytorch dataloader.
- **`preprocessing`**: jupyter notebooks for preprocessing the data (filling the data_preprocessed directory) and parsing the data to the right format to create the BioDataset (filling the InData directory) and creating the hyperparameters' grid for grid search. 
- **`python_scripts`**: examples of python scripts on how to use the high-level training functions. 
- **`requirements.txt`**: libraries version.
- **`Tutorials`**: jupyter notebooks as tutorials to run the batch effects pipeline or grid search. 


## Setting up your workspace

To install the batchaif library, make sure you have installed python 3.9 and run the following command in your bash terminal: <br>
`pip install batchaif`

To clone this repository, run the following command in your bash terminal: <br>
`git clone https://gitlab-research.centralesupelec.fr/mics_biomathematics/biomaths/batchaif.git`

To set up your environment, make sure you are using python 3.9 and run the following command in your bash terminal: <br>
`pip install -r requirements.txt`

## Download the data

You can download the human blood dendritic cells (DC) scRNA-seq from GEO accession GSE94820  (referred to as dataset 1) at: https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE94820


## References
[1] Adversarial Information Factorization, Antonia Cresswell, Yumnah Mohamied, Biswa Sengupta, Anil A Bharath. <br>
[2] A benchmark of batch-effect correction methods for single-cell RNA sequencing data, Hoa Thi Nhu Tran, Kok Siong Ang, Marion Chevrier, Xiaomeng Zhang, Nicole Yee Shin Lee, Michelle Goh and Jinmiao Chen. <br>


## License

MIT.
