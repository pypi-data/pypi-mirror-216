## TEAMANCHORHELLO

Team Anchor say hello using Pypi package.


## UPDATE PACKAGE
1. $vim teamanchorhello\src\teamanchorhello.py
    * print('Team Anchor say hello <UPDATE>')
2. $vim setup.py
    * version: <UPDATE>
3. python3 setup.py sdist bdist_wheel
    * verify vesion update: $ cat teamanchorhello\src\teamanchorhello.egg-info\PKG-INFO
4. pip3 install -e .
5. pyhon3
    * import teamanchorhello
    * teamanchorhello.hello()
6. Upload to testpypi:
    * python3 -m twine upload --repository testpypi dist/*
        * Enter user & password (register if you didn't have).
7. Upload to pypi:
    * python3 -m twine upload dist/*

## FASTEST WAY
1. $vim teamanchorhello\src\teamanchorhello.py
    * print('Team Anchor say hello <UPDATE>')
2. $vim setup.py
    * version: <UPDATE>
3. Delete file in dist/*
    * rm -rf dist/*
4. Upload to Pypi:
    * python3 -m twine upload dist/*
## PYPI
TESTPYPI: https://test.pypi.org/project/teamanchorhello/
PYPI: https://pypi.org/project/teamanchorhello/

## CERTIFICATE ISSUE
* Can't use venv, exit venv & upload to Pypi.
* If use Python >= 3.10, maybe can use https://pip.pypa.io/en/latest/topics/https-certificates/.