from rulebased.simpleindicators import SimpleIndicators as SI
import pickle
import json
from rulebased.clipser import Clipser
from rulebased.dempsterschaffer import DempsterS
si =None
def set_data_for_si(data):
    global si
    si=SI(data,25)
class RBS:
    def __init__(self):
        #si=SI(data,25)
        #obj=self.load_from_file()
        #self.returns=obj['returns']
        #self.volumereturns=obj['volumereturns']
        #self.wbb=obj['wbb']
        self.groups=[]
        self.fuzzylimits={
            "volumebig":100,
            "pricebig":50,
            "wbbbig":10,
            "etabig":10

        }
        self.finaldecisions=[]
        #self.returns = si.returns()
        #self.volumereturns=si.volumereturns()
    def calculate_rv(self,data):
        set_data_for_si(data)
        global si
        self.returns = si.returns()
        self.volumereturns=si.volumereturns()

    def calculate_wbb(self):
        global si
        self.wbb=si.deltawbb()
        wbbdifference=len(self.returns)-len(self.wbb)
        self.returns=self.returns[wbbdifference:]
        self.volumereturns=self.volumereturns[wbbdifference:]
        self.volatilitychange=self.volatilitychange[wbbdifference:]
        #arr2=[len(arr2)-len(arr1):]
    def calculate_volatilty(self):
        global si
        self.volatilitychange=si.volatility_change()
    def start(self):
        self.classify([self.returns,self.volumereturns,self.wbb, self.volatilitychange])
        #print(self.groups)
        clipser=Clipser(self.groups)
        clipser.start()
        decisions=clipser.return_decisions()
        print(decisions)
        self.dempster.take_decision(decisions)
        self.finaldecisions=self.dempster.signals
        #for d in decisions:
        #    self.make_decision(d)
        #print(self.groups)
        #print(self.returns)
        #print(self.volumereturns)
        #print(self.wbb)
    def classify(self,indicators):
        for i in range(len(indicators[0])):
            dayGroup=[]
            if indicators[0][i]>self.fuzzylimits["pricebig"]:
                dayGroup.append("Plus_Price_Big")
            elif indicators[0][i]<(self.fuzzylimits["pricebig"]*(-1)):
                dayGroup.append("Price_MinusBig")
            else:
                dayGroup.append("Price_Medium")
            if indicators[1][i]>self.fuzzylimits["volumebig"]:
                dayGroup.append("Plus_Volume_Big")
            elif indicators[1][i]<(self.fuzzylimits["volumebig"]*(-1)):
                dayGroup.append("Volume_MinusBig")
            else:
                dayGroup.append("Volume_Medium")
            if indicators[2][i]>(self.fuzzylimits["wbbbig"]*(-1)) and indicators[2][i]<self.fuzzylimits["wbbbig"]:
                dayGroup.append("Plus_WBB_Medium")
            if indicators[2][i]>=self.fuzzylimits["wbbbig"]:
                dayGroup.append("Plus_WBB_Big")
            if indicators[2][i]<=(self.fuzzylimits["wbbbig"]*(-1)):
                dayGroup.append("Plus_WBB_Low") 
            if indicators[3][i]>=self.fuzzylimits["etabig"]:
                dayGroup.append("Plus_ETA_Big")
            elif indicators[3][i]<=(self.fuzzylimits["etabig"]*(-1)):
                dayGroup.append("ETA_MinusBig")
            else:
                dayGroup.append("ETA_Normal")
            self.groups.append(dayGroup)
    def save_rbs_obj_to_json(self):
        #assert(len(self.returns)==len(self.volumereturns)==len(self.wbb))
        #jsonObj=[]
        #wbbday=len(self.returns)-len(self.wbb)
        #j=0
        #if len(self.returns)!=len(self.wbb):
        #    print("UWAGA DLUGOSC TABLIC JEST ROZNA WBB {} PRICES {}".format(len(self.wbb),len(self.returns)))
        if len(self.returns)!=len(self.volatilitychange):
            print("UWAGA DLUGOSC TABLIC JEST ROZNA ETA {} PRICES {}".format(len(self.volatilitychange),len(self.returns)))
        assert(len(self.returns)==len(self.volumereturns)==len(self.volatilitychange))
        #print(self.__dict__)
        with open("indicators.json", "w") as write_file:
            json.dump(self.__dict__, write_file)
        #for i in range(len(self.returns)):
        #    dic={"pricedelta":self.returns[i], "volumedelta": self.volumereturns[i]}
        #    if i>=wbbday:
        #        dic["wbbdelta"]=self.wbb[j]
        #        j+=1
         #   jsonObj.append(dic)
        
        #for price in data:
    def find_in_groups(self, group):
        k=0
        for i in range(len(self.groups)):
            for j in range(len(self.groups[0])):
                if self.groups[i][j]==group: 
                    k+=1
                   #print("FOUND {} GROUP IN DELTA VALUE {} : {}".format(group,self.returns[i],self.volatilitychange[i]))
        #print("{} OCCURENCES OF GROUP {}".format(k,group))
    def load_from_file(self):
        with open('indicators.json','r') as ifile:
            objdic=json.load(ifile)
        #print(objdic['returns'])
        self.returns=objdic['returns']
        self.volumereturns=objdic['volumereturns']
        self.wbb=objdic['wbb']
        self.volatilitychange=objdic['volatilitychange']
        self.set_fuzzy_indicators()
    def make_decision(self,d):
        if len(d.split(' ')[1].split('_'))==2:
            demps=DempsterShaffer(d)
    def set_fuzzy_indicators(self):
        self.indicatorsmin={
            "price":min(self.returns),
            "volume":min(self.volumereturns),
            "wbb":min(self.wbb),
            "eta":min(self.volatilitychange)
        }
        self.indicatorsmax={
            "price":max(self.returns),
            "volume":max(self.volumereturns),
            "wbb":max(self.wbb),
            "eta":max(self.volatilitychange)
        }
        self.indicators={
            "price":self.returns,
            "volume":self.volumereturns,
            "wbb":self.wbb,
            "eta":self.volatilitychange
        }
        self.dempster=DempsterS(self.indicatorsmin, self.indicatorsmax,self.indicators)
