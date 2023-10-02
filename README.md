# pygame 2D framework
A framework/engine to make 2D pygame games with a game loader.
First game is the classic snake with upgrades.

# Available Games
## Snake_game
A game of snake. Can play it by hand or via the AI.
  - as a twist there are portals that occasionally move around that teleport you from one to the other

# generate requirements.txt when developing
```
pip3 install pygame
pip3 freeze > requirements.txt
```

# Setting up development Windows
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

# Setting up development Mac/Linux
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