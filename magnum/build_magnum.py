#!/usr/bin/env python3
"""Download Magnum's actual historical API draws, audit against independent archive, export five sheets."""
import csv, json, re, time
from collections import Counter,defaultdict
from datetime import datetime,timedelta,date
from pathlib import Path
from decimal import Decimal, InvalidOperation
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from openpyxl import Workbook,load_workbook
from openpyxl.styles import PatternFill,Font,Alignment,Border,Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT="https://www.magnum4d.my"
API=ROOT+"/results/past/between-dates/null/{end}/{count}"
CSV_SOURCE="https://raw.githubusercontent.com/deadboy18/malaysia-4d/main/data/magnum_draws.csv"
DATES={
"4D Classic":date(1985,4,25),
"4D Jackpot":date(2009,9,23),
"4D Jackpot Gold":date(2014,11,8),
"mgold":date(2017,5,17),
"Magnum Life":date(2018,4,23)}
END=date(2026,10,25)
OUT="Magnum_4D_All_Games_1985-2026_Verified.xlsx"
JSON_FILE="Magnum_Official_Raw_1985-2026.json"
NUM_KEYS=["FirstPrize","SecondPrize","ThirdPrize"]+[f"Special{i}" for i in range(1,11)]+[f"Console{i}" for i in range(1,11)]
BASE_KEYS=["prize_1","prize_2","prize_3"]+[f"special_{i}" for i in range(1,11)]+[f"consol_{i}" for i in range(1,11)]

def client():
 s=requests.Session()
 s.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36","Accept":"application/json","Referer":ROOT+"/results/draw-results"})
 s.mount("https://",HTTPAdapter(max_retries=Retry(total=4,backoff_factor=1.2,status_forcelist=[429,500,502,503,504])))
 return s

def number(s,n=4):
 s=str(s or "").strip()
 return s.zfill(n) if re.fullmatch(r"\d{1,%d}"%n,s) else None

def money(v):
 if v in (None,""):return None
 try:return float(Decimal(str(v).replace(",","")))
 except(InvalidOperation,ValueError):return None

def plain(v):
 return "" if v is None else str(v)

def parse_dt(s):
 return datetime.strptime(s,"%d/%m/%Y").date()

def audit_source(s):
 r=s.get(CSV_SOURCE,timeout=65);r.raise_for_status()
 raw=list(csv.DictReader(r.text.splitlines()))
 out={}
 for x in raw:
  try:d=date.fromisoformat(x["date"])
  except:continue
  if DATES["4D Classic"]<=d<=END:
   if d.isoformat() in out:raise ValueError("Duplicate independent row: "+str(d))
   out[d.isoformat()]=x
 print("INDEPENDENT_CSV_RECORDS",len(out),flush=True)
 return out

def download(s):
 seen={}
 end=END
 pages=0
 for page in range(32):
  url=API.format(end=end.isoformat(),count=1000)
  response=s.get(url,timeout=85);response.raise_for_status()
  j=response.json()
  if not isinstance(j,list):raise TypeError("API did not respond with list")
  if not j:break
  new=0;dates=[]
  for item in j:
   try:d=parse_dt(item["DrawDate"])
   except Exception as e:raise ValueError("Date format issue: "+repr(item)[:120]) from e
   dates.append(d)
   if not DATES["4D Classic"]<=d<=END:continue
   key=d.isoformat()
   if key in seen:
    if seen[key]!=item:raise ValueError("Inconsistent duplicate API record "+key)
   else:
    seen[key]=item;new+=1
  min_date=min(dates);max_date=max(dates)
  pages+=1
  print("API_PAGE",page+1,"FETCHED",len(j),"NEW",new,"DATE_RANGE",min_date,max_date,"TOTAL",len(seen),flush=True)
  if min_date<=DATES["4D Classic"]:break
  if min_date>=end:raise RuntimeError("API pagination stuck")
  end=min_date-timedelta(days=1)
  time.sleep(.18)
 if not seen:raise ValueError("No data obtained from operator")
 if min(seen)!=DATES["4D Classic"].isoformat():raise ValueError("Earliest classic record missing "+min(seen))
 if max(seen)!=END.isoformat():raise ValueError("Latest record missing "+max(seen))
 return seen,pages

def xldt(s):
 return date.fromisoformat(s)
def urlrow(d):
 return API.format(end=d,count=1)

