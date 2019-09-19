'''
Created on 27-Aug-2019

@author: asarkar
'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import datetime
import logging
import os
import re
import re

from nltk.corpus import stopwords
from rasa_nlu import utils
from rasa_nlu.extractors import EntityExtractor
import requests
import simplejson

from actions.constant import EXTRACTOR_CRF, EXTRACTOR_KEYWORD,\
    EXTRACTOR_DUCKLING, EXTRACTOR_NER_SPACY, EXTRACTOR_PROVIDER_NAME_SEARCH,\
    EXTRACTOR_PERSON_NAME_SEARCH
from actionutils.configUtil import ret_config_urls


# try:
#     import spacy
#     nerSpacy=spacy.load("en")
# except ImportError:
#     spacy = None
## IMPORT libraries
logger = logging.getLogger(__name__)


## here is the ORDER of METHOD calls
## init->create->train->persist->load->process
class PersonNameExtractor(EntityExtractor):
    """Searches for structured entites, e.g. dates, using a duckling server."""

    name = "pipeline.person_name_extractor.PersonNameExtractor"

    provides = ["entities"]

    defaults = {

        "entityType": None,
        
        "colomnNames": None,
        
        "indexName": None,
		
		"url": None
    }

    def __init__(self, component_config=None, language=None):
        # type: (Text, Optional[List[Text]]) -> None

        super(PersonNameExtractor, self).__init__(component_config)
        # declare class instance for TfIdfVectorizer
        
        ret_config_urls.cache_clear()
        config_items=ret_config_urls("URLS")
        self.serverURI = config_items["search-service_gatewayenv"]
        self.serviceName = config_items["service-name_gatewayenv"]
        
        
    def _regexMatch(self,mypattern,tobematchedtext):
        
        return re.search(mypattern, tobematchedtext, re.IGNORECASE)
    
    def _findWholeWord(self,w):
        
        return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search
        
      ##Create Method
#     @classmethod
#     def create(cls, config):
#         # type: (RasaNLUModelConfig) -> DucklingHTTPExtractor
# 
#         return cls(config.for_component(cls.name,
#                                         cls.defaults),
#                    config.language)


    
    ## TRAINING phase
    def train(self, training_data, cfg=None, **kwargs):
        # type: (TrainingData, RasaNLUModelConfig, **Any) -> None
        """Take parameters from config and
            construct a new count vectorizer using the sklearn framework."""
            
        #print("No training required")
    
    ## PREDICTION phase     
#     def process(self, message, **kwargs):
#     # type: (Message, **Any) -> None      
#         
#         entityType = self.component_config["entityType"]
#         print("******entityType********")
#         print(entityType)
#         
#         message.set("entities",[])

    def _preProcess(self,message):
        
        print("PrePocess")
        
        myParams = {"entities":message.get("entities"),"text":message.text}
        
        unExtractedStr = self._getUnExtractedText(myParams)
        
        print("UNEXTRACTED............")
        print(unExtractedStr)
        if unExtractedStr!=None or len(unExtractedStr)>0:
            unExtractedStr = unExtractedStr.strip()
            if len(unExtractedStr)>0:
                unExtractedWordTokens = unExtractedStr.split(" ")
                print("UNEXTRACTED............")
                return unExtractedWordTokens
            else:
                return None
        else:
            return None
        
        
    def _convert_pipeline_def_format(self,releventInfos):
        
        extracted = []
        
        #print("releventInfos")
        #print(releventInfos)

        for info in releventInfos:
            #print(info)
            detail = info["additional_info"]
            entity = {"start": detail["start"],
                      "end": detail["end"],
                      "text": detail["body"],
                      "value": info["expectedvalues"],
                      "confidence": 1.0,
                      "entity": self.component_config["entityType"]}
    
            extracted.append(entity)
    
        return extracted
    
    def _extractInfo(self,message,unExtractedWordTokens, attributeResultList):
        print("_extractInfo")
        
        colomnNames = self.component_config["colomnNames"]
        
        extractedInfos = []

        searchWordMap = {}

        for searchIndex in unExtractedWordTokens:
            for resultIndex in attributeResultList:
                pattern = r"\b(?=\w)" + re.escape(searchIndex) + r"\b(?!\w)"
                print(pattern)
                x = self._regexMatch(pattern, resultIndex[colomnNames[0]])
                if (x):
                    print("YES! We have a match!")
                    print(x)
                    if searchIndex in searchWordMap:
                        oldMap = searchWordMap[searchIndex]
                        oldMap["expectedvalues"].append(resultIndex)
                    else:
                        mymap = {
                            "expectedvalues": [resultIndex],
                            "additional_info": ""}
                        searchWordMap[searchIndex] = mymap
                else:
                    print(x)
                    print("No match")

        print("==============================")
        print("Displaying the match")
        print(searchWordMap)

        print("-----------------------")
        fullText = message.text
        print(fullText)

        for searchIndex in searchWordMap:
            pattern = r"\b(?=\w)" + re.escape(searchIndex) + r"\b(?!\w)"
            x = self._regexMatch(pattern, fullText)
            if (x):
                print("YES! We have a match!")
                print(x)
                print(x.start())
                print(x.end())
                if searchIndex in searchWordMap:
                    additional_info = {
                        "start": x.start(),
                        "end": x.end(),
                        "body": searchIndex}
                    oldMap = searchWordMap[searchIndex]
                    oldMap["additional_info"] = additional_info
    
            else:
                print(x)
                print("No match")

        print("==============================")
        print("FINAL =====Displaying the match")
        print(searchWordMap)
        
        for wordIndex in searchWordMap:
            extractedInfos.append(searchWordMap[wordIndex])
        
        return extractedInfos

        
    def _postProcess(self,message,unExtractedWordTokens,nameSearchResponse):
        print("postProcess")
        
        attributeResultList = []
        colomnNames = self.component_config["colomnNames"]
        
        if 'page' in nameSearchResponse and 'source' in nameSearchResponse and len(nameSearchResponse['source'])>0:
            
            for result in nameSearchResponse['source']:
                print(result[colomnNames[0]])
                print(result[colomnNames[1]])
                attributeResultList.append({colomnNames[0]:result[colomnNames[0]],colomnNames[1]:result[colomnNames[1]]})
                
            return self._extractInfo(message,unExtractedWordTokens, attributeResultList)             
            
            
        
        
        
    def process(self, message, **kwargs):
        # type: (Message, **Any) -> None
        
        entityType = self.component_config["entityType"]
        print("******entityType********")
        print(entityType)
        
        colomnNames = self.component_config["colomnNames"]
        print("*******colomnNames***********")
        print(colomnNames)
        
        
        indexName = self.component_config["indexName"]
        print("****indexName*********")
        print(indexName)
        
        print("self.serviceName")
        print(self.serviceName)
        
        print("message------------")
        print(message.get("entities"))
        
        unExtractedWordTokens = self._preProcess(message)
        
        extracted = []
        
        if unExtractedWordTokens!=None and self._url()!=None and self.component_config["indexName"]!=None:
            
            nameSearchResponse = self._nameSearch(unExtractedWordTokens)
            print("nameSearchResponse")
            print(nameSearchResponse)
            relevent_matches = self._postProcess(message,unExtractedWordTokens,nameSearchResponse)
            print("relevent_matches")
            print(relevent_matches)
            if relevent_matches!=None:
                extracted = self._convert_pipeline_def_format(relevent_matches)
        else:
            logger.warning("No Search Service URL or indexName or unExtractedWord in component in pipeline")
            
            
        if len(extracted)>0:
            extracted = self.add_extractor_name(extracted)
            
            message.set("entities",
                    message.get("entities", []) + extracted,
                    add_to_output=True)
        
        
        
    def _url(self):
        """Return url of the duckling service. Environment var will override."""
        
        print("self.component_config")
        print(self.component_config)
        print(self.component_config.get("url"))
        
        if os.environ.get("SEARCH_SERVICE_HTTP_URL"):
            return os.environ["SEARCH_SERVICE_HTTP_URL"]+self.serverURI

        return self.component_config.get("url")+self.serverURI
        
        
    def _payload(self,unExtractedWordTokens,indexName,projections=None):
        
        unExtractedWordTokensStr = ""
        
        counter = 0
        print("_payload")
        for etoken in unExtractedWordTokens:
            print(etoken)
            if counter < len(unExtractedWordTokens)-1:
                unExtractedWordTokensStr = unExtractedWordTokensStr + etoken +"','"
            else:
                unExtractedWordTokensStr = unExtractedWordTokensStr + etoken
                
            counter = counter + 1
                
        unExtractedWordTokensStr = "('"+unExtractedWordTokensStr+"')"
        
        projectionsStr = ''
        
        counter = 0
        
        if projections!=None:
            for eProj in projections:
                if counter < len(projections)-1:
                    projectionsStr = projectionsStr +  eProj +","
                else:
                    projectionsStr = projectionsStr + eProj
                    
                counter = counter + 1
                    
        else:
            projectionsStr = "*"
            
        
        data_json = {}
        data_json["attributes"] = {"additionalProp1": "string"}
        data_json["sql"]="select " + projectionsStr + " from  "+indexName+"  where "+self.component_config["colomnNames"][0]+" IN "+unExtractedWordTokensStr

        print("my data json")
        print(data_json)
            
        return data_json
           
    def _nameSearch(self, unExtractedWordTokens):
        """Sends the request to the duckling server and parses the result."""

        try:
            
            projections = self.component_config["colomnNames"]
            indexName = self.component_config["indexName"]
            
            payload = self._payload(unExtractedWordTokens,indexName,projections)
            headers = {"Content-Type": "application/json","X-TENANT-ID":"test1","SERVICE-NAME":self.serviceName}
            response = requests.post(self._url(),
                                     json=payload,
                                     headers=headers,
                                     verify=False)
            if response.status_code == 200:
                print("Search Service Response....")
                return simplejson.loads(response.text)
            else:
                logger.error("Failed to get a proper response from remote "
                             "Search Service. Status Code: {}. Response: {}"
                             "".format(response.status_code, response.text))
                return []
        except requests.exceptions.ConnectionError as e:
            logger.error("Failed to connect to Search Service. Make sure "
                         "the Search Service server is running and the proper host "
                         "and port are set in the configuration"
                         "Error: {}".format(e))
            return []
        
        
    def _getUnExtractedText(self,params,inputConfidence=0.20):
    
        residVect = params["text"].lower()
        myentities = params["entities"]
        
        for entity in myentities:
            if 'confidence' in entity and entity['confidence'] > inputConfidence:
                if entity['extractor']==EXTRACTOR_PROVIDER_NAME_SEARCH:
                    residVect = re.sub(entity['text'].lower(),'',residVect)
                    
        for entity in myentities:
            if 'confidence' in entity and entity['confidence'] > inputConfidence:
                if entity['extractor']==EXTRACTOR_PERSON_NAME_SEARCH:
                    residVect = re.sub(entity['text'].lower(),'',residVect)
        
        for entity in myentities:
            if 'confidence' in entity and entity['confidence'] > inputConfidence:
                if entity['extractor']==EXTRACTOR_DUCKLING:
                    residVect = re.sub(entity['text'].lower(),'',residVect)
                    
    
        for entity in myentities:
            if 'confidence' in entity and entity['confidence'] > inputConfidence:
                #print(entity['confidence'])
                startIndex = entity['start']
                endIndex = entity['end']
                if entity['extractor']==EXTRACTOR_NER_SPACY:
                    #print("entity   :::   ", entity)
                    residVect = re.sub(entity['value'].lower(),'',residVect)
                    #print("after ner_spacy_extractor::   ",residVect)
                    
                if entity['extractor']==EXTRACTOR_CRF:
                    #print("entity   :::   ", entity)
                    val = entity['value'].lower()
                    
                    if 'processors' in entity:
                        #print("processors is present  ",entity['processors'])
                        actualVal = params["text"].lower()[startIndex:endIndex]
                        #print("valval  ",actualVal)
                        residVect = re.sub(actualVal,'',residVect)
                        
                        #print("residVect  processors  ",residVect)
                    
                    if len(val.split())==1 and self._findWholeWord(val)(residVect):
                        text1 = [word for word in residVect.split() if word not in [val]]
                        residVect = ' '.join(text1)
                    else:
                        residVect = re.sub(val,'',residVect)
                    #print("after custom_ner_crf::   ",residVect)
                
                if entity['extractor']==EXTRACTOR_KEYWORD:
                    #print("entity   :::   ", entity)
                    actualVal = params["text"].lower()[startIndex:endIndex]
                    residVect = re.sub(actualVal,'',residVect)
                    #print("after ner_custom_keyword_extractor::   ",residVect)
            else:
                ssnPatt = r'\b\d{3}-\d{2}-\d{4}\b'
                text = entity['value']
                if entity['extractor']==EXTRACTOR_CRF and re.search(ssnPatt,text):
                    residVect = re.sub(text,'',residVect)
                    
        #print("FINAL residVect =",residVect)
        
        if residVect and len(residVect)>0:
            #text1 = [re.sub('['+string.punctuation+']',' ',word) for word in residVect.split()]
            text1 = [word for word in residVect.split() if word not in stopwords.words('english')]
            stopwds=['before','find','search','cases','case','get','which','yet','till','date','for','type','related',
                    'riskscore','risk score','risk','score','since','roup','whose']
            text1 = [word for word in text1 if word not in stopwds]
            residVect = ' '.join(text1)
            #residVect = re.sub(r'\d+|\s+',' ',residVect)
            residVect = residVect.strip()
            
        return residVect
    

    ## SAVE the model
#     def persist(self, model_dir):
#         # type: (Text) -> Dict[Text, Any]
#         """Persist this model into the passed directory.
#         Returns the metadata necessary to load the model again."""
# 
# 
#         return {}
    
    ## LOAD the model
#     @classmethod
#     def load(cls,
#              model_dir=None,  # type: Text
#              model_metadata=None,  # type: Metadata
#              cached_component=None,  # type: Optional[DucklingHTTPExtractor]
#              **kwargs  # type: **Any
#              ):
#         # type: (...) -> DucklingHTTPExtractor
# 
#         component_config = model_metadata.for_component(cls.name)
#         return cls(component_config, model_metadata.get("language"))
