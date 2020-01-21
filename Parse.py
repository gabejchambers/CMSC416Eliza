'''
def parse(userInput):
    keyword = use RegEx to ID a keyword #this needs to be robust as per instructions
    return keyword
'''
import re

def parse(userInput):
    sentance = re.split(r'\s+', userInput)
    return sentance[0]
