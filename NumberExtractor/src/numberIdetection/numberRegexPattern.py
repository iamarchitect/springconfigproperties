from numberIdetection.match_my_pattern import matchmypattern


def numberRegexPattern():

    numberPattern = "\d+"

    pattern_1 = "\\b(on or before|on or after|more than|greater than|less than)\\b(\s?)" + numberPattern + "(\s?)(\\b(and|but|or)\\b\s?)(\\b(on or before|on or after|more than|greater than|less than)\\b)(\s?)" + numberPattern

    pattern_2 = "\\b(on or before|on or after|more than|greater than|less than)\\b(\s?)" + numberPattern + "(\s?)(\\b(and|or)\\b\s?)(\s?)" + numberPattern

    pattern_3 = "\\b(on or before|on or after|more than|greater than|less than)\\b(\s?)" + numberPattern

    pattern_4 = "\\b(between|in between)\\b(\s?)" + numberPattern + "(\s?)(\\b(and|but|or)\\b\s?)(\s?)" + numberPattern

    pattern_5 = "\\b(from)\\b(\s?)" + numberPattern + "(\s?)(\\b(till)\\b\s?)" + numberPattern

    pattern_6 = "\\b(from)\\b(\s?)" + numberPattern

    pattern_7 = "\\b(till)\\b(\s?)" + numberPattern


    rawtext1 = "risk score less than 883 or more than 20001 denied"

    rawtext2 = "risk score more than 883 or 344 and date more than 01/01/2019"

    rawtext3 = "risk score more than 883"

    rawtext4 = "risk score in between 17 and 23"

    rawtext5 = "risk score from 15 till 18"

    rawtext6 = "risk score from 15"

    rawtext7 = "risk score till 15"

    # textpattern = pattern_1
    # text = rawtext1
    matchmypattern(pattern_1, rawtext1)

    # textpattern = pattern_2
    # text = rawtext2
    matchmypattern(pattern_2, rawtext2)

    # textpattern = pattern_3
    # text = rawtext3
    matchmypattern(pattern_3, rawtext3)

    # textpattern = pattern_4
    # text = rawtext4
    matchmypattern(pattern_4, rawtext4)

    # textpattern = pattern_5
    # text = rawtext5
    matchmypattern(pattern_5, rawtext5)

    # textpattern = pattern_6
    # text = rawtext6
    matchmypattern(pattern_6, rawtext6)

    # textpattern = pattern_7
    # text = rawtext7
    matchmypattern(pattern_7, rawtext7)

if __name__ == '__main__':
    numberRegexPattern()

