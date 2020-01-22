'''
def parse(userInput):
    keyword = use RegEx to ID a keyword #this needs to be robust as per instructions
    return keyword
'''
import re


#TODO: check multiple templates, go with whatever is last. ex: "I remember when my dad died" -> "your dad died", not "remembering when my dad died"
#looking for personal pronouns seems key.
def findSentenceTemplate(sentence):
    if re.search(r'(\bI\s)(?!.*\1)(.*?)$', sentence) is not None:
        #i-length = 
    #if i-phrase shoerter than my phrase
        return IPhrase(sentence)
    #else: ie if my-prase is longer
        #return myPrase(sentence)
    return "unknown"


#TODO: multiple I statments "I think I am going crazy"
#TODO: chamge up the pass phrased. randomly: "I save money" -> "saving money" or "your savings".
#Note: the "your savings" format wont work for verb "have", or "am". "tell me more about your havings/beings" is no good
#TODO: fuck, adverbs kill this system. "I really hate myself" will break it. maybe check if word after "I" ends in "ly", if so it is a adverb, check next?
    #only 55 of these, maybe greenlight the common ones and fuck the less common ones
#TODO: "I do not like eggs" breaks. "how do you feel about doing not like eggs" is BS
#TODO: "I can verb" and "I can not verb" verb break it. ie "I can not believe Jake's behavior"
def IPhrase(sentence):
    token = re.search(r'(\bI\s)(?!.*\1)(.*?)$', sentence)
    phrase = token.group(numGroups(token))
    phrase = verbPhraseToGerundPhrase(phrase)
    return phrase


#TODO fails on "verb gerund", ex "I am lying to him" -> "being lying to him". 
    #recognize gerunds in phrase, go with them instead. ex -> "lying to him" | simply, "lying"
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


#finds person's name, where given alone or in a sentence.
def extractName(name):
    if re.search(r'\b[i|I][s|S]\b', name) is not None: #finds incetances of the word "is"
        name = re.search(r'\b[i|I][s|S]\b\s(.*?)$', name) #assigns name to string following is ex: my name is Rob -> Rob
        return name.group(1)
    elif re.search(r'\bam\b', name) is not None: #finds incetances of the word "am"
        name = re.search(r'\bam\b\s(.*?)$', name) #assigns name to string following am ex: I am Rob -> Rob
        return name.group(1)
    return name #return standalone name


#returns num of groups a token has bc they confuse me 
def numGroups(token):
    return len(token.groups())