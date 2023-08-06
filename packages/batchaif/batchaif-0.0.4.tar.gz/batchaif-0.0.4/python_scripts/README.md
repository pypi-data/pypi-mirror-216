Batch-effects correction with Adversarial Information Factorization
===================================

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Description
In this directory, we provided python scripts examples on how to use the high-level training functions (batch-effects correction pipeline, grid search and robust grid search), with different versions of the model:
- **intrinsic weighting** (_AIF_) for raw counts,
- **normalization of the losses** (_AIF norm_) for normalized counts.
- **relative dynamic weighting** (_AIF rel dyn_) for both raw and normalized counts followed by a log1p transformation, to tackle the losses' different order of magnitude,
- **weighted Cross Entropy** (_weighted CE_), balancing the classes using their inverse frequencies to efficiently address unbalanced batches' issue,
- **projection constraint** (_AIF proj boost_) for using the projection constraint to add some cross-over and regulation between the batches conditional distribution, 
- **delayed networks** (_aux dis delayed_), for delaying both the Auxiliary and GAN networks' training to soften the factorization constraint in the case of batch-specific cell types,
- **decayed learning-rate** (_decay exp_), for decaying the learning with an exponential decay to address MSE's very steep decrease for log-normalized counts.


## Directory structure
This directory is organized as follows:
- **Grid search scripts**:
  - **`run_grid_search_aif.py`**: run a grid search on the losses' weights and the training hyperparameters for the _AIF_ model on raw counts.
  - **`run_grid_search_aif_norm.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF norm_ model on normalized counts.
  - **`run_grid_search_aif_norm_log_rel_dyn.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF rel dyn_ (relative dynamic weigthing) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_norm_log_rel_dyn_weighted_ce.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF rel dyn weighted CE_ (relative dynamic weigthing with weighted cross entropy) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_proj_boost_norm_log_rel_dyn.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_proj_boost_norm_log_rel_dyn_aux_dis_delayed_decay_exp.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn aux dis delayed decay exp_ (relative dynamic weigthing with projection constraint delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_proj_boost_norm_log_rel_dyn_weighted_ce.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn weighted CE_ (relative dynamic weigthing with projection constraint and weighted cross entropy) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_proj_boost_norm_log_rel_dyn_weighted_ce_aux_dis_delayed_decay_exp.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn weighted CE_ (relative dynamic weigthing with projection constraint, weighted cross entropy, delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_grid_search_aif_proj_boost_rel_dyn.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on raw counts.
  - **`run_grid_search_aif_proj_boost_rel_dyn_aux_dis_delayed.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn aux dis delayed_ (relative dynamic weigthing with projection constraint and delayed networks) model on raw counts.
  - **`run_grid_search_aif_proj_boost_rel_dyn_decay_exp.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn decay exp_ (relative dynamic weigthing with projection constraint and decayed learning rate) model on raw counts.
  - **`run_grid_search_aif_rel_dyn.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF rel dyn_ model on raw counts.
  - **`run_grid_search_aif_rel_dyn_weighted_ce.py`**: run a grid search (with a single training) on the losses' weights and the training hyperparameters for the _AIF rel dyn weighted CE_ model on raw counts.
- **Batch-effects pipeline scripts**:
  - **`run_pipeline_aif.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF_ model on raw counts.
  - **`run_pipeline_aif_norm.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF norm_ model on normalized counts.
  - **`run_pipeline_aif_norm_log_rel_dyn.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF rel dyn_ model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_norm_log_rel_dyn_weighted_ce.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF rel dyn weighted CE_ model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_proj_boost_norm_log_rel_dyn.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_proj_boost_norm_log_rel_dyn_aux_dis_delayed_decay_exp.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn aux dis delayed decay exp_ (relative dynamic weigthing with projection constraint, delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_proj_boost_norm_log_rel_dyn_weighted_ce.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn weighted ce_ (relative dynamic weigthing with projection constraint and weighted cross entropy) model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_proj_boost_norm_log_rel_dyn_weighted_ce_aux_dis_delayed_decay_exp.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn weighted ce aux dis delayed decay exp_ (relative dynamic weigthing with projection constraint, weighted cross entropy, delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_pipeline_aif_proj_boost_rel_dyn.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on raw counts.
  - **`run_pipeline_aif_proj_boost_rel_dyn_aux_dis_delayed.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint and delayed networks) model on raw counts.
  - **`run_pipeline_aif_proj_boost_rel_dyn_decay_exp.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF proj boost rel dyn decay exp_ (relative dynamic weigthing with projection constraint and decayed learning rate) model on raw counts.
  - **`run_pipeline_aif_rel_dyn.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF rel dyn_ model on raw counts.
  - **`run_pipeline_aif_rel_dyn_weighted_ce.py`**: run the batch-effects correction pipeline (training and batch-effects correction) for the _AIF rel dyn weighted CE_ model on raw counts.
- **Robust grid search scripts**:
  - **`run_robust_grid_search_aif.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF_ model on raw counts.
  - **`run_robust_grid_search_aif_norm.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF norm_ model on normalized counts.
  - **`run_robust_grid_search_aif_norm_log_rel_dyn.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF rel dyn_ model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_norm_log_rel_dyn_weighted_ce.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF rel dyn weighted CE_ model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_proj_boost_norm_log_rel_dyn.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_proj_boost_norm_log_rel_dyn_aux_dis_delayed_decay_exp.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn aux dis delayed decay exp_ (relative dynamic weigthing with projection constraint, delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_proj_boost_norm_log_rel_dyn_weighted_ce.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn weighted ce_ (relative dynamic weigthing with projection constraint and weighted cross entropy) model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_proj_boost_norm_log_rel_dyn_weighted_ce_aux_dis_delayed_decay_exp.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn weighted ce aux dis delayed decay exp_ (relative dynamic weigthing with projection constraint, weighted cross entropy, delayed networks and decayed learning rate) model on normalized counts followed by a log1p transformation.
  - **`run_robust_grid_search_aif_proj_boost_rel_dyn.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn_ (relative dynamic weigthing with projection constraint) model on raw counts.
  - **`run_robust_grid_search_aif_proj_boost_rel_dyn_aux_dis_delayed.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn aux dis delayed_ (relative dynamic weigthing with projection constraint and delayed networks) model on raw counts.
  - **`run_robust_grid_search_aif_proj_boost_rel_dyn_decay_exp.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF proj boost rel dyn decay exp_ (relative dynamic weigthing with projection constraint and decayed learning rate) model on raw counts.
  - **`run_robust_grid_search_aif_rel_dyn.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF rel dyn_ model on raw counts.
  - **`run_robust_grid_search_aif_rel_dyn_weighted_ce.py`**: run a robust grid search (with multiple trainings) on the losses' weights and the training hyperparameters for the _AIF rel dyn weighted CE_ model on raw counts.


## License

MIT.
