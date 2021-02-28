invspec
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/invspec/workflows/CI/badge.svg)](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/invspec/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/invspec/branch/master/graph/badge.svg)](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/invspec/branch/master)


Generates stochastic matrices with given properties

```{python}
>>> import invspec
>>> import numpy as np
>>> 
>>> eigenvalues = np.array([0.9, 0.8, 0.4, 0.2])
>>> matrix = invspec.stochastic_matrix(eigenvalues)
>>> 
>>> evals, evecs = np.linalg.eig(matrix)
>>> evals
[1, 0.9, 0.8, 0.4, 0.2]
```

### Copyright

Copyright (c) 2021, rob arbon


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.5.
