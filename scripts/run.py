#!/usr/bin/env python3
"""Ask a chat the test questions through its API and save every answer in full.

    python3 scripts/run.py --chat deepseek [--sample 100] [--seed 158] [--hard] [--repeat 1] [--limit N]

Writes runs/<date>-<chat>/answers.jsonl and run.json (what was asked, how, when, and the model the API reported).
Keys come from the environment or a .env file in the repo root (git-ignored); chats/providers.json says which
variable each chat reads. A chat's API is not its consumer app: no app system prompt, no memory, no web search
unless the provider adds it. run.json says so, and results must be reported that way.
"""
import argparse
import datetime
import json
import os
import random
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def load_env():
    p = os.path.join(ROOT, '.env')
    if os.path.exists(p):
        for line in open(p):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"\''))


def pick_questions(sample, seed, hard):
    bank = json.load(open(os.path.join(ROOT, 'questions', 'health-consumer-questions.json')))['questions']
    qs = []
    if sample:
        rnd = random.Random(seed)
        qs = [dict(q, set='sample') for q in rnd.sample(sorted(bank, key=lambda q: q['id']), sample)]
    if hard:
        qs += [dict(q, set='hard') for q in json.load(open(os.path.join(ROOT, 'questions', 'hard-cases.json')))['questions']]
    return qs


def ask(p, question):
    key = os.environ.get(p['key_env'])
    if not key:
        sys.exit(f"Set {p['key_env']} (environment or .env) to run this chat.")
    if p['api'] == 'anthropic':
        url = p['base_url'].rstrip('/') + '/v1/messages'
        body = {'model': p['model'], 'max_tokens': 2000, 'messages': [{'role': 'user', 'content': question}]}
        headers = {'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json'}
    else:  # OpenAI-compatible chat completions (OpenAI, DeepSeek, xAI, Perplexity, Gemini's compat endpoint, OpenRouter)
        url = p['base_url'].rstrip('/') + '/chat/completions'
        body = {'model': p['model'], 'messages': [{'role': 'user', 'content': question}], 'max_tokens': 2000}
        body.update(p.get('extra', {}))
        headers = {'Authorization': f'Bearer {key}', 'content-type': 'application/json'}
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=headers, method='POST')
    for attempt in range(4):
        try:
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.load(r)
            secs = round(time.time() - t0, 1)
            break
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 529) and attempt < 3:
                time.sleep(5 * (attempt + 1))
                continue
            return {'error': f'HTTP {e.code}: {e.read().decode()[:300]}'}
        except Exception as e:  # network
            if attempt < 3:
                time.sleep(5)
                continue
            return {'error': str(e)[:300]}
    if p['api'] == 'anthropic':
        text = ''.join(b.get('text', '') for b in d.get('content', []))
        usage = d.get('usage', {})
    else:
        text = d['choices'][0]['message'].get('content') or ''
        usage = d.get('usage', {})
    out = {'answer': text, 'model': d.get('model'), 'usage': usage, 'seconds': secs}
    if d.get('citations'):  # Perplexity
        out['citations'] = d['citations']
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chat', required=True)
    ap.add_argument('--sample', type=int, default=100)
    ap.add_argument('--seed', type=int, default=158)
    ap.add_argument('--hard', action='store_true')
    ap.add_argument('--repeat', type=int, default=1)
    ap.add_argument('--limit', type=int, default=0, help='first N questions only (a smoke test)')
    ap.add_argument('--date', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    load_env()
    providers = json.load(open(os.path.join(ROOT, 'chats', 'providers.json')))['providers']
    if a.chat not in providers:
        sys.exit(f'{a.chat} is not in chats/providers.json')
    p = providers[a.chat]
    qs = pick_questions(a.sample, a.seed, a.hard)
    if a.limit:
        qs = qs[:a.limit]
    out_dir = os.path.join(ROOT, 'runs', f'{a.date}-{a.chat}')
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, 'answers.jsonl')
    done = set()
    if os.path.exists(path):
        for l in open(path):
            r = json.loads(l)
            if 'error' not in r:
                done.add((r['id'], r['try']))
    rows = [r for r in (json.loads(l) for l in open(path)) if 'error' not in r] if os.path.exists(path) else []
    n = 0
    with open(path, 'w') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
        for q in qs:
            for t in range(1, a.repeat + 1):
                if (q['id'], t) in done:
                    continue
                r = ask(p, q['text'])
                rec = {'id': q['id'], 'set': q['set'], 'try': t, 'chat': a.chat, 'question': q['text'], 'asked': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'), **r}
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                f.flush()
                n += 1
                print(f"{n} {q['id']} {'ERR ' + r['error'][:80] if 'error' in r else len(r['answer'])}", flush=True)
    models = sorted({json.loads(l).get('model') or '' for l in open(path)} - {''})
    json.dump({'chat': a.chat, 'provider': {k: v for k, v in p.items() if k != 'key_env'}, 'date': a.date, 'sample': a.sample, 'seed': a.seed,
               'hard': a.hard, 'repeat': a.repeat, 'questions': len(qs), 'modelsReported': models,
               'how': 'API, one user message, no system prompt, fresh conversation per question, provider default temperature, max_tokens 2000. Not the consumer app.'},
              open(os.path.join(out_dir, 'run.json'), 'w'), indent=1)
    print(f'{n} new answers -> {os.path.relpath(path, ROOT)}')


if __name__ == '__main__':
    main()
