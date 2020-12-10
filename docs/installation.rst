*****************************************************************************
Installation
*****************************************************************************

Install
=======

#.  Create a virtual environment using your tool of choice
    (e.g. ``virtualenv``, ``conda``, etc).

    -  Using `Anaconda <https://www.anaconda.com/>`__

    .. code:: bash

       conda config --add channels conda-forge
       # use conda to install compas
       conda create -n total_station_robot_localization python=3.8 compas==0.15.6
       conda activate total_station_robot_localization

    -  Using `virtualenv <https://github.com/pypa/virtualenv>`__

    .. code:: bash

       virtualenv --python=python3.8 {{path/to/venv}}
       source {{path/to/venv}}/bin/activate

#.  Install package.

    .. code:: bash

       # or last version
       pip install total_station_robot_localization
       # or specific version
       total_station_robot_localization=={version}
       # from latest commit on git
       pip install git+https://github.com/gramaziokohler/total_station_robot_localization

#.  Make package accessible in Rhino and Grasshopper

    .. code:: bash

       python -m total_station_robot_localization.rhino_install

Update
======

To update the repository run:

.. code:: bash

   pip install -U total_station_robot_localization
   # or if you installed directly from github
   pip install -U git+https://github.com/gramaziokohler/total_station_robot_localization
