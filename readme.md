# ConnectX

A small application to play connect 4 from the command line

# Command line arguments

* First posiional argument: number of columns in the game
* --mode: type of game, where
** hxh: human vs human (default)
** hxr: human vs bot
** rxh: bot vs human
** rxr: bot vs bot
* --repeat: number of games to play (default: 1)

# Example:

```python connect4.py 7 --mode rxr --repeat 10```
