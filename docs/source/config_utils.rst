py_config_runner.config_utils
=============================

This module contains some helper methods to minimally check input configuration inside running script.


.. currentmodule:: py_config_runner.config_utils

.. automodule:: py_config_runner.config_utils
   :members:


Required fields for basic configurations
----------------------------------------

Following attributes can be used with :meth:`~py_config_runner.config_utils.assert_config` inside the running script to check input configuration.


.. attribute:: BASE_CONFIG 

List of required fields for a base configuration: integer `seed` and boolean `debug` 


.. attribute:: TORCH_DL_BASE_CONFIG 

List of required fields for a base torch deep learning configuration: BASE_CONFIG with `device` and `model` 


.. attribute:: TRAIN_CONFIG 

List of required fields for torch training configuration


.. attribute:: TRAINVAL_CONFIG 

List of required fields for torch training and validation configuration


.. attribute:: INFERENCE_CONFIG 

List of required fields for torch inference configuration
