import json,re,random
from collections import Counter
pool=json.load(open("pool.json")); allr={x["pmid"]:x for x in json.load(open("tagged-all.json"))}
EX=set("""41512731 41481915 41313175 37798296 41401240 41128430 40662463 42752479 41406368 40225559 41232097 38553693 41014309 40153782 40549427 41367594 38486402 37868075 41444884 38412023 38631422 39626235 37353578 41195352 41250109 35029538 35704383 32673216 31622850 38934788 39953464 39911020 39523628 40582721 42139691 39983102 38733640 36981544
42160710 40251634 40084448 41551040 39860820 41871866 37886027 41243110 41359706 40258342 40188094 41145883 40715040 42830368 38857745 40745595 40753040 42337008 40802997 41148324 39198112 39383705 41479969 37832818 41300923 40380434 39248448 40417557 40147615 38012986 41032743 32876349 40588891 39320544 41413824 42310130 42527439 41719483 42338520 41769785 39310414""".split())
KIND={"39405325":"systematic-review","39614219":"systematic-review","42618044":"systematic-review","40360677":"guideline-framework","39747685":"guideline-framework","38553625":"guideline-framework","41742713":"guideline-framework","34719011":"guideline-framework","37957381":"guideline-framework","41343765":"guideline-framework","42527491":"guideline-framework","38276872":"guideline-framework","40747871":"guideline-framework","39779929":"guideline-framework","41143093":"benchmark","42978863":"benchmark","42286322":"benchmark",
"41420748":"evaluation-study","42747529":"evaluation-study","41731097":"evaluation-study","39057156":"evaluation-study","41410329":"evaluation-study","37693201":"evaluation-study","41985209":"evaluation-study","38378899":"evaluation-study","37722842":"evaluation-study","39854615":"evaluation-study","41865615":"evaluation-study","41311033":"evaluation-study","39283333":"evaluation-study","40775964":"evaluation-study","37927093":"evaluation-study","41464727":"evaluation-study","40007763":"evaluation-study","39697584":"evaluation-study","38111813":"evaluation-study","40238861":"evaluation-study","40625933":"evaluation-study","41129154":"evaluation-study","39443664":"evaluation-study","40680485":"guideline-framework","42546264":"systematic-review"}
sel=[];seen=set()
for x in pool:
    if x["pmid"] in EX: continue
    if x["pmid"] in KIND: x["study_kind"]=KIND[x["pmid"]]
    sel.append(x); seen.add(x["pmid"])
for p in KIND:
    if p not in seen and p in allr and p not in EX: allr[p]["study_kind"]=KIND[p]; allr[p]["score"]=5; sel.append(allr[p]); seen.add(p)
pri=[x for x in sel if x["study_kind"]!="evaluation-study"]
ev=[x for x in sel if x["study_kind"]=="evaluation-study"]
print(len(pri),len(ev),Counter(x["study_kind"] for x in pri))
json.dump({"pri":pri,"ev":ev},open("sel.json","w"))
for x in ev: print(x["pmid"],x["year"],x["specialty"][:14],"|",x["title"][:95])
