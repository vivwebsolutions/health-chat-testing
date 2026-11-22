from lib import *
import json
LLM='("large language model*"[tiab] OR ChatGPT[tiab] OR chatbot*[tiab] OR "generative AI"[tiab] OR Gemini[tiab] OR Copilot[tiab] OR OpenEvidence[tiab])'
H='(patient* OR health OR medical OR clinical)'
SR='("systematic review"[pt] OR "meta-analysis"[pt] OR "systematic review"[ti] OR "scoping review"[ti] OR "meta-analysis"[ti])'
Q=[
("sr",f'{LLM} AND {SR} AND {H} AND (accuracy OR quality OR performance OR evaluat*)',50),
("sr2",f'{LLM} AND {SR} AND (readability OR safety OR bias OR hallucinat* OR "patient education" OR "health information")',40),
("guide",'("large language model*"[tiab] OR chatbot*[tiab] OR ChatGPT[tiab] OR "generative AI"[tiab]) AND (reporting[ti] OR guideline*[ti] OR checklist[ti] OR framework[ti] OR "TRIPOD-LLM"[tiab] OR CHART[ti] OR METRICS[ti] OR QUEST[ti]) AND (health OR medical OR clinical OR healthcare)',50),
("bench",f'{LLM} AND (benchmark*[ti] OR HealthBench[tiab] OR "rubric"[ti]) AND {H}',30),
("read",f'{LLM} AND (readability[ti] OR "readability"[tiab]) AND {H}',30),
("safety",f'{LLM} AND (safety[ti] OR harm*[ti] OR "patient safety"[ti]) AND {H}',30),
("crisis",f'{LLM} AND (suicid*[tiab] OR crisis[ti] OR "mental health"[ti]) AND (response* OR evaluat* OR safety)',30),
("halluc",f'{LLM} AND (hallucinat*[ti] OR fabricat*[ti] OR misinformation[ti] OR "references"[ti] OR citation*[ti])',30),
("bias",f'{LLM} AND (bias*[ti] OR equity[ti] OR disparit*[ti])',25),
("lang",f'{LLM} AND (multilingual[ti] OR "non-English"[ti] OR Spanish[ti] OR Chinese[ti] OR Arabic[ti] OR languages[ti])',25),
("pq",f'{LLM} AND ("patient question*"[tiab] OR Reddit[tiab] OR "patient portal"[tiab] OR "public question*"[tiab] OR "frequently asked"[ti]) AND {H}',30),
("emerg",f'{LLM} AND (triage[ti] OR emergency[ti] OR "self-diagnosis"[ti] OR "symptom checker*"[ti])',30),
("emp",f'{LLM} AND (empath*[ti] OR compassion*[ti])',15),
("oe",'OpenEvidence[tiab] OR (Gemini[tiab] AND Copilot[tiab] AND ChatGPT[tiab] AND (patient* OR health))',30),
("judge",f'{LLM} AND ("LLM-as-a-judge"[tiab] OR "LLM as a judge"[tiab] OR "automated evaluation"[tiab] OR "evaluation framework"[ti])',25),
("consist",f'{LLM} AND (reproducib*[ti] OR repeatab*[ti] OR consisten*[ti])',20),
("spec",f'{LLM} AND (ChatGPT[ti] OR chatbot*[ti]) AND (oncology[ti] OR cardiology[ti] OR ophthalmology[ti] OR dermatology[ti] OR pediatric*[ti] OR orthop*[ti] OR urology[ti] OR dental[ti] OR pharmacy[ti] OR drug[ti] OR nutrition[ti] OR diabetes[ti] OR pregnancy[ti] OR vaccin*[ti] OR "cancer"[ti]) AND (accuracy[ti] OR quality[ti] OR reliability[ti] OR readability[ti] OR evaluat*[ti] OR comparison[ti] OR compar*[ti])',60),
("early",f'(ChatGPT[ti] OR "large language model*"[ti]) AND (accuracy[ti] OR quality[ti] OR appropriateness[ti] OR "health information"[ti]) AND medical',40),
]
cand={}
for k,q,n in Q:
    c,ids=search(q,retmax=n,sort="relevance")
    print(k,c,len(ids),flush=True)
    for i in ids: cand.setdefault(i,[]).append(k)
json.dump(cand,open("candidates.json","w"))
print(len(cand))
