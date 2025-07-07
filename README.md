# Cryptex
python3 combination lock solver for a finding words from possible letter values of each dial. 
Assumes that each dial has possible letter values listed in JSON data file. Tries every possible combination of dial values and uses PyEnchant dictionary to find possible words. Returns list of words in output file (CSV).

## Purpose
I was playing a puzzle game (Blue Prince) and it presents a series of 5-9 letter tumblers (dials) to create a word that matches a picture. \
Unable to solve this by inferring the correct word from the image (Room8 puzzle) I built a brute-force tool for seeing all the possible words that could be created using the letter-dials. \
Browsing through just a few hundred words allowed me to pick a few likely and solve the needed word. \
I bet you will find another use for it.

## Requirements
### Python3 https://www.python.org/downloads/
If you know; you know.

### PyEnchant https://pyenchant.github.io/pyenchant/
A python module for determining if a string of characters are an english word
I tested this on Windows and it should be possible to use on other platforms but I could not make it work. See the pyenchant URL above for instructions.
I tested this using US english. Other languages could work.

```
python -m venv venv
venv\scripts\activate.bat
pip install -r requirements.txt
```

## Use
it took 3min to solve a 6 dial puzzle, and 3 times this to solve 7 dials. 

create a JSON file with the letter combinations for each dial and then run the Python script.
I included two examples (from Blue Prince). Just a list of lists. Named word1.json and word2.json

```
venv\scripts\activate.bat
python combo_lock.py -h
python combo_lock.py word.json --output results.json
python combo_lock.py -f word2.json -o results.json
```

the output (-o) file will be appeneded (JSON) with new results indexed by the input file and have a list of possible words.

