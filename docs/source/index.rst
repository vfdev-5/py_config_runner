Python Configuration Runner documentation
=========================================

Command line executable to run a script with python configuration file.

**Why a python file as configuration?**

- Configuration of any complexity
- No need to serialize the configuration
- No neeed other meta-languages for the configuration


Installation
============

From pip:

.. code:: bash

    pip install py-config-runner

Basic usage
===========

Once installed, user can run its script with a configuration:

.. code:: bash

    cd /path/to/my/project
    py_config_runner scripts/training.py configs/train/baseline.py

or if needed to run it as a module with `python` or other executable:

.. code:: bash

    cd /path/to/my/project
    python -u -m py_config_runner.__main__ scripts/training.py configs/train/baseline.py


The only condition on the script file is it should contain `run(config, **kwargs)` callable method. Additionally,
argument kwargs contains `logger` (e.g. `kwargs['logger']`) and `local_rank` (e.g. `kwargs['logger']`)
for distributed computations.


No restrictions are applied on the configuration file. It is user's responsibility to provide the script file that can
consume given configuration file. Provided configuration file is loaded as python module and exposed into the script as
the module named `config`.
