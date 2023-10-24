# Status
[![CodeFactor](https://www.codefactor.io/repository/github/nmurphy101/pygame2dframework/badge)](https://www.codefactor.io/repository/github/nmurphy101/pygame2dframework) ![Release](https://github.com/nmurphy101/pygame2dframework/actions/workflows/build.yml/badge.svg?branch=main) ![Build](https://github.com/nmurphy101/pygame2dframework/actions/workflows/python-app.yml/badge.svg)

# pygame 2D framework
A framework/engine to make 2D pygame games with a game loader.
First game is the classic snake with portals.

# Just interested in playing one of the available games?
Go to the releases section or click here [HERE](https://github.com/nmurphy101/pygame2Dframework/releases)

Then download the most recent release's `pygame_framework_version_number.zip` file in the Assests section of that release

Unzip and run the main.exe file.

Enjoy!

# Available Games
## Snake
A game of snake. Can play it by yourself or vs one or many AI.
  - as a twist there are portals that occasionally move around that teleport you from one to the other
  - gameplay settings give control over options like number of ai, invinsibility, etc


# Want to develop a game with this project?
## Before starting
Use the snake game in the games directory as an example of how to write your game
Make a new directory in the pkg/games directory to store your game files
Store your assets in the _internal/assets directory

## Windows
### Setting up development environment
install and setup python3
setup a virtual environment, enter virtual environment, and install needed packages
```
python3 -m virtualenv venv
venv/Scripts/Activate.ps1
pip3 install -r requirements.txt
```

run the main file
```
python ./main.py
```

#### Manual build to exe
pyinstaller main.spec

## Mac/Linux
### Setting up development environment
install and setup python3
setup a virtual environment, enter virtual environment, and install needed packages
```
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

run the main file
```
python ./main.py
```
