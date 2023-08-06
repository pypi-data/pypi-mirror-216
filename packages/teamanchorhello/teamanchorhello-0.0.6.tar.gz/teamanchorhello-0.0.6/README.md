## TEAMANCHORHELLO

Team Anchor say hello using Pypi package.

## VENV
Active: source venv/bin/activate  
Deactive: deactivate
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
6. Upload to testpypi (can't upload same file version else delete dist/*):
    * python3 -m twine upload --repository testpypi dist/*
        * Enter user & password (register if you didn't have).
7. Upload to pypi:
    * python3 -m twine upload dist/*

## UPDATE PACKAGE - FASTEST WAY
1. $vim teamanchorhello\src\teamanchorhello.py
    * print('Team Anchor say hello <UPDATE>')
2. $vim setup.py
    * version: <UPDATE>
3. Upload to Pypi:
    * python3 -m twine upload dist/*

## HOW TO USE
1. $ pip3 install teamanchorhello
2. $ pyhon3
3. `>> import teamanchorhello`
4. `>> teamanchorhello.hello() // Output: Team Anchor say hello 0.0.5`
## PYPI
TESTPYPI: https://test.pypi.org/project/teamanchorhello/  
PYPI: https://pypi.org/project/teamanchorhello/

## CERTIFICATE ISSUE
* Can't use venv, exit venv & upload to Pypi.
* If use Python >= 3.10, maybe can use https://pip.pypa.io/en/latest/topics/https-certificates/.