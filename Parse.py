'''
def parse(userInput):
    keyword = use RegEx to ID a keyword #this needs to be robust as per instructions
    return keyword
'''
import re

def parse(userInput):
    tokens = re.split(r'\s+', userInput)

    #finds an I and sends clause after it as keyword
    #need to be done:
    #if multiple I's (I think I am crazy), sends everything after the initial I. probly use that clause, but switch 'I's to 'you's -> 'tell me more about you crazy' not perfect idk
    #doesnt recognize I'm
    #verb after I needs to be handled. sometimes it would be okay to bring (I think I am crazy -> Why do you think you are crazy)
    #   but often wouldnt make sense (I am sad !-> tell me more about am sad), actually, i think "am" is the only problomatic verb.

    Itoken = re.search(r'I\s(.*?)$', userInput)
    if Itoken is not None:
        #print(Itoken.group(0)) #TESTING group(0) whole sentence
        #print(Itoken.group(1)) #everything after the I
        #print("^was taken out")
        return Itoken.group(1)

    return tokens[0] #only for testing


def findSentenceTemplate(sentence):
    if re.search(r'\bI\s(.*?)$', sentence) is not None:
        return IPhrase(sentence)
    elif re.search(r'\b[i\'m|I\'m|Im|im]\s(.*?)$', sentence) is not None:
        return ImPhrase(sentence)
    return "unknown"


#TODO: verb after I.
    #am -> being
    #ends in e? -> remove e, add ing. ex: strive -> striving
    #else add ing
    #
    #recognize I'm
def IPhrase(sentence):
    token = re.search(r'\b[i|I]\s(.*?)$', sentence)
    phrase = token.group(1)
    verb = re.search(r'\b\w*\b',token.group(1)) #verb.group(0) is the verb
    phrase = re.search(r'\b\w*\b\s(.*?)$',token.group(1)) #phrase without verb
    verb = verb.group(0) #cuts verb to simple string
    #fails on words like "hit", outputs "hiting" not "hitting"
    if phrase is not None:
        phrase = phrase.group(1) #cuts phrase down to a simple string
    else:
        phrase = ""
    #if verb end in E:
    if re.search(r'\w*e$', verb) is not None:
        verb = re.search(r'(\w*)e$', verb)
        verb = verb.group(1)
        verb = verb + 'ing'
        phrase = verb + ' ' + phrase
    #if verb is am:
    elif verb == 'am':
        phrase = 'being ' + phrase
    #if verb is neither:
    else:
        verb = verb + 'ing'
        phrase = verb + ' ' + phrase
    return phrase


def ImPhrase(sentence):
    token = re.search(r'\b[i\'m|I\'m|Im|im]\s(.*?)$', sentence)
    return "being " + token.group(1)


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