import json,re
recs=json.load(open("abstracts-cache.json")); cand=json.load(open("candidates.json"))
D={
"quality/accuracy":r"accura|correctness|appropriateness|concordan|agreement with",
"quality/completeness":r"complete(ness)?\b|comprehensive",
"quality/currency":r"up-to-date|outdated|currency|knowledge cutoff|recent guideline",
"quality/sources":r"citation|reference[s]? (were|was|generated|accuracy)|fabricated reference|source attribution|references?\b.{0,40}(fabricat|valid|verif|real)|provenance|retrieval-augmented|\bRAG\b",
"quality/consistency":r"consistency|reproducib|repeatab|stability|run-to-run|test-retest|intra-?rater|variability (in|across|between) (responses|outputs|runs)",
"quality/uncertainty":r"uncertaint|calibrat|confidence|hedg",
"safety/harm":r"harm(ful|s)?\b|safety|unsafe|dangerous|potentially (dangerous|harmful)",
"safety/emergencies":r"emergenc|crisis|suicid|988|911|triage|self-harm|urgent",
"safety/scope":r"refus|over-?refus|decline|scope|guardrail",
"safety/false-premise":r"false premise|incorrect premise|misleading prompt|sycophan|adversarial|jailbreak|misinformation prompt|leading question",
"safety/hallucination":r"hallucinat|fabricat|confabulat|misinformation",
"communication/readability":r"readab|flesch|reading level|grade level|lexile|SMOG|plain language|health literacy",
"communication/empathy":r"empath|compassion|bedside|tone",
"communication/actionability":r"actionab|understandab|PEMAT|usab|patient education",
"communication/language":r"multilingual|non-english|spanish|chinese|arabic|language[s]? other|low-resource|translation|languages",
"equity/bias":r"(?<!risk of )(?<!publication )(?<!selection )\bbias(es)?\b(?! tool)|disparit|fairness|stereotyp|racial|\brace\b|equity|demographic",
"equity/accessibility":r"accessib|health literacy|low literacy|underserved|disabilit|visually impaired|digital divide",
"trust/privacy":r"privacy|confidential|HIPAA|data protection|data security",
"trust/transparency":r"transparen|explainab|interpretab|disclos|trustworth|reporting (guideline|standard|checklist)",
"method/expert-rating":r"expert|specialist|physician[s]? (rated|graded|evaluat|reviewed)|clinician[s]? (rated|graded|evaluat)|blinded|reviewers?\b|raters?\b|graded by|rated by|independent(ly)? (assessed|evaluated|reviewed)",
"method/llm-judge":r"LLM-as-a-judge|LLM as a judge|model-graded|automated (evaluation|scoring|grading)|GPT-4 (as|was used to) (judge|grade|evaluat|rate)|judge model|AI grader",
"method/instrument":r"DISCERN|PEMAT|flesch|likert|\bGQS\b|global quality score|JAMA benchmark|SMOG|gunning|coleman|QUEST|SERVQUAL|\bEQIP\b|HONcode|ROBIS|PROBAST|QUADAS|AMSTAR|\bGRADE\b|rubric",
"method/real-questions":r"reddit|patient portal|real[- ](world )?(patient|questions|queries)|public (question|queries)|NLM|consumer questions|frequently asked|google trends|people also ask|patient[- ]generated|online forum|social media (post|question)|ask(ed)? (by|from) (patients|the public)|patient messages|patient inquir",
"method/guideline":r"guideline|consensus statement|recommendation[s]? (from|of) |NCCN|ACOG|AHA|ASCO|AAO|society (guideline|recommendation)|evidence-based|clinical practice guideline",
}
INS={"DISCERN":r"DISCERN","PEMAT":r"PEMAT","Flesch Reading Ease":r"flesch reading ease|\bFRE\b","Flesch-Kincaid Grade Level":r"flesch[- ]kincaid|\bFKGL\b|\bFKRL\b",
"SMOG":r"\bSMOG\b","Gunning Fog":r"gunning|fog index","Coleman-Liau":r"coleman","Likert scale":r"likert","Global Quality Score":r"global quality score|\bGQS\b",
"JAMA benchmark":r"JAMA benchmark","HONcode":r"HONcode|health on the net","EQIP":r"\bEQIP\b","QUEST":r"\bQUEST\b","CHART":r"\bCHART\b","TRIPOD-LLM":r"TRIPOD[- ]LLM","METRICS":r"\bMETRICS\b",
"PROBAST":r"PROBAST","QUADAS":r"QUADAS","ROBIS":r"\bROBIS\b","AMSTAR":r"AMSTAR","GRADE":r"\bGRADE\b","PRISMA":r"PRISMA","HealthBench":r"HealthBench","MedQA/USMLE":r"MedQA|USMLE","MultiMedQA":r"MultiMedQA|Med-PaLM",
"SQuAD/BLEU/ROUGE":r"\bBLEU\b|\bROUGE\b|BERTScore","Cohen/Fleiss kappa":r"kappa","ICC":r"intraclass|\bICC\b","SERVQUAL":r"SERVQUAL","Lexile":r"lexile","CLEAR tool":r"CLEAR tool|\bCLEAR\b","PDQI-9":r"PDQI","DISCERN-like/modified DISCERN":r"modified DISCERN","SUS":r"system usability scale","Rubric":r"rubric","Bloom taxonomy":r"bloom"}
def kind(r):
    t=r["title"].lower(); pt=" ".join(r["pubtypes"]).lower(); a=r["abstract"].lower()
    if re.search(r"systematic review|meta-analysis|scoping review|umbrella review|narrative review|\breview\b",t) or "systematic review" in pt or "meta-analysis" in pt: 
        if re.search(r"review|meta-analysis",t+pt): return "systematic-review"
    if re.search(r"guideline|reporting|checklist|framework|consensus|recommendations|standard|tripod|\bchart\b|\bmetrics\b|\bquest\b|delphi|taxonomy|tool for",t) or "practice guideline" in pt: return "guideline-framework"
    if re.search(r"benchmark|healthbench|dataset|leaderboard",t): return "benchmark"
    if re.search(r"compar|evaluat|assess|accura|quality|reliab|readab|performance|appropriat|response|answer|test",t+" "+a[:300]): return "evaluation-study"
    return "other"
