#!/usr/bin/python
# cryptex.py
# print every combination of multi-tumbler lock data that forms an english word. Other languages might work.
# cracking puzzle from a video game where it has letter-based dials for finding a word.
# the game puzzle was similar to the Cryptex cylinder from the Da Vinci Code
# works for any number of dials in the combinataion
# uses enchant to confirm is letter combo is a english word. Works on Windows ATM.

from os import path
from dataclasses import dataclass
from argparse import ArgumentParser
import json
from datetime import datetime

@dataclass
class Dial:
    '''Cryptex has many dials. Each dial has many values but only one selection (index)'''
    position: int # index within Lock
    values: list[str]
    selection: int = 0
    # Dial(['one','two'], 0) thanks dataclass
    def set(self, index):
        self.selection = index
    def get(self, index=None):
        '''returns the symbol of the index or selected-index if None, use str() if you want the selection symbol'''
        if not index:
            index = self.selection
        return self.values[index]        
    def spin(self):
        new_index = self.selection + 1
        if new_index > len(self.values):
            raise StopIteration("out of bounds")
        self.selection = new_index
        return self.selection
    def __len__(self):
        return len(self.values)
    def __str__(self):
        return str(self.values[self.selection])
    def __iter__(self):
        self.selection = -1
        return self
    def __next__(self):
        # if self.selection < 0: #first pass
        #     self.selection = 0
        #     return self.selection
        
        old_index = self.selection
        new_index = old_index + 1
        if new_index >= len(self.values):
            raise StopIteration("out of bounds")
        self.selection = new_index
        return new_index

@dataclass
class Cryptex:
    '''name is based on Da Vinci Code puzzle box with similar mechanic
    holds spinner dials with letters'''
    dials: list[Dial] 
    def __init__(self, dial_dataset_dict):
        '''pass in dictionary of lock combinations'''
        self.dials = []
        for dial_values in dial_dataset_dict:
            dial_pos = len(self.dials)
            dial = Dial(dial_pos, dial_values)            
            self.dials.append(dial)
    def set(self, list_of_indexes):
        for dial_index, value in enumerate(list_of_indexes):
            dial = self.dials[dial_index]
            dial.set(value)
    def get(self, index):
        return self.dials[index]
    def __len__(self):
        return len(self.dials)
    def __iter__(self):
        self.iter_idx = 0
        return self
    def __next__(self):
        old_idx = self.iter_idx
        self.iter_idx += 1
        if self.iter_idx >= len(self.dials):
            raise StopIteration
        return self.dials[old_idx]
    
    def spin(self, dial_index):
        '''spins the dial and returns its new index, will be 0 if it wrapped'''
        try:
            self.dials[dial_index].inc()
        except StopIteration:
            self.dials[dial_index].set(0)
        return self.dials[dial_index].get()

    def __str__(self):
        return ''.join([str(dial) for dial in self.dials])

##############################################################################
#
# get the filename and load it
parser = ArgumentParser("Cryptex",usage="cryptex <datafile.json>", description="create a JSON with with a list of dial values. First list can be any length of tublers/dials. Each dial list within are just a list of string values possible for that tumber. ")
parser.add_argument("file", help="datafile.json") # positional arg
parser.add_argument("-o", "--output", help="results.json file with list of possible words. Appends with new results.", default="results.json", required=False)
parser.add_argument("-n", "--noenchant", help="dont try loading enchant and assume all words are valid", default=False, action='store_true')
args = parser.parse_args()
with open(args.file, 'r') as file:
    data = json.load(file)

if not args.noenchant: # made a way to disable enchant for debugging when it was not working/available
    import enchant # python -m pip install pychant
    enchanted_dictionary = enchant.Dict("en_US") # use check('word') - other languages should work

# verify all rows have the same number of columns
inconsistent_data = list(filter(lambda row: len(row) != len(data[0]), data))
assert len(inconsistent_data) == 0, "Error, word data is an inconsistent length " +str(len(inconsistent_data)) +" != 0"
    
cryptex_lock = Cryptex(data) # init combination lock data
words = [] # output of english words from dial combinations

def is_word(word):
    try:
        if enchanted_dictionary:
            return enchanted_dictionary.check(word)
        return True
    except:
        print("enchanted not working, all combinations returned")
        return True

def spin_all_selections(dial_to_spin):
    '''used to try all combinations of the last dial in the lock'''
    for value in dial_to_spin: # iter moves the selection so that printing cypher_lock has a different seting
        word = str(cryptex_lock)
        if is_word(word):
            words.append(word)        

def for_all_symbols_of(dial):
    '''iter over this dial and all dials to the right
    if this is the second to last dial, spin the last dial through its posibles printing each possible
    '''
    dial_idx = dial.position
    dial_cnt = len(cryptex_lock)
    for position in dial: #iterator moves selection pointer in object so that printing cypher_lock has a different seting 
        print(f"{len(words)} words found, checking {str(cryptex_lock)}\r",end='')
        if dial_idx < dial_cnt - 1:
            dial_to_right = cryptex_lock.get(dial_idx + 1)
            for_all_symbols_of(dial_to_right)
        else:
            spin_all_selections(dial)

def update_results(input_filename, output_filename, word_list):
    '''update the results.JSON with new results using input_filename is key to word_list'''
    if path.exists(output_filename):
        with open(output_filename, 'r') as file:
            try:
                content = json.load(file)
            except:
                content = {}
    else:
        content = {}
    content[input_filename] = word_list
    with open(output_filename, 'w') as file:        
        json.dump(content, file, indent=2)

def main():    
    print("started "+ str(datetime.now()))
    for_all_symbols_of(cryptex_lock.get(0)) # seed the recursive call with first tumbler
    print("\nfinshed "+ str(datetime.now()))
    update_results(args.file, args.output, words)
    print(f"{len(words)} words found from data in {args.file}. Results written to {args.output}")

if __name__=="__main__":
    main()

# below is the manual method, does not scale, for reference, replaced by dynamic method above
def manual_menthod_reference():
    first_letter_possibles = data[0]
    second_letter_possibles = data[1]
    third_letter_possibles = data[2]
    fourth_letter_possibles = data[3]
    fifth_letter_possibles = data[4]
    sixth_letter_possibles = data[5]
    #seventh_letter_possibles = data[6]

    progress100 = len(first_letter_possibles)+\
        len(second_letter_possibles)+\
        len(third_letter_possibles)+\
        len(fourth_letter_possibles)+\
        len(fifth_letter_possibles)+\
        len(sixth_letter_possibles)
        #len(seventh_letter_possibles)

    for index1, first in enumerate(first_letter_possibles, start=1):
        for index2, second in enumerate(second_letter_possibles, start=1):
            for index3, third in enumerate(third_letter_possibles, start=1):
                for index4, fourth in enumerate(fourth_letter_possibles, start=1):
                    for index5, fifth in enumerate(fifth_letter_possibles, start=1):
                        for index6, sixth in enumerate(sixth_letter_possibles, start=1):
                            #for index7, seventh in enumerate(seventh_letter_possibles, start=1): 
                            word = ''.join([first,second,third,fourth,fifth,sixth])# ,seventh])
                            progress = index1+index2+index3+index4+index5+index6 #+index7 # notworkingv 
                            if is_word(word):
                                words.append(word)
                                print(str(int(progress / progress100)) +'% '+ word)
                            else:
                                print('.', end='')
                                


                    
