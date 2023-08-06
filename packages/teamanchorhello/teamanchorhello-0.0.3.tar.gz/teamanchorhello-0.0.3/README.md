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
    * python3 -m t

## PYPI
TESTPYPI: https://test.pypi.org/project/teamanchorhello/
PYPI: https://pypi.org/project/teamanchorhello/
