'''
starting idea:
2 classes

main class outline:
while true:
    print a respose from eliza to user based on input string 
    #first response or two wont be based on input obv
    save a string equal to user input to feed into eliza on next cycle
    #loop waits at line above until user inputs
    #maybe only read in first 400 chars or something so they dont do weird stuff with your memory
    if user inputs a safe word
        break



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
import Parse 
import Respond 

#initial set up
Respond.askName()
name = input()
name = Parse.stripTrailingPunctuation(name)
name = Parse.extractName(name)
Respond.initiateConversation(name)

#conversation loop
while True:   
    userInput = input()
    #to exit loop:
    if userInput == ("stop" or "Stop"): break
    sentence = Parse.stripTrailingPunctuation(userInput)
    keyphrase = Parse.findSentenceTemplate(sentence) #find key phrase in user input
    Respond.respond(keyphrase) #generate response using keyphrase
