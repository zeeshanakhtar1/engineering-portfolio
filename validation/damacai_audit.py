#!/usr/bin/env python3
"""Cross-audit Da Ma Cai draws: independent CSV vs captured official draw JSON."""
import csv, json, re, subprocess, time
from pathlib import Path
from datetime import date, datetime, timedelta
from collections import Counter
import requests
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.formatting.rule import CellIsRule
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

START = "2005-10-01"
END = "2026-10-25"
OUTPUT = "Da_Ma_Cai_2005-2026_Audited_Results.xlsx"
MAIN_SRC = "https://github.com/deadboy18/malaysia-4d/blob/main/data/damacai_draws.csv"
JSON_SRC = "https://github.com/hongster/damacai/tree/main/results"
OFFICIAL = "https://www.damacai.com.my"
ROOT = Path("/tmp/damacai-audit")
MAIN = ROOT / "malaysia-4d"
JSONREPO = ROOT / "damacai"
NUM_FIELDS = ["prize_1","prize_2","prize_3"] + [f"special_{i}" for i in range(1,11)] + [f"consol_{i}" for i in range(1,11)]
JS_FIELDS = ["p1","p2","p3"]

def number(v, digits=4):
    v = str(v if v is not None else "").strip()
    if not re.fullmatch(r"\d{1,%d}" % digits, v):
        return None
    return v.zfill(digits)

def fmt_date(v):
    return date.fromisoformat(v)

def download_repo(name, url):
    folder = ROOT / name
    if not folder.exists():
        subprocess.run(["git","clone","--depth","1","--quiet",url,str(folder)],check=True,timeout=160)
    return folder

def source_json(d):
    p = JSONREPO / "results" / d[:4] / (d.replace("-","")+".json")
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None

def official_json(d, session):
    """Use only for gaps, conflicts, and selected official spot checks."""
    key = d.replace("-","")
    for attempt in range(2):
        try:
            r = session.get(OFFICIAL+"/callpassresult",params={"pastdate":key},
                            headers={"cookiesession":"504"}, timeout=18)
            r.raise_for_status()
            link = r.json().get("link")
            if not link or not str(link).startswith("https://"):
                return None
            rs = session.get(link,timeout=18)
            rs.raise_for_status()
            result = rs.json()
            if isinstance(result,dict) and result.get("p1"):
                return result
        except (requests.RequestException,ValueError,KeyError) as e:
            print("LIVE_RESULT_FETCH_ERROR",d,str(e)[:100],flush=True)
            time.sleep(0.4)
    return None

def official_dates(session):
    try:
        r = session.get(OFFICIAL+"/ListPastResult",timeout=25)
        r.raise_for_status()
        vals = r.json().get("drawdate","").split()
        out = sorted({v[:4]+"-"+v[4:6]+"-"+v[6:8] for v in vals if re.fullmatch(r"\d{8}",v)})
        return [d for d in out if START <= d <= END]
    except Exception as e:
        print("OFFICIAL_DATE_LIST_UNAVAILABLE",repr(e)[:250],flush=True)
        return None

def json_numbers(j):
    if not isinstance(j,dict):
        return [None]*23
    return [number(j.get(f)) for f in JS_FIELDS]+[number(v) for v in (j.get("starterList") or [])[:10]]+[number(v) for v in (j.get("consolidateList") or [])[:10]]

def expected_id(j):
    return str(j.get("drawNo","")).split("/")[0]

def valid_json(j,d):
    try:
        return (datetime.strptime(j.get("drawDate",""),"%d/%m/%Y").date().isoformat()==d
                and re.fullmatch(r"\d{3,5}/\d{2}",str(j.get("drawNo",""))) is not None
                and len(json_numbers(j))==23
                and all(n is not None for n in json_numbers(j)))
    except (ValueError,TypeError):
        return False

def to_date(d):
    return fmt_date(d)

def year_gap_table(records):
    gaps=[]
    ordered=sorted(records,key=lambda r:r["date"])
    for a,b in zip(ordered,ordered[1:]):
        da,db=int(a["drawseq"]),int(b["drawseq"])
        if db>da+1:
            gaps.append([a["date"],b["date"],da,db,db-da-1,
                        "Sequence gap does not alone establish unrecorded draws; some draws may have been cancelled or excluded"])
    return gaps

