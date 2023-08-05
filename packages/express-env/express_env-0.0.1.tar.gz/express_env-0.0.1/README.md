# Express env, .env generator

Express env configuration is safe to be committed to the repository,
as it does not contain any secrets, but contain information where secrets are stored.
All secret values are collected from third party services like `vault`,
`1Password`, etc.

```
Example usage:
    ee --config-file .ee/default.yaml generate .env
    # or
    source $(ee generate -)
```


## Installation

Using pipx:
```
pipx isntall express-env
```

Using pip:
```
pip install express-env
```

From source:
```
git clone 
