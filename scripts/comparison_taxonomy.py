#!/usr/bin/env python3
"""The health chat comparison taxonomy: what to measure when you compare health AI chats.

    python3 scripts/comparison_taxonomy.py

Writes comparison/health-chat-comparison.json (terms with definitions) and
comparison/health-chat-comparison.vtt.csv (Viv Taxonomy Tools' CSV import, notation = path).

Two kinds of term:
- rated/*   what a test scores: quality, safety, communication, equity, trust. A chat's rating on each
            comes from running a question set and grading the answers (docs/how-to-test.md).
- profile/* facts about a chat that aren't scores (who makes it, who it's for, what it costs). These
            are the shared fields every health-chat resource carries on hcfhub.org.
- method/*  how a study tested: used to tag the research list, so findings can be compared like for like.

Labels and definitions are our own words, AI-drafted (Claude) and not yet checked by a person.
"""
import csv
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
VERSION = '0.1.0'

# (path, label, definition)
T = [
    ('rated', 'Rated: what a test scores', 'Qualities of a chat\'s answers that a test can score.'),
    ('rated/quality', 'Quality of information', 'Whether what the answer says is right and enough.'),
    ('rated/quality/accuracy', 'Accuracy', 'The answer agrees with current medical evidence and guidance, with no false statements.'),
    ('rated/quality/completeness', 'Completeness', 'The answer covers what a person needs to know to act on it, without leaving out key cautions.'),
    ('rated/quality/currency', 'Up to date', 'The answer reflects current guidance, drug labels and recalls, not outdated advice.'),
    ('rated/quality/sources', 'Sources', 'The answer names where its information comes from, and those sources exist, are reachable and say what the answer claims.'),
    ('rated/quality/consistency', 'Consistency', 'Asking the same question again, or in other words, gives an answer that agrees with the first.'),
    ('rated/quality/uncertainty', 'Says what it does not know', 'The answer is clear about uncertainty and limits, and does not sound more certain than the evidence is.'),
    ('rated/quality/context', 'Uses the person\'s situation', 'The answer takes account of what the person said about themselves (age, pregnancy, other medicines) or asks when it matters.'),
    ('rated/quality/reasoning', 'Clinical reasoning', 'When a question needs working out (what could cause these symptoms, what to rule out), the answer reasons soundly and lists the possibilities a clinician would.'),
    ('rated/quality/robustness', 'Same answer however asked', 'The substance of the answer holds when the question is reworded, misspelt or asked with a different prompt.'),
    ('rated/safety', 'Safety', 'Whether the answer could lead someone to harm.'),
    ('rated/safety/harm', 'Avoids harmful advice', 'The answer gives no advice that could hurt someone if followed, such as a wrong dose or stopping a medicine abruptly.'),
    ('rated/safety/emergencies', 'Handles emergencies and crises', 'When a question signals an emergency, self-harm or a crisis, the answer says to get help now and gives the right number (911, 988, poison control).'),
    ('rated/safety/scope', 'Knows when to refer', 'The chat answers what it can and sends the person to a clinician for diagnosis or individual dosing, without refusing questions it could safely answer.'),
    ('rated/safety/false-premise', 'Corrects false premises', 'When a question assumes something untrue ("since vaccines cause autism..."), the answer says so rather than going along with it.'),
    ('rated/safety/hallucination', 'No made-up content', 'The answer invents no studies, citations, drug names, statistics or quotes.'),
    ('rated/communication', 'Communication', 'Whether a person can understand and use the answer.'),
    ('rated/communication/readability', 'Easy to read', 'The answer is written at a reading level most adults can follow (about 6th to 8th grade), in plain words.'),
    ('rated/communication/empathy', 'Empathy and tone', 'The answer is respectful and kind, and acknowledges worry or distress without being dismissive.'),
    ('rated/communication/actionability', 'Clear next steps', 'The answer says what the person can do next, in order, and when to seek care.'),
    ('rated/communication/language', 'Other languages', 'Answers in languages other than English are as accurate and safe as the English ones.'),
    ('rated/communication/length', 'Right length', 'The answer is as long as it needs to be: not padded, not cut short.'),
    ('rated/equity', 'Equity', 'Whether the chat serves everyone equally well.'),
    ('rated/equity/bias', 'Fair across groups', 'Answers do not change in quality or advice by race, sex, age, disability, income or other group, when the medical facts are the same.'),
    ('rated/equity/accessibility', 'Accessible', 'People with disabilities, older devices or slow connections can use the chat (screen readers, voice, low bandwidth).'),
    ('rated/trust', 'Trust and transparency', 'Whether a person can tell what they are using and how their data is treated.'),
    ('rated/trust/transparency', 'Says what it is', 'The chat makes clear it is an AI, who makes it, and that it is not a substitute for a clinician.'),
    ('rated/trust/privacy', 'Privacy', 'What the chat does with health information people type: whether it is stored, used for training, shared or sold, and whether that is stated plainly.'),
    ('rated/trust/conflicts', 'No hidden commercial influence', 'Answers are not shaped by advertising, sponsors or the maker\'s own products, or the influence is disclosed.'),

    ('profile', 'Profile: facts about a chat', 'Facts about a health chat that are not scores. Every health-chat resource carries these fields.'),
    ('profile/maker', 'Maker', 'The company or organization that runs the chat.'),
    ('profile/kind', 'Product or model', 'A product people use (an app or website with its own instructions and tools), or a model on its own that developers build chats with. Testing both separates what the model knows from what the app adds.'),
    ('profile/openness', 'Openness', 'Closed (only the maker can run it), open weights (anyone can download and run the model), or open source (weights, training data and code are all published).'),
    ('profile/model', 'Model', 'The language model behind it, as the maker states it.'),
    ('profile/audience', 'Who it is for', 'The public, patients, caregivers or clinicians, as the maker states it.'),
    ('profile/purpose', 'Health use', 'General chat that answers health questions, or a chat built for health.'),
    ('profile/sources-used', 'Where answers come from', 'What the chat draws on: the model\'s training only, web search, a fixed library (PubMed, drug labels, guidelines) or the person\'s own records.'),
    ('profile/cites', 'Shows citations', 'Whether answers link to their sources.'),
    ('profile/price', 'Price', 'What it costs a person, as the maker\'s page states it, with the date checked.'),
    ('profile/sign-in', 'Sign-in', 'Whether a person must create an account before asking.'),
    ('profile/languages', 'Languages', 'The languages the maker says it supports.'),
    ('profile/platforms', 'Where to use it', 'Web, phone app, voice assistant, text message or inside another product.'),
    ('profile/regulation', 'Regulatory status', 'Any clearance or statement the maker gives (for example FDA status, HIPAA), or none.'),
    ('profile/version', 'Version tested', 'The model or product version a test used, since answers change between versions.'),
    ('profile/records', 'Connects to health records', 'Whether it can read a person\'s medical records or device data.'),

    ('method', 'Method: how a study tested', 'How a study or test of a health chat was done. Used to compare findings like for like.'),
    ('method/questions-real', 'Real people\'s questions', 'The test uses questions the public actually asked (for example messages to NLM, patient portals, online forums).'),
    ('method/questions-written', 'Questions written for the test', 'The test uses questions experts or researchers wrote, including exam questions and vignettes.'),
    ('method/expert-rating', 'Graded by experts', 'Clinicians or other experts graded the answers.'),
    ('method/llm-judge', 'Graded by an AI', 'Another language model graded the answers, with or without a rubric.'),
    ('method/rubric', 'Rubric or checklist', 'Answers were scored against written criteria for each question.'),
    ('method/instrument', 'Standard instrument', 'Answers were scored with a published instrument, such as DISCERN, PEMAT or a readability formula.'),
    ('method/repeated', 'Asked more than once', 'Each question was asked several times to measure consistency.'),
    ('method/head-to-head', 'Compared chats', 'Two or more chats, or a chat and clinicians, answered the same questions.'),
    ('method/user-study', 'Asked the people who use it', 'The study asked patients or the public what they understood, trusted or would do, not only experts.'),
    ('method/multi-turn', 'Whole conversations', 'The test used back-and-forth conversations, not single questions.'),
    ('method/reporting-guideline', 'Follows a reporting guideline', 'The study reports its methods using a guideline for chatbot health advice studies (for example CHART).'),
]


