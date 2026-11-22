from lib import *
import json
LLM='("large language model*"[tiab] OR ChatGPT[tiab] OR chatbot*[tiab] OR "generative AI"[tiab])'
H='(patient* OR health OR medical)'
Q={
"core":f'{LLM} AND (accuracy OR quality OR evaluat* OR reliab* OR readab*) AND {H}',
"llm_any":LLM,
"readability":f'{LLM} AND (readability[tiab] OR "Flesch"[tiab] OR "reading level"[tiab] OR "grade level"[tiab]) AND {H}',
"safety_harm":f'{LLM} AND (safety[tiab] OR harm*[tiab] OR "patient safety"[tiab]) AND {H}',
"mental_health_crisis":f'{LLM} AND ("mental health"[tiab] OR suicid*[tiab] OR crisis[tiab]) AND (safety OR response* OR evaluat* OR accuracy)',
"misinformation_hallucination":f'{LLM} AND (misinformation[tiab] OR hallucinat*[tiab] OR fabricat*[tiab]) AND {H}',
"bias_equity":f'{LLM} AND (bias*[tiab] OR equity[tiab] OR disparit*[tiab] OR fairness[tiab]) AND {H}',
"non_english":f'{LLM} AND (multilingual[tiab] OR "non-English"[tiab] OR Spanish[tiab] OR Chinese[tiab] OR Arabic[tiab] OR "low-resource"[tiab]) AND {H}',
"systematic_reviews":f'{LLM} AND (systematic[sb] OR "systematic review"[pt] OR "meta-analysis"[pt] OR "scoping review"[tiab]) AND {H}',
"reporting_guidelines":'(CHART[tiab] OR "TRIPOD-LLM"[tiab] OR QUEST[tiab] OR METRICS[tiab]) AND ("large language model*"[tiab] OR chatbot*[tiab] OR ChatGPT[tiab]) AND (reporting OR checklist OR framework OR guideline*)',
"citations_references":f'{LLM} AND (citation*[tiab] OR reference*[tiab] OR "source attribution"[tiab]) AND (fabricat* OR accuracy OR valid* OR verif*) AND {H}',
"consistency_repeatability":f'{LLM} AND (reproducib*[tiab] OR repeatab*[tiab] OR consisten*[tiab]) AND (response* OR output*) AND {H}',
"emergency_triage":f'{LLM} AND (triage[tiab] OR emergency[tiab] OR "emergency department"[tiab]) AND {H}',
"empathy":f'{LLM} AND (empath*[tiab] OR compassion*[tiab]) AND (patient* OR physician*)',
"patient_questions":f'{LLM} AND ("patient question*"[tiab] OR "patient portal"[tiab] OR Reddit[tiab] OR "frequently asked question*"[tiab]) AND {H}',
"openevidence":'OpenEvidence[tiab]',
"llm_as_judge":f'{LLM} AND ("LLM-as-a-judge"[tiab] OR "LLM as a judge"[tiab] OR "automated evaluation"[tiab] OR "model-graded"[tiab])',
"benchmark":f'{LLM} AND (benchmark*[tiab] OR HealthBench[tiab]) AND {H}',
"DISCERN_PEMAT":f'{LLM} AND (DISCERN[tiab] OR PEMAT[tiab] OR "Global Quality Score"[tiab] OR "JAMA benchmark"[tiab])',
}
out={"date":"2026-11-21","database":"PubMed","queries":{}}
for k,q in Q.items():
    c,_=search(q); out["queries"][k]={"query":q,"count":c}; print(k,c,flush=True)
json.dump(out,open("counts.json","w"),indent=1)
