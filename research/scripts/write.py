import json,re
from collections import Counter,defaultdict
F=json.load(open("final-pre.json"))
cache=json.load(open("abstracts-cache.json"))
KL={"systematic-review":"Review","guideline-framework":"Framework/guideline","benchmark":"Benchmark","evaluation-study":"Evaluation"}
PH={"quality/accuracy":"accuracy","quality/completeness":"completeness","quality/currency":"currency of information","quality/sources":"source/citation quality","quality/consistency":"consistency across runs","quality/uncertainty":"uncertainty handling","safety/harm":"harm/safety","safety/emergencies":"emergency/crisis handling","safety/scope":"scope/refusal behaviour","safety/false-premise":"false-premise/sycophancy robustness","safety/hallucination":"hallucination/misinformation","communication/readability":"readability","communication/empathy":"empathy","communication/actionability":"actionability/understandability","communication/language":"non-English/language handling","equity/bias":"bias/equity","equity/accessibility":"accessibility/health literacy","trust/privacy":"privacy","trust/transparency":"transparency/reporting","method/expert-rating":"expert rating","method/llm-judge":"LLM-as-judge","method/instrument":"validated instruments","method/real-questions":"real-user questions","method/guideline":"guideline-based reference"}
out=[]
for x in F:
    core=[PH[d] for d in x["dimensions"] if not d.startswith("method/")][:4]
    meth=[PH[d] for d in x["dimensions"] if d.startswith("method/")]
    ins=(" using "+", ".join(x["instruments"][:3])) if x["instruments"] else ""
    sub={"systematic-review":"Review synthesising evidence on LLM/chatbot health use","guideline-framework":"Proposes or reports a framework/reporting standard","benchmark":"Benchmarks models","evaluation-study":"Tests chatbot answers"}[x["study_kind"]]
    why=f"{sub} ({x['specialty']}); focus: {', '.join(core) or 'general performance'}{ins}"+(f"; method: {', '.join(meth)}" if meth else "")
    out.append(dict(pmid=x["pmid"],doi=x["doi"],title=x["title"],authors=x["authors"],journal=x["journal"],year=x["year"],study_kind=x["study_kind"],specialty=x["specialty"],dimensions=x["dimensions"],instruments=x["instruments"],why=why,pubtypes=x["pubtypes"]))
json.dump(out,open("papers.json","w"),indent=1,ensure_ascii=False)
print(Counter(p["study_kind"] for p in out)); 
dc=Counter(d for p in out for d in p["dimensions"]); print(dc.most_common(30))
ic=Counter(i for p in out for i in p["instruments"]); print(ic.most_common(30))
# gaps: candidate dims across all relevant candidates + curated
cands={
"cost/efficiency/latency":r"\bcost\b|latency|token usage|computational cost|inference time",
"prompt sensitivity/prompt engineering":r"prompt engineering|prompt (design|variation|sensitiv)|prompt strateg",
"model comparison / version drift":r"version(s)? of|model version|temporal|over time|drift|updated version",
"comparison with physician/human responses":r"compared (with|to) (physician|clinician|human|expert|specialist|doctor)|physician[- ]written|versus (physician|clinician|doctor|human)",
"comparison with web/Google search or traditional materials":r"google search|web ?site|traditional (patient )?(education|resources|materials)|online (resources|information)|search engine",
"tone / style / verbosity / length":r"word count|response length|verbos|\blength\b|concise|\btone\b",
"patient/user perception, satisfaction & trust (end-user)":r"satisfaction|perception|user experience|trust in|acceptab|usability|preferred",
"clinical reasoning / differential diagnosis":r"differential diagnos|clinical reasoning|diagnostic accuracy|diagnos",
"reading-level targeting (e.g. 6th grade) & text simplification":r"sixth[- ]grade|6th[- ]grade|simplif|reading level",
"image / multimodal input":r"multimodal|image|vision",
"RAG / grounding in guidelines":r"retrieval[- ]augmented|\bRAG\b|grounded|grounding",
"medication / drug interaction information":r"drug interaction|medication (information|question)|dosage|dosing|polypharmacy",
"cultural competence / cultural sensitivity":r"cultur",
"age/pediatric/caregiver-targeted answers":r"caregiver|parent[s]?\b|adolescen",
"legal/regulatory/liability/disclaimers":r"disclaimer|liabilit|regulat|FDA|medicolegal",
"conversational / multi-turn behaviour":r"multi-turn|multiturn|follow-up question|conversation(al)? (flow|quality)|dialogue",
"overconfidence / authoritative tone without caveats":r"overconfiden|authoritative|caveat|hedg",
"recommendation to seek professional care (referral)":r"seek (professional|medical)|consult (a|your) (doctor|physician|healthcare)|referral|recommend(ed|ing) (consult|seeing)",
"web search / browsing-enabled vs. offline":r"web[- ]search|browsing|internet access|search-enabled",
"Open-source vs. proprietary / regional (Chinese) models":r"deepseek|qwen|open-source|ernie|llama",
"duplication/identification of AI-written text":r"detect(ion|ing) (of )?(AI|ChatGPT)|AI-generated text detect|identify(ing)? ChatGPT",
"dose of harm severity grading (e.g. likelihood/extent of harm scales)":r"likelihood of harm|extent of harm|severity of harm|AHRQ|harm scale",
}
rel=[x for x in json.load(open("tagged-all.json")) if x["rel"]]
cnt={}
for k,rx in cands.items():
    m=[x["pmid"] for x in F if re.search(rx,x["title"]+" "+cache[x["pmid"]]["abstract"],re.I)]
    cnt[k]=m
