import re, random


templates = [
    #I was
    [r'(\bi\swas\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you were INSERT.',
            'Why do you think you were INSERT?'
        ]
    ],#end I 
    #I
    [r'(\bi\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you INSERT.',
            'Why do you think you INSERT?'
        ]
    ],#end I 
    #my
    [r'.*?\b[M|m]y\s(.*\b)',
        #responses:
        [
            'Why do you think your INSERT?',
            'Why is it so important to you that your INSERT?',
            'How does it make you feel that your INSERT?'
        ]
    ],#end my
    #one or two words (more acurately 1 or 0 spaces)
    [r'((^[^\s]+$)|(^[^\s]+\s[^\s]*$))',
        [
            "What is so important about INSERT to you?",
            "Tell me more about INSERT.",
            "Why does INSERT make you feel so much?",
            "What is it about INSERT that makes you feel so much?"
        ]
    ],#end one or two words
    #unkown, catchall, etc
    [r'.*?',
        [
            "I don't quite understand, could you rephrase that?",
            "I don't follow, could you explain a little more simply?"
        ]
    ]#end catch all
]#end list


#dictionary of personal pronouns and first person common verbs to flip to second person in response:
#TODO: must check split() tokens against this, right now if these are in the middle of a word it fucks it
    #i.e. parameter -> parareeter SMH
flip = {
    'am' : 'are',
    'my' : 'your',
    'i' : 'you',
    'me' : 'you'
}


def stripPunctuation(sentence):
    if re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence) is not None:
        stripped = re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence)
        return stripped.group(1)
    return sentence



def toLower(sentence):
    return sentence.lower()



def formatSentence(sentence):
    return stripPunctuation(toLower(str(sentence)))



#finds person's name, where given alone or in a sentence.
def extractName(name):
    name = stripPunctuation(name)
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



def respond(sentence):
    for regex, responseOptions in templates:
        phrase = re.search(regex, sentence)
        if phrase is not None:
            phrase = phrase.group(numGroups(phrase))
            respond = random.choice(responseOptions)
            #TODO: split() phrase into tokens and check each token against the flip table,
            #  this way both leading 'i', ending, and middle will be clecked and you can get rid of the whitespaces in the flip table
            for firstPerson, secondPerson in flip.items():
                phrase = phrase.replace(firstPerson, secondPerson)
            respond = respond.replace("INSERT", phrase)
            return respond



def askName(): #need parse this in case they say ex 'my name is Rob' isntead of just 'Rob'
    print("Hi, I am Eliza, a psychotherapist. What is yor name?")



def initiateConversation(name):
    print("Nice to meet you " + str(name) + ". What can I help you with today?")



#initial set up
askName()
name = input()
name = extractName(name)
initiateConversation(name)

while True:
    userInput = input()
    #to exit loop:
    if userInput == ("stop" or "Stop"): break
    sentence = formatSentence(userInput)
    print(respond(sentence))




