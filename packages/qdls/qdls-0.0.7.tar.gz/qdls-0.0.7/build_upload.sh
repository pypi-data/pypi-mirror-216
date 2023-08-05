rm ./dist/*
python -m build 

# Zsqpypi980.
python3 -m twine upload dist/*