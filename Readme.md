# Wikipedia Run
This python project has been done to be able to play a *Wikipedia Run* without worrying of cheating.

# Rules
The game es intended to be played on several computers (at the same time for more fun) and in teams of 2, one computer per team. The goal is to go from a *Wikipedia* page to another one, passing by a third one in the middle. When the middle page is accessed, the team swap the seaker.

More precisely:
- Player 1 begins,
- Player 1 starts on page A,
- When player 1 has reached page B, player 2 takes his place,
- Player 2 starts on page B,
- When player 2 has reached page C, the game ends.

# Usage
For playing, only use the command:
```sh
python3 play.py
```

For debugging, use the command:
```sh
python3 play.py -d
```
*Nota bene: `-d` flag only allow to show informations that are in a print like:*
```py
if debug: print("debug info")
```

# Setting up the game
You can choose the 3 *Wikipedia* pages by setting the 3 variables `start` (page A), `mid` (page B) and `end` (page C) in the python code to be the 3 urls.

*For example:* `start = "https://fr.wikipedia.org/wiki/Cookie_(informatique)"`
