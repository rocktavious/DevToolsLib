VERSION=$(env PYTHONPATH=. python -c 'import setup; print(setup.DTL.__version__)')

TEMP_DIR=$(mktemp -d)
./setup.py sdist -d $TEMP_DIR

ls $TEMP_DIR

cp $TEMP_DIR/DTL-$VERSION.tar.gz ./package.tar.gz