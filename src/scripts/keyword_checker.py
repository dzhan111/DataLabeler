
from typing import List

words = 'Snow, Bench, Person, Scarf, Dog, Leash, Buildings, Trees, Pigeons, Park'.split(', ')
words = [i.lower() for i in words]

transcript = ""
with open('src/scripts/script.txt', 'r') as file:
    transcript = " ".join([i.strip() for i in file.readlines()])

script_words: List[str] = transcript.split(' ')
script_words = [i.strip(' .,!?').lower() for i in script_words]
ct = 0
for word in words:
    if word in script_words:
        print(word)
        ct += 1
print(ct)
print(len(script_words))