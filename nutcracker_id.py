#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-only
# Copyright (C) 2026 Joost van Bruggen — NUTCRACKER-ID
# Wijzigingen voor publicatievoorbereiding: 2026-11-02; zie COPYRIGHT-STATUS.md.
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 only.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License
# for more details. A copy is included in COPYING.
# If not, see <https://www.gnu.org/licenses/>.
"""Local, experimental white-plumage similarity prototype for anonymous photos."""
from __future__ import annotations
import argparse, html, json, math, os
from pathlib import Path
from urllib.parse import quote
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REGIONS = ["kop", "wenkbrauw", "wang", "kruin", "nek", "keel", "hals"]
COLORS = ["#e53935", "#8e24aa", "#3949ab", "#039be5", "#00897b", "#7cb342", "#fb8c00"]

def load_image(path):
    """Load pixels without carrying original image metadata into reports."""
    with Image.open(path) as original:
        image = original.convert("RGB")
        image.load()
    image.info.clear()
    return image


def file_url(path):
    return quote(str(path).replace(os.sep, "/"), safe="/")


def candidate_groups(pairs):
    """Require the threshold for every pair inside each candidate group."""
    eligible = {
        frozenset((p["a"], p["b"]))
        for p in pairs
        if p["score"] >= 67 and p["region_count"] >= 3 and p["matched_features"] >= 7
    }
    groups = []
    for pair in pairs:
        a, b = pair["a"], pair["b"]
        if frozenset((a, b)) not in eligible:
            continue
        left = next((g for g in groups if a in g), None)
        right = next((g for g in groups if b in g), None)
        if left is not None and left is right:
            continue
        left_members = left if left is not None else [a]
        right_members = right if right is not None else [b]
        if not all(frozenset((x, y)) in eligible for x in left_members for y in right_members):
            continue
        merged = list(left_members) + list(right_members)
        if left is not None:
            groups.remove(left)
        if right is not None:
            groups.remove(right)
        groups.append(merged)
    return groups


def gray(im):
    return np.asarray(ImageOps.grayscale(im), dtype=np.float32) / 255.0