instr_extra={"GQS (Global Quality Score)":r"global quality score|\bGQS\b","Modified DISCERN":r"modified DISCERN","SAM (Suitability Assessment of Materials)":r"suitability assessment of materials|\bSAM\b","CLEAR":r"\bCLEAR\b tool","DISCERN":r"DISCERN","PEMAT":r"PEMAT","Likert (any)":r"likert","Flesch-Kincaid":r"flesch","SMOG":r"SMOG","Gunning Fog":r"gunning","Coleman-Liau":r"coleman","ARI (Automated Readability Index)":r"automated readability","Cohen/Fleiss kappa":r"kappa","ICC":r"intraclass","Bland-Altman":r"bland","PDQI-9":r"PDQI","QUEST":r"\bQUEST\b","SQUIRE/other":r"SQUIRE","HealthBench":r"HealthBench","MedHELM":r"MedHELM","MultiMedQA/Med-PaLM":r"MultiMedQA|Med-PaLM","USMLE/MedQA":r"USMLE|MedQA","CHART":r"\bCHART\b","TRIPOD-LLM":r"TRIPOD","METRICS":r"\bMETRICS\b","PRISMA":r"PRISMA","PROBAST":r"PROBAST","QUADAS":r"QUADAS","AMSTAR":r"AMSTAR","GRADE":r"\bGRADE\b","Delphi consensus":r"delphi","CLEVER":r"\bCLEVER\b","Rubric-based grading":r"rubric"}
ic2={k:[x["pmid"] for x in F if re.search(rx,x["title"]+" "+cache[x["pmid"]]["abstract"],0 if k in("QUEST","CHART","METRICS","GRADE","CLEAR","SAM (Suitability Assessment of Materials)","CLEVER") else re.I)] for k,rx in instr_extra.items()}
with open("gaps.md","w") as f:
    f.write("# Gaps and instruments (n=%d curated papers; keyword tagging of title/abstract, so counts are approximate)\n\n"%len(F))
    f.write("Date: 2026-11-21. Tags were assigned by regex over title+abstract (not manual reading); treat counts as indicative.\n\n")
    f.write("## Dimensions measured but not in our list\n\n| Candidate dimension | Papers | Example PMIDs |\n|---|---|---|\n")
    for k,m in sorted(cnt.items(),key=lambda kv:-len(kv[1])):
        f.write(f"| {k} | {len(m)} | {', '.join(m[:5])} |\n")
    f.write("\n## Named instruments / frameworks / benchmarks mentioned\n\n| Instrument | Papers | Example PMIDs |\n|---|---|---|\n")
    for k,m in sorted(ic2.items(),key=lambda kv:-len(kv[1])):
        if m: f.write(f"| {k} | {len(m)} | {', '.join(m[:5])} |\n")
    f.write("\n## Dimension counts in our list\n\n| Dimension | Papers |\n|---|---|\n")
    for d,c in dc.most_common(): f.write(f"| {d} | {c} |\n")
print({k:len(v) for k,v in cnt.items()}); print({k:len(v) for k,v in ic2.items() if v})
