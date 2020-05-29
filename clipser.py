import clips

env=clips.Environment()

class Clipser:
    def __init__(self,facts):
        env.load("rulebased\defrules.clp")
        self.facts=facts
        self.decisions=[]
        self.index=0
    def start(self):
        for f in self.facts:
            self.assert_fact(f)
            self.index+=1
    def assert_fact(self,facts):
        for fact in facts:
            factarr=fact.split('_')
            command="(delta{} {})".format(factarr[-2].lower(),factarr[-1].lower())
            #print(command)
            env.assert_string(command)
        decision=self.return_decision()
        self.decisions+= [decision] if decision is not None else []
        env.reset()
    def return_decision(self):
        env.run()
        decisions=[]
        decision= [str(f) for f in env.facts()]
        if decision[-1].split(" ")[0]=='(price_decision' or decision[-1].split(" ")[0]=='(eta_decision':
            decisions.append(decision[-1])
        if decision[-2].split(" ")[0]=='(price_decision' or decision[-2].split(" ")[0]=='(eta_decision':
            decisions.append(decision[-2])
        if len(decisions)!=0: return decisions+[self.index]
    def return_decisions(self):
        return self.decisions