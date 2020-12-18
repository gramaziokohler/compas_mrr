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
       conda create -n compas_mobile_robot_reloc python=3.8 compas==0.19.3
       conda activate compas_mobile_robot_reloc

    -  Using `virtualenv <https://github.com/pypa/virtualenv>`__

    .. code:: bash

       virtualenv --python=python3.8 {{path/to/venv}}
       source {{path/to/venv}}/bin/activate

#.  Install package.

    .. code:: bash

       # or last version
       pip install compas_mobile_robot_reloc
       # or specific version
       compas_mobile_robot_reloc=={version}
       # from latest commit on git
       pip install git+https://github.com/gramaziokohler/compas_mobile_robot_reloc

#.  Make package accessible in Rhino and Grasshopper

    .. code:: bash

       python -m compas_mobile_robot_reloc.rhino_install

Update
======

To update the repository run:

.. code:: bash

   pip install -U compas_mobile_robot_reloc
   # or if you installed directly from github
   pip install -U git+https://github.com/gramaziokohler/compas_mobile_robot_reloc
