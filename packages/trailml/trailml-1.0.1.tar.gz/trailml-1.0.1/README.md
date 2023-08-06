# Trail

Trail brings more transparency to your ML experiments.
Start by using MLflow to track experiments and follow the steps below.

# Installation

Install Trail from PyPI via ```pip install trailml```

# Get started

```python
import mlflow
from trail import Trail

with mlflow.start_run() as run:
    with Trail('myProjectAlias'):
      ...your training code...
```

# User configuration

Primary path: ```trailconfig.yml```  
Secondary path: ```~/.config/trail.yml```

```yaml
username: <YOUR_USERNAME>
password: <YOUR_PASSWORD>
projects:
  myProjectAlias:
    id: 1234ABC
    parentExperimentId: ABCD123
```

The project alias is used to reference project configurations at runtime and is only applied locally.

## Required options:
- username
- password

Project-specific options are required if not overwritten at runtime.