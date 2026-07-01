#!/usr/bin/env python3
# Regenerate manifest.json for the One More Door media kit.
# Usage: drop files into media/files/ then run: python3 build_manifest.py
import os, json, datetime
try:
    from PIL import Image; HAVE_PIL=True
except Exception: HAVE_PIL=False

HERE=os.path.dirname(os.path.abspath(__file__))
FILES=os.path.join(HERE,"files"); THUMBS=os.path.join(HERE,"thumbs")
os.makedirs(THUMBS,exist_ok=True)
VIDEO_DL=os.environ.get("VIDEO_DL","")
UID="e6d372aa80c2623d7c8f2a7bb8481dd1"

# filename -> (category, nice title). Unknown files fall back to "More".
MAP={
 "building-hero.jpg":("Photos","Teen Living Center — Exterior (Hero)"),
 "building-front.jpg":("Photos","Teen Living Center — Front Entrance"),
 "common-room.jpg":("Photos","Common Room / Lounge"),
 "bedroom.jpg":("Photos","Student Bedroom"),
 "teen-living-center-logo.png":("Logos","Teen Living Center Logo (PNG)"),
 "teen-living-center-logo.webp":("Logos","Teen Living Center Logo (WEBP)"),
 "switchpoint-logo.png":("Logos","Switchpoint Logo (PNG)"),
 "sunburst-mark.svg":("Logos","Sunburst Mark (SVG)"),
 "tlc-faq-trifold.pdf":("Print & Documents","TLC FAQ Tri-Fold Brochure (PDF)"),
 "tlc-brochure.jpg":("Print & Documents","TLC Brochure Panel"),
 "tlc-peachjar-flyer.jpg":("Print & Documents","Peachjar Flyer"),
 "stability-flyer-1.jpg":("Print & Documents","“Where Stability Begins” Graphic 1"),
 "stability-flyer-2.jpg":("Print & Documents","“Where Stability Begins” Graphic 2"),
}
ORDER=["Photos","Logos","Print & Documents","More","Video"]
IMG={".jpg",".jpeg",".png",".webp"}

def prettify(stem):
    return stem.replace("-"," ").replace("_"," ").strip().title()

def ensure_thumb(fn, stem, ext):
    if ext==".svg": return "files/"+fn
    if ext in IMG:
        tp=os.path.join(THUMBS,stem+".jpg")
        if not os.path.exists(tp) and HAVE_PIL:
            try:
                im=Image.open(os.path.join(FILES,fn)).convert("RGBA")
                bg=Image.new("RGB",im.size,(255,255,255)); bg.paste(im,mask=im.split()[-1])
                if bg.width>480: bg=bg.resize((480,int(bg.height*480/bg.width)),Image.LANCZOS)
                bg.save(tp,"JPEG",quality=80,optimize=True)
            except Exception: return "files/"+fn
        return "thumbs/"+stem+".jpg" if os.path.exists(tp) else "files/"+fn
    return None  # pdf/other -> badge

cats={}
for fn in sorted(os.listdir(FILES)):
    p=os.path.join(FILES,fn)
    if not os.path.isfile(p): continue
    stem,ext=os.path.splitext(fn); ext=ext.lower()
    cat,title=MAP.get(fn,("More",prettify(stem)))
    cats.setdefault(cat,[]).append({
        "title":title,"file":"files/"+fn,"thumb":ensure_thumb(fn,stem,ext),
        "type":ext.lstrip(".").upper(),"bytes":os.path.getsize(p)})

manifest={"updated":datetime.date.today().isoformat(),"categories":[]}
for c in ORDER:
    if c=="Video": continue
    if cats.get(c):
        note={"Photos":"Full-resolution JPG — click Download.","Logos":"Transparent background."}.get(c,"")
        manifest["categories"].append({"name":c,"note":note,"items":cats[c]})
# any leftover categories not in ORDER
for c,items in cats.items():
    if c not in ORDER: manifest["categories"].append({"name":c,"note":"","items":items})
# video
vid={"title":"Teen Living Center — Film","stream_uid":UID,
     "poster":f"https://videodelivery.net/{UID}/thumbnails/thumbnail.jpg?time=3s&height=480",
     "embed":f"https://iframe.videodelivery.net/{UID}","type":"MP4"}
if VIDEO_DL: vid["file"]=VIDEO_DL
manifest["categories"].append({"name":"Video","note":"Hosted on Cloudflare Stream.","items":[vid]})

json.dump(manifest,open(os.path.join(HERE,"manifest.json"),"w"),indent=2)
print("manifest.json ->",[c["name"]+f"({len(c['items'])})" for c in manifest["categories"]])
