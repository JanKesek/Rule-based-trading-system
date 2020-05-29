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
            i+=1
    def compute_belief_intervals(self, masdic):
        beliefintervals={}
        for elem in masdic:
            #print(elem)
            decisions=elem.split("-")
            for el in decisions:
                if el not in beliefintervals: 
                    beliefintervals[el]=0
        for elem1 in beliefintervals:
            bel=0
            pl=0
            for elem2 in masdic:
                decisions=elem2.split("-")
                if elem1 in decisions:
                    bel+=masdic[elem2]
                    #pl+=masdic[elem2]
            beliefintervals[elem1]=bel
            #beliefintervals[elem1].extend([bel,pl])
        return max(beliefintervals, key=beliefintervals.get)
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

