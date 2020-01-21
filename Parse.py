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

'''
def findSentenceTemplate(sentence):
    if re.search(r'I\s(.*?)$', sentence) is not None:
'''

#Strips trailing punctuation, including multiple in case of elipses or '!!!' emphasis
def stripTrailingPunctuation(sentence):
    if re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence) is not None:
        stripped = re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence)
        return stripped.group(1)
    return sentence


#finds person's name, where given alone or in a sentence.
def extractName(name):
    if re.search(r'\b[i|I][s|S]\b', name) is not None: #finds incetances of the word "is"
        name = re.search(r'\b[i|I][s|S]\b\s(.*?)$', name) #assigns name to string following is ex: my name is Rob -> Rob
        return name.group(1)
    return name #return standalone name