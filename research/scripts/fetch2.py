from lib import *
import json
ids=json.load(open("new.json"))
recs=json.load(open("abstracts-cache.json"))
for s in range(0,len(ids),100):
    x=call("efetch.fcgi",db="pubmed",id=",".join(ids[s:s+100]),retmode="xml")
    root=ET.fromstring(x)
    for a in root.findall("PubmedArticle"):
        pmid=a.findtext(".//PMID")
        art=a.find(".//Article")
        au=[(e.findtext("LastName") or e.findtext("CollectiveName") or "")+" "+(e.findtext("Initials") or "") for e in art.findall(".//Author")]
        authors=", ".join(au[:3])+(" et al." if len(au)>3 else "")
        doi=""
        for e in a.findall(".//ArticleId"):
            if e.get("IdType")=="doi": doi=e.text
        yr=a.findtext(".//PubDate/Year") or (a.findtext(".//PubDate/MedlineDate") or "")[:4]
        ab=" ".join("".join(t.itertext()) for t in art.findall(".//Abstract/AbstractText"))
        recs[pmid]=dict(pmid=pmid,doi=doi,title="".join(art.find("ArticleTitle").itertext()),authors=authors,
          journal=art.findtext(".//Journal/Title"),year=yr,pubtypes=[e.text for e in art.findall(".//PublicationType")],abstract=ab)
    print(s,len(recs),flush=True)
json.dump(recs,open("abstracts-cache.json","w"))
