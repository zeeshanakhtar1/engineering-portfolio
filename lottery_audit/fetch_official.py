#!/usr/bin/env python3
"""Operator-to-operator-result audit: obtain every official historical draw record."""
import json,sys,time,threading,requests
from datetime import date,datetime,timedelta
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
from urllib.parse import urlsplit
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from collections import Counter
OUT=Path("official_data")
OUT.mkdir(exist_ok=True)
TODAY=date(2026,10,25)
DAM_START=date(2005,10,1)
MAG_START=date(1985,4,25)
local=threading.local()
def session():
    if not hasattr(local,"session"):
        s=requests.Session()
        s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36","Accept":"application/json"})
        s.mount("https://",HTTPAdapter(max_retries=Retry(total=2,backoff_factor=.35,status_forcelist=[429,500,502,503,504]),pool_connections=16,pool_maxsize=16))
        local.session=s
    return local.session
def get(url,timeout=22,headers=None):
    res=session().get(url,headers=headers,timeout=timeout)
    res.raise_for_status()
    return res.json()
def draw_date(j):
    return datetime.strptime(j["DrawDate"],"%d/%m/%Y").date()
def magnum():
    results={}
    end=TODAY
    for i in range(20):
        url="https://www.magnum4d.my/results/past/between-dates/null/"+end.isoformat()+"/1000"
        records=get(url,timeout=60,headers={"Referer":"https://www.magnum4d.my/results/draw-results"})
        if not isinstance(records,list) or len(records)<1:break
        mindate=min(draw_date(x) for x in records)
        for j in records:
            d=draw_date(j)
            if MAG_START<=d<=TODAY:
                k=d.isoformat()
                if k in results and results[k]!=j:raise ValueError("Different duplicate Magnum "+k)
                results[k]=j
        print("MAGNUM_PAGE",i+1,len(records),"TOTAL",len(results),"OLDEST",mindate,flush=True)
        if mindate<=MAG_START:break
        end=mindate-timedelta(days=1)
    if min(results)!=MAG_START.isoformat() or max(results)!=TODAY.isoformat():raise ValueError("Magnum bad endpoints")
    (OUT/"magnum_live.json").write_text(json.dumps(results,separators=(",",":")))
    return {"count":len(results),"first":min(results),"last":max(results),"source":"www.magnum4d.my/results/past/between-dates"}
def dam_dates():
    j=get("https://www.damacai.com.my/ListPastResult",timeout=40)
    raw=j.get("drawdate","").split()
    ds=sorted(set(x for x in raw if len(x)==8 and x.isdecimal() and DAM_START.strftime("%Y%m%d")<=x<=TODAY.strftime("%Y%m%d")))
    if len(ds)<3000:raise ValueError("Too few official dates: "+str(len(ds)))
    return ds
def dam_one(d):
    dt=d[:4]+"-"+d[4:6]+"-"+d[6:8]
    tries=[]
    for attempt in range(4):
        try:
            j=get("https://www.damacai.com.my/callpassresult?pastdate="+d,timeout=22,headers={"cookiesession":"504","Referer":"https://www.damacai.com.my/past-draw-result/"})
            link=j.get("link")
            if not link or not isinstance(link,str):raise ValueError("No blob link: "+repr(j)[:120])
            if urlsplit(link).scheme!="https":raise ValueError("Non-https blob URL")
            v=get(link,timeout=28)
            if not isinstance(v,dict):raise ValueError("Result not object")
            if v.get("drawDate")!=f"{d[6:8]}/{d[4:6]}/{d[:4]}":raise ValueError("Result date differs "+str(v.get("drawDate")))
            if not v.get("p1") or not v.get("p2") or not v.get("p3"):raise ValueError("Missing main prizes")
            return dt,v,None
        except Exception as e:
            tries.append(str(e)[:130])
            time.sleep((attempt+1)*.25)
    return dt,None,"; ".join(tries[-2:])
def damacai():
    dates=dam_dates()
    print("DAM_OFFICIAL_DATES",len(dates),"FIRST",dates[0],"LAST",dates[-1],flush=True)
    official={}
    errors={}
    with ThreadPoolExecutor(max_workers=12) as executor:
        fut=[executor.submit(dam_one,d) for d in dates]
        for count,f in enumerate(as_completed(fut),1):
            dt,j,error=f.result()
            if error:errors[dt]=error
            else:official[dt]=j
            if count%250==0 or count==len(dates):
                print("DAM_PROGRESS",count,"/",len(dates),"SUCCESS",len(official),"FAILED",len(errors),flush=True)
    (OUT/"damacai_live.json").write_text(json.dumps(official,separators=(",",":")))
    (OUT/"damacai_live_errors.json").write_text(json.dumps(errors,indent=2))
    (OUT/"damacai_official_dates.json").write_text(json.dumps([d[:4]+"-"+d[4:6]+"-"+d[6:8] for d in dates]))
    return {"dates":len(dates),"fetched":len(official),"failed":len(errors),"first":dates[0],"last":dates[-1],"source":"www.damacai.com.my/ListPastResult and callpassresult"}
def main():
    summary={}
    for op,fn in [("magnum",magnum),("damacai",damacai)]:
        try:summary[op]=fn()
        except Exception as e:
            import traceback
            traceback.print_exc()
            summary[op]={"error":str(e)}
    (OUT/"fetch_summary.json").write_text(json.dumps(summary,indent=2))
    print("FETCH_SUMMARY",json.dumps(summary),flush=True)
    if "error" in summary.get("magnum",{}) or "error" in summary.get("damacai",{}):
        sys.exit(1)
if __name__=="__main__":main()
