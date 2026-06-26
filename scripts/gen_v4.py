#!/usr/bin/env python3
"""
Xiaohongshu card generator v5 - Macaron/crayon style + proper tag handling.
Usage: python gen_v4.py --post-name <name>
"""

import os, json, time, random, subprocess, sys, urllib.request

BASE = "D:/Hermes agnet"
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
URL = "https://creator.xiaohongshu.com/publish/publish?source=official"

# Crayon-style SVG backgrounds at low opacity (inline, base64-free)
CRAYON_BG = """
<svg xmlns="http://www.w3.org/2000/svg" width="540" height="720" viewBox="0 0 540 720">
  <!-- hand-drawn circles -->
  <circle cx="80" cy="100" r="40" fill="none" stroke="currentColor" stroke-width="2" opacity="0.06"/>
  <circle cx="450" cy="200" r="60" fill="none" stroke="currentColor" stroke-width="2.5" opacity="0.05"/>
  <circle cx="120" cy="500" r="30" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.06"/>
  <circle cx="420" cy="600" r="50" fill="none" stroke="currentColor" stroke-width="2" opacity="0.05"/>
  <circle cx="270" cy="360" r="80" fill="none" stroke="currentColor" stroke-width="3" opacity="0.04"/>
  <!-- hand-drawn squiggly lines -->
  <path d="M0 50 Q100 20 200 50 T400 50 T540 50" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.06"/>
  <path d="M0 150 Q80 180 160 150 T320 150 T540 150" fill="none" stroke="currentColor" stroke-width="1" opacity="0.05"/>
  <path d="M0 670 Q120 640 240 670 T480 670 T540 650" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.06"/>
  <!-- hand-drawn stars/dots -->
  <text x="50" y="300" font-size="20" opacity="0.08" fill="currentColor">✦</text>
  <text x="470" y="450" font-size="16" opacity="0.07" fill="currentColor">✦</text>
  <text x="170" y="650" font-size="14" opacity="0.06" fill="currentColor">✦</text>
  <text x="380" y="80" font-size="18" opacity="0.07" fill="currentColor">✦</text>
  <!-- tiny dots -->
  <circle cx="160" cy="180" r="3" fill="currentColor" opacity="0.06"/>
  <circle cx="380" cy="320" r="2.5" fill="currentColor" opacity="0.05"/>
  <circle cx="90" cy="400" r="2" fill="currentColor" opacity="0.06"/>
  <circle cx="450" cy="520" r="3" fill="currentColor" opacity="0.05"/>
  <circle cx="220" cy="250" r="2" fill="currentColor" opacity="0.06"/>
  <!-- hand-drawn underline -->
  <path d="M30 180 Q100 186 200 180 Q300 174 400 180" fill="none" stroke="currentColor" stroke-width="1.5" opacity="0.05"/>
  <path d="M100 420 Q200 426 300 420 Q400 414 500 420" fill="none" stroke="currentColor" stroke-width="1" opacity="0.04"/>
</svg>
"""

SCHEMES = {
    "macaron": {"bg": "#FFD1DC", "tc": "#5D4037", "lc": "#4E342E", "ac": "#FF8A80", "pattern": CRAYON_BG},
    "macaron-blue": {"bg": "#B3E5FC", "tc": "#1A237E", "lc": "#283593", "ac": "#40C4FF", "pattern": CRAYON_BG},
    "macaron-green": {"bg": "#C8E6C9", "tc": "#1B5E20", "lc": "#2E7D32", "ac": "#69F0AE", "pattern": CRAYON_BG},
    "macaron-yellow": {"bg": "#FFF9C4", "tc": "#4E342E", "lc": "#5D4037", "ac": "#FFD54F", "pattern": CRAYON_BG},
    "macaron-purple": {"bg": "#E1BEE7", "tc": "#311B92", "lc": "#4527A0", "ac": "#CE93D8", "pattern": CRAYON_BG},
    "macaron-peach": {"bg": "#FFE0B2", "tc": "#4E342E", "lc": "#5D4037", "ac": "#FFAB91", "pattern": CRAYON_BG},
}

