from lib import *
import json
Q=[
'"framework for human evaluation of large language models in healthcare" ',
'METRICS checklist[tiab] AND generative AI[tiab] AND (healthcare OR medicine)',
'Ayers[au] AND ("physician and artificial intelligence chatbot responses" OR "patient questions")',
'"Large language models encode clinical knowledge"[ti]',
'"Evaluating the Performance of ChatGPT in Ophthalmology"[ti] OR "Appropriateness of Cardiovascular Disease Prevention Recommendations"[ti]',
'"Assessing the Accuracy and Reliability of AI-Generated Medical Responses"[ti]',
'"Assessment of Artificial Intelligence Chatbot Responses to Top Searched Queries About Cancer"[ti]',
'"Comparison of ChatGPT, Gemini"[ti] AND readability',
'"Evaluating Artificial Intelligence Responses to Public Health Questions"[ti]',
'"Evaluation of Oncology Clinical Decision-Making"[ti] OR "Use of Artificial Intelligence Chatbots for Cancer Treatment Information"[ti]',
'"Accuracy and Reliability of Chatbot Responses to Physician Questions"[ti]',
'"Performance of ChatGPT on suicide"[ti] OR "Evaluating the efficacy of large language models in responding to suicide"[ti] OR "Evaluation of Alignment Between Large Language Models and Expert Clinicians in Suicide Risk"[ti]',
'"Ethical and regulatory challenges of large language models in medicine"[ti] OR "The imperative for regulatory oversight of large language models"[ti]',
'(chatbot* OR "large language model*") AND "systematic review"[ti] AND (accuracy OR "health information" OR "patient education" OR "medical advice")',
'(chatbot* OR "large language model*") AND (assessment tools[ti] OR "evaluation metrics"[ti] OR "evaluation methods"[ti] OR "human evaluation"[ti])',
'"HealthBench"[tiab]',
'(chatbot* OR "large language model*") AND ("citation accuracy"[tiab] OR "fabricated references"[tiab] OR "reference accuracy"[tiab])',
'(chatbot* OR "large language model*") AND ("sycophancy"[tiab] OR "false premise"[tiab] OR "leading questions"[tiab])',
'(chatbot* OR "large language model*") AND ("988"[tiab] OR "crisis line"[tiab] OR "crisis resources"[tiab])',
'(chatbot* OR "large language model*") AND ("health literacy"[tiab]) AND (reading[tiab]) AND (systematic OR scoping)',
]
c=json.load(open("candidates.json")); new=[]
for q in Q:
    n,ids=search(q,retmax=12,sort="relevance"); print(n,len(ids),q[:60])
    for i in ids:
        if i not in c: c[i]=["extra"]; new.append(i)
json.dump(c,open("candidates.json","w")); json.dump(new,open("new.json","w")); print(len(new))
