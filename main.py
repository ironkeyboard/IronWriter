'''
IronWriter

Author: Ironkeyboard | fishingfights on repl.it 
'''
#setup all libraries

#terminal colors
from colorama import Fore,init
init()

#os
from os import system

#re
import re

#natural language processing library
import nltk
from nltk.corpus import wordnet

#time lib
import time as t

print(Fore.RED + "[console] preparing all libraries")
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('tagsets')
nltk.download('wordnet')
print(Fore.RED + "[console] done.")

print(Fore.GREEN)

#tokenize a text
tag = lambda x: nltk.pos_tag(nltk.word_tokenize(x))

def wordPos(word, context=None):
    """
    Returns the part of speech of a word in its given context if possible
    """
    if context == None:
        context = nltk.pos_tag(nltk.word_tokenize(word))
    try: return next(iter(y for x,y in context if x == word))
    except: return False

#flatten list
flatten = lambda t: [item for sublist in t for item in sublist]

def strOfList(lst):
    '''turn a list into a string'''
    space = " "
    return(space.join(lst))

def synonyms(word, context):
    '''
    returns a list of synonyms for a word with its given context
    '''
    replaceContext = lambda x: strOfList([x for x,y in context]).replace(word, x)

    synonyms = wordnet.synsets(word)
    pos = wordPos(word, context)
    synlist = flatten([word.lemma_names() for word in synonyms])
    perfectSyns = [i for i in synlist if wordPos(i, tag(replaceContext(i))) == pos and i != word]

    if perfectSyns:
        return list(dict.fromkeys(perfectSyns))
    else:
        return list(dict.fromkeys([i for i in synlist if i != word]))

#clear screen
clear = lambda: system('clear')

def printNested(nestedText):
    for x,i in enumerate(nestedText):
        if type(i) != list:
            print(i, end = " ")
        else:
            print(f"[{i[0]}]", end = " ")
    print("\n-------------------------------------------")

def process(nestedText):
    printNested(nestedText)
    for x,i in enumerate(nestedText):
        if type(i) == list:
            print()
            print(f"options for word #{x+1}: {list(enumerate(i, 1))}")
            print()
            cycle = int(input(f"which word do you want from the list (1-{len(i)}): "))
            nestedText[x] = i[cycle-1]
        clear()
        printNested(nestedText)
    return re.sub(r'\s([?.!"](?:\s|$))', r'\1', " ".join(nestedText).capitalize().replace("_", " "))

# config set up
print("Welcome To IronWriter - The Anti-Anti-Plagiarism Tool 😉")
print("Developed with ❤  by ironkey [github: ironkeyboard]")
print()
print("Beta testers:")
print("myunging")
print("ironkeyboard")

t.sleep(7)

clear()
print("The sensitivity setting adjusts the detection rate on parts of speech that the program detects as replaceable.\nPlease note that sensitivities other than 1 are highly experimental")

sens = int(input("Please select your sensitivity setting (1/2/3) [1 is recommended for highly readable text]: "))

#https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
if sens == 2:
    replaceable = ["VB", "RB", "RBR", "JJ", "JJR", "JJS", "VBD", "VBG", "VBN"]
elif sens == 3:
    replaceable = ["VB", "RB", "RBR", "JJ", "JJR", "JJS", "VBD", "VBG", "VBN", "VBP", "VBZ"]
else: replaceable = ["VB", "RB", "RBR", "JJ", "JJR", "JJS"]

clear()

while True:
    text = input("text: ")

    tagged = tag(text)
    
    clear()
    
    result = process([[x] + synonyms(x, tagged) if y in replaceable else x for x,y in tagged])
    
    clear()
    
    print(result)

    print()

    input("press enter to continue: ")

    clear()