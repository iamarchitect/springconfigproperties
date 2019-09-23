#date_extrator
import json
import re

from numberIdetection.regex_pipeline.message_entity import MessageEntity


class DateExtractor:

    def __init__(self):
        #print("__init__")

        self.patternList = self._loadRegexPattern()

    def _prepareRegexPattern(self):
        #print("_prepareRegexPattern")

        with open('regex.json', 'r') as data_file:
            regexData = json.loads(data_file.read())
            data_file.close()

        return regexData


    def _createDateRegexPattern(self,regexList,type):
        for reg in regexList:
            for reg1 in reg:
                if type == reg1:
                    return reg[type]

    def _createRegexPattern(self,regexList):
        regexStr = ""
        counter = 0
        for reg in regexList:
            if counter < len(regexList)-1:
                regexStr = regexStr + reg + "|"
            else:
                regexStr = regexStr + reg
            counter = counter + 1

        return "("+regexStr+")"


    def _loadRegexPattern(self):
        #print("_loadPattern")

        regexPhraseMap = self._prepareRegexPattern()

        patternList = []

        datePattern = self._createDateRegexPattern(regexPhraseMap["datePattern_US"],"mmddyyyy")

        print("datePatterndatePattern")
        print(datePattern)

        # pattern_1 = "\\b"+self._createRegexPattern(regexPhraseMap["greater"])+"\\b(\s?)" + datePattern + "(\s?)(\\b"+self._createRegexPattern(regexPhraseMap["condition"])+"\\b\s?)(\\b"+self._createRegexPattern(regexPhraseMap["greater"])+"\\b)(\s?)" + datePattern
        #
        # pattern_2 = "\\b"+self._createRegexPattern(regexPhraseMap["greater"])+"\\b(\s?)" + datePattern + "(\s?)(\\b"+self._createRegexPattern(regexPhraseMap["condition"])+"\\b\s?)(\s?)" + datePattern
        #
        # pattern_3 = "\\b"+self._createRegexPattern(regexPhraseMap["greater"])+"\\b(\s?)" + datePattern
        #
        # pattern_4 = "\\b"+self._createRegexPattern(regexPhraseMap["range"])+"\\b(\s?)" + datePattern + "(\s?)(\\b"+self._createRegexPattern(regexPhraseMap["condition"])+"\\b\s?)(\s?)" + datePattern
        #
        pattern_5 = "\\b"+self._createRegexPattern(regexPhraseMap["from"])+"\\b(\s?)" + datePattern + "(\s?)(\\b"+self._createRegexPattern(regexPhraseMap["till"])+"\\b\s?)" + datePattern
        #
        # pattern_6 = "\\b"+self._createRegexPattern(regexPhraseMap["from"])+"\\b(\s?)" + datePattern
        #
        #pattern_7 = "\\b"+self._createRegexPattern(regexPhraseMap["till"])+"\\b(\s?)" + datePattern

        #patternList.append(pattern_1)
        # patternList.append(pattern_2)
        # patternList.append(pattern_3)
        # patternList.append(pattern_4)
        patternList.append(pattern_5)
        # patternList.append(pattern_6)
        #patternList.append(pattern_7)

        return patternList


    def _processRegexPattern(self,regexPattern,message):
        #print("_processRegexPattern")

        isFound = False

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("regexPattern  " + regexPattern)
        print("message         " + message)
        print("========FINDITER===============")
        iterator = re.finditer(regexPattern, message, 2)
        #print(next(iterator))

        counter = -1
        for match in iterator:
            if (match):
                print("Match FOUND")
                print(match)
                counter = counter + 1

        if counter > -1:
            print("counter ==>"+str(counter))
            isFound = True

        # print("========FINDALL===============")
        # z = re.findall(regexPattern,message,re.IGNORECASE)
        # if (z):
        #     print("Match FOUND")
        #     print(z)
        # else:
        #     print("NO Match")

        print("========SEARCH===============")
        x = re.search(regexPattern, message, 2)

        if (x and isFound):
            print("Match FOUND")
            return MessageEntity(x.group(),x.start(),x.end(), x.end()-x.start())
        else:
            return None



    def process(self,message):

        list = []

        for pl in self.patternList:
            result = self._processRegexPattern(pl,message)
            if result!=None:
                list.append(result)


        if len(list)>0:
            print("Before sorted")
            for obj in list:
                print(obj.__str__())

            print("List is sorted")
            list.sort(key=lambda x: x.diff,reverse=True)
            for obj in list:
                print(obj.__str__())
            print("==Return ===")
            return list
        else:
            return None
