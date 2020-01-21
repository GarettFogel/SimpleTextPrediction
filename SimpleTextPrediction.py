import sys
import glob
import errno
import os
import string
from collections import Counter 

fName = input("Name of directory containing training data?: ")
path = os.path.join(fName,'*.txt')  
files = glob.glob(path)
previousWord = ""
firstWords = dict()
print("Processing training data...")
for name in files:
    try:
        with open(name) as f:
            for line in f:
                for word in line.split():
                    word = word.lower() #case does not matter to me
                    word = word.translate(str.maketrans('', '', string.punctuation)) #This line removes all punctuation
                    if previousWord in firstWords: #previous word has been seen
                        if word in firstWords[previousWord]: #previous word has been seen with the current word after it.
                            firstWords[previousWord][word] += 1
                        else: #previous word has been seen, but not with this word following it yet
                            firstWords[previousWord][word] = 1
                    else: #previous word has not yet been seen
                        firstWords[previousWord] = dict()
                        firstWords[previousWord][word] = 1
                    previousWord = word
            previousWord = "" #reset previous word after parsing entire file
    except IOError as exc:
        if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
            raise # Propagate other kinds of IOError.
print("Training complete.")
flag = True
while flag:
    checkWord = input("Enter a word to predict the next word: ").lower()
    if checkWord in firstWords:
        k = Counter(firstWords[checkWord])
        # Finding 3 highest values 
        top3predictions = k.most_common(3)
        print("Top 3 most likely words to appear next: ")
        for i in top3predictions:
            print(i[0]),
    else:
        print("This word did not appear in the training data")
    leave = False
    while not leave:
        choice = input("Would you like to enter another word? (y/n): ").lower().strip()
        if choice == 'y':
            leave = True
        elif choice == 'n':
            flag = False
            leave = True
        else:
            print("Invalid choice, please select y or n.")
print("Goodbye!")
