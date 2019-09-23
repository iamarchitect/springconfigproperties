from numberIdetection.regex_pipeline.phrase_extractor import PhraseExtractor


outlist = []

phraseExtractor = PhraseExtractor()
#messageText = "cases till 89"
messageText = "npi till 43 or riskscore in between 03 and 06 or riskscore more than 30 or less than 59"
#messageText = "npi till 43 or between 03 and 06/12/2019 or from 34 till 89 or till 100 or riskscore more than 30 or less than 59"
#messageText = "cases from 12-01 till 12-03-2019"
#messageText = "npi till 43 or riskscore more than 30 or less than 59"
#messageText = "npi till 43 or between 03 and 06"
list1 = phraseExtractor.process(messageText)
print("==========00000000000========")

if list1!=None:
    for ph in list1:
        outlist.append(ph)


if outlist!=None:
    for obj in outlist:
        print(obj.__str__())