# Express-env, .env generator

Express env configuration is safe to be committed to the repository,
as it does not contain any secrets, but contain information where secrets are stored.
All secret values are collected from third party services like `vault`,
`1Password`, etc.

## Usage

1. Create confing file: `.ee/default.yml` with the following content:
```yaml
# .ee/default.yml
env:
  CONST_VARIABLE: value
  CONST_VARIABLE_LONG_FORMAT:
    type: const
    value: value
  VARIABLE_FROM_VAULT:
    type: vault
    path: secret/path
    field: value
```

2a. Run `express-env` to generate `.env` file:
```bash
ee generate > .env
```

2b (or) Run `express-env` to set environment variables:
```bash
eval "$(ee generate --format bash)"
```

## Installation

Using pipx:
```bash
pipx install express-env
```

Using pip:
```bash
pip install express-env
```

From source:
```bash
git clone https://github.com/dswistowski/express-env ~/.express-env
cd ~/.express-env
pip install .
```
