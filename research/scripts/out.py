import json,re
from collections import Counter
S=json.load(open("sel.json")); pri,ev=S["pri"],S["ev"]
X=set("39625719 42712533 40969781 40745627 42259903 34690656 39451358 40882613 42631512 40943770 38432929 39176994 37949111 40408109 41639446 40986301 38778332 39405330 39187702 40874763 38976267 37581690 41418321 37671415 39098369 38801461 41552655 38135548 42223976 40975905 40997804 39228001 40385687 38511501 39202267 40140500 39857105 39121263 38483451 40588883 38153778 38705894 39793700 42421134 39667051 38593984 41965213 40033814 41078673 38432929 41289178 42450919".split())
ev=[x for x in ev if x["pmid"] not in X]
# diversity: round-robin by specialty over score-sorted
ev.sort(key=lambda x:-x["score"])
need=150-len(pri); 
by={}
for x in ev: by.setdefault(x["specialty"].split(";")[0],[]).append(x)
pick=[]
while len(pick)<need and any(by.values()):
    for k in list(by):
        if by[k] and len(pick)<need: pick.append(by[k].pop(0))
final=pri+pick
def why(x):
    return None
json.dump(final,open("final-pre.json","w"))
print(len(final),Counter(x["study_kind"] for x in final))
for x in final: print(x["pmid"],x["study_kind"][:3],x["year"],x["specialty"][:12],"|",x["title"][:80],"|",",".join(d.split("/")[1][:6] for d in x["dimensions"]))
