import re

def findAllNumberPosition(pattern,text):
    
    z = re.findall(pattern, text, 2)
    if (z):
        print("Match FOUND in FINDALL")
        print(z)
    else:
        print("NO Match")


def matchmypattern(textpattern,text):
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("textpattern  "+textpattern)
    print("text         "+text)
    print("========FINDITER===============")
    iterator = re.finditer(textpattern, text,2)
    if iterator ==None:
        print("NO Match")
    for match in iterator:
        if (match):
            print("Match FOUND")
            print(match)

    # print("========FINDALL===============")
    # z = re.findall(textpattern,text,re.IGNORECASE)
    # if (z):
    #     print("Match FOUND")
    #     print(z)
    # else:
    #     print("NO Match")

    print("========SEARCH===============")
    x = re.search(textpattern, text, 2)

    if (x):
        print("Match FOUND")
        print(x)
        print(x.group())
        print(x.start())
        print(x.end())
    else:
        print("NO Match")

    print("#################################")

if __name__ == '__main__':
    #matchmypattern()
    numberPattern = "\d+"
    from_till = "\\b(from)\\b(\s?)" +"("+ numberPattern +"?)"+ "(\s?)\\b(till)\\b(\s?)" +"("+ numberPattern +"?)"
    between_and = "\\b(between|in between)\\b(\s?)" +"("+ numberPattern +"?)"+ "(\s?)\\b(and|but)\\b(\s?)" +"("+ numberPattern +"?)"
    findAllNumberPosition(from_till,"from 33 till 18 or till 10")
    matchmypattern(from_till,"from 33 till 18 or till 10")
    print("===========")
    findAllNumberPosition(between_and,"between 44 and 54")
    matchmypattern(between_and,"between 44 and 54")