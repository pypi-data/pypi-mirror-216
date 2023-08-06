# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neuralsens']

package_data = \
{'': ['*'], 'neuralsens': ['data/*']}

install_requires = \
['matplotlib>=3.5.2,<4.0.0',
 'numpy>=1.22.4,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'scipy>=1.8.1,<2.0.0']

setup_kwargs = {
    'name': 'neuralsens',
    'version': '0.0.15',
    'description': 'Calculate word counts in a text file.',
    'long_description': '# NeuralSens <img src="docs/source/_static/NeuralSens.PNG" width="135px" height="140px" align="right" style="padding-left:10px;background-color:white;" />\n\n#### *Jaime Pizarroso Gonzalo, jpizarroso@comillas.edu*\n#### *Antonio Muñoz San Roque, Antonio.Munoz@iit.comillas.edu*\n#### *José Portela González, jose.portela@iit.comillas.edu*\n<!-- badges: start -->\n\n[![Documentation Status](https://readthedocs.org/projects/neuralsens/badge/?version=latest)](https://neuralsens.readthedocs.io/en/latest/?version=latest)\n[![pypi](https://img.shields.io/pypi/v/neuralsens.svg)](https://pypi.python.org/pypi/neuralsens)\n[![python](https://img.shields.io/badge/python-%5E3.8-blue)]()\n[![os](https://img.shields.io/badge/OS-Ubuntu%2C%20Mac%2C%20Windows-purple)]()\n<!-- badges: end -->\nThis is the development repository for the `neuralsens` package.  Functions within this package can be used for the analysis of neural network models created in Python. \n\nThe last version of this package can be installed using pip:\n\n```bash\n$ pip install neuralsens\n```\n\nIt can also be installed with conda:\n```bash\n$ conda install -c jaipizgon neuralsens\n```\n\n### Bug reports\n\nPlease submit any bug reports (or suggestions) using the [issues](https://github.com/JaiPizGon/NeuralSens/issues) tab of the GitHub page.\n\n### Functions\n\nOne function is available to analyze the sensitivity of a multilayer perceptron, evaluating variable importance and plotting the analysis results.\n\n```python\n# Import necessary packages to reproduce the example\nimport neuralsens.partial_derivatives as ns\nfrom neuralsens.daily_demand_tr import load_daily_data_demand_tr\nimport pandas as pd\nfrom sklearn.neural_network import MLPRegressor\n\n# Load data and scale variables\ndaily_demand_tr = load_daily_data_demand_tr()\nX_train = daily_demand_tr[["WD","TEMP"]]\nX_train.iloc[:, 1] = X_train.iloc[:, 1] / 10\ny_train = daily_demand_tr["DEM"] / 100\n```\n\nThe `jacobian_mlp` function analyze the sensitivity of the output to the input and  plots three graphics with information about this analysis. To calculate this sensitivity it calculates the partial derivatives of the output to the inputs using the training data. \nThe first plot shows information between the mean and the standard deviation of the sensitivity among the training data:\n- if the mean is different from zero, it means that the output depends on the input because the output changes when the input change.\n- if the mean is nearly zero, it means that the output could not depend on the input. If the standard deviation is also near zero it almost sure that the output does not depend on the variable because for all the training data the partial derivative is zero.\n- if the standard deviation is different from zero it means the the output has a non-linear relation with the input because the partial derivative derivative of the output depends on the value of the input.\n- if the standard deviation is nearly zero it means that the output has a linear relation with the input because the partial derivative of the output does not depend on the value of the input.\nThe second plot gives an absolute measure to the importance of the inputs, by calculating the sum of the squares of the partial derivatives of the output to the inputs.\nThe third plot is a density plot of the partial derivatives of the output to the inputs among the training data, giving similar information as the first plot.\n\n```python\n### Create MLP model\nmodel = MLPRegressor(solver=\'sgd\', # Update function\n                    hidden_layer_sizes=[40], # #neurons in hidden layers\n                    learning_rate_init=0.1, # initial learning rate\n                    activation=\'logistic\', # Logistic sigmoid activation function\n                    alpha=0.005, # L2 regularization term\n                    learning_rate=\'adaptive\', # Type of learning rate used in training\n                    max_iter=500, # Maximum number of iterations\n                    batch_size=10, # Size of batch when training\n                    random_state=150)\n\n# Train model\nmodel.fit(X_train, y_train)\n\n# Obtain parameters to perform jacobian\nwts = model.coefs_\nbias = model.intercepts_\nactfunc = [\'identity\',model.get_params()[\'activation\'],model.out_activation_]\nX = pd.DataFrame(X_train, columns=["WD","TEMP"])\ny = pd.DataFrame(y_train, columns=["DEM"])\nsens_end_layer = \'last\'\nsens_end_input = False\nsens_origin_layer = 0\nsens_origin_input = True\n\n# Perform jacobian of the model\njacobian = ns.jacobian_mlp(wts, bias, actfunc, X, y)\njacobian.plot("sens")\n```\n\n![](docs/source/_static/readme_example_sensplots.png)<!-- -->\n\nApart from the plot created with the `"sens"` argument by an internal call\nto `sensitivity_plots()`, other plots can be obtained to analyze the neural \nnetwork model (although they are yet to be coded, thanks for your patience!).\n\n### Citation\n\nPlease, to cite NeuralSens in publications use:\n\nPizarroso J, Portela J, Muñoz A (2022). “NeuralSens: Sensitivity Analysis of Neural Networks.” _Journal of\nStatistical Software_, *102*(7), 1-36. doi: 10.18637/jss.v102.i07 (URL:\nhttps://doi.org/10.18637/jss.v102.i07).\n\n### License\n\nThis package is released in the public domain under the General Public License [GPL](https://www.gnu.org/licenses/gpl-3.0.en.html). \n\n### Association\nPackage created in the Institute for Research in Technology (IIT), [link to homepage](https://www.iit.comillas.edu/index.php.en) \n',
    'author': 'Jaime Pizarroso Gonzalo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JaiPizGon/NeuralSens',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
