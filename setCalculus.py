class setCalc:
    def __init__(self, d1, d2):
        self.dict1 = dict(d1)
        self.dict2 = dict(d2)

        sum1 = 0
        for d in self.dict1:
            sum1+=self.dict1[d]

        maxVal1=max(self.dict1.values())
        for d in self.dict1:
            #self.dict1[d] /= sum1
            self.dict1[d] /= maxVal1

        sum2 = 0
        for d in self.dict2:
            sum2+=self.dict2[d]

        maxVal2=max(self.dict2.values())
        for d in self.dict2:
            #self.dict2[d] /= sum2
            self.dict2[d] /= maxVal2

    def getInter(self):
        samekeys = self.dict1.keys()&self.dict2.keys()
        intersect = {}
        for k in samekeys:
            v = min(self.dict1[k],self.dict2[k])
            intersect[k]=v
        return intersect

    def getDiff1(self):
        inter=self.getInter()
        diffa = dict(self.dict1)
        for i in inter:
            diffa[i]=self.dict1[i]-inter[i]
        return diffa
        
    def getDiff2(self):
        inter=self.getInter()
        diffb = dict(self.dict2)
        for i in inter:
            diffb[i]=self.dict2[i]-inter[i]
        return diffb


