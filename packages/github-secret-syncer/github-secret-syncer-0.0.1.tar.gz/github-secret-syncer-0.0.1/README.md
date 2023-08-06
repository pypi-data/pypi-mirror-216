# Github Secret Syncer

Synchronize Github secrets with local `.env` file.

# Publish to PyPI

## Install building tools
Before publishing, you need to setup a virtual Python environment and install some tools.
```
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip wheel twine
```

## Publish to test.pypi.org (for testing purpose)
This makes you test your package before actually publishing it.

```python
# Build & Upload & Cleanup
python setup.py sdist bdist_wheel && python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/* && rm -rf dist build *egg-info
```

install it with:
```
pip install -i https://test.pypi.org/simple/ your-lovely-package-name
```

## Publish to pypi.org
This makes you actually publish the package to `pypi.org` (where you can `pip install` packages from it).

```python
# Build & Upload & Cleanup
python setup.py sdist bdist_wheel && python -m twine upload dist/* && rm -rf dist build *egg-info
```

You can then install it with regular pip command you normally use:
```
pip install your-lovely-package-name
```
