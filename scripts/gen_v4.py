#!/usr/bin/env python3
"""
Xiaohongshu card generator v4
Reads post config from JSON, generates 4 cards with correct scrollbar/DPI settings.
Usage: python gen_v4.py --post-name <name>
"""

import os, json, time, random, subprocess, sys

BASE = "D:/Hermes agnet"
CHROME = "C:/Program Files/Google/Chrome/Application/chrome.exe"
URL = "https://creator.xiaohongshu.com/publish/publish?source=official"

# Card color schemes
SCHEMES = {
    "dark":   {"bg": "#1a1a2e", "tc": "#ffffff", "lc": "#ffffff", "ac": "#ff6b35"},
    "orange": {"bg": "#bf360c", "tc": "#ffffff", "lc": "#ffffff", "ac": "#ffcc02"},
    "teal":   {"bg": "#004d40", "tc": "#ffffff", "lc": "#ffffff", "ac": "#80cbc4"},
    "white":  {"bg": "#ffffff", "tc": "#1a1a2e", "lc": "#333333", "ac": "#ff6b35"},
    "navy":   {"bg": "#0d1b2a", "tc": "#ffffff", "lc": "#ffffff", "ac": "#ff6b35"},
}

def make_card(title, sub, scheme_name, out):
    s = SCHEMES.get(scheme_name, SCHEMES["dark"])
    # Split subtitle by \n
    sub_lines = sub.split("\\n")
    sub_html = ""
    for line in sub_lines:
        sub_html += f'<div style="font-size:36px;font-weight:700;color:{s["lc"]};line-height:1.5;margin-bottom:2px;">{line}</div>'

    html = f'''<!DOCTYPE html><html><meta charset="utf-8">
<body style="margin:0;display:flex;justify-content:center;align-items:center;background:#ccc;overflow:hidden;">
<style>::-webkit-scrollbar{{display:none;}}</style>
<div style="width:540px;height:720px;background:{s["bg"]};padding:44px 36px;display:flex;flex-direction:column;justify-content:center;font-family:'Microsoft YaHei','微软雅黑',sans-serif;overflow:hidden;">
<div style="font-size:48px;font-weight:900;color:{s["tc"]};line-height:1.2;margin-bottom:16px;">{title}</div>
{sub_html}
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

    # Check Chrome
    import urllib.request
    try:
        r = urllib.request.urlopen(f"http://localhost:{cfg['port']}/json/version", timeout=3)
        print(f"Chrome OK port {cfg['port']}")
    except:
        print(f"Chrome on port {cfg['port']} not responding! Start it first.")
        sys.exit(1)

    out_dir = os.path.join(BASE, "assets", post_name)
    os.makedirs(out_dir, exist_ok=True)

    # 4 cards from config
    cards = [
        {"f": "01_cover.png",    "title": cfg.get("card_cover_title",""), "sub": cfg.get("card_cover_sub",""),  "style": cfg.get("card_cover_style","dark")},
        {"f": "02_why.png",      "title": cfg.get("card2_title",""),      "sub": cfg.get("card2_sub",""),       "style": cfg.get("card2_style","dark")},
        {"f": "03_problems.png", "title": cfg.get("card3_title",""),      "sub": cfg.get("card3_sub",""),       "style": cfg.get("card3_style","dark")},
        {"f": "04_tips.png",     "title": cfg.get("card4_title",""),      "sub": cfg.get("card4_sub",""),       "style": cfg.get("card4_style","dark")},
    ]

    images = []
    for c in cards:
        p = os.path.join(out_dir, c["f"])
        print(f"{c['f']}...", end=" ")
        ok = make_card(c["title"], c["sub"], c["style"], p)
        if ok:
            sz = os.path.getsize(p)//1024
            print(f"✅ {sz}KB")
            images.append(p)
        else:
            print("❌")
            return

    print(f"\n✅ {len(images)} cards")

    # Upload
    print("Uploading to draft...")
    from DrissionPage import ChromiumPage
    p = ChromiumPage(addr_or_opts=cfg['port'])
    p.get(URL)
    time.sleep(random.uniform(3,5))

    p.run_js('''
    var a=document.querySelectorAll("span,div");
    for(var i=0;i<a.length;i++){
        var t=a[i].textContent.trim();
        if(t==="\\u4e0a\\u4f20\\u56fe\\u6587"&&a[i].offsetHeight>0){
            var e=a[i];
            for(var j=0;j<5;j++){if(e.tagName==="DIV"){e.click();return;}if(e.parentElement)e=e.parentElement;}
        }
    }
    ''')
    time.sleep(random.uniform(3,5))

    for img in images:
        inp = p.ele('tag:input@type=file')
        if inp:
            inp.input(img)
            time.sleep(random.uniform(3,6))

    time.sleep(random.uniform(3,5))

    title = cfg["title"][:20]
    p.run_js('''
    var ins=document.querySelectorAll("input");
    for(var i=0;i<ins.length;i++){
        var ph=ins[i].placeholder||"";
        if(ph.includes("\\u6807\\u9898")){
            var s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,"value").set;
            s.call(ins[i],arguments[0]);
            ins[i].dispatchEvent(new Event("input",{bubbles:true}));
        }
    }
    ''', title)
    time.sleep(random.uniform(2,4))

    p.run_js('''
    var eds=document.querySelectorAll("[contenteditable=true]");
    for(var i=0;i<eds.length;i++){
        if(eds[i].offsetHeight>50){
            eds[i].focus();
            eds[i].innerText=arguments[0];
            eds[i].dispatchEvent(new Event("input",{bubbles:true}));
        }
    }
    ''', cfg["body"])
    time.sleep(2)

    print(f"\n✅ Draft saved! {len(images)}images | title='{title}' | {len(cfg['body'])}chars body")
    print("📌 Open creator → 草稿箱 → 检查 → 发布")


if __name__ == "__main__":
    main()
