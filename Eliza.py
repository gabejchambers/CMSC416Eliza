'''
Eliza class outline:

functions: response(userInput), parse(userInput), respond(keyword)

def response(userInput)
    keyword = parse(userInput) #where keyword is a string
    return respond(keyword) #returns to print statment in main

def parse(userInput):
    keyword = use RegEx to ID a keyword #this needs to be robust as per instructions
    return keyword

def respond(keyword):
    #use switch or if statment to pick a response template
    #insert keyword into template
    #construct edgecase cases like gibberish, complicated user input, or first couple messages
    return chosen response, with keyword inserted

ezpz B)
'''

def response(userInput):
    keyword = parse(userInput) #where keyword is a string
    return respond(keyword) #returns to print statment in main


def parse(userInput):
    return 0


def respond(keyword):
    pass