# Build

Install:

```bash
python -m pip install --upgrade build
```

Build:

```bash
python -m build
```

Check:

```bash
py -m twine check dist/*
```

Publish:

```bash
py -m twine upload dist/*
```