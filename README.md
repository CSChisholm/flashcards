# Flashcards

A PyQt5 app for making flashcards and running testing sessions with flashcards.

# Usage

First activate virtual environment (see [Development](#development)).

From command line: `python3 flashcards.py`

The user will be presented with a blank interface, to get started build sets by clicking `Build Set` or open an exist set by clicking `Open Set` or open all sets in a directory by clicking `Open Directory`.

The game mode can be set to use either side of the card as a prompt (the other side is the answer). Or, the side of each card can be chosen at random.

# Development

Clone repository:
`git clone https://github.com/CSChisholm/flashcards`

Set up virtual environment:

## Linux + macOS
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
```

## Windows
```
python3 -m venv venv
venv\Scripts\activate
python3 -m pip install -r requirements.txt
```

# License

Copyright © 2026 Craig S. Chisholm

Version - 1.0.1

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="https://www.gnu.org/licenses/">https://www.gnu.org/licenses</a>.
