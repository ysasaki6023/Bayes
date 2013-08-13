import os,sys,copy

###############################
class Factor:
    #
    def __init__(self,parents=[],child=None,probTable={}):
        self.parents = parents
        self.child   = child
        self.probTable = probTable
        #print self.probTable
    #
    def CalcProb(self,sets,evid={}):
        if self.child in evid.keys():
            if 
        key_parents = []
        if self.parents:
            for p in self.parents:
                assert p in sets
                key_parents.append(sets[p])
        else:
            key_parents = (None,)

        key_child   = sets[self.child]
        key = tuple([tuple(key_parents),key_child])

        return self.probTable[key]
###############################
class Variable:
    #
    def __init__(self,name,statuses):
        self.name   = name
        self.statuses = statuses
###############################
class BayesNet:
    def __init__(self):
        self.Variables = []
        self.Factors   = []
        pass
    def AddVariables(self,Variables):
        self.Variables = Variables
    def AddFactors(self,Factors):
        self.Factors   = Factors
    def MakeValList(self,exclude):
        keyList = []
        for v in self.Variables:
            if v in exclude:continue
            newkeyList = []
            for s in v.statuses:
                if not keyList:
                    newkeyList.append({v:s})
                else:
                    for k in keyList:
                        nk = copy.copy(k)
                        nk.update({v:s})
                        newkeyList.append(nk)
            keyList = newkeyList
        return keyList
    def CalcProb(self,query,evidene={}):
        mykeys = []
        elimVals = query.keys() + evidence.keys()
        valList = self.MakeValList(elimVals)
        for k in valList:
            t = copy.copy(k)
            t.update(query)
            mykeys.append(t)
        if not valList:
            mykeys = [copy.copy(query)]

        prob = 0.
        for k in mykeys:
            tempProb = 1.
            for f in self.Factors:
                aprob = f.CalcProb(k,evidence)
                tempProb *= aprob
                print aprob,
            print
            print [(v.name,k[v]) for v in sorted(k,cmp=lambda x,y:cmp(x.name,y.name))],tempProb
            prob += tempProb
        return prob



def test1():
    v1 = Variable('v1',['T','F'])
    v2 = Variable('v2',['T','F'])
    v3 = Variable('v3',['T','F'])

    f_1   = Factor(parents=None,child=v1,probTable={((None,),'T'):0.6,
                                                    ((None,),'F'):0.4})

    f_1_2 = Factor(parents=[v1],child=v2,probTable={(('T',),'T'):0.9,
                                                    (('T',),'F'):0.1,
                                                    (('F',),'T'):0.2,
                                                    (('F',),'F'):0.8})

    f_2_3 = Factor(parents=[v2],child=v3,probTable={(('T',),'T'):0.3,
                                                    (('T',),'F'):0.7,
                                                    (('F',),'T'):0.5,
                                                    (('F',),'F'):0.5})

    print f_1_2.CalcProb(sets={v1:'T',v2:'F'})
    print f_1  .CalcProb(sets={v1:'T'})
    bn = BayesNet()
    bn.AddVariables([v1,v2,v3])
    bn.AddFactors([f_1,f_1_2,f_2_3])
    print bn.CalcProb({v3:'T'})
    print bn.CalcProb({v3:'F'})

def test2():
    v1 = Variable('v1',['T','F'])
    v2 = Variable('v2',['T','F'])
    v3 = Variable('v3',['T','F'])
    v4 = Variable('v4',['T','F'])
    v5 = Variable('v5',['T','F'])

    f_1   = Factor(parents=None,child=v1,probTable={((None,),'T'):0.6,
                                                    ((None,),'F'):0.4})

    f_1_2 = Factor(parents=[v1],child=v2,probTable={(('T',),'T'):0.2,
                                                    (('T',),'F'):0.8,
                                                    (('F',),'T'):0.75,
                                                    (('F',),'F'):0.25})

    f_1_3 = Factor(parents=[v1],child=v3,probTable={(('T',),'T'):0.8,
                                                    (('T',),'F'):0.2,
                                                    (('F',),'T'):0.1,
                                                    (('F',),'F'):0.9})

    f_23_4 = Factor(parents=[v2,v3],child=v4,probTable={(('T','T'),'T'):0.95,
                                                        (('T','T'),'F'):0.05,
                                                        (('T','F'),'T'):0.9,
                                                        (('T','F'),'F'):0.1,
                                                        (('F','T'),'T'):0.8,
                                                        (('F','T'),'F'):0.2,
                                                        (('F','F'),'T'):0.0,
                                                        (('F','F'),'F'):1.0})

    f_3_5 = Factor(parents=[v3],child=v5,probTable={(('T',),'T'):0.7,
                                                    (('T',),'F'):0.3,
                                                    (('F',),'T'):0.0,
                                                    (('F',),'F'):1.0})

    bn = BayesNet()
    bn.AddVariables([v1,v2,v3,v4,v5])
    bn.AddFactors([f_1,f_1_2,f_1_3,f_23_4,f_3_5])
    #print 'v1=T,v2=T,v3=T,v4=T,v4=T,v5=T :',bn.CalcProb({v1:'T',v2:'T',v3:'T',v4:'T',v5:'T'})
    print 'evidence : v1=T,v2=F'
    print 'v4=T,v5=T :',bn.CalcProb({v1:'T',v2:'F',v4:'T',v5:'T'})
    print 'v4=T,v5=F :',bn.CalcProb({v1:'T',v2:'F',v4:'T',v5:'F'})
    print 'v4=F,v5=T :',bn.CalcProb({v1:'T',v2:'F',v4:'F',v5:'T'})
    print 'v4=F,v5=F :',bn.CalcProb({v1:'T',v2:'F',v4:'F',v5:'F'})

if __name__=="__main__":
    test2()
