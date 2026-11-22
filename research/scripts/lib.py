import urllib.request, urllib.parse, time, json, xml.etree.ElementTree as ET
B="https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
def call(ep, **p):
    p["tool"]="healthchat-review"
    data=urllib.parse.urlencode(p).encode()
    for i in range(4):
        try:
            time.sleep(0.4)
            return urllib.request.urlopen(urllib.request.Request(B+ep, data=data),timeout=60).read()
        except Exception as e:
            time.sleep(2+i*2)
    raise RuntimeError("fail")
def search(q, retmax=0, sort=None, **kw):
    p=dict(db="pubmed",term=q,retmode="json",retmax=retmax,**kw)
    if sort: p["sort"]=sort
    d=json.loads(call("esearch.fcgi",**p))["esearchresult"]
    return int(d["count"]), d["idlist"]
