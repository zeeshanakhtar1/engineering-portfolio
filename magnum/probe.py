import requests,re
s=requests.Session();s.headers.update({"User-Agent":"Mozilla/5.0"})
for d in ["2014-11-08","2017-05-17","2018-04-25","2020-05-10","2026-10-25"]:
 for u in ["https://4dresultnow.com/en/result/"+d+"/","https://my4d.club/en/results/"+d,"https://www.businesslist.my/lottery/results/history?date="+d]:
  try:
   r=s.get(u,timeout=15);t=r.text
   print("DATE",d,"URL",u,"STATUS",r.status_code,"LEN",len(t),"TITLE",re.findall(r'<title[^>]*>(.*?)</title>',t,re.S|re.I)[:1],"MGOLD",t.lower().find("mgold"),"GOLD",t.lower().find("jackpot gold"),"BLOCK",re.sub('<[^>]+>',' ',t[max(0,t.lower().find('mgold')-150):t.lower().find('mgold')+500])[:600],flush=True)
  except Exception as e:print(type(e).__name__,str(e)[:200],flush=True)
