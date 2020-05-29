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
        #print(indicator_value)
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
                rules={
                    "price_buy":["price","volume","wbb"],
                    "price_buy-hold":["price","volume","wbb"],
                    "price_hold":["price","volume","wbb"],
                    "price_sell":["price","volume","wbb"],
                    "eta_buy":["eta","volume","wbb"],
                    "eta_buy-hold":["eta","volume","wbb"],
                    "eta_sell":["eta","volume","wbb"],
                    "eta_sell-hold":["eta","volume","wbb"]
                }
                mus={}
                for el in rules:
                    indic=el.split("_")[0]
                    mus[el]=min([self.computemu(self.indicators[rules[el][j]][i], indic) for j in range(len(rules[el]))])
                mus2=self.compute_cumulated_mass_asignments(mus)
                beliefintervals=self.compute_belief_intervals(mus2)
                #print("DECISION FROM DST: {} ".format(beliefintervals))
                self.signals.append([beliefintervals,i])
                #for deltas in d[:-1]:
                #    source=deltas.split(" ")[0][1:].split("_")[0]
                #    mus=[self.computemu(self.indicators[k][d[-1]],k) for k in [source,"volume","wbb"]]
                #    print(mus)
                #    generalDecision=deltas.split(" ")[1][:-1]
                #    detailDecision=generalDecision
                #    if len(generalDecision.split("_"))>1:
                #        detailDecision=generalDecision.split("_")
                #    basicafs.append(MassFunction({k:mus[i] for i,k in enumerate([source[0],"volume"[0],"wbb"[0]])}))
                    #basicafs.append(MassFunction({k:mus[i] for }))
                #    sources.append(source)
                #    finaldecs.append(detailDecision)
                #basicafs.append(MassFunction({k:mus[i] for i,k in enumerate(sources)})            
                #ms=self.combination_rule(basicafs,finaldecs)
                #for m in ms:
                #    print("BEL {} PL {} DECISION {}".format(m[0].bel(),m[0].pl(), m[1]))
                #print(basicafs)
                #self.combination_rule(basicafs,sources,finaldecs)
                #generalmus=[]
                #for s in sources: generalmus.append(self.combination_rule(s))
            i+=1
    def compute_belief_intervals(self, masdic):
        beliefintervals={}
        for elem in masdic:
            #print(elem)
            decisions=elem.split("-")
            #if len(elem.split("_")[1].split("-"))>1:
            #    for el in elem.split("_")[1].split("-"):
            # 3       if el not in beliefintervals: beliefintervals[el]=[]
            #else:
            #    if elem not in beliefintervals:
            for el in decisions:
                if el not in beliefintervals: 
                    #beliefintervals[elem]=[]
                    beliefintervals[el]=0
        for elem1 in beliefintervals:
            bel=0
            pl=0
            for elem2 in masdic:
                decisions=elem2.split("-")
                if len(decisions)==1:
                    if decisions[0]==elem1:
                        bel+=masdic[elem2]
                        pl+=masdic[elem2]
                else: 
                    if elem1 in decisions:
                        bel+=masdic[elem2]
                        pl+=masdic[elem2]
            beliefintervals[elem1]=bel
            #beliefintervals[elem1].extend([bel,pl])
        return max(beliefintervals, key=beliefintervals.get)
        #return beliefintervals
                #source=elem2.split("_")[0]
                #decision=elem2.split("_")[1].split("-")
                #if elem1.split("_")[0]==source and elem1.split("_")[1] in decision:
                #    beliefintervals[elem1].append(masdic[elem2])
        #for elem in beliefintervals:
        #    beliefintervals[elem]=[min(beliefintervals[elem]),max(beliefintervals[elem])]
        #return beliefintervals                
    def check_decision_equivalence(self,decision):
        d=decision[0].split(" ")[1].split("_")
        if len(decision)==2 and len(d)==1:
            return d[0]
    def compute_cumulated_mass_asignments(self, mus):
        lstfinalrules=[]
        lstfinalsources=[]
        finalmas={}
        for el in mus:
            rule=el.split("_")[1]
            source=el.split("_")[0]
            if rule not in lstfinalrules: lstfinalrules.append(rule)
            if source not in lstfinalsources: lstfinalsources.append(source)
        for rule in lstfinalrules:
            m=[]
            for source in lstfinalsources:
                currentkey=source+"_"+rule
                if currentkey in mus:
                    K=0
                    m1=mus[currentkey]
                    for el in mus:
                        if el != currentkey and rule in el:
                            m1*=mus[el]
                        elif el!=currentkey and rule not in el:
                            K+=mus[el]
                    #else:
                    m.append(m1)
            finalmas[rule]=sum(m)/(1-K)
        return finalmas
                    #if el.split("_")[1]!=rule:
                    #    m+=mus[el]*

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
