import re

messageStartPattern = "\\b(from)\\b(\s?)"
dateRegexPattern_mmdd = "(1[0-2]|0?[1-9])\\s?[/-]\\s?(3[01]|[12]\\d|0?[1-9])"    #"mm/dd"
dateRegexPattern_mmddyyyy = "(1[0-2]|0?[1-9])[-/\\s](3[01]|[12]\\d|0?[1-9])([-/\\s](\\d{2,4})?)"  #mm/dd/yyyy
messageEndPattern = "(\s?)(\\b(and|or|but|till)\\b\s?)"

messagePattern = messageStartPattern + dateRegexPattern_mmddyyyy + messageEndPattern + dateRegexPattern_mmddyyyy

message = "from 12-01 till 12-03-2019"

x = re.search(messagePattern, message, re.IGNORECASE)
if (x):
    print("Match FOUND")
    print(x)
else:
    print("NO Match")