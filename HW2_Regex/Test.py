from ProductCharacteristicsExteractor import *
import json
class Test:
    def runTest():
        fp=open('Testsamples.json', 'r') 
        obj = json.load(fp)
        count=len(obj)
        correct=0
        for i in obj:
            t=ProductCharacteristicsExteractor(i["inputcomment"])
            if t==i["output"]:
                correct=correct+1
        return correct/count