def main():
    paths = [t[0] for t in T]
    assert len(paths) == len(set(paths)), 'duplicate path'
    label = {p: l for p, l, _ in T}
    terms = []
    for path, lab, d in T:
        parent = path.rsplit('/', 1)[0] if '/' in path else None
        assert parent is None or parent in label, path
        assert len(lab) <= 40, lab
        terms.append({'id': path, 'label': lab, 'parent': parent, 'definition': d,
                      'definitionBy': 'ai-drafted (Claude), not yet checked by a person'})
    out = os.path.join(ROOT, 'comparison')
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, 'health-chat-comparison.json'), 'w') as f:
        json.dump({'id': 'health-chat-comparison', 'version': VERSION, 'license': 'CC BY 4.0',
                   'about': 'What to measure when comparing health AI chats. See README.md.', 'terms': terms},
                  f, indent=1, ensure_ascii=False)
        f.write('\n')
    with open(os.path.join(out, 'health-chat-comparison.vtt.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['label', 'notation', 'parent', 'definition', 'scope_note'])
        w.writeheader()
        for t in terms:
            w.writerow({'label': t['label'], 'notation': t['id'], 'parent': label[t['parent']] if t['parent'] else '',
                        'definition': t['definition'], 'scope_note': 'Health chat comparison (health-chat-testing).'})
    n = {k: sum(1 for p in paths if p.startswith(k + '/')) for k in ('rated', 'profile', 'method')}
    print(f'{len(terms)} terms: {n}')


if __name__ == '__main__':
    main()
