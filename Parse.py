'''
def parse(userInput):
    keyword = use RegEx to ID a keyword #this needs to be robust as per instructions
    return keyword
'''
import re


def findSentenceTemplate(sentence):
    if re.search(r'\bI\s(.*?)$', sentence) is not None:
        return IPhrase(sentence)
    return "unknown"


#TODO: multiple I statments "I think I am going crazy"
#TODO: chamge up the pass phrased. randomly: "I save money" -> "saving money" or "your savings".
#Note: the "your savings" format wont work for verb "have", or "am". "tell me more about your havings/beings" is no good
def IPhrase(sentence):
    token = re.search(r'\b[i|I]\s(.*?)$', sentence)
    phrase = token.group(1)
    phrase = verbPhraseToGerundPhrase(phrase)
    return phrase


def verbPhraseToGerundPhrase(phrase):#where phrase is the phrase with old verb
    verb = re.search(r'\b\w*\b', phrase) #verb.group(0) is the verb
    phrase = re.search(r'\b\w*\b\s(.*?)$',phrase) #phrase without verb
    verb = verb.group(0) #cuts verb to simple string
    if phrase is not None:
        phrase = phrase.group(1) #cuts phrase down to a simple string
    else:
        phrase = ""
    gerund = verbToGerund(verb)
    phrase = gerund + ' ' + phrase
    return phrase


#TODO fails on words like "hit", outputs "hiting" not "hitting"
def verbToGerund(verb):
    #if verb end in E:
    if re.search(r'\w*e$', verb) is not None:
        verb = re.search(r'(\w*)e$', verb)
        verb = verb.group(1)
        gerund = verb + 'ing'
    #if verb is am:
    elif verb == 'am':
        gerund = 'being'
    #if verb does not end in e:
    else:
        gerund = verb + 'ing'
    return gerund


#Strips trailing punctuation, including multiple in case of elipses or '!!!' emphasis
def stripTrailingPunctuation(sentence):
    if re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence) is not None:
        stripped = re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence)
        return stripped.group(1)
    return sentence


#TODO maybe allow "my name is Rob"
#TODO allow "I am Gabe"
#finds person's name, where given alone or in a sentence.
def extractName(name):
    if re.search(r'\b[i|I][s|S]\b', name) is not None: #finds incetances of the word "is"
        name = re.search(r'\b[i|I][s|S]\b\s(.*?)$', name) #assigns name to string following is ex: my name is Rob -> Rob
        return name.group(1)
    return name #return standalone name