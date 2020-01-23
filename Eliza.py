#Gabe Chambers - V00774588
#cmsc 416 -- NLP
#Project 1: Eliza
#summary: immitates a therapist session. takes your input to talk back to you.
import re, random


#a data structure to store possible regex expressions that a response could fit into.
#if a phrase matches a regex, a random corresponding list of possible responses is chosen.
#list is searched through top to bottom, giving regex higher in list more weight over lower regex.
#ex.: sentence with "I was" is checked before sentences with simply "I"
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
    #regex puts all words AFTER the LAST INSTANCE of "i was" into the final group of the token
    [r'(\bi\swas\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you were INSERT.',
            'Why do you think you were INSERT?'
        ]
    ],
    #Yes, no, and I am. 
    # naturally come up a lot and the one word template below is very awkward with these.
    #matches to lines which are solely "yes", "no", or "i am"
    [r'^(no|yes|i\sam)$',
        [
            'You seem very sure.',
            'Why is it so clear to you?',
            'Why was that such a fast conclusion to come to?',
            'Are you happy with that? Why or why not?'
        ]
    ],
    #I
    #regex uses negative lookahead (second group) to identify the LAST clause of a sentence that begins with an "I"
    #everything after the last "I" is used (in the third group) to generate responses
    [r'(\bi\s)(?!.*\1)(.*?)$',
        #responses:
        [
            'Tell me more about how you INSERT.',
            'Why do you think you INSERT?'
        ]
    ],
    #my
    #regex searches for any instance of "my" and creates a group of all following words
    [r'.*?\bmy\s(.*\b)',
        #responses:
        [
            'Why do you think your INSERT?',
            'Why is it so important to you that your INSERT?',
            'How does it make you feel that your INSERT?'
        ]
    ],
    #she
    #for she, they, and he (the following regex), all basically the same. 
    #looks for instance of the pronoun and captures following words into a group
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
    #one or two words
    #one or two word answers go here. 
    # even if they dont have certain keywords, the general catch-all responses felt akward with this category.
    # regex looks is the whole line contains either 0 or exactly 1 space. if so, puts the whole thing into group.
    [r'(^[^\s]+\s[^\s]*$|^[^\s]+$)',
        [
            "What is so important about INSERT to you?",
            "Tell me more about INSERT.",
            "Why does INSERT make you feel so much?",
            "What is it about INSERT that makes you feel so much?"
        ]
    ],
    #you 
    #for when the person uses no other keywords, so is most likely talking about Eliza.
    #regex puts into group everything after the "you"
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
    #for when the input does not match any of the above templates
    [r'.*?',
        [
            "I don't quite understand, could you rephrase that?",
            "I don't follow, could you explain a little differently?",
            "Lets talk about you.",
            "That is interesting, but lets keep the topic on you"
        ]
    ]
]#end list



#dictionary (python hash table) of personal pronouns and irregular verbs
# taken from input to switch from either [first to second person] or [second to first person]
#used to flip captured phrases from [user input] into [Eliza output]
#ex input: "I want to run from MY past."
#ex output with flipped pronouns: "Why do you want to run from YOUR past?"
flip = {
    #first person -> second person
    'am' : 'are',
    'my' : 'your',
    'i' : 'you',
    'me' : 'you',
    #second person -> first person:
    'you' : 'me',#this one is annoying. 'you' can go to 'me' or 'I'. decided 'me' was more common.
    'are' : 'am',
    'your' : 'my'
}


#function is run on user input to strip all punctuation from end of input making it easier to regex
#strips all trailing punctuation to allow for elipses (...) or other multi-punctuation emphasis (ex: !!!!)
#leaves punctuation in middle as it can be part of name etc
def stripPunctuation(sentence):
    #regex logic: (...) group allows for entire sentence.
    #[^...]+$ says: at end of line, if there are one or more symbol characters, do not include in the group
    if re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence) is not None:
        stripped = re.search(r'(.*?)[^a-zA-Z\d\s:]+$', sentence)
        return stripped.group(1)
    return sentence



#simple function uses native python .lower() to lowercase entire string for easier regex.
def toLower(sentence):
    return sentence.lower()


#function formats sentence for easier regex. 
# uses two functions above to strip punctuation and put to lowercase
def formatSentence(sentence):
    return stripPunctuation(toLower(str(sentence)))



#finds person's name, where given alone or in a sentence.
#only used at beginning of conversation.
#takes in the input given for the name phrase and outputs just the name.
def extractName(name):
    name = stripPunctuation(name)
    if re.search(r'\b[i|I][s|S]\b', name) is not None: #finds incetances of the word "is"
        name = re.search(r'\b[i|I][s|S]\b\s(.*?)$', name) #assigns name to string following "is" ex: my name is Rob -> Rob
        return name.group(1)
    elif re.search(r'\bam\b', name) is not None: #finds incetances of the word "am"
        name = re.search(r'\bam\b\s(.*?)$', name) #assigns name to string following am ex: I am Rob -> Rob
        return name.group(1)
    return name #return standalone name



#returns num of groups a token has
def numGroups(token):
    return len(token.groups())


#Generating the response based on user input is done here
#takes in input
#finds the regex in "templates" data structure that matches it.
#all regex set up so that the last group is the one which should be pasted into the responses.
#takes that group and checks if any of the words in the "flip" dictionary should be swapped out
#pastes the refined user phrase into instance of "INSERT" in the template sentence
#returns the final response
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



#function to ask user name. only used once at beginning of conversation
def askName():
    print("Hi, I am Eliza, a psychotherapist. What is your name?")


#salutations to user and prompts for first response. only happens at beginning of convo
def initiateConversation(name):
    print("Nice to meet you " + str(name) + ". What can I help you with today?")



#initial set up
#asking and getting name happen here
askName()
name = input()
name = extractName(name)
initiateConversation(name)


#conversation loop. 
#waits for user input, generates a response, and prints it to the console
#listens for keyword "stop" to break loop
while True:
    userInput = input()
    #to exit loop:
    if userInput == ("stop" or "Stop"): break
    sentence = formatSentence(userInput)
    print(respond(sentence))




