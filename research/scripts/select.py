import json,re
o=json.load(open("tagged-all.json"))
EXC=r"extraction|synthetic|summariz|knowledge graph|phenotyp|\bdataset\b|traditional chinese medicine|randomi[sz]ed|\bEHR\b|electronic health record|data harmoni|image|segmentation|PET|genom|single-cell|drug response|pathology report|code generation|ExoGAN|recipe|nursing diagnos|prediction|mortality|clinical notes|documentation|scribe|ambient|survey study|editorial|erratum"
INC=r"patient|public|consumer|health information|medical advice|health advice|health question|responses? to|answer|chatbot|queries|questions|readab|recommendation"
sel=[]
for x in o:
    if not x["rel"]: continue
    t=x["title"]
    if re.search(EXC,t,re.I) and x["study_kind"] not in("guideline-framework",): 
        if not re.search("review|framework|guideline|reporting",t,re.I): continue
    if "Editorial" in x["pubtypes"] and x["study_kind"]!="guideline-framework": continue
    if "Preprint" in x["pubtypes"]: continue
    txt=t+" "+x["abstract"]
    if not re.search(INC,txt,re.I): continue
    if not x["abstract"] and x["study_kind"]!="guideline-framework": continue
    s=0
    s+={"systematic-review":6,"guideline-framework":6,"benchmark":4,"evaluation-study":2,"other":0}[x["study_kind"]]
    s+=len(x["dimensions"])*0.3+len(x["instruments"])*0.3
    s+=1 if len(x["queries"])>1 else 0
    if re.search("systematic|meta-analysis|scoping",t,re.I): s+=2
    if re.search(r"chatgpt|gemini|copilot|openevidence|claude|llama|chatbot",t,re.I): s+=0.5
    x["score"]=s; sel.append(x)
sel.sort(key=lambda x:-x["score"])
json.dump(sel,open("pool.json","w"))
from collections import Counter
print(len(sel),Counter(x["study_kind"] for x in sel))
for x in sel:
    if x["study_kind"] in("systematic-review","guideline-framework","benchmark","other"): print(x["pmid"],x["study_kind"][:4],x["year"],x["title"][:105])
