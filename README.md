# Solver for: "Calculator:The Game"

Writen in Python 2/3
Solves all the problems until level 199 which to the moment I write this is the last level

# Input
Input is given from the command line:

```bash
./solver steps goal start [buttons ...]
```

The list buttons to use is given the exact same way they are written in the interface.

Tip 1: Every button that contains '>' or '<' has to be given in quotes because they are special bash characters in bash

Tip 2: For the last levels you tell the programm to use memory with the "MEM" command and to use portals with "p03" where 0 and 3 are the character that the portal is on from right to left

# Bugs
There is a bug with memory where it doesn't report back where it used the button correctly. I am not sure if that part is bulletproof but it may have a problem 1 or 2 puzzles at most

# Info 
The code is far from optimal but the app restrains you to about 1-8 steps and 1-5 buttons at most thus making it enough for this app. Every puzzle run for less than a second.

