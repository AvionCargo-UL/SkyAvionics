# SkyAvionics
Beep boop on the plane!

# Building :hammer_and_wrench:

## :computer: On machine
1. Download [Python 3.10](https://www.python.org/downloads/release/python-3100/)
2. Download [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) or [VSCode](https://code.visualstudio.com/download)
3. Install packages with `dev-requirements.txt`
   1. When your venv is activated run: `pip install -r dev-requirements.txt`

## :gear: .yaml configuration
1. At the root of the project create aig.yaml file named `dev-conf`.
2. Add the following lines for to the configuration file:
    ```yaml
   vision:
     camera_index: 0
     fps: 0.25
    ```

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
