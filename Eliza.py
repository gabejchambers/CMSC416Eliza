import re, random


templates = [
    #Family members
        #regex looks to match any instance of dad, mom, etc. family memober
        [r'.*?(\bdad\b|\bmom\b|\bsister\b|\bbrother\b|\bfather\b|\bmother\b|\baunt\b|\buncle\b|\bgrandma\b|\bgrandpa\b|\bgrandmother\b|\bgrandfather\b).*?',
        #responses:
        [
            'Tell me more about your family.',
            'What are some of your favorite memories about your family?',
            'Are you close with your family?'
        ]
    ],
    #I was
    [r'(\bi\swas\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you were INSERT.',
            'Why do you think you were INSERT?'
        ]
    ],
    #Yes, no, and I am. naturally come up a lot and the one word template below is very awkward with these.
    [r'^(no|yes|i\sam)$',
        [
            'You seem very sure.',
            'Why is it so clear to you?',
            'Why was that such a fast conclusion to come to?',
            'Are you happy with that? Why or why not?'
        ]
    ],
    #I
    [r'(\bi\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you INSERT.',
            'Why do you think you INSERT?'
        ]
    ],
    #my
    [r'.*?\bmy\s(.*\b)',
        #responses:
        [
            'Why do you think your INSERT?',
            'Why is it so important to you that your INSERT?',
            'How does it make you feel that your INSERT?'
        ]
    ],
    #she
    [r'.*?\bshe\s(.*\b)',
        #responses:
        [
            'How does it make you feel that she INSERT?',
            'Why do you think she INSERT?',
            'Can you control how she INSERT?'
        ]
    ],
    #he
    [r'.*?\bhe\s(.*\b)',
        #responses:
        [
            'How does it make you feel that he INSERT?',
            'Why do you think he INSERT?',
            'Can you control how he INSERT?'
        ]
    ],
    #they
    [r'.*?\bthey\s(.*\b)',
        #responses:
        [
            'How does it make you feel that they INSERT?',
            'Why do you think they INSERT?',
            'Can you control how they INSERT?'
        ]
    ],
    #one or two words (more acurately 1 or 0 spaces)
    [r'(^[^\s]+\s[^\s]*$|^[^\s]+$)',
        [
            "What is so important about INSERT to you?",
            "Tell me more about INSERT.",
            "Why does INSERT make you feel so much?",
            "What is it about INSERT that makes you feel so much?"
        ]
    ],
    #you NOTE: keep toward bottom
    [r'.*?\byou\s(.*\b)',
        #responses:
        [
            'We aren\'t here to talk about me.',
            'I am not interested in talking about myself.',
            'Why do you feel the need to talk about me?',
            'Why don\'t we stay focused on you.'
        ]
    ],
    #unkown, catchall, etc
    [r'.*?',
        [
            "I don't quite understand, could you rephrase that?",
            "I don't follow, could you explain a little differently?",
            "Lets talk about you.",
            "That is interesting, but lets keep the topic on you"
        ]
    ]
]#end list


#dictionary of personal pronouns and first person common verbs to flip to second person in response:
flip = {
    #first person -> second person
    'am' : 'are',
    'my' : 'your',
    'i' : 'you',
    'me' : 'you',
    #second person -> first person:
    'you' : 'me',#this one is annoying. 'you' can go to 'me' or 'I'
    'are' : 'am',
    'your' : 'my'
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
            phrase = phrase.group((numGroups(phrase)))#problem line for length 1 strings
            respond = random.choice(responseOptions)
            tokens = re.split(r'\s+', phrase)
            for index, token in enumerate(tokens):
                for firstPerson, secondPerson in flip.items():
                    if token == firstPerson:
                        tokens[index] = secondPerson
            phrase = ' '.join(tokens)
            respond = respond.replace("INSERT", phrase)
            return respond



def askName(): #need parse this in case they say ex 'my name is Rob' isntead of just 'Rob'
    print("Hi, I am Eliza, a psychotherapist. What is your name?")



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