SP={"oncology/cancer":r"oncolog|cancer|tumou?r|chemotherap","cardiology":r"cardi|heart|hypertens","ophthalmology":r"ophthalm|eye|cataract|myopia|retina|glaucoma","dermatology":r"dermat|skin|melanoma","pediatrics":r"pediatric|paediatric|child","orthopedics":r"orthop|arthroplast|fracture|spine|sports","urology":r"urolog|prostat|kidney","dentistry":r"dental|dentist|orthodont|endodon|periodon","pharmacy/drugs":r"pharmac|drug|medication","mental health":r"mental|suicid|depress|psychiat|anxiety","diabetes/endocrine":r"diabet|endocrin|thyroid","obstetrics/gynecology":r"pregnan|obstet|gyne|maternal|contracept|fertility|menopaus","radiology":r"radiolog|imaging","surgery":r"surg(ery|ical)","ENT":r"otolaryng|\bENT\b|hearing|sinus|tonsil","infectious disease/vaccines":r"vaccin|infect|HIV|covid","neurology":r"neurolog|stroke|dementia|alzheimer|epilep","gastroenterology":r"gastro|liver|colonoscop|hepat|bowel","nutrition":r"nutrition|diet","emergency medicine":r"emergency|triage"}
out=[];
for p,r in recs.items():
    txt=r["title"]+" "+r["abstract"]
    dims=[d for d,rx in D.items() if re.search(rx,txt,re.I if d!="method/instrument" else re.I)]
    ins=[k for k,rx in INS.items() if re.search(rx,txt,0 if k in("QUEST","CHART","METRICS","GRADE","CLEAR tool","ICC","FRE") else re.I)]
    if "method/instrument" in dims and not ins and not re.search("likert|rubric",txt,re.I): dims.remove("method/instrument")
    if ins and "method/instrument" not in dims: dims.append("method/instrument")
    sp=[k for k,rx in SP.items() if re.search(rx,r["title"]+" "+r["abstract"][:600],re.I)]
    r2=dict(r); r2.update(study_kind=kind(r),specialty=sp[0] if len(sp)==1 else ("; ".join(sp[:2]) if sp else "general"),dimensions=dims,instruments=ins,queries=cand[p])
    # relevance
    rel=bool(re.search(r"chatgpt|large language|llm|chatbot|generative|gpt|gemini|copilot|openevidence|claude|llama",txt,re.I)) and bool(re.search(r"health|medic|patient|clinical|disease|cancer|care",txt,re.I))
    ev=bool(re.search(r"accura|quality|evaluat|assess|reliab|readab|compar|performance|safety|appropriat|bias|hallucin|benchmark|guideline|framework|reporting",txt,re.I))
    r2["rel"]=rel and ev
    out.append(r2)
json.dump(out,open("tagged-all.json","w"))
from collections import Counter
print(Counter(o["study_kind"] for o in out if o["rel"]), sum(o["rel"] for o in out))