def build():
 s=client()
 official,pages=download(s)
 independent=audit_source(s)
 bad=[];issues=[];verified=0;valid=0;outcome=Counter();raw_rows=[]
 for k,j in sorted(official.items()):
  d=date.fromisoformat(k)
  seq=str(j.get("DrawID",""))
  vals=[number(j.get(x)) for x in NUM_KEYS]
  if len(vals)!=23 or any(x is None for x in vals):
   issues.append([d,seq,"CRITICAL","Invalid or blank core 4D result in official API",urlrow(k)])
   continue
  if not re.fullmatch(r"\d{1,4}/\d{2}",seq):
   issues.append([d,seq,"WARNING","Unusual official DrawID format",urlrow(k)])
  valid+=1
  r=independent.get(k)
  if r:
   archive=[number(r.get(x)) for x in BASE_KEYS]
   if all(x is not None for x in archive) and vals==archive:
    verified+=1;outcome["SOURCE_MATCH"]+=1
   else:
    outcome["SOURCE_MISMATCH"]+=1
    for field,a,b in zip(NUM_KEYS,vals,archive):
     if a!=b:bad.append([d,seq,field,b or "",a or "",urlrow(k),CSV_SOURCE])
  else:
   outcome["NOT_IN_ARCHIVE"]+=1
  raw_rows.append((d,seq,j,vals,"MATCH" if r and vals==[number(r.get(x)) for x in BASE_KEYS] else "CHECK SOURCE"))
 if valid !=len(official):raise RuntimeError("Official entries with invalid core numbers: "+str(len(official)-valid))
 print("VALID_CORE_DRAWS",valid,"CROSS_SOURCE_MATCH_DRAWS",verified,"DISAGREE",len(bad),"MISSING_ARCHIVE",outcome["NOT_IN_ARCHIVE"],flush=True)
 rawj={k:v for k,v in sorted(official.items())}
 Path(JSON_FILE).write_text(json.dumps(rawj,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
 styles={"header":"132C5A","text":"13334E","source":"176B46"}
 wb=Workbook();wb.remove(wb.active)
 def make_sheet(name,head,rows,width=None):
  ws=wb.create_sheet(name);ws.sheet_view.showGridLines=False
  ws.append(head)
  for x in rows:ws.append(x)
  ws.freeze_panes="C2"
  ws.row_dimensions[1].height=34
  for c in ws[1]:
   c.fill=PatternFill("solid",fgColor=styles["header"]);c.font=Font(color="FFFFFF",bold=True,size=10,name="Aptos")
   c.alignment=Alignment(wrap_text=True,vertical="center")
  for i in range(1,len(head)+1):
   w=width[i-1] if width and i<=len(width) else 16
   ws.column_dimensions[get_column_letter(i)].width=w
  ws.auto_filter.ref=f"A1:{get_column_letter(len(head))}{ws.max_row}"
  for r in ws.iter_rows(min_row=2):
   for c in r:
    if isinstance(c.value,(date,datetime)):c.number_format="dd mmm yyyy"
    if isinstance(c.value,str) and c.value.startswith("https://"):
     c.hyperlink=c.value;c.font=Font(name="Aptos",size=9,color="2168B6",underline="single")
    elif c.column>=3:
     c.font=Font(name="Aptos",size=10,color=styles["source"])
    else:c.font=Font(name="Aptos",size=10,color=styles["text"])
  ws.sheet_properties.pageSetUpPr.fitToPage=True
  return ws
 def metadata(j):
  return str(j.get("Official","")),j.get("DrawDay","")
 classic=[];jack=[];gold=[];mgold=[];life=[];master=[];annual=defaultdict(Counter)
 for d,seq,j,vals,status in raw_rows:
  annual[d.year]["4D Classic"]+=1
  common=[d,seq]
  src=urlrow(d.isoformat())
  classic.append(common+vals+[status,src,CSV_SOURCE])
  # Original top-three 4D values. Jackpot 1 matches any two of the top three numbers.
  if d>=DATES["4D Jackpot"] and j.get("IsDateValidJackpot") is True:
   annual[d.year]["4D Jackpot"]+=1
   pairs=[f"{vals[i]} + {vals[k]}" for i,k in [(0,1),(1,0),(0,2),(2,0),(1,2),(2,1)]]
   jack.append(common+pairs+[money(j.get("Jackpot1Amount")),money(j.get("Jackpot2Amount")),
             plain(j.get("Jackpot1Winner")),plain(j.get("Jackpot2Winner")),src])
  if d>=DATES["4D Jackpot Gold"] and j.get("IsDateValidGoldJackpot") is True:
   annual[d.year]["4D Jackpot Gold"]+=1
   gold.append(common+[number(j.get("Powerball1"),2) or "",number(j.get("Powerball2"),2) or "",
       money(j.get("GoldJackpot1Amount")),money(j.get("GoldJackpot2Amount")),
       plain(j.get("GoldJackpot1Winner")),plain(j.get("GoldJackpot2Winner")),
       money(j.get("PowerballJackpot1Amount")),money(j.get("PowerballJackpot2Amount")),
       plain(j.get("PowerballJackpot1aWinner")),plain(j.get("PowerballJackpot1bWinner")),
       plain(j.get("PowerballJackpot1cWinner")),plain(j.get("PowerballJackpot2Winner")),
       src])
  if d>=DATES["mgold"] and j.get("IsDateValidMGold") is True:
   annual[d.year]["mgold"]+=1
   # Original official field list has no 6-digit mgold winning number field.
   mgold.append(common+[money(j.get("mGold1Amount")),"6-digit winning number not exposed by this API",src])
  if d>=DATES["Magnum Life"] and j.get("IsDateValidMagnumLife") is True:
   annual[d.year]["Magnum Life"]+=1
   life.append(common+[(number(j.get("LifeNum"+str(n)),2) or "") for n in range(1,9)]
           +[(number(j.get("LifeBonusNum"+str(n)),2) or "") for n in range(1,3)]
           +[plain(j.get("LifeWinnerCnt1")),plain(j.get("LifeWinnerCnt2")),src])
  master.append(common+[j.get("DrawDay",""),str(j.get("Official",""))]+vals+
   [j.get("Powerball1",""),j.get("Powerball2","")]
   +[j.get("LifeNum"+str(n),"") for n in range(1,9)]
   +[j.get("LifeBonusNum"+str(n),"") for n in range(1,3)]
   +[plain(j.get(z)) for z in ["Jackpot1Amount","Jackpot2Amount","Jackpot1Winner","Jackpot2Winner",
      "GoldJackpot1Amount","GoldJackpot2Amount","GoldJackpot1Winner","GoldJackpot2Winner",
      "mGold1Amount","PowerballJackpot1Amount","PowerballJackpot2Amount",
      "LifeWinnerCnt1","LifeWinnerCnt2"]]
   +[str(j.get(x,"")) for x in ["IsDateValidJackpot","IsDateValidGoldJackpot","IsDateValidMGold","IsDateValidMagnumLife"]]+[src])
 overview=[
  ["Data source",ROOT+"/results/draw-results"],
  ["Underlying official API",ROOT+"/results/past/between-dates/null/YYYY-MM-DD/count"],
  ["Data collected through",END.isoformat()],
  ["Official Classic draws",len(classic)],
  ["4D Classic start","25 Apr 1985"],
  ["4D Jackpot start","23 Sep 2009"],
  ["4D Jackpot Gold start","08 Nov 2014"],
  ["mgold start","17 May 2017"],
  ["Magnum Life start","23 Apr 2018"],
  ["Game | 4D Jackpot draws",len(jack)],
  ["Game | 4D Jackpot Gold draws",len(gold)],
  ["Game | mgold draws",len(mgold)],
  ["Game | Magnum Life draws",len(life)],
  ["Official Classic rows independently cross-checked",verified],
  ["Core 4D prize number cells matched",verified*23],
  ["Core 4D prize discrepancies",len(bad)],
  ["Rows not available in independent archive",outcome["NOT_IN_ARCHIVE"]],
  ["API pages requested",pages],
  ["Classic source check method","Compare all 23 prize numbers per draw to separate CSV scraped from Magnum"],
  ["Historical raw JSON file",JSON_FILE],
  ["IMPORTANT: mgold","Official historical API used here contains mgold prize amount but NO 6-digit mgold winning number. This sheet does not fabricate a number."],
  ["Jackpot Gold powerballs","Powerball1 and Powerball2 are reproduced under their original official API field labels. These may relate to Gold variant; see fields."],
  ["Jackpot 1 combinations","Six pairs derived from first three 4D prizes; not separately supplied as a list by historical API."],
  ["Official flags","Games rows only included when their respective IsDateValid... flags are true, after their launch dates."],
  ["Validation scope","Actual Magnum API data for every row, with independent Classic prize cross-check; game amounts retained from official API."],
  ["Status","Only results through 25 October 2026 inclusive"],
 ]
 make_sheet("READ ME",["Item","Explanation"],overview,[49,114])
 make_sheet("4D Classic",["Draw date","Draw number","1st Prize","2nd Prize","3rd Prize"]+
  [f"Special {i}" for i in range(1,11)]+[f"Consolation {i}" for i in range(1,11)]+
  ["Independent archive check","Official record URL","Archive CSV URL"],classic,[18,13]+[15]*23+[25,80,90])
 make_sheet("4D Jackpot",["Draw date","Draw number"]+[f"Ordered top-three pair {i} (derived)" for i in range(1,7)]+
  ["Jackpot 1 amount RM","Jackpot 2 amount RM","Jackpot 1 winners API","Jackpot 2 winners API","Official record URL"],
  jack,[18,13]+[28]*6+[23,23,24,24,85])
 make_sheet("4D Jackpot Gold",["Draw date","Draw number","Powerball1 (API)","Powerball2 (API)",
  "Gold Jackpot 1 amount RM","Gold Jackpot 2 amount RM","Gold Jackpot 1 winners API",
  "Gold Jackpot 2 winners API","Powerball Jackpot 1 amount RM","Powerball Jackpot 2 amount RM",
  "Powerball Jackpot 1a winners","Powerball Jackpot 1b winners","Powerball Jackpot 1c winners",
  "Powerball Jackpot 2 winners","Official record URL"],gold,[18,13,19,19]+[26]*10+[84])
 make_sheet("mgold",["Draw date","Draw number","mgold 1st prize amount RM","Winning-number availability","Official record URL"],
  mgold,[18,13,24,66,86])
 make_sheet("Magnum Life",["Draw date","Draw number"]+[f"Main {i}" for i in range(1,9)]+
  ["Bonus 1","Bonus 2","Grand prize winning count","2nd prize winning count","Official record URL"],
  life,[18,13]+[13]*10+[27,27,86])
 aud=[]
 for d,seq,j,vals,status in raw_rows:
  aud.append([d,seq,status,j.get("Official",""),len(vals),
              "PASS" if len(vals)==23 and all(re.fullmatch(r"\d{4}",v) for v in vals) else "FAIL",
              urlrow(d.isoformat()),CSV_SOURCE])
 make_sheet("Validation Audit",["Draw date","Draw number","Archive agreement","Operator 'Official' flag",
              "4D results count","Format test","Official API URL","Independent source URL"],aud,
  [18,14,25,25,22,17,90,90])
 make_sheet("Number Differences",["Draw date","Draw number","Prize field","Independent value","Operator value",
              "Official API URL","Independent CSV URL"],bad,[18,14,23,20,20,90,90])
 make_sheet("Validation Issues",["Draw date","Draw number","Severity","Issue","Official API URL"],issues,[18,14,17,82,90])
 cover=[[year]+[annual[year][g] for g in DATES] for year in sorted(annual)]
 make_sheet("Annual Coverage",["Year"]+list(DATES),cover,[17]+[24]*5)
 allfields=list(next(iter(official.values())).keys())
 raw=[ [d,seq]+[plain(j.get(k)) for k in allfields]+[urlrow(d.isoformat())] for d,seq,j,vals,status in raw_rows]
 make_sheet("Raw API Fields",["Draw date","Draw number"]+allfields+["Official API record URL"],raw,
  [18,14]+[21]*len(allfields)+[90])
 for sheetname,columns in {"4D Jackpot":[9,10],"4D Jackpot Gold":[5,6,9,10],"mgold":[3]}.items():
  ws=wb[sheetname]
  for row in ws.iter_rows(min_row=2):
   for c in columns:
    row[c-1].number_format='"RM" #,##0.00'
 for ws in wb:
  for row in ws.iter_rows(min_row=2):
   for c in row:
    if isinstance(c.value,date):c.number_format="dd/mm/yyyy"
 if bad:
  for row in wb["Number Differences"].iter_rows(min_row=2):
   for c in row:c.fill=PatternFill("solid",fgColor="FFF1DC")
 if issues:
  for row in wb["Validation Issues"].iter_rows(min_row=2):
   for c in row:c.fill=PatternFill("solid",fgColor="FFF1DC")
 wb.save(OUT)
 check=load_workbook(OUT,read_only=True,data_only=True)
 assert check["4D Classic"].max_row-1==len(classic)
 assert check["4D Classic"]["C2"].value=="1972"
 assert check["4D Classic"]["D2"].value=="7055"
 assert check["4D Classic"]["E2"].value=="8296"
 assert check["4D Classic"][f"C{check['4D Classic'].max_row}"].value=="3719"
 assert check["4D Classic"][f"D{check['4D Classic'].max_row}"].value=="0831"
 assert check["Magnum Life"].max_row-1==len(life)
 check.close()
 summary={"all_games":{g:len([x for x in [classic,jack,gold,mgold,life][i]]) for i,g in enumerate(DATES)},
  "classic_rows":len(classic),"checked_classic_rows":verified,
  "checked_core_4d_numbers":verified*23,"number_discrepancies":len(bad),
  "unmatched_against_archive":outcome["NOT_IN_ARCHIVE"],
  "issues":issues[:30],"pages":pages,"first":min(official),"last":max(official),
  "raw_api_fields":allfields,"files":[OUT,JSON_FILE]}
 Path("Magnum_Validation_Summary.json").write_text(json.dumps(summary,default=str,ensure_ascii=False,indent=2))
 print("FINAL_SUMMARY",json.dumps({k:v for k,v in summary.items() if k not in ["raw_api_fields","issues"]}),flush=True)
 print("WORKBOOK_BYTES",Path(OUT).stat().st_size,"RAW_BYTES",Path(JSON_FILE).stat().st_size,flush=True)
if __name__=="__main__":build()
