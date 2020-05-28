from statistics import stdev as sd
class SimpleIndicators:
    def __init__(self,data,ma_n):
        self.ma_n=ma_n
        self.volumes=[i['volume'] for i in data]
        self.prices=[i['close'] for i in data]
        self.low=[i['low'] for i in data]
        self.high=[i['high'] for i in data]
        self.size=len(self.prices)
        self.madic={}
        self.sddic={}
    def returns(self):
        deltas=[self.prices[i+1]-self.prices[i] for i in range(self.size-1)]
        return deltas
    def volumereturns(self):
        deltas=[self.volumes[i+1]-self.volumes[i] for i in range(len(self.volumes)-1)]
        return deltas
    def deltawbb(self):
        deltas=[self.wbb(i+1)-self.wbb(i) for i in range(self.size-1,self.ma_n,-1)]
        return deltas
    def wbb(self,i):
        #domain=self.prices[i-self.ma_n:]
        #domainsd=sd(domain)
        #if i in self.sddic:
        #    sdval=self.sddic[i]
        #else:
        #    sdval=sd(domain)
        #    self.sddic[i]=sdval
        if i in self.madic:
            ma=self.madic[i]
        else:
            ma=self.ma(self.ma_n,i)
            self.madic[i]=ma
        print("MOVING AVERAGES: ", ma)
        return (ma[-1]+sd(ma))-(ma[-1]-sd(ma))
        #return (ma+2*domainsd)-(ma-2*domainsd)
    def ma(self,n,j):
        i=j-n+1
        ma=[]
        while i<j and i>0:
            window=self.prices[i:j]
            print(window, " i: {} j: {}".format(i,j))
            windowavg=sum(window)/len(window)
            ma.append(windowavg)
            i+=1
        return ma
    def volatility_change(self):
        vol_change=[ ((self.low[i]+self.high[i])-(self.low[i-1]+self.high[i-1]))/2 for i in range(1,len(self.low)) ]
        return vol_change