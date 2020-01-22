import re, random


templates = [
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
            'You seem to think a lot about your INSERT.',
            'Why is your INSERT so important to you?'
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
            respond = random.choice(responseOptions)
            respond = respond.replace("INSERT", phrase.group(numGroups(phrase)))
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




