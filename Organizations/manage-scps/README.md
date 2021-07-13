# scp-helper

This script supports
- reading policy files (json) in the specified folder, and
- comparing current SCPs against the expected policies and managing SCPs accordingly

## Usage

First, install requirements

```bash
pip install -r requirements.txt
```

### To compare local policy files with the current deployed SCPs

Use `--dry-run` to see the potential changes.

```bash
python scp_helper.py --input-dir policies/
```
