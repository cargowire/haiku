import re
import random
import sys

def read_file_words(file):
    words = []

    with open(file,'r') as f:
        for line in f:
            for word in line.split():
               words.append(word.lower())

    return words

def process_dictionary(words, keyWordSize=1):
    dictionary = {}

    for i in range(len(words)):
        if i < len(words) - keyWordSize and words[i].isalpha() and words[i + keyWordSize].isalpha():
            workingstring = words[i]

            for j in range(1, keyWordSize):
                workingstring += " " + words[i + j]

            if workingstring not in dictionary:
                dictionary[workingstring] = [re.sub(r'\W+', '', words[i + keyWordSize])]
            else:
                dictionary[workingstring].append(re.sub(r'\W+', '', words[i + keyWordSize]))
    
    return dictionary

def count_syllables(word):
    vowels = ['a', 'e', 'i', 'o', 'u']

    on_vowel = False
    in_diphthong = False
    minsyl = 0
    maxsyl = 0
    lastchar = None

    word = word.lower()
    for c in word:
        is_vowel = c in vowels

        if on_vowel == None:
            on_vowel = is_vowel

        # y is a special case
        if c == 'y':
            is_vowel = not on_vowel

        if is_vowel:
            if not on_vowel:
                # We weren't on a vowel before.
                # Seeing a new vowel bumps the syllable count.
                minsyl += 1
                maxsyl += 1
            elif on_vowel and not in_diphthong and c != lastchar:
                # We were already in a vowel.
                # Don't increment anything except the max count,
                # and only do that once per diphthong.
                in_diphthong = True
                maxsyl += 1

        on_vowel = is_vowel
        lastchar = c

    # Some special cases:
    if word[-1] == 'e':
        minsyl -= 1
    # if it ended with a consonant followed by y, count that as a syllable.
    if word[-1] == 'y' and not on_vowel:
        maxsyl += 1

    return maxsyl

words = process_dictionary(read_file_words("book.txt"), 1)
syllables = {word: count_syllables(word) for word in words.keys()}

# print syllables

one_syllable_words = [k for k,v in syllables.items() if v == 1]

# print one_syllable_words


def generate_line(start_word, number_of_syllables):
    start_syllables = count_syllables(start_word)
    next_word = start_word
    remaining_number_of_syllables = number_of_syllables - start_syllables
    line = start_word
    
    while remaining_number_of_syllables > 0:
    
        possible_next_word = filter(lambda w : syllables.get(w, 9999) <= remaining_number_of_syllables and syllables.get(w, 9999) != count_syllables(next_word) and not w == next_word, words.get(next_word, []))
        
        if len(possible_next_word) == 0:
            possible_next_word = filter(lambda w : syllables.get(w, 9999) <= remaining_number_of_syllables and not w == next_word, words.get(next_word, []))
        
        # print next_word, possible_next_word
        if len(possible_next_word) == 0:
            next_word = random.choice(one_syllable_words)
        else:
            next_word = random.choice(possible_next_word)
        line += " " + next_word
        remaining_number_of_syllables -= syllables[next_word]
        
    return line

def generate_haiku(start_word):
    line1 = generate_line(start_word, 5)
    line2 = generate_line(random.choice(words.keys()), 7)
    line3 = generate_line(random.choice(words.keys()), 5)
    return "%s\n%s\n%s" % (line1, line2, line3)

start_word = raw_input("Start word: ")

if start_word == "":
    start_word = random.choice(words.keys())

line = generate_haiku(start_word)
print line