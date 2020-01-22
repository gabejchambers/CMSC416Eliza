import re, random


templates = [
    #I
    [r'.*?\b[I|i]\s(.*)',
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
            'You seem to think a lot about INSERT.',
            'Why is INSERT so important to you?'
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

def respond(sentence):
    for regex, responseOptions in templates:
        phrase = re.search(regex, sentence)
        if phrase is not None:
            respond = random.choice(responseOptions)
            respond = respond.replace("INSERT", phrase.group(1))
            return respond





print('What can I help you with today?')
while True:
    userInput = input()
    #to exit loop:
    if userInput == ("stop" or "Stop"): break
    sentence = formatSentence(userInput)
    print(respond(sentence))




