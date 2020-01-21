'''
def respond(keyword):
    #use switch or if statment to pick a response template
    #insert keyword into template
    #construct edgecase cases like gibberish, complicated user input, or first couple messages
    return chosen response, with keyword inserted

'''

def askName(): #need parse this in case they say ex 'my name is Rob' isntead of just 'Rob'
    print("Hi, I am Eliza, a psychotherapist. What is yor name?")

def initiateConversation(name):
    print("Nice to meet you " + str(name) + ". What can I help you with today?")

def respond(keyword):
    print("Tell me more about " + str(keyword) + ".")