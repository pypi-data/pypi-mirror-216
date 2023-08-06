Batch-effects correction with Adversarial Information Factorization
===================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
The Adversarial Information Factorization (AIF) method, originally developped by Creswell et al. [1], relies on the conditional sampling of images with respect to an attribute: from smiling and unsmiling faces of celebrities, the model is able to generate any celberity's face under any of those 2 conditions. 

This method is adapted to the batch-effect correction problem in scRNA-seq data. 
The model is trained to accurately reconstruct samples with respect to their batch label, by learning a joint latent space distribution, as it supposed to be deprived from any batch-effect. Once the model is trained, the batch-effect correction relies on the projection of one batch's cell distributions onto the other ones. To do so, we use the same batch label for all cells to reconstruct the samples. 

To evaluate the model, we borrowed the evaluation framework proposed in [2].

## Architecture

The AIF's architecture is presented bellow, as well as the different blocks' optimization objective. 

<img src="../images/AIF_architecture.png" width="450" height="200">
<img src="../images/aif_losses.png" width="350" height="350">

## Directory structure
This directory is organized as follows:
- **`batch_removal_functions.py`**: useful functions to correct batch effects once the model is trained (single draw or robust version).
- **`dataload.py`**: BioDataset class to work with pytorch dataloader.
- **`evaluation_functions.py`**: overall function to run the evaluation pipeline.
- **`metrics_functions.py`**: useful functions to evaluate the batch-effects correction based on a clustering task (ARI, ASW or LISI).
- **`model_auxiliary_functions.py`**: model auxiliary functions (plot losses' evolution, sample z).
- **`models.py`**: useful classes for each block of the AIF model (CVAE, Auxiliary, Discriminator).
- **`plotting_functions.py`**: useful functions for post-training analysis: plot models' comparison based on the best losses' value, 
the corresponding metrics or the losses' evolution.
- **`training_functions.py`**: useful functions to train and test the model, or high-level training functions (run the batch-effects correction pipeline,
run a grid search or a robust grid search on the losses' weights and training hyperparameters).
- **`weighting_functions.py`**: weighting strategies functions for weighing the losses during training.

## References
[1] Adversarial Information Factorization, Antonia Cresswell, Yumnah Mohamied, Biswa Sengupta, Anil A Bharath. <br>
[2] A benchmark of batch-effect correction methods for single-cell RNA sequencing data, Hoa Thi Nhu Tran, Kok Siong Ang, Marion Chevrier, Xiaomeng Zhang, Nicole Yee Shin Lee, Michelle Goh and Jinmiao Chen. <br>

## License

MIT.
