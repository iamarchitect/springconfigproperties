class MessageEntity():

    def __init__(self, body, start ,end , diff,matchPattern=None, value=None):
        self.body = body
        self.start = start
        self.end = end
        self.value = value
        self.diff = diff
        self.matchPattern = matchPattern
        self.length = len(body)
        
    def getStart(self):
        return self.start

    def __str__(self):
        return "body:"+self.body+", start:"+str(self.start)+",end:"+str(self.end)+", value:"+str(self.value)+",diff:"+str(self.diff)+",self.length: "+str(self.length)+",self.matchPattern: "+str(self.matchPattern)