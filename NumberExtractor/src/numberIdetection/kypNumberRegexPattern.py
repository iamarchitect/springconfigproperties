from match_my_pattern import matchmypattern

def kypNumberRegexPattern():

    numberPattern = "\d+"

    ssnPattern = "[0-9]{1,3}-[0-9]{1,2}-[0-9]{1,4}"
    ssnNumberFormatRawText = "1433-44-1217"

    numberFormatPattern = "[0-9]+" #numberPattern
    numberFormatRawText = "cases with 232323"

    # textpattern = ssnPattern
    # text = ssnNumberFormatRawText
    matchmypattern(ssnPattern, ssnNumberFormatRawText)

    # textpattern = numberFormatPattern
    # text = numberFormatRawText
    matchmypattern(numberFormatPattern, numberFormatRawText)

if __name__ == '__main__':
    kypNumberRegexPattern()
