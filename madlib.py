import re, sys, textwrap

import requests
import random
import collections


def get_random_graf():
    url = "https://www.gutenberg.org/files/514/514.txt" # Little Women

    text = requests.get(url).text
    text = text.encode("iso8859-1").decode("utf-8")
    text = text.replace("\r\n", "\n")
    text = text.partition("End of the Project Gutenberg EBook")[0]
    grafs = text.split("\n\n")

    wordlens = collections.Counter()
    good = []

    for graf in grafs:
        words = graf.split()
        wordlen = len(words)
        wordlens[wordlen] += 1
        if 25 <= wordlen <= 40:
            good.append(" ".join(words))

    graf = random.choice(good)
    print(graf)
    return graf

def partofspeech(word):
    url = f"https://api.datamuse.com/words?sp={word}&md=p&max=1"
    data = requests.get(url).json()
    if data:
        tags = data[0].get("tags", [])
        if len(tags) == 1:
            tagsdefs = {"n": "noun", 'v': 'verb', 'adj': "adjective", "adv": 'adverb'}
            return tagsdefs.get(tags[0], "?")
    return "?"

def make_madlib(text):
    result = ""
    for word in text.split():
        if random.random() < .33:
            part = partofspeech(word)
            if part != "?":
                result += "[" + part + "] "
            else:
                result += word + " "
        else:
            result += word + " "
    return result

def main():
    arg = sys.argv[1]
    if arg == "random":
        madlib = make_madlib(get_random_graf())
    else:
        madlib = open(sys.argv[1])
        madlib = madlib.read()
        madlib = madlib.replace("\n", " ")

    result = ""
    for chunk in re.split(r"(\[\w+\])", madlib):
        if chunk.startswith("["):
            next = input(f"Give me a {chunk}: ")
        else:
            next = chunk
        result = result + next

    print("\n".join(textwrap.wrap(result)))

main()
