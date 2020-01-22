import re

def numGroups(token):
    return len(token.groups())


def example():
    sentence = "I crave to rule the world"
    token = re.search(r'^(.*?)\s(crave)\s(.*?)$', sentence)
    print(numGroups(token))



example()
