## Installation

If you've just cloned the repository, you'll need to set up a virtual environment to bring in some dependencies. These steps only need to be run once.

``` shell
python3 -m venv --upgrade venv
venv/bin/python -m ensurepip --upgrade
venv/bin/python -m pip install --upgrade pip setuptools wheel
```

If your goal is to reproduce the last good analysis, you should install dependencies from the `requirements.txt` file.

``` shell
venv/bin/python -m pip install -r requirements.txt
venv/bin/python -m pip install virtualenv
venv/bin/virtualenv venv
```

If you're doing development, you should instead install the most recent versions of all the dependencies:

``` shell
venv/bin/python -m pip install -e .
```

If you want to use Jupyter Lab, you'll need to register your virtual environment with the server. Assuming you already have jupyterlab installed (as a system package or using pipx):

``` shell
venv/bin/python -m pip install ipykernel  # this has to be done for any fresh virtual environment
venv/bin/python -m ipykernel install --user --name=induction  # only do this if you haven't registered the kernel before
```

Some of the analysis/plotting notebooks use R instead of Python. Activate the virtual environment first before running the following commands in R to register a kernel with Jupyter and to install dependencies. This only needs to be done once per user.
``` shell
source venv/bin/activate
```

``` R
install.packages(c('tidyverse', 'lme4', 'emmeans', 'ggplot2', 'bssm'))   # direct code dependencies
install.packages(c('repr', 'IRdisplay', 'IRkernel'))             # for the R notebooks
```

## Running the code

In Jupyter Lab, you'll need to set the kernel for your notebook to `induction`. If you're running a script, make sure to activate your venv first (`source venv/bin/activate`) or run it using the virtualenv python (`venv/bin/python <my-script>`)

## Quirks

1) The cmap used for the publication is `pyart_balance`, imported by the package `pyart`. In newer versions of the package, the cmap was renamed to just `balance`.
2) The `transform` function in the PLS models from `sklearn` changed its parameter name from `Y` to `y` in newer versions. 
