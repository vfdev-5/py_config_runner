py_config_runner CLI
====================

Command line tool to run a script with python configuration file:

.. code-block:: bash

    py_config_runner scripts/training.py configs/train/baseline.py


Script file ``scripts/training.py`` should define ``run(config, **kwargs)`` method. 
Argument ``config`` is loaded from ``configs/train/baseline.py``.

See `Example for Machine/Deep Learning <https://github.com/vfdev-5/py_config_runner/tree/master/examples/README.md>`_ for details.
