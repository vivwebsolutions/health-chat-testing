#!/usr/bin/env python3
"""Check every submitted run before it's merged (CI runs this on pull requests).

    python3 scripts/validate.py

A run folder runs/<date>-<chat>[-<who>]/ needs run.json, answers.jsonl and grades.jsonl. This checks the
fields, that every question id exists, that grades match answers, that no secret is in the files, and that the
leaderboard files are what scripts/aggregate.py makes from the runs.
"""
import csv
import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SECRET = re.compile(r'(sk-[A-Za-z0-9_-]{20,}|Bearer\s+[A-Za-z0-9._-]{20,}|AIza[0-9A-Za-z_-]{30,}|xai-[A-Za-z0-9]{20,})')


def main():
    errs = []
    chats = {r['id'] for r in csv.DictReader(open(os.path.join(ROOT, 'chats', 'health-chats.csv')))}
    ids = {q['id'] for q in json.load(open(os.path.join(ROOT, 'questions', 'health-consumer-questions.json')))['questions']}
    ids |= {q['id'] for q in json.load(open(os.path.join(ROOT, 'questions', 'hard-cases.json')))['questions']}
    for d in sorted(glob.glob(os.path.join(ROOT, 'runs', '*'))):
        name = os.path.basename(d)
        for fn in ('run.json', 'answers.jsonl', 'grades.jsonl'):
            p = os.path.join(d, fn)
            if not os.path.exists(p):
                errs.append(f'{name}: missing {fn}')
            elif SECRET.search(open(p).read()):
                errs.append(f'{name}/{fn}: looks like it contains an API key; remove it and rotate the key')
        if errs and errs[-1].startswith(name + ': missing'):
            continue
        meta = json.load(open(os.path.join(d, 'run.json')))
        for k in ('chat', 'date', 'how', 'submittedBy'):
            if not meta.get(k):
                errs.append(f'{name}/run.json: needs "{k}"')
        if meta.get('chat') not in chats:
            errs.append(f'{name}: chat "{meta.get("chat")}" is not in chats/health-chats.csv (add it there first)')
        answers = [json.loads(l) for l in open(os.path.join(d, 'answers.jsonl'))]
        grades = [json.loads(l) for l in open(os.path.join(d, 'grades.jsonl'))]
        for a in answers:
            if a.get('id') not in ids:
                errs.append(f'{name}: unknown question id {a.get("id")}')
            if 'answer' not in a and 'error' not in a:
                errs.append(f'{name}: answer {a.get("id")} has no answer text')
        if {(g['id'], g['try']) for g in grades} - {(a['id'], a['try']) for a in answers}:
            errs.append(f'{name}: grades for answers that are not in answers.jsonl')
        if any(g.get('judge', '').split(':')[0] == meta.get('chat') for g in grades):
            errs.append(f'{name}: the chat graded itself')
        if meta.get('verified') and not meta.get('verifiedBy'):
            errs.append(f'{name}: "verified" needs "verifiedBy" (a maintainer, and how they checked)')
    before = {p: open(os.path.join(ROOT, p)).read() if os.path.exists(os.path.join(ROOT, p)) else '' for p in ('chats/ratings.csv', 'leaderboard.json', 'LEADERBOARD.md')}
    subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'aggregate.py')], check=True, capture_output=True)
    for p, old in before.items():
        if open(os.path.join(ROOT, p)).read() != old:
            errs.append(f'{p} is out of date: run python3 scripts/aggregate.py and commit the result')
    print('\n'.join(errs) or 'ok: all runs valid, leaderboard up to date')
    sys.exit(1 if errs else 0)


if __name__ == '__main__':
    main()
