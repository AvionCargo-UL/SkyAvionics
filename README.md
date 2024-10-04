# SkyAvionics
Beep boop on the plane!

# Building :hammer_and_wrench:

## :computer: On machine
1. Download [Python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Download [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) or [VSCode](https://code.visualstudio.com/download)
3. Install packages with `requirements.txt`
   1. When your venv is activated run: `pip install -r requirements.txt`
    
# Launching :rocket:

## :computer: On machine
```commandline
python main.py
```

## Commands
To fix linter and format issues run these two commands:
```commandline
black .
ruff check . --fix
```
