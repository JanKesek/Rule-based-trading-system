import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from pyds import MassFunction
class DempsterS:
    def __init__(self,indicatorsmin, indicatorsmax,indicatordic):
        self.antecedents={}
        self.consequents={}
        self.rules={}
        self.indicators =indicatordic
        self.controls={}
        self.signals=[]
        for k in indicatorsmin:
            self.antecedents[k]=ctrl.Antecedent(
                np.arange(indicatorsmin[k],indicatorsmax[k],1),k
            )
            self.antecedents[k].automf(3)
            self.consequents[k]=ctrl.Consequent(np.arange(0,100,1),k)
            self.consequents[k].automf(3)
            self.rules[k]=[
                ctrl.Rule(self.antecedents[k][i],self.consequents[k][i]) for i in self.antecedents[k].terms
            ]
    def computemu(self,indicator_value,indicator_name):
        if indicator_name not in self.controls:
            self.controls[indicator_name]=ctrl.ControlSystem(self.rules[indicator_name])
        mu=ctrl.ControlSystemSimulation(self.controls[indicator_name])
        mu.input[indicator_name]=indicator_value
        mu.compute()
        return mu.output[indicator_name]/100
    def take_decision(self, decisions):
        i=0
        for d in decisions:
            basicafs,sources,finaldecs=[],[],[]
            dsimple=self.check_decision_equivalence(d)
            if dsimple!=None:
                self.signals.append([dsimple[:-1],i])
            else:
                for deltas in d[:-1]:
                    source=deltas.split(" ")[0][1:].split("_")[0]
                    mus=[self.computemu(self.indicators[k][d[-1]],k) for k in [source,"volume","wbb"]]
                    print(mus)
                    generalDecision=deltas.split(" ")[1][:-1]
                    detailDecision=generalDecision
                    if len(generalDecision.split("_"))>1:
                        detailDecision=generalDecision.split("_")
                    basicafs.append(MassFunction({k:mus[i] for i,k in enumerate([source[0],"volume"[0],"wbb"[0]])}))
                    #basicafs.append(MassFunction({k:mus[i] for }))
                    sources.append(source)
                    finaldecs.append(detailDecision)
                #basicafs.append(MassFunction({k:mus[i] for i,k in enumerate(sources)})            
                ms=self.combination_rule(basicafs,finaldecs)
                for m in ms:
                    print("BEL {} PL {} DECISION {}".format(m[0].bel(),m[0].pl(), m[1]))
                #print(basicafs)
                #self.combination_rule(basicafs,sources,finaldecs)
                #generalmus=[]
                #for s in sources: generalmus.append(self.combination_rule(s))
            i+=1
    def check_decision_equivalence(self,decision):
        d=decision[0].split(" ")[1].split("_")
        if len(decision)==2 and len(d)==1:
            return d[0]
    def combination_rule(self,basicMFs,decisions):
        i=0
        ms=[]
        while i!=len(decisions):
            for j in range(len(basicMFs)):
                if i!=j:
                    ms.append([basicMFs[i]&basicMFs[j], decisions[i]+decisions[j]])
            i+=1
        return ms
        #m=basicMFs[0]
        #for i in range(1,len(basicMFs)):
        #    m&basicMFs[i]
        #return m
    #def combination_rule(self, basicafs,sources,decisions):
    #    K=0
    #    uniqueSources=list(set(sources))
    #    uniqueDecisions=list(set(decisions))
    #    for decisionMP in uniqueDecisions:
    #        if 
