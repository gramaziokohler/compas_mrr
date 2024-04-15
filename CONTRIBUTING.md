# Contributing

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

### Setup

1. Fork [the repository](https://github.com/gramaziokohler/compas_mrr) and clone the fork.

2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

    * Using [Anaconda](https://www.anaconda.com/)

    ```bash
    conda env update -f environment.yml
    conda activate compas_mrr-dev
    pip install -e .[dev]
    ```

    * Using [virtualenv](https://github.com/pypa/virtualenv)

    ```bash
    virtualenv --python=python3.10 {{path/to/venv}}
    source {{path/to/venv}}/bin/activate
    pip install -e .[dev]
    ```

4. (Optional) Make package accessible in Rhino and Grasshopper

   ```bash
   python -m compas_rhino.install
   ```

### Make a pull request

1. Make sure all tests pass on the unmodified code:

   ```bash
   pytest
   ```

1. Start making your changes to the **main** branch (or branch off of it) on your fork.
1. Make sure all tests still pass:

   ```bash
   pytest
   ```

1. Document the changes in the `CHANGELOG.md`
1. Commit your changes and push your branch to GitHub.
1. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

## Bug reports

When [reporting a bug](https://github.com/gramaziokohler/compas_mrr/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/gramaziokohler/compas_mrr/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
