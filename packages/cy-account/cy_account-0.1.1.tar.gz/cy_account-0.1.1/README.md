#cy-packages


python -m pip install --upgrade setuptools wheel

python setup.py sdist bdist_wheel


pip install D:\work\py\cy-packages\dist\cy-account-0.1.0.tar.gz

pip install --upgrade twine

twine upload --repository-url https://upload.pypi.org/legacy/ dist/*