'''
Created on 24-Jan-2019

@author: asarkar
'''
import nltk
from nltk.corpus import wordnet



def getNameFromNLTK(text):
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    
    person_list = []

    person = []
    name = ""
    print(sentt)
    print(sentt.pos())
    print("Above is POS")
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            print(leaf[0])
            person.append(leaf[0])
            #print(len(person))
        if len(person) > 1: #avoid grabbing lone surnames
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        else:
            person_list.append(leaf[0])
        person = []
    #print (person_list)
    print("+++++++")
    print(person_list)
    print("+++++++")
    return person_list

# text = "dentist Sam"
# 
# names = get_human_names(text)
# for person in person_list:
#     person_split = person.split(" ")
#     for name in person_split:
#         if wordnet.synsets(name):
#             if(name in person):
#                 person_names.remove(person)
#                 break
# 
# print(person_names)

def testMe():
    
    text = "UTLEY JENNIFER ANNIE ORP SHEUGS"
    
    text = "Brandon billing"
    
    print("============BEFORE PROCESSING===========")
    getNameFromNLTK(text)
    print("====NLTK RESULT======")
    print("============LOWER===========")
    lowertext = text.lower()
    getNameFromNLTK(lowertext)
    print("====NLTK RESULT======")
    print("============TITLE===========")
    titletext = text.title()
    getNameFromNLTK(titletext)
    print("====NLTK RESULT======")
    print("============UPPER===========")
    uppertext = text.upper()
    getNameFromNLTK(uppertext)


if __name__ == '__main__':
    
    #testMe()
    #getNameFromNLTK("Brandon Billing")
    testMe()
 
"""
{
  "namelists": [
    {
      "ProviderName": "UTLEY, JENNIFER",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha revalidation 4",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "UTLEY, JENNIFER",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "SHEUGS",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "SHEUGS",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "R, Raghu",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "R, Jacob",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "GOLDSMITH, JAY",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "RAHMAN, RAKHSHANDA",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "JOHNSON, MARIA ELIZABETH",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "DEMO_IGSP",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "S, Sparsha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "Incorporated Individual Physician",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "GRPG BUSINESS martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "ISP",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "JENKINS, JUDITH",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "MOLLERE, RODNEY",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "MA, SHUO",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "KIM, JONGYEOL",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "JENSEN, CRAIG",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "SETHI, USHA",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "SCANLON, CLAYTON",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "P STEPHEN O NEILL LMSWPLLC",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "CHILDRENS HOSPITAL LOS ANGELES",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "ALLINE, KRISTIN",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "OGAWA, SADIE",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "KIM, JONGYEOL",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "THOMPSON, KENT",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "EISENBAUM, ALLAN",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "ALALAWI, RAED",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "saradhi, partha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "chandra, Hema",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "A, Nag",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "MARTHA CHOA SANCEZ",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "lee, brandon",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "Incorporated Individual Physician",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha SUPPLEMENTAL NR",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "sanchez, martha",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "R, Adarsh rtp and resubmission",
      "index": "globalsearch_final"
    },
    {
      "ProviderName": "DOWIS, DAVID",
      "index": "globalsearch_final"
    }
  ]
}
"""
