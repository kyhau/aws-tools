pip3 install wheel setuptools

python3 setup-app2.py bdist_wheel --universal --bdist-dir ~/temp/bdistwheel
python3 setup-app3.py bdist_wheel --universal --bdist-dir ~/temp/bdistwheel

rm -rf *.egg-info build dist/app dist/*.egg-info dist/*.dist-info
