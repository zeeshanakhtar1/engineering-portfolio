import requests,json,time
s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36","Accept":"application/json","Referer":"https://www.magnum4d.my/results/draw-results"})
URLs=[
"https://www.magnum4d.my/results/past/between-dates/null/2026-10-25/2",
"https://www.magnum4d.my/results/past/between-dates/null/2018-04-25/2",
"https://www.magnum4d.my/results/past/between-dates/null/2017-05-17/2",
"https://www.magnum4d.my/results/past/between-dates/null/2014-11-08/2",
"https://www.magnum4d.my/results/past/between-dates/null/2009-09-23/2",
"https://www.magnum4d.my/results/past/between-dates/null/1985-04-25/2",
"https://www.magnum4d.my/results/draw-results",
]
for u in URLs:
 try:
  t=time.monotonic();r=s.get(u,timeout=22);print("\\nURL:",u,"STATUS",r.status_code,"SIZE",len(r.content),"SECS",round(time.monotonic()-t,1),flush=True)
  if "application/json" in r.headers.get("Content-Type","") or r.text[:1] in ["[","{"]:
   j=r.json()
   print("TYPE",type(j).__name__,"LEN",len(j))
   if isinstance(j,list):
    for x in j[:2]:
     print("KEYS",list(x.keys()),flush=True)
     print("SAMPLE",json.dumps(x,ensure_ascii=False)[:18000],flush=True)
   else:print("DATA",json.dumps(j,ensure_ascii=False)[:18000],flush=True)
  else:print("BODY",r.text[:900],flush=True)
 except Exception as e: print("ERROR",type(e).__name__,str(e)[:350],flush=True)
