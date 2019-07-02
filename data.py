extratedEntityMapArray =[{"index":1,"entity":"logicalOperator","value":"NOT","consumed":"N"},
                         {"index": 2, "entity": "caseStatus", "value": "assigned", "consumed": "N"},
                         {"index": 3, "entity": "time", "value": {"to":"DATE1","from":"DATE2"}, "consumed": "N"},
                         {"index": 4, "entity": "condition", "value": "OR", "consumed": "N"},
                         {"index": 5, "entity": "caseStatus", "value": "due", "consumed": "N"},
                         {"index": 6, "entity": "time", "value": {"to": "DATE1", "from": "DATE2"}, "consumed": "N"},
                         {"index": 7, "entity": "caseStatus", "value": "accepted", "consumed": "N"},
                         {"index": 8, "entity": "time", "value": {"to": "DATE1", "from": "DATE2"}, "consumed": "N"},
                         {"index":9,"entity":"logicalOperator","value":"NOT","consumed":"N"},
                         {"index": 10, "entity": "caseStatus", "value": "assigned", "consumed": "N"},
                         {"index": 11, "entity": "time", "value": {"to":"DATE3","from":"DATE4"}, "consumed": "N"}
                         ]


attributeValueList=["assigned","due","accepted"]
primaryEntityList=["caseStatus"]
secondaryEntityList=["logicalOperator","time","condition"]

attributeValueMap ={}
attributeValueMap["accepted"] = {"relatedFields":["accepteddate"],"name":"activityAccept","type":"text","entityType":"caseStatus"}
attributeValueMap["accepteddate"] = {"relatedFields":[],"name":"activityAcceptedDate","type":"date","entityType":"time"}
attributeValueMap["assigned"] = {"relatedFields":["assigneddate"],"name":"activityStatus","type":"text","entityType":"caseStatus"}
attributeValueMap["assigneddate"] = {"relatedFields":[],"name":"activityStatus","type":"date","entityType":"time"}
attributeValueMap["due"] = {"relatedFields":[],"name":"dueDate","type":"date","entityType":"time"}



def getEntityDetail(cc):

    entityValue = cc['value']

    if attributeValueMap[entityValue]!=None:
        print("entityValue.name     " + attributeValueMap[entityValue]['name'])
        print(attributeValueMap[entityValue]['name'])
        if len(attributeValueMap[entityValue]['relatedFields'])>0:
            print("relatedFields available")
            return attributeValueMap[entityValue],attributeValueMap[entityValue]['relatedFields']
        else:
            print("relatedFields not available")
            return attributeValueMap[entityValue], []




def rec(extratedEntityMapArray,index,tmp=[]):

    if index == len(extratedEntityMapArray):
        return tmp

    mytmp = tmp
    bb = extratedEntityMapArray[index]
    bb['consumed'] = 'Y'

    #print("  bb['entity'] " + bb['entity'])

    if bb['entity'] in primaryEntityList:
        print("Primary Attribute Found : " + bb['entity'] +"  value "+bb['value'])
        if bb['entity']!='time':
            print("NOT JOSN")
            detail,relatedDetail = getEntityDetail(bb)
            if len(relatedDetail)>0:
                print("related fields .....")
                mytmp.append(bb)
                index = index + 2
                return rec(extratedEntityMapArray, index, mytmp)
            else:
                print("only detail ")
                mytmp.append(bb)
                index = index + 1
                return rec(extratedEntityMapArray, index, mytmp)
        else:
            print("DATE FORM")
    else:
        print("Secondary Attribute Found : " + bb['entity'])

        if bb['entity']=='condition':
            mytmp = []
            mytmp.append(bb)
            index = index + 1
            return rec(extratedEntityMapArray, index, mytmp)


        mytmp.append(bb)
        index = index + 1
        return rec(extratedEntityMapArray, index, mytmp)




    print(tmp)
    return tmp

def callme():
    print("AA")
    list = []
    print("aaaaaaaaaaaaa  ",len(extratedEntityMapArray))
    count = 0
    while (count < len(extratedEntityMapArray)):
        tmpList = []
        print(count)

        print(extratedEntityMapArray[count])

        if extratedEntityMapArray[count]['entity'] == 'condition':
            tmpList.append(extratedEntityMapArray[count])
            list.append(tmpList)
            count = count + 1
        else:
            #if extratedEntityMapArray[count]['entity'] == 'caseStatus':
            if extratedEntityMapArray[count]['entity'] in primaryEntityList:
                print("===")
                detail, relatedDetail = getEntityDetail(extratedEntityMapArray[count])
                tmpList.append(extratedEntityMapArray[count])
                if len(relatedDetail)>0:
                    for hh in relatedDetail:
                        print(attributeValueMap[hh])
                        if attributeValueMap[hh]['entityType'] == extratedEntityMapArray[count+1]['entity']:
                            tmpList.append(extratedEntityMapArray[count+1])
                            list.append(tmpList)
                            count = (count+1) + 1

                else:
                    print(detail)
                    if detail['entityType'] == extratedEntityMapArray[count+1]['entity']:
                        tmpList.append(extratedEntityMapArray[count + 1])
                        list.append(tmpList)
                        count = (count+1) + 1




            elif extratedEntityMapArray[count]['entity'] == 'logicalOperator':
                tmpList.append(extratedEntityMapArray[count])
                #list.append(tmpList)
                newCount = count + 1
                if extratedEntityMapArray[newCount]['entity'] in primaryEntityList:
                    print("===")
                    detail, relatedDetail = getEntityDetail(extratedEntityMapArray[newCount])
                    tmpList.append(extratedEntityMapArray[newCount])
                    if len(relatedDetail) > 0:
                        for hh in relatedDetail:
                            print(attributeValueMap[hh])
                            if attributeValueMap[hh]['entityType'] == extratedEntityMapArray[newCount + 1]['entity']:
                                tmpList.append(extratedEntityMapArray[newCount + 1])
                                list.append(tmpList)
                                count = (newCount + 1) + 1

                    else:
                        print(detail)
                        if detail['entityType'] == extratedEntityMapArray[newCount + 1]['entity']:
                            tmpList.append(extratedEntityMapArray[newCount + 1])
                            list.append(tmpList)
                            count = (newCount + 1) + 1
                #count = count + 1






    print(count)
    # for aa in extratedEntityMapArray:
    #     if aa['consumed']=='N':
    #         return
    #
    #     tmp = []
    #     aa['consumed']='Y'
    #     tmp1 = rec(extratedEntityMapArray,0,tmp)
    #     list.append(tmp1)


    print("List all......")
    print(list)
    print(extratedEntityMapArray)

if __name__ == "__main__":
    callme()
