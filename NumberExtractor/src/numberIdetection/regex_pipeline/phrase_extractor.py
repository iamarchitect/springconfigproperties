#phrase_extrator
import json
import re

from numberIdetection.regex_pipeline.message_entity import MessageEntity


class PhraseExtractor:

    def __init__(self):
        #print("__init__")

        self.numberPattern = None
        self.greaterPattern = None
        self.lessPattern = None
        self.entityTokens = None
        self.rangePattern = None
        self.patternList = self._loadRegexPattern()

    def _prepareRegexPattern(self):
        #print("_prepareRegexPattern")

        with open('regex.json', 'r') as data_file:
            regexData = json.loads(data_file.read())
            data_file.close()

        #for rd in regexData:
            #print(rd)
            #print(regexData[rd])

        return regexData


    def _createRegexPattern(self,regexList):
        regexStr = ""
        counter = 0
        for reg in regexList:
            if counter < len(regexList)-1:
                regexStr = regexStr + reg + "|"
            else:
                regexStr = regexStr + reg
            counter = counter + 1

        return regexStr


    def _loadRegexPattern(self):
        #print("_loadPattern")

        regexPhraseMap = self._prepareRegexPattern()

        patternList = []

        numberPattern = self._createRegexPattern(regexPhraseMap["numberPattern"])#"\d+"

        self.numberPattern = numberPattern
        
        entityTokens = self._createRegexPattern(regexPhraseMap["domainEntityTokens"])
        self.entityTokens = entityTokens

        greaterPattern = self._createRegexPattern(regexPhraseMap["greater"])
        self.greaterPattern = greaterPattern
        lessPattern = self._createRegexPattern(regexPhraseMap["less"])
        self.lessPattern = lessPattern
        rangePattern = self._createRegexPattern(regexPhraseMap["range"])
        self.rangePattern = rangePattern
        fromPattern = self._createRegexPattern(regexPhraseMap["from"])
        self.fromPattern = fromPattern
        tillPattern = self._createRegexPattern(regexPhraseMap["till"])
        self.tillPattern = tillPattern
        conditionPattern = self._createRegexPattern(regexPhraseMap["condition"])
        self.conditionPattern = conditionPattern

        pattern_1 = "\\b("+greaterPattern+")\\b(\s?)" + numberPattern + "(\s?)(\\b("+conditionPattern+")\\b\s?)(\\b("+lessPattern+")\\b)(\s?)" + numberPattern
        
        pattern_4 = "\\b("+lessPattern+")\\b(\s?)" + numberPattern + "(\s?)(\\b("+conditionPattern+")\\b\s?)(\\b("+greaterPattern+")\\b)(\s?)" + numberPattern

        #pattern_2 = "\\b("+greaterPattern+")\\b(\s?)" + numberPattern + "(\s?)(\\b("+conditionPattern+")\\b\s?)(\s?)" + numberPattern

        pattern_1_1 = "\\b("+greaterPattern+")\\b(\s?)" + numberPattern
        
        pattern_1_2 = "\\b("+lessPattern+")\\b(\s?)" + numberPattern

        pattern_2 = "\\b("+rangePattern+")\\b(\s?)" + numberPattern + "(\s?)(\\b("+"and"+")\\b\s?)(\s?)" + numberPattern

        pattern_3 = "\\b("+fromPattern+")\\b(\s?)" + numberPattern + "(\s?)(\\b("+tillPattern+")\\b\s?)" + numberPattern

        pattern_3_1 = "\\b("+fromPattern+")\\b(\s?)" + numberPattern

        pattern_3_2 = "\\b("+tillPattern+")\\b(\s?)" + numberPattern
        
        pattern_5 = "\\b("+entityTokens+")\\b"

        patternList.append({"patternNum":1,"pattern":pattern_1,"related":[{"patternNum":1,"pattern":pattern_1_1,"related":None},{"patternNum":2,"pattern":pattern_1_2,"related":None}]})
        patternList.append({"patternNum":4,"pattern":pattern_4,"related":[{"patternNum":2,"pattern":pattern_1_2,"related":None},{"patternNum":1,"pattern":pattern_1_1,"related":None}]})
        #patternList.append({"patternNum":2,"pattern":pattern_2})
        patternList.append({"patternNum":2,"pattern":pattern_2,"related":None})
        patternList.append({"patternNum":3,"pattern":pattern_3,"related":[{"patternNum":1,"pattern":pattern_3_1,"related":None},{"patternNum":2,"pattern":pattern_3_2,"related":None}]})
        #patternList.append({"patternNum":5,"pattern":pattern_5})
        #patternList.append({"patternNum":6,"pattern":pattern_6})
        #patternList.append({"patternNum":7,"pattern":pattern_7})
        newpatternList = []
        newpatternList.append({"patternNum":1,"pattern":pattern_1_1,"related":None})
        newpatternList.append({"patternNum":2,"pattern":pattern_1_2,"related":None})
        newpatternList.append({"patternNum":3,"pattern":pattern_2,"related":None})
        newpatternList.append({"patternNum":4,"pattern":pattern_3_1,"related":None})
        newpatternList.append({"patternNum":5,"pattern":pattern_3_2,"related":None})
        newpatternList.append({"patternNum":6,"pattern":pattern_5,"related":None})

        return newpatternList
    
    
    def _processRegexPattern(self,patternNum,regexPattern,message,relatedPatterns=None):
        #print("_processRegexPattern")

        listMessageEntity = []

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print('patternNum '+ str(patternNum))
        print("regexPattern  " + regexPattern)
        print("message         " + message)
        print("========FINDITER===============")
        iterator = re.finditer(regexPattern, message, 2)

        counter = -1
        for match in iterator:
            if (match):
                print("Match FOUND in FINDITER")
                print(match)
                z = re.findall(self.numberPattern, match.group(), 2)
                if (z):
                    print("Match FOUND in FINDALL")
                    print(z)
                else:
                    print("NO Match")
                listMessageEntity.append(MessageEntity(match.group().strip(),match.start(),match.end(), match.end()-match.start(),regexPattern,z))
                counter = counter + 1
                
                
        if counter > -1:
            print("counter ==>"+str(counter))
            return listMessageEntity
        else:
            return None