def find_eye(a):
    """Heuristic eye proposal: dark compact center surrounded by brighter pixels."""
    h,w=a.shape
    if min(h,w)<24: return None,0.0
    # Restrict to upper/middle crop; eye candidate is locally dark with a brighter ring.
    best=(-1,None)
    # Search the upper image area where these framed bird portraits usually show the head.
    # This is a heuristic and photos with a differently placed subject may be mislocalized.
    for y in range(max(4,int(h*.06)), min(h-4,int(h*.36)), max(1,h//140)):
        for x in range(max(4,int(w*.12)), min(w-4,int(w*.88)), max(1,w//100)):
            c=float(a[y-1:y+2,x-1:x+2].mean())
            ring=np.concatenate((a[y-4:y-2,x-2:x+3].ravel(),a[y+2:y+4,x-2:x+3].ravel(),a[y-2:y+3,x-4:x-2].ravel(),a[y-2:y+3,x+2:x+4].ravel()))
            contrast=float(ring.mean()-c)
            # favor moderate dark core and ring contrast, penalize black background
            score=contrast - max(0,.18-c)*.25
            if score>best[0]: best=(score,(x,y))
    return best[1], max(0.0,min(1.0,best[0]*3))

def propose_regions(im, direction):
    a=gray(im); h,w=a.shape; eye,conf=find_eye(a)
    if eye is None or conf < .12: return {}, conf, eye
    ex,ey=eye; s=max(14,min(w*.35,h*.38)); d=(-1 if direction=="links" else 1 if direction=="rechts" else direction)
    # Relative boxes are deliberately broad proposals. Clip to the image bounds.
    raw={
      "kop":(ex-.48*s,ey-.36*s,ex+.55*s,ey+.68*s),
      "wenkbrauw":(ex-.32*s,ey-.31*s,ex+.35*s,ey+.02*s),
      "wang":(ex-.38*s,ey+.03*s,ex+.42*s,ey+.48*s),
      "kruin":(ex-.36*s,ey-.67*s,ex+.30*s,ey-.27*s),
      "nek":(ex-d*.95*s,ey+.18*s,ex-d*.24*s,ey+1.04*s),
      "keel":(ex+d*.15*s,ey+.30*s,ex+d*.88*s,ey+1.04*s),
      "hals":(ex-.48*s,ey+.64*s,ex+.50*s,ey+1.30*s),
    }
    boxes={}
    for k,(x1,y1,x2,y2) in raw.items():
        l=max(0,int(min(x1,x2))); r=min(w,int(max(x1,x2))); t=max(0,int(y1)); b=min(h,int(y2))
        if r-l>=8 and b-t>=8: boxes[k]=(l,t,r,b)
    return boxes,conf,eye

def describe(im, box):
    crop=im.crop(box); a=gray(crop); h,w=a.shape
    if min(h,w)<8: return None
    # Local high-pass brightness detects small, bright feather marks while suppressing broad illumination.
    smooth=np.asarray(Image.fromarray(np.uint8(a*255)).filter(ImageFilter.GaussianBlur(radius=max(1,min(w,h)*.055)),),dtype=np.float32)/255
    residual=a-smooth
    mask=(a>.43)&(residual>.035)
    # Coarse normalized mask gives a repeatable pattern descriptor; no image synthesis.
    small=Image.fromarray(np.uint8(mask*255)).resize((32,32),Image.Resampling.BOX)
    m=np.asarray(small,dtype=np.float32)/255
    # Connected components on 32x32 mask.
    binary=m>.16; seen=np.zeros_like(binary); pts=[]
    for yy in range(32):
      for xx in range(32):
        if not binary[yy,xx] or seen[yy,xx]: continue
        stack=[(yy,xx)]; seen[yy,xx]=1; comp=[]
        while stack:
          cy,cx=stack.pop(); comp.append((cy,cx))
          for ny,nx in ((cy-1,cx),(cy+1,cx),(cy,cx-1),(cy,cx+1),(cy-1,cx-1),(cy-1,cx+1),(cy+1,cx-1),(cy+1,cx+1)):
            if 0<=ny<32 and 0<=nx<32 and binary[ny,nx] and not seen[ny,nx]: seen[ny,nx]=1; stack.append((ny,nx))
        if 2<=len(comp)<=40:
          pts.append([sum(p[1] for p in comp)/len(comp)/32, sum(p[0] for p in comp)/len(comp)/32])
    sharp=float(np.clip(np.std(residual)*8,0,1)); coverage=float(mask.mean())
    return {"mask":m.tolist(),"points":pts,"count":len(pts),"sharpness":round(sharp,3),"coverage":round(coverage,3),"size":[w,h]}

def direction_for(im):
    # Lightweight orientation proxy from the photo's image content: weighted foreground centroid
    # against central crop. Mark uncertain directions as unknown and omit such comparisons.
    a=gray(im); h,w=a.shape
    dark=a<.35; yy,xx=np.where(dark)
    if len(xx)<20: return None
    # Only a weak composition heuristic; it is not a validated beak-side detector.
    cx=float(np.median(xx)); return "links" if cx<w*.46 else "rechts" if cx>w*.54 else None

def compare_region(a,b):
    pa,pb=a["points"],b["points"]
    # Greedy one-to-one spatial matches; coordinates are normalized within proposed ROI.
    candidates=sorted((math.dist(x,y),i,j) for i,x in enumerate(pa) for j,y in enumerate(pb))
    useda=set(); usedb=set(); matched=0
    for dist,i,j in candidates:
      if dist>.20: break
      if i not in useda and j not in usedb: useda.add(i); usedb.add(j); matched+=1
    aa=np.asarray(a["mask"]); bb=np.asarray(b["mask"]); shifts=[]
    for dy in range(-2,3):
      for dx in range(-2,3):
        ay=slice(max(0,dy),min(32,32+dy)); by=slice(max(0,-dy),min(32,32-dy))
        ax=slice(max(0,dx),min(32,32+dx)); bx=slice(max(0,-dx),min(32,32-dx))
        shifts.append(float(np.mean(aa[ay,ax]*bb[by,bx])))
    corr=max(shifts) if shifts else 0
    count_sim=min(len(pa),len(pb))/max(1,max(len(pa),len(pb)))
    spatial=min(1,matched/max(1,min(len(pa),len(pb))))
    score=100*(.65*spatial+.20*count_sim+.15*min(1,corr*18))
    return round(score,1),matched

def locate_head_crop(im):
    """Propose an eye-centered head/neck crop using local dark-round-feature contrast.

    This deliberately returns unknown when the strongest candidate is weak or ambiguous.
    It is a lightweight image heuristic, not a trained bird detector.
    """
    # Work on a bounded preview but map the selected rectangle back to original pixels.
    scale=min(1.0,900/im.width)
    preview=im.resize((max(1,int(im.width*scale)),max(1,int(im.height*scale))),Image.Resampling.LANCZOS) if scale<1 else im
    a=np.asarray(ImageOps.grayscale(preview),dtype=np.float32)/255.0
    h,w=a.shape
    if min(w,h)<40: return None,0.0,None
    # Multi-scale center/ring contrast. A round, dark eye is a better cue than a
    # single darkest pixel, which often lands on branches or the back.
    best_score=-1.0; best=None; scores=[]
    for r in (2,3,4,5,7,9):
        img=Image.fromarray(np.uint8(a*255))
        core=np.asarray(img.filter(ImageFilter.BoxBlur(max(1,r//2))),dtype=np.float32)/255.0
        broad=np.asarray(img.filter(ImageFilter.BoxBlur(2*r)),dtype=np.float32)/255.0
        contrast=broad-core
        valid=(a<.48)&(a>.015)
        score=contrast*np.clip((.50-a)/.35,0,1)*valid
        # Avoid borders and emphasize compactness: elongated dark lines are often beaks.
        score[:max(8,3*r),:]=0; score[-max(8,3*r):,:]=0; score[:,:max(8,3*r)]=0; score[:,-max(8,3*r):]=0
        idx=int(np.argmax(score)); y,x=np.unravel_index(idx,score.shape); val=float(score[y,x])
        scores.append(val)
        if val>best_score: best_score=val; best=(x,y,r)
    if best is None: return None,0.0,None
    x,y,r=best
    # Estimate direction from the longer dark, narrow extension at eye height (the bill).
    def extension(sign):
        total=0
        for dist in range(2*r, min(28*r,w//2), max(1,r)):
            xx=x+sign*dist
            if not 0<=xx<w: break
            band=a[max(0,y-r):min(h,y+r+1),max(0,xx-r//2):min(w,xx+r//2+1)]
            if band.size and float((band<.32).mean())>.55: total+=1
            elif total: break
        return total
    left,right=extension(-1),extension(1)
    direction=1 if right>left*1.25 and right>=3 else -1 if left>right*1.25 and left>=3 else 0
    # Confidence considers cue strength and whether this candidate wins distinctly.
    sorted_scores=sorted(scores,reverse=True); distinct=(sorted_scores[0]-sorted_scores[1]) if len(sorted_scores)>1 else best_score
    confidence=float(np.clip((best_score-.025)*14,0,1)*np.clip(.55+distinct*8,0,1))
    # A conservative crop extends away from the bill and down the neck. All pixels
    # are copied directly from the original image; no artificial detail is added.
    ox=x/scale; oy=y/scale; rr=r/scale
    if direction==0 or confidence<.20: return None,confidence,(int(ox),int(oy))
    # Make the eye sit near the bill-facing edge and upper quarter of a broad crop;
    # this retains the crown, cheek, and as much visible neck/throat as framing allows.
    cropw=max(30*rr,.30*im.width); croph=max(34*rr,.42*im.height)
    eye_fraction=.68 if direction<0 else .32
    left_x=ox-eye_fraction*cropw; right_x=left_x+cropw
    top=oy-.24*croph; bottom=top+croph
    box=(max(0,int(left_x)),max(0,int(top)),min(im.width,int(right_x)),min(im.height,int(bottom)))
    if box[2]-box[0]<40 or box[3]-box[1]<40: return None,confidence,(int(ox),int(oy))
    return box,confidence,(int(ox),int(oy))

def create_crop_review(photos_dir, output_dir):
    files=sorted(photos_dir.glob('*.png'))
    if not files: raise SystemExit(f"Geen PNG-foto's gevonden in {photos_dir}")
    output_dir.mkdir(parents=True,exist_ok=True)
    (output_dir/'originals').mkdir(exist_ok=True)
    items=[]
    for f in files:
        im=load_image(f)
        box,confidence,point=locate_head_crop(im)
        stem=f.stem
        # Preserve original image files; report derivatives are kept in a separate directory.
        im.save(output_dir/'originals'/f.name)
        crop_name=None
        if box:
            crop_name=f'{stem}_uitsnede.png'
            im.crop(box).save(output_dir/crop_name)
        overlay=im.copy(); draw=ImageDraw.Draw(overlay)
        if box:
            draw.rectangle(box,outline='red',width=max(3,im.width//350))
        elif point:
            x,y=point; r=max(8,im.width//60); draw.ellipse((x-r,y-r,x+r,y+r),outline='orange',width=max(3,im.width//350))
        overlay.thumbnail((900,700)); overlay.save(output_dir/f'{stem}_kader.jpg',quality=90)
        items.append({'name':f.name,'width':im.width,'height':im.height,'box':box,'point':point,'confidence':round(confidence,3),'crop':crop_name,'overlay':f'{stem}_kader.jpg','status':'kader voorgesteld; menselijk te controleren' if box else 'kop niet betrouwbaar gelokaliseerd'})
    # Handmatige beoordelingen horen bij de dataset en worden niet meegeleverd.
    for item in items:
        item['visual_review']='niet beoordeeld'
    (output_dir/'kopdetectie.json').write_text(json.dumps(items,ensure_ascii=False,indent=2),encoding='utf-8')
    write_crop_html(items,output_dir/'index.html')
    good=sum(bool(x['box']) for x in items)
    print(f"Foto's: {len(items)} | kader voorgesteld: {good} | als onbetrouwbaar gemarkeerd: {len(items)-good}")

def write_crop_html(items,path):
    esc=lambda s:html.escape(str(s))
    parts=['<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Kopdetectiecontrole</title>', '<style>body{font:15px system-ui;max-width:1500px;margin:2rem auto;padding:0 1rem;color:#222}.item{border:1px solid #bbb;margin:1rem 0;padding:1rem}.row{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.7rem}.row img{width:100%;height:330px;object-fit:contain;background:#eee}.label{font-weight:600}.warn{color:#8a4300}code{overflow-wrap:anywhere}@media(max-width:800px){.row{grid-template-columns:1fr}}</style>', '<h1>Automatische kopuitsneden</h1><p>Per foto: origineel, rood voorgesteld kader en uitsnede. De uitsnede bevat alleen oorspronkelijke pixels. Oranje cirkel betekent dat het programma geen betrouwbaar kader kon vaststellen. Automatische kwaliteit is geen menselijke bevestiging.</p>']
    reliable=sum(bool(x['box']) for x in items)
    total=len(items)
    parts.append(f'<p>Automatisch kader voorgesteld: {reliable}/{total}; geen kader voorgesteld: {total-reliable}/{total}. Handmatige visuele beoordeling: niet uitgevoerd.</p>')
    for it in items:
        original='originals/'+it['name']; overlay=it['overlay']; crop=it['crop'] or ''
        parts.append(f'<section class="item"><h2>{esc(it["name"])}</h2><p class="label">{esc(it["status"])} · automatische aanwijzingsscore {it["confidence"]} · visuele controle: {esc(it["visual_review"])} · bron {it["width"]}×{it["height"]}</p><div class="row"><div><b>Origineel</b><img loading="lazy" src="{esc(file_url(original))}"></div><div><b>Rood kader</b><img loading="lazy" src="{esc(file_url(overlay))}"></div><div><b>Uitsnede</b>'+ (f'<img loading="lazy" src="{esc(file_url(crop))}">' if crop else '<p class="warn">Geen uitsnede gemaakt: koplocatie onbekend.</p>') +'</div></div></section>')
    parts.append('<h2>Beperkingen</h2><p>De detector gebruikt lokale donker-lichtcontrasten en een langwerpige donkere lijn als aanwijzing voor oog en snavel. Takken, schors, schaduw en een onscherp oog kunnen deze aanwijzingen nabootsen. De score meet alleen de sterkte van die aanwijzingen; hij bewijst geen juiste plaatsing. Controleer de kaders vóór patroonvergelijking.</p></html>')
    path.write_text(''.join(parts),encoding='utf-8')

def main():

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--photos", type=Path, help="expliciete invoermap met lokale PNG-afbeeldingen")
    ap.add_argument("--output", type=Path, help="uitvoermap voor patroonvergelijking")
    ap.add_argument("--crop-review", action="store_true", help="alleen kopuitsnedecontrole")
    ap.add_argument("--crop-output", type=Path, help="uitvoermap voor kopuitsnedecontrole")
    args = ap.parse_args()
    if args.photos is None:
        if args.crop_review or args.output is not None or args.crop_output is not None:
            ap.error("Geef --photos expliciet op om afbeeldingen te verwerken.")
        ap.print_help()
        return
    if not args.photos.is_dir():
        ap.error("De opgegeven invoermap bestaat niet of is geen map.")
    args.photos = args.photos.resolve()
    files = sorted(args.photos.glob("*.png"))
    if not files:
        ap.error("De invoermap bevat geen PNG-afbeeldingen.")
    try:
        for image_path in files:
            with Image.open(image_path) as image:
                if image.format != "PNG":
                    raise ValueError("Geen PNG")
                image.verify()
    except (OSError, ValueError):
        ap.error("De invoermap bevat een onleesbare of ongeldige PNG-afbeelding.")
    default_root = Path(__file__).resolve().parent / ".local-output"
    output = (args.crop_output if args.crop_review else args.output)
    output = (output if output is not None else
              default_root / ("kopcontrole" if args.crop_review else "patronen")).resolve()
    if output == args.photos or output.is_relative_to(args.photos):
        ap.error("Kies een uitvoermap buiten de invoermap.")
    if args.crop_review:
        create_crop_review(args.photos, output)
        return
    args.output = output
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "regions").mkdir(exist_ok=True)
    records=[]
    for f in files:
      im=load_image(f); direction=direction_for(im); boxes,conf,eye=propose_regions(im,direction or 1)
      regions={}
      for name,box in boxes.items():
        desc=describe(im,box)
        if desc: regions[name]=desc
      # Region availability requires several detectable bright features and tolerable sharpness.
      available={k:v for k,v in regions.items() if v["count"]>=2 and v["sharpness"]>=.04}
      overlay=im.copy(); draw=ImageDraw.Draw(overlay)
      for i,(name,box) in enumerate(boxes.items()):
        draw.rectangle(box,outline=COLORS[i],width=max(2,im.width//500)); draw.text((box[0],box[1]),name,fill=COLORS[i],stroke_width=2,stroke_fill="white")
        if name in available: im.crop(box).save(args.output/"regions"/f"{f.stem}_{name}.png")
      overlay.thumbnail((1200,900)); overlay.save(args.output/"regions"/f"{f.stem}_overlay.jpg",quality=88)
      records.append({"name":f.name,"direction":direction,"eye_confidence":round(conf,3),"eye":eye,"regions":regions,"available":sorted(available),"usable":len(available)>=2})
    pairs=[]
    for i,a in enumerate(records):
      for b in records[i+1:]:
        if not a["direction"] or a["direction"]!=b["direction"]: continue
        shared=sorted(set(a["available"])&set(b["available"]))
        if not shared: continue
        per=[]; total_matches=0
        for reg in shared:
          sc,n=compare_region(a["regions"][reg],b["regions"][reg]); per.append({"region":reg,"score":sc,"features_a":a["regions"][reg]["count"],"features_b":b["regions"][reg]["count"],"matched":n}); total_matches+=n
        # Missing regions do not enter the mean. Support count is shown separately to prevent overclaiming.
        score=round(sum(x["score"] for x in per)/len(per),1)
        pairs.append({"a":a["name"],"b":b["name"],"score":score,"regions":per,"region_count":len(per),"matched_features":total_matches})
    pairs.sort(key=lambda p:p["score"],reverse=True)
    groups = candidate_groups(pairs)
    assigned = {name for group in groups for name in group}
    data={"photos":records,"pairs":pairs,"groups":groups,"unassigned":[r["name"] for r in records if r["name"] not in assigned],"insufficient":[r["name"] for r in records if not r["usable"]],"method":"Bright local feather-mark proposals in approximate eye-anchored regions; missing regions excluded from pair mean."}
    (args.output/"groepsindeling.json").write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    write_html(data,args.output/"index.html")
    print(f"Foto's: {len(records)} | kandidaatgroepen: {len(groups)} | paren met gedeelde gebieden: {len(pairs)} | onvoldoende/ongegroepeerd: {len(data['unassigned'])}")

def write_html(data,path):
    esc=lambda x:html.escape(str(x))
    s=['<!doctype html><html lang="nl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Nutcracker-ID | gedeeltelijke verenpatronen</title>', '<style>body{font:15px system-ui;max-width:1200px;margin:2rem auto;padding:0 1rem;color:#222}table{border-collapse:collapse;width:100%;margin:1rem 0}td,th{border:1px solid #ccc;padding:.45rem;text-align:left;vertical-align:top}th{background:#eee}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:1rem}.card{border:1px solid #ccc;padding:.7rem}.card img{width:100%}.small{color:#555;font-size:.9em}code{overflow-wrap:anywhere}</style><h1>Nutcracker-ID: gedeeltelijk zichtbare verenpatronen</h1>', '<p><b>Technische gelijkenisscore, geen kans op dezelfde identiteit.</b> Alleen overeenkomstige voorgestelde gebieden met dezelfde geschatte kijkzijde tellen mee. Ontbrekende gebieden leveren geen straf op.</p>', '<p>De oogpositie, kijkzijde en anatomische vakken zijn ruwe beeldheuristieken. Controleer de gekleurde uitsneden visueel. Scores zijn experimenteel en geen bewezen herkenning.</p>', '<h2>Kandidaatgroepen</h2>']
    if not data['groups']: s.append('<p>Geen kandidaatgroepen voldeden aan de minimale hoeveelheid gedeeld bewijs.</p>')
    for i,g in enumerate(data['groups'],1): s.append(f'<h3>Groep {i}</h3><p>'+', '.join(f'<code>{esc(x)}</code>' for x in g)+'</p>')
    s.append('<h2>Hoogste paarscores</h2><table><tr><th>Foto A</th><th>Foto B</th><th>Score</th><th>Gebieden</th><th>Herkenbare / gekoppelde kenmerken</th></tr>')
    for p in data['pairs']:
      detail='; '.join(f"{esc(r['region'])}: {r['score']}% ({r['features_a']}/{r['features_b']} kenmerken; {r['matched']} overeenkomend)" for r in p['regions'])
      s.append(f"<tr><td>{esc(p['a'])}</td><td>{esc(p['b'])}</td><td>{p['score']}%</td><td>{p['region_count']}: {detail}</td><td>{p['matched_features']} koppelingen</td></tr>")
    s.append('</table><h2>Onvoldoende informatie</h2><p>'+str(len(data['insufficient']))+' foto’s leverden minder dan twee gebieden met voldoende gevonden kenmerken op: '+', '.join(f'<code>{esc(x)}</code>' for x in data['insufficient'])+'</p><h2>Foto-overzicht</h2><p>Foto’s zonder kandidaatgroep zijn niet automatisch onbruikbaar. Alle uitsneden zijn benaderingen.</p><div class="grid">')
    for r in data['photos']:
      overlay='regions/'+Path(r['name']).stem+'_overlay.jpg'
      feature_text='; '.join(f"{esc(k)} {v['count']} (scherpte {v['sharpness']})" for k,v in r['regions'].items())
      s.append(f'<div class="card"><img loading="lazy" src="{esc(file_url(overlay))}"><b>{esc(r["name"])}</b><p>Kijkzijde-proxy: {esc(r["direction"] or "onduidelijk")}<br>Gebieden: {esc(", ".join(r["available"]) or "geen voldoende informatie")}<br>Ooganker-zekerheid: {r["eye_confidence"]}</p><p class="small">Kenmerken per voorgesteld gebied: {feature_text}</p></div>')
    s.append('</div><h2>Beperkingen</h2><ul><li>Geen getraind vogel- of landmarkmodel gebruikt; de gebiedsgrenzen en kijkzijde zijn grof geschat.</li><li>Lokale helderheidsvlekken kunnen echte veren missen of lichtreflecties meetellen.</li><li>Belichting, onscherpte, verenstand en kijkhoek veranderen de kenmerken.</li><li>Een technische score is geen identiteitsoordeel. Groepering vraagt minimaal drie gedeelde gebieden en zeven gekoppelde kenmerken.</li><li>Alleen de PNG-bestanden uit de expliciet opgegeven map zijn verwerkt.</li></ul></html>')
    path.write_text(''.join(s),encoding='utf-8')

if __name__=='__main__': main()
