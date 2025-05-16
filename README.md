# black-magic

Pre-commit hook to sanitize and restore magic commands for code formatters like Black

Handles magic commands induced into .py files by Databricks notebooks, such as:

```
%load_ext autoreload
%autoreload 2
```
Firstly `blackmagic-sanitize` is run to make .py backups, comment out the magic commands, then a formatter hook can be run. Finally, `blackmagic-restore` unpacks the original .py files from backups.

### Sample install:

`.pre-commit-hooks.yaml`
```{yaml}
repos:
  - repo: https://github.com/MarvinHerzogTE/black-magic
    rev: v0.1.0
    hooks:
      - id: blackmagic-sanitize

  - repo: https://github.com/psf/black
    rev: 24.3.0
    hooks:
      - id: black
        language_version: python3.11
        args: [--line-length=120]

  - repo: https://github.com/MarvinHerzogTE/black-magic
    rev: v0.1.0
    hooks:
      - id: blackmagic-restore
```