#         elif relatedPatterns !=None:
#             relatedPatternList = []
#             for rPattern in relatedPatterns:
#                 resultList = self._processRegexPattern(rPattern["patternNum"], rPattern["pattern"], message, rPattern["related"])
#                 if resultList != None:
#                     for result in resultList:
#                         relatedPatternList.append(result)
# 
# 
#             return relatedPatternList


        # print("========FINDALL===============")
        # z = re.findall(regexPattern,message,re.IGNORECASE)
        # if (z):
        #     print("Match FOUND in FINDALL")
        #     print(z)
        # else:
        #     print("NO Match")

        # print("========SEARCH===============")
        # x = re.search(regexPattern, message, re.IGNORECASE)
        #
        # if (x and isFound):
        #     print("Match FOUND in SEARCH")
        #     print(x)
        #     return MessageEntity(x.group(),x.start(),x.end(), x.end()-x.start())
        # else:
        #     return None


    def process(self,message):

        list = []
        print("Message length = "+str(len(message)))

        #patternNumber = 1
        for pl in self.patternList:
            resultList = self._processRegexPattern(pl["patternNum"],pl["pattern"],message,pl["related"])
            #patternNumber = patternNumber + 1
            if resultList!=None:
                for result in resultList:
                    list.append(result)
                    
        
        if len(list)>0:
            print("Before sorted")
            for obj in list:
                print(obj.__str__())

            print("List is sorted by start")
            list.sort(key=lambda x: x.start)
            for obj in list:
                print(obj.__str__())

            # print("List is sorted by diff")
            # list.sort(key=lambda x: x.diff,reverse=True)
            # for obj in list:
            #     print(obj.__str__())
            print("==Return ===")
            return list
        else:
            return None