def make_card(title, sub, scheme_name, out):
    s = SCHEMES.get(scheme_name, SCHEMES["macaron"])
    sub_html = ""
    
    # Card with macaron bg + crayon SVG pattern overlayed at low opacity
    # SVG uses currentColor which inherits from text color but at ~5% opacity
    pattern = s.get("pattern", "").replace("currentColor", s["tc"])
    
    if sub and sub.strip():
        for line in sub.split("\\n"):
            sub_html += f'<div class="line">{line}</div>'

    html = f'''<!DOCTYPE html><html><meta charset="utf-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{display:flex;justify-content:center;align-items:center;background:#ccc;min-height:720px;overflow:hidden;}}
::-webkit-scrollbar{{display:none;}}
.card{{width:540px;height:720px;position:relative;background:{s["bg"]};overflow:hidden;display:flex;flex-direction:column;justify-content:center;}}
.bg{{position:absolute;top:0;left:0;width:100%;height:100%;}}
.content{{position:relative;z-index:2;padding:44px 36px;}}
.title{{font-size:48px;font-weight:900;color:{s["tc"]};line-height:1.2;margin-bottom:16px;font-family:'SimHei','黑体','Noto Sans SC',sans-serif;}}
.line{{font-size:36px;font-weight:700;color:{s["lc"]};line-height:1.5;margin-bottom:2px;font-family:'SimHei','黑体','Noto Sans SC',sans-serif;}}
</style>
<body><div class="card">
<div class="bg">{pattern}</div>
<div class="content">
<div class="title">{title}</div>
{sub_html}
</div>
</div></body></html>'''

    os.makedirs(os.path.dirname(out), exist_ok=True)
    hp = out.replace(".png", ".html")
    with open(hp, "w", encoding="utf-8") as f:
        f.write(html)
    subprocess.run([
        CHROME, "--headless=new", f"--screenshot={out}",
        "--window-size=540,720", "--device-scale-factor=2",
        f"file:///{hp.replace(os.sep, '/')}"
    ], capture_output=True, timeout=15)
    return os.path.exists(out)


def main():
    post_name = None
    for i, a in enumerate(sys.argv):
        if a == "--post-name" and i+1 < len(sys.argv):
            post_name = sys.argv[i+1]
            break
    if not post_name:
        print("Usage: python gen_v4.py --post-name <name>")
        sys.exit(1)

    config_path = os.path.join(BASE, "posts", f"{post_name}.json")
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    try:
        r = urllib.request.urlopen(f"http://localhost:{cfg['port']}/json/version", timeout=3)
        print(f"Chrome OK port {cfg['port']}")
    except:
        print(f"Chrome on port {cfg['port']} not responding!")
        sys.exit(1)

    out_dir = os.path.join(BASE, "assets", post_name)
    os.makedirs(out_dir, exist_ok=True)

    card_configs = [
        ("01_cover.png",    "card_cover_title", "card_cover_sub", "card_cover_style"),
        ("02_why.png",      "card2_title",      "card2_sub",      "card2_style"),
        ("03_problems.png", "card3_title",      "card3_sub",      "card3_style"),
        ("04_tips.png",     "card4_title",      "card4_sub",      "card4_style"),
    ]

    images = []
    for fname, tkey, skey, stylekey in card_configs:
        p = os.path.join(out_dir, fname)
        print(f"{fname}...", end=" ")
        ok = make_card(cfg.get(tkey,""), cfg.get(skey,""), cfg.get(stylekey,"macaron"), p)
        if ok:
            sz = os.path.getsize(p)//1024
            print(f"✅ {sz}KB")
            images.append(p)
        else:
            print("❌"); return

    print(f"\n✅ {len(images)} cards")
    print("Uploading to draft...")

    from DrissionPage import ChromiumPage
    p = ChromiumPage(addr_or_opts=cfg['port'])
    p.get(URL)
    time.sleep(random.uniform(3,5))
    
    # Click 上传图文 tab
    p.run_js('var a=document.querySelectorAll("span,div");for(var i=0;i<a.length;i++){var t=a[i].textContent.trim();if(t==="\\u4e0a\\u4f20\\u56fe\\u6587"&&a[i].offsetHeight>0){var e=a[i];for(var j=0;j<5;j++){if(e.tagName==="DIV"){e.click();return;}if(e.parentElement)e=e.parentElement;}}}')
    time.sleep(random.uniform(3,5))

    # Upload images
    for img in images:
        inp = p.ele('tag:input@type=file')
        if inp:
            inp.input(img)
            print(f"  Uploaded: {os.path.basename(img)}")
            time.sleep(random.uniform(3,6))

    time.sleep(random.uniform(3,5))
    
    # Fill title
    title = cfg["title"][:20]
    p.run_js('var ins=document.querySelectorAll("input");for(var i=0;i<ins.length;i++){var ph=ins[i].placeholder||"";if(ph.includes("\\u6807\\u9898")){var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;s.call(ins[i],arguments[0]);ins[i].dispatchEvent(new Event("input",{bubbles:true}));}}', title)
    time.sleep(random.uniform(2,4))
    
    # Fill body (without #tags in text - tags added separately via UI)
    body_text = cfg["body"]
    # Remove #tags from body text if they exist (tags added separately)
    import re
    body_clean = re.sub(r'#[^\s#]+', '', body_text).strip()
    # Clean up extra whitespace
    body_clean = re.sub(r'\n{3,}', '\n\n', body_clean)
    
    p.run_js('var eds=document.querySelectorAll("[contenteditable=true]");for(var i=0;i<eds.length;i++){if(eds[i].offsetHeight>50){eds[i].focus();eds[i].innerText=arguments[0];eds[i].dispatchEvent(new Event("input",{bubbles:true}));}}', cfg["body"])
    time.sleep(2)

    print(f"\n✅ Draft saved! {len(images)}images | title='{title}'")
    print("📌 Open creator → 草稿箱 → 检查 → 发布")


if __name__ == "__main__":
    main()