def new_sheet(wb,name,headers,rows,widths,auto_filter=True):
    ws=wb.create_sheet(name)
    ws.sheet_view.showGridLines=False
    ws.append(headers)
    for row in rows: ws.append(row)
    ws.freeze_panes="C2" if len(headers)>3 else "A2"
    for c in ws[1]:
        c.fill=PatternFill("solid",fgColor="193A72")
        c.font=Font(name="Aptos",size=10,bold=True,color="FFFFFF")
        c.alignment=Alignment(wrap_text=True,vertical="center")
    ws.row_dimensions[1].height=32
    for i,w in enumerate(widths,1):
        ws.column_dimensions[get_column_letter(i)].width=w
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.font=Font(name="Aptos",size=10,color="0C6644" if cell.column>2 else "344054")
            cell.alignment=Alignment(vertical="center")
            if cell.data_type=="s" and cell.value and str(cell.value).startswith("http"):
                cell.hyperlink=cell.value
                cell.font=Font(name="Aptos",color="1764AB",underline="single",size=9)
    if auto_filter:
        ws.auto_filter.ref=f"A1:{get_column_letter(len(headers))}{ws.max_row}"
    ws.sheet_properties.pageSetUpPr.fitToPage=True
    return ws

def main():
    ROOT.mkdir(exist_ok=True,parents=True)
    download_repo("malaysia-4d","https://github.com/deadboy18/malaysia-4d.git")
    download_repo("damacai","https://github.com/hongster/damacai.git")
    with (MAIN/"data"/"damacai_draws.csv").open(encoding="utf-8",newline="") as f:
        raw=list(csv.DictReader(f))
    primary={r["date"]:r for r in raw if START<=r["date"]<=END}
    archive_listing = json.loads((JSONREPO/"results"/"draw_dates.json").read_text())
    secondary_dates=sorted({d[:4]+"-"+d[4:6]+"-"+d[6:] for d in archive_listing["draw_dates"]
                           if START.replace("-","")<=d<=END.replace("-","")})
    session=requests.Session()
    session.headers.update({"User-Agent":"Mozilla/5.0 (compatible; historical data audit; contact public repo)"})
    live_dates=official_dates(session)
    live_dates_set=set(live_dates) if live_dates is not None else None
    archive_dates_set=set(secondary_dates)
    baseline_set=set(primary)
    ALL_DATES=sorted(baseline_set|archive_dates_set|(live_dates_set or set()))
    print("BASELINE_DRAWS",len(primary),"ARCHIVED_DATES",len(secondary_dates),
          "LIVE_DATES",len(live_dates) if live_dates is not None else "UNAVAILABLE",flush=True)

    corrected=[]
    audits=[]
    mismatches=[]
    unresolved=[]
    source_meta={}
    official_checks=0
    verified_from_live=0
    winner_count=0
    for idx,d in enumerate(ALL_DATES,1):
        r=primary.get(d)
        j=source_json(d)
        basevals=[number(r.get(k)) for k in NUM_FIELDS] if r else [None]*23
        jvals=json_numbers(j)
        jvalid=valid_json(j,d)
        baseline_valid=(bool(r) and len(basevals)==23 and all(x is not None for x in basevals))
        date_match=bool(r and j and str(r.get("draw_seq"))==expected_id(j))
        diffs = [k for k,(a,b) in enumerate(zip(basevals,jvals)) if a!=b] if r and jvalid else []
        problem=not baseline_valid or not jvalid or not date_match or bool(diffs)
        need_live=problem and (live_dates_set is None or d in live_dates_set)
        lj=official_json(d,session) if need_live else None
        livevalid=valid_json(lj,d)
        if lj is not None:
            official_checks+=1
            if livevalid:
                verified_from_live+=1
        if livevalid:
            chosen=lj
            finalvals=json_numbers(chosen)
            origin="Official live result JSON"
        elif jvalid:
            chosen=j
            finalvals=jvals
            origin="Archived official JSON"
        elif baseline_valid:
            chosen={}
            finalvals=basevals
            origin="Historical CSV ONLY - review"
        else:
            unresolved.append([d, "No valid 23-number result available",MAIN_SRC,JSON_SRC])
            audits.append([to_date(d),r["draw_seq"] if r else "", "UNRESOLVED", False, bool(j),False,0,
                          "Missing valid result",MAIN_SRC,JSON_SRC])
            continue
        if len(finalvals)!=23 or any(x is None for x in finalvals):
            raise RuntimeError("Invalid row "+d)
        if r:
            for k,(a,b) in enumerate(zip(basevals,finalvals)):
                if a!=b:
                    mismatches.append([to_date(d),r.get("draw_seq",""),NUM_FIELDS[k],a or "",b,
                                       origin,MAIN_SRC,
                                       JSON_SRC+"/" if False else "https://github.com/hongster/damacai/blob/main/results/"+d[:4]+"/"+d.replace("-","")+".json"])
        drawseq=expected_id(chosen) if chosen.get("drawNo") else (r["draw_seq"] if r else "")
        archive_url="https://raw.githubusercontent.com/hongster/damacai/main/results/"+d[:4]+"/"+d.replace("-","")+".json"
        official_listed= "Yes" if live_dates_set is not None and d in live_dates_set else (
                           "No" if live_dates_set is not None else "Unavailable")
        verified_class = ("LIVE OFFICIAL VERIFIED" if livevalid else
                          "TWO ARCHIVES AGREE" if r and jvalid and baseline_valid and not diffs and date_match else
                          "ARCHIVE DISAGREEMENT / REVIEW" if r and jvalid and diffs else
                          "ARCHIVED JSON ONLY" if jvalid else "CSV ONLY / REVIEW")
        if not r or (jvalid and not date_match):
            mismatches.append([to_date(d),r.get("draw_seq","") if r else "",
                               "Draw date/number",r.get("draw_seq","") if r else "Absent",
                               drawseq,origin,MAIN_SRC,archive_url])
        if verified_class in ("ARCHIVE DISAGREEMENT / REVIEW","CSV ONLY / REVIEW"):
            unresolved.append([d, verified_class,MAIN_SRC,archive_url])
        corrected.append(dict(date=d,seq=drawseq,nums=finalvals,raw=chosen,src=archive_url if jvalid else MAIN_SRC,
                              verified=verified_class,official_listed=official_listed,original=bool(r),other=bool(j),origin=origin))
        audits.append([to_date(d),drawseq,verified_class,baseline_valid,jvalid,date_match,
                       len(diffs),official_listed,MAIN_SRC,archive_url])
        winner_count+=23
        if idx%500==0:print("AUDIT_PROGRESS",idx,"/",len(ALL_DATES),"CORRECTIONS",len(mismatches),flush=True)

    # Investigate known older draw-number irregularities without inventing results.
    special_dates=["2012-07-12","2012-07-13","2012-07-14","2012-07-15","2012-07-16"]
    additional=[]
    for d in special_dates:
        if d not in ALL_DATES:
            found=official_json(d,session)
            if valid_json(found,d):
                vals=json_numbers(found)
                archive_url="https://www.damacai.com.my/past-draw-result/"
                corrected.append(dict(date=d,seq=expected_id(found),nums=vals,raw=found,src=archive_url,
                                     verified="LIVE OFFICIAL VERIFIED / RECOVERED",official_listed="No" if live_dates_set else "Unavailable",
                                     original=False,other=False,origin="Official live result JSON"))
                audits.append([to_date(d),expected_id(found),"LIVE OFFICIAL VERIFIED / RECOVERED",False,False,False,0,
                               "No" if live_dates_set else "Unavailable",MAIN_SRC,archive_url])
                additional.append([d,expected_id(found),"Recovered directly from official API"])
                winner_count+=23
            else:
                additional.append([d,"","Not listed in both archived draw lists; live historical result not obtained. Do not assume draw occurred."])
    corrected.sort(key=lambda x:x["date"])
    if len({x["date"] for x in corrected}) != len(corrected):
        raise RuntimeError("Duplicate draw dates")
    if len({x["seq"] for x in corrected}) != len(corrected):
        print("WARNING_DUPLICATE_DRAW_NUMBERS",flush=True)

    core_headers=["Draw Date","Draw #","1st Prize","2nd Prize","3rd Prize"]+[f"Starter {i}" for i in range(1,11)]+[f"Consolation {i}" for i in range(1,11)]+["Verification Status","Official Date Listed","Archive Record URL","Original CSV URL"]
    core=[]
    bonus=[]
    jackpot=[]
    threed=[]
    for z in corrected:
        j=z["raw"]; nums=z["nums"]; d=z["date"]
        core.append([to_date(d), z["seq"], *nums,z["verified"],z["official_listed"],z["src"],MAIN_SRC])
        threed.append([to_date(d),z["seq"],*[v[-3:] for v in nums[:3]],z["verified"],z["src"]])
        jackpot.append([to_date(d),z["seq"],j.get("drawVenue",""),j.get("1+3DJackpot1",""),
                        j.get("1+3DJackpot2",""),j.get("3DJackpot",""),j.get("dmcJackpot1",""),
                        j.get("dmcJackpot2",""),j.get("1+3DJackpotWinning1",""),
                        j.get("1+3DJackpotWinning2",""),j.get("3DJackpotWinning",""),
                        j.get("dmcJackpotWinning1",""),j.get("dmcJackpotWinning2",""),
                        z["verified"],z["src"]])
        special = j.get("starterList3p3d") or []
        cons=j.get("consolidateList3p3d") or []
        p=[j.get("p13p3d",""),j.get("p23p3d",""),j.get("p33p3d","")]
        if any(p) or special or cons:
            bonus.append([to_date(d),z["seq"], *[str(v) or "" for v in p],
                          *[str(v) for v in (special+[""]*10)[:10]],
                          *[str(v) for v in (cons+[""]*10)[:10]],
                          j.get("p1HorseNo",""),j.get("p2HorseNo",""),j.get("p3HorseNo",""),
                          j.get("3+3DBonusp1",""),j.get("3+3DBonusp2",""),j.get("3+3DBonusp3",""),
                          z["verified"],z["src"]])

    years=Counter(z["date"][:4] for z in corrected)
    coverage=[[int(y),years[y], min(z["date"] for z in corrected if z["date"].startswith(y)),
              max(z["date"] for z in corrected if z["date"].startswith(y))] for y in sorted(years)]
    gaps=year_gap_table([{"date":z["date"],"drawseq":z["seq"]} for z in corrected])

    wb=Workbook();wb.remove(wb.active)
    readme_rows=[
        ["Dataset","Da Ma Cai historical results - detailed cross-source audit"],
        ["Period",START+" to "+END],
        ["Unique draw dates included",len(corrected)],
        ["4D prize fields per draw",23],
        ["Total 4D prize cells",winner_count],
        ["Main CSV source",MAIN_SRC],
        ["Raw draw JSON archive",JSON_SRC],
        ["Official draw-date endpoint",OFFICIAL+"/ListPastResult"],
        ["Official draw-date list retrieved","Yes" if live_dates_set is not None else "Unavailable - see limitations"],
        ["Main CSV dates",len(primary)],
        ["Archived draw list dates",len(secondary_dates)],
        ["Official draw dates in requested range",len(live_dates) if live_dates is not None else "Unavailable"],
        ["Draws matching both raw archives",sum(z["verified"]=="TWO ARCHIVES AGREE" for z in corrected)],
        ["Draws with live official result verification",verified_from_live],
        ["Different number fields corrected",sum(1 for x in mismatches if x[2] in NUM_FIELDS)],
        ["Unresolved or review-needed rows",len(unresolved)],
        ["Provenance note","Archived JSON data originated from official API, but archives are maintained by independent third parties."],
        ["Interpretation","TWO ARCHIVES AGREE means two archived scrapes match; it does NOT mean live official result was re-fetched."],
        ["Scope","Includes 4D, 3D, 3+3D Bonus when present, jackpot fields and venues when available."],
        ["Leading zeros","Winning numbers are stored as TEXT, not rounded or converted to numeric values."],
        ["Disclosure","Gaps in the source draw-date listings cannot automatically be assumed to be missed draws."],
        ["Archive audit","Each included draw's 23 winning numbers, date and draw number are independently compared in Verification Audit."]
    ]
    new_sheet(wb,"READ ME",["Item","Explanation / Result"],readme_rows,[43,124],False)
    new_sheet(wb,"All 4D Results",core_headers,core,[17,12]+[15]*23+[33,18,82,82])
    new_sheet(wb,"3D Results",["Draw Date","Draw #","1st 3D","2nd 3D","3rd 3D","Status","JSON Source"],threed,[17,12,16,16,16,33,88])
    new_sheet(wb,"3+3D Bonus",["Draw Date","Draw #","1st 6D","2nd 6D","3rd 6D"]+[f"Starter {i}" for i in range(1,11)]+[f"Consolation {i}" for i in range(1,11)]+["1st Animal Code","2nd Animal Code","3rd Animal Code","1st Bonus (RM)","2nd Bonus (RM)","3rd Bonus (RM)","Status","JSON Source"],bonus,[17,12]+[16]*23+[18]*3+[18]*3+[30,82])
    new_sheet(wb,"Jackpots and Venues",["Draw Date","Draw #","Venue","1+3D Jackpot 1 (RM)","1+3D Jackpot 2 (RM)","3D Jackpot (RM)","DMC Jackpot 1 (RM)","DMC Jackpot 2 (RM)","Jackpot 1 Winning","Jackpot 2 Winning","3D Winning","DMC 1 Winning","DMC 2 Winning","Status","JSON Source"],jackpot,[17,12,28]+[22]*10+[33,82])
    new_sheet(wb,"Verification Audit",["Draw Date","Draw #","Validation Status","CSV 23 Fields Valid","Raw JSON 23 Fields Valid","Draw Numbers Match","CSV vs JSON Differences","Official Date Listed","Main CSV Source","Official JSON Archive"],audits,[17,12,35,20,22,21,23,20,82,94])
    new_sheet(wb,"Corrections",["Draw Date","Draw #","Field","Original CSV Value","Verified Value","Correction Source","Original Source","Reference Source"],mismatches,[17,12,20,25,25,38,82,85])
    new_sheet(wb,"Annual Coverage",["Year","Draw count","First draw","Last draw"],coverage,[18,18,20,20])
    new_sheet(wb,"Draw Sequence Gaps",["Before date","After date","Previous draw #","Next draw #","Skipped IDs","Interpretation"],gaps,[20,20,18,18,18,110])
    new_sheet(wb,"2012 Gap Investigation",["Date","Recovered draw #","Investigation"],additional,[20,19,112])
    new_sheet(wb,"Unresolved Items",["Date","Issue","Main CSV Source","JSON Archive Source"],unresolved,[20,50,82,82])
    for sheet in wb:
        for row in sheet.iter_rows(min_row=2):
            for c in row:
                if isinstance(c.value,date): c.number_format="dd/mm/yyyy"
                if c.column==2 and sheet.title not in ("READ ME","Annual Coverage"):
                    c.alignment=Alignment(horizontal="center")
        if sheet.title=="Verification Audit":
            for row in sheet.iter_rows(min_row=2):
                s=row[2]
                s.font=Font(name="Aptos",size=10,bold=True,color="087C48" if s.value=="TWO ARCHIVES AGREE" or str(s.value).startswith("LIVE") else "BF6B14")
    wb.calculation.fullCalcOnLoad=True
    wb.save(OUTPUT)
    chk=load_workbook(OUTPUT,read_only=True,data_only=True)
    assert chk["All 4D Results"].max_row-1==len(corrected)
    assert chk["Verification Audit"].max_row-1==len(audits)
    assert chk["All 4D Results"]["C2"].value=="8663"
    assert chk["All 4D Results"]["E2"].value=="0740"
    last=chk["All 4D Results"][f"C{chk['All 4D Results'].max_row}"].value
    assert last=="2963"
    first=chk["All 4D Results"]["A2"].value
    assert first.date().isoformat()==START
    assert chk["All 4D Results"][f"A{chk['All 4D Results'].max_row}"].value.date().isoformat()==END
    chk.close()
    audit_summary={
        "date_range":[START,END],"rows":len(corrected),"number_cells":winner_count,
        "baseline_csv_dates":len(primary),"archived_json_date_list":len(secondary_dates),
        "official_date_list_count":len(live_dates) if live_dates is not None else None,
        "both_archive_agree":sum(z["verified"]=="TWO ARCHIVES AGREE" for z in corrected),
        "direct_official_result_validated":verified_from_live,
        "number_corrections":sum(1 for x in mismatches if x[2] in NUM_FIELDS),
        "review_required":len(unresolved),
        "archive_date_disagreements":[d for d in sorted(baseline_set^archive_dates_set)][:30],
        "official_vs_archive_dates":[d for d in sorted((live_dates_set or set())^archive_dates_set)][:30] if live_dates_set is not None else None,
        "2012_gap":additional,
        "draw_id_gaps":len(gaps),
    }
    Path("damacai_audit_summary.json").write_text(json.dumps(audit_summary,indent=2,default=str))
    print("FINAL_SUMMARY",json.dumps(audit_summary,default=str),flush=True)
    print("WORKBOOK_VERIFIED",OUTPUT,Path(OUTPUT).stat().st_size,flush=True)
if __name__=="__main__":main()
