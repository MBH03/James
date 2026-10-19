#!/usr/bin/env python3
"""Generate the per-lake pages, sitemap.xml, robots.txt and llms.txt.

Run from the repo root:  python3 tools/build_lakes.py
Change BASE when the site moves to a custom domain, then re-run.
"""
import json, html, datetime, pathlib

BASE = "https://mbh03.github.io/James/"
PHONE_DISPLAY, PHONE_TEL, EMAIL = "(435) 592-0680", "+14355920680", "henrieoutfitters@gmail.com"
INSTAGRAM = "https://www.instagram.com/henrieoutfitters/"
TODAY = datetime.date.today().isoformat()
ROOT = pathlib.Path(__file__).resolve().parent.parent

LAKES = [
 dict(slug="sand-hollow-reservoir", name="Sand Hollow Reservoir", where="near St. George and Hurricane, Utah", town="St. George",
      angle="Desert bass hunting", tagline="Red Rock Bass Factory",
      hook="Chase largemouth bass in crystal blue water surrounded by Southern Utah red rock.",
      experience=["This is desert bass fishing with a completely different backdrop. You are casting for largemouth along red sandstone cliffs, sandy shorelines, flooded structure and clear blue water. It is the kind of place where you can spend the morning working shallow cover and then chase bass around deeper structure as the sun climbs."],
      why="Year round bass fishing, dramatic scenery, and the chance to catch numbers of largemouth while still having a legitimate shot at a big fish.",
      species=["Largemouth bass", "Bluegill"], access="Good boat and shore access."),
 dict(slug="lake-powell", name="Lake Powell", where="on the Utah and Arizona border", town="Utah and Arizona",
      angle="Canyon striper adventure", tagline="Striper Canyon",
      hook="Run the canyons, find the bait and watch the stripers explode on the surface.",
      experience=["Lake Powell feels less like fishing a lake and more like fishing an enormous canyon system. You run through narrow sandstone canyons, stop where bait is holding and cast for striped bass. When the stripers are schooling, the action can become frantic, with fish chasing bait right to the surface."],
      why="Massive water, endless canyon structure and the possibility of catching striped bass by the dozens when you find an active school.",
      species=["Striped bass", "Smallmouth bass", "Largemouth bass", "Walleye", "Crappie", "Catfish", "Bluegill"], access="Best fished by boat."),
 dict(slug="panguitch-lake", name="Panguitch Lake", where="near Panguitch and Cedar City, Utah", town="Panguitch",
      angle="Trophy trout hunting", tagline="Big Fish Reboot",
      hook="Fish the lake named \u2018Big Fish\u2019 for Southern Utah\u2019s trophy trout.",
      experience=["Panguitch is built around one thing: trout. You can troll open water for cruising fish, work shorelines and structure, or target tiger trout and cutthroat with more aggressive presentations. The lake\u2019s high elevation and open basin make changing weather and conditions part of the experience."],
      why="This is where you go when the goal is not simply catching trout but looking for a genuinely large Southern Utah trout.",
      species=["Rainbow trout", "Cutthroat trout", "Tiger trout"], access="Good boat access.",
      details=["Full 8 hour guided fishing trip", "All fishing gear and equipment provided", "Lunch provided",
               "Customized start and end times to fit your schedule", "Expert instruction and local knowledge",
               "Perfect for beginners, families and experienced anglers"]),
 dict(slug="gunlock-reservoir", name="Gunlock Reservoir", where="near St. George, Utah", town="St. George",
      angle="Intimate red rock bass fishing", tagline="Comeback Waterfall Bass",
      hook="Fish a red rock bass lake that came back from the brink.",
      experience=["Gunlock feels more intimate than Sand Hollow or Powell. You are fishing a smaller red rock reservoir where finding the right shoreline, point or piece of cover can make all the difference. It is a good lake for slowing down and actually learning where the bass are holding.",
                  "And when conditions are right, the fishing trip comes with something you cannot manufacture: Gunlock Falls spilling over the dam."],
      why="Smaller water, less overwhelming than Powell, beautiful red rock scenery and a bass fishery with an unusual comeback story.",
      species=["Largemouth bass", "Crappie", "Catfish"], access="Smaller warm water lake."),
 dict(slug="quail-creek-reservoir", name="Quail Creek Reservoir", where="near St. George and Hurricane, Utah", town="St. George",
      angle="Clear water trophy bass", tagline="Record Factory",
      hook="A desert reservoir where stocked trout help grow trophy bass.",
      experience=["Quail Creek is one of those lakes that can surprise you. It does not look like a trophy fishery from the shore, but beneath the clear water is an unusual combination of warm water bass habitat and stocked trout. Largemouth can key on trout, creating opportunities to target bigger bass around deeper water and structure."],
      why="Clear water, big largemouth, aggressive smallmouth-style sight fishing opportunities and the unusual possibility of catching trout and bass in the same day.",
      species=["Largemouth bass", "Crappie", "Bluegill", "Rainbow trout"], access="Good facilities and boat ramps."),
 dict(slug="fish-lake", name="Fish Lake", where="near Loa and Torrey, Utah", town="Loa and Torrey",
      angle="Deep water Mackinaw hunting", tagline="Alpine Mackinaw Lake",
      hook="Go deep for a trophy Mackinaw in the heart of Utah\u2019s high country.",
      experience=["Fish Lake is not a numbers game in the same way as some of the Southern Utah bass lakes. This is about hunting. You are working deep water for lake trout, watching electronics, finding the right depth and putting a bait or lure in front of a fish that can weigh tens of pounds.",
                  "In summer, the high-elevation setting makes the boat trip itself part of the experience. In winter, the entire lake transforms into an ice fishing destination."],
      why="Trophy lake trout, high alpine scenery and the feeling that every deep-water mark on the electronics could be the fish you came for.",
      species=["Lake trout", "Splake", "Rainbow trout", "Cutthroat trout", "Other trout"], access="Worth the longer drive."),
]
for _l in LAKES:
    _l["blurb"] = _l["hook"]

E = html.escape
LAKE_IMG = {  # slug: (width, height, alt text) of assets/lakes/<slug>.jpg
 "sand-hollow-reservoir": (1500, 997, "Sand Hollow Reservoir near St. George with deep blue water, red sandstone shoreline and distant red rock cliffs"),
 "lake-powell": (876, 912, "Aerial view of Lake Powell with red sandstone buttes rising from deep blue canyon water"),
 "panguitch-lake": (1600, 1067, "Panguitch Lake in autumn with aspen covered hills reflected in still water"),
 "gunlock-reservoir": (1201, 797, "Aerial view of Gunlock Reservoir with blue water, a winding road and red rock hills"),
 "quail-creek-reservoir": (1108, 1108, "Aerial view of Quail Creek Reservoir with turquoise water and a boat leaving a long wake"),
 "fish-lake": (1320, 606, "Fish Lake from above with blue water ringed by pine forest and golden hills"),
}

def lake_img(slug, prefix=""):
    w, h, alt = LAKE_IMG[slug]
    return f'<img src="{prefix}assets/lakes/{slug}.jpg" alt="{E(alt)}" width="{w}" height="{h}" loading="lazy" decoding="async">'

def jl(obj):  # JSON-LD script tag
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"

BUSINESS = {"@type": "LocalBusiness", "@id": BASE + "#business", "name": "Henrie Outfitters LLC",
            "url": BASE, "telephone": "+1-435-592-0680", "email": EMAIL}

def faq(l):
    sp = ", ".join(s.lower() for s in l["species"][:-1]) + " and " + l["species"][-1].lower() if len(l["species"]) > 1 else l["species"][0].lower()
    qa = [
     (f"Does Henrie Outfitters guide fishing trips at {l['name']}?",
      f"Yes. Henrie Outfitters LLC, owned and guided by James Henrie, runs guided fishing trips at {l['name']} and at other lakes across Southern Utah."),
     (f"What fish can I catch at {l['name']}?", f"{l['name']} has {sp}."),
     ("How do I book a guided fishing trip?",
      f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form on the Henrie Outfitters website. Customized trip packages are available."),
    ]
    if l["slug"] == "panguitch-lake":
        qa.insert(2, ("What is included on a guided fishing trip at Panguitch Lake?",
            "A full 8 hour guided fishing trip, all fishing gear and equipment, lunch, customized start and end times to fit your schedule, and expert instruction and local knowledge."))
    return qa

def sp_short(l):
    s = [x.lower() for x in l["species"][:3]]
    return ", ".join(s[:-1]) + " and " + s[-1] if len(s) > 1 else s[0]

def lake_page(l):
    # Optional per-lake facts. Add keys to a lake in LAKES to show them:
    #   details = ["Best months: ...", "Boat ramp: ...", "Typical catch: ..."]
    exp_html = "".join(f"<p>{E(p)}</p>" for p in l["experience"])
    details_html = ""
    if l.get("details"):
        details_html = "<h3>Good to know</h3><ul class=\"know\">" + "".join(f"<li>{E(d)}</li>" for d in l["details"]) + "</ul>"
    url = f"{BASE}lakes/{l['slug']}.html"
    if l["name"] == "Lake Powell":
        title = "Lake Powell Fishing Guide, Utah and Arizona | Henrie Outfitters"
    else:
        title = f"{l['name']} Fishing Guide near {l['town']}, UT | Henrie Outfitters"
    if len(title) > 70:
        title = f"{l['name']} Fishing Guide near {l['town']}, UT"
    desc = f"{l['hook']} Guided fishing trips at {l['name']}, {l['where']}, with Henrie Outfitters. Call {PHONE_DISPLAY}."
    qa = faq(l)
    cur = ' aria-current="page"'
    dd_items = "".join(f'<a href="{o["slug"]}.html"{cur if o["slug"] == l["slug"] else ""}>{E(o["name"])}</a>' for o in LAKES)
    others = "".join(f'<li><a href="{o["slug"]}.html">{E(o["name"])}</a></li>' for o in LAKES if o["slug"] != l["slug"])
    park_links = "".join(f'<p>Visiting {E(x["name"])}? See <a href="../{x["slug"]}.html">{E(x["h1"].lower().replace("fishing near", "fishing near"))}</a>.</p>' for x in PARK_FOR_LAKE.get(l["slug"], []))
    fish = "".join(f"<li>{E(s)}</li>" for s in l["species"])
    faq_html = "".join(f"<details open><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in qa)
    graph = [
      {"@context": "https://schema.org", "@type": "Service", "name": f"Guided fishing trips at {l['name']}",
       "serviceType": "Guided fishing trip", "description": f"{l['tagline']}. {l['hook']} {l['experience'][0]}", "url": url,
       "areaServed": {"@type": "Place", "name": f"{l['name']}, Utah"},
       "provider": {**BUSINESS, "founder": {"@type": "Person", "name": "James Henrie"}}},
      {"@context": "https://schema.org", "@type": "FAQPage",
       "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Henrie Outfitters", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": HUB["label"], "item": f"{BASE}{HUB['slug']}.html"},
        {"@type": "ListItem", "position": 3, "name": l["name"], "item": url}]},
    ]
    book = f"{BASE}?lake={l['name'].replace(' ', '%20')}#contact"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Henrie Outfitters">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/lakes/{l["slug"]}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/logo-96.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/lake.css">
{"".join(jl(g) for g in graph)}
</head>
<body>
<header class="nav"><a class="brand" href="../"><img src="../assets/logo-96.webp" alt="Henrie Outfitters LLC logo" width="44" height="44">Henrie Outfitters</a>
<nav><div class="dd"><a class="ddlink" href="../{HUB["slug"]}.html">Lakes</a><button class="ddbtn" type="button" aria-label="Show all lakes" aria-expanded="false">&#9662;</button><div class="ddmenu"><a href="../{HUB["slug"]}.html">All lakes</a>{dd_items}</div></div><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="book" href="{book}">Book now &rarr;</a></nav></header>
<main>
<section class="hero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="../{HUB["slug"]}.html">{E(HUB["label"])}</a> / <span>{E(l["name"])}</span></nav>
<p class="kicker">{E(l["angle"])} &middot; {E(l["where"])}</p>
<h1>Guided fishing trips at {E(l["name"])}</h1>
<p class="sub">{E(l["hook"])}</p>
<a class="btn" href="{book}"><span>Book a trip at {E(l["name"])}</span><i>&rarr;</i></a>
</div></section>
<section><div class="wrap two">
<div><div class="lphoto">{lake_img(l["slug"], "../")}</div><p class="eyebrow">The experience</p><h2>{E(l["tagline"])}</h2>
{exp_html}
<h3>Why fish {E(l["name"])}</h3><p>{E(l["why"])}</p>
{details_html}
<p class="guide">Guided by James Henrie, owner of Henrie Outfitters LLC. Call <a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> or email <a href="mailto:{EMAIL}">{EMAIL}</a> to plan a trip.</p></div>
<div><h2>Fish you can catch at {E(l["name"])}</h2><ul class="fish">{fish}</ul>
<p class="note">{E(l["access"])}</p></div>
</div></section>
<section class="alt"><div class="wrap"><h2>Questions about {E(l["name"])}</h2>{faq_html}</div></section>
<section><div class="wrap"><h2>Other Southern Utah lakes we fish</h2><ul class="others">{others}</ul>
<p>See <a href="../{HUB["slug"]}.html">all guided fishing trips in Southern Utah</a>.</p>
{park_links}
<p><a class="btn" href="{book}"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>
</main>
<footer><div class="wrap"><p><strong>Henrie Outfitters LLC</strong> &middot; Guided fishing and hunting in Southern Utah with James Henrie</p>
<p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{INSTAGRAM}">Instagram</a></p></div></footer>
<script>document.querySelector(".ddbtn").addEventListener("click",function(){{var d=this.parentNode,o=d.classList.toggle("open");this.setAttribute("aria-expanded",o)}});document.addEventListener("click",function(e){{var d=document.querySelector(".dd");if(d&&!d.contains(e.target)){{d.classList.remove("open")}}}});</script>
</body>
</html>
'''

PHOTOS = [
 dict(file="tiger-trout-net", caption="Tiger trout in the net",
      alt="Smiling angler in a bucket hat holding a landing net with a striped tiger trout, calm lake and forested hills behind"),
 dict(file="tiger-trout-hand", caption="Tiger trout up close",
      alt="Hand holding a tiger trout with green and gold tiger stripes above the water"),
 dict(file="tiger-trout-lure", caption="Tiger trout on the lure",
      alt="Tiger trout hanging from a fishing line with a lure in its mouth inside an aluminum fishing boat"),
 dict(file="rainbow-trout", caption="Rainbow trout",
      alt="Angler in a camouflage jacket holding a rainbow trout on a boat with fishing rods and mountains in the background"),
 dict(file="rainbow-trout-closeup", caption="Rainbow trout up close",
      alt="Close view of a rainbow trout with black spots and a pink stripe held over the water beside an aluminum fishing boat"),
 dict(file="tiger-trout-guest", caption="Tiger trout catch",
      alt="Bearded angler in a camouflage jacket holding a tiger trout on a boat under a cloudy sky with forested hills behind"),
 dict(file="tiger-trout-boat", caption="Tiger trout on deck",
      alt="Hand holding a striped tiger trout in an aluminum fishing boat with a forested shoreline and blue sky behind"),
 dict(file="tiger-trout-hooked", caption="Tiger trout, just landed",
      alt="Tiger trout hanging from a crankbait lure over a boat with calm water and forested hills in the background"),
]

def photos_page():
    url = BASE + "photos.html"
    title = "Photos: Guided Fishing Trips in Southern Utah | Henrie Outfitters"
    desc = "Photos from guided fishing trips with Henrie Outfitters in Southern Utah: tiger trout, rainbow trout and days on the water."
    items = "".join(
        f'<figure><a href="assets/photos/{p["file"]}.jpg"><img src="assets/photos/{p["file"]}-sm.jpg" alt="{E(p["alt"])}" width="640" height="850" loading="lazy"></a></figure>'
        for p in PHOTOS)
    dd_items = "".join(f'<a href="lakes/{o["slug"]}.html">{E(o["name"])}</a>' for o in LAKES)
    graph = [
      {"@context": "https://schema.org", "@type": "ImageGallery", "name": "Guided fishing trip photos", "url": url,
       "about": "Guided fishing trips in Southern Utah with Henrie Outfitters",
       "image": [{"@type": "ImageObject", "contentUrl": f"{BASE}assets/photos/{p['file']}.jpg", "caption": p["caption"], "description": p["alt"]} for p in PHOTOS]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Henrie Outfitters", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": "Photos", "item": url}]},
    ]
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Henrie Outfitters">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/photos/{PHOTOS[0]["file"]}.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo-96.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/lake.css">
{"".join(jl(g) for g in graph)}
</head>
<body>
<header class="nav"><a class="brand" href="./"><img src="assets/logo-96.webp" alt="Henrie Outfitters LLC logo" width="44" height="44">Henrie Outfitters</a>
<nav><div class="dd"><a class="ddlink" href="./#lakes">Lakes</a><button class="ddbtn" type="button" aria-label="Show all lakes" aria-expanded="false">&#9662;</button><div class="ddmenu"><a href="./#lakes">All lakes</a>{dd_items}</div></div><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="book" href="./#contact">Book now &rarr;</a></nav></header>
<main>
<section class="hero"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a> / <span>Photos</span></nav>
<p class="kicker">On the water</p>
<h1>Photos from the boat</h1>
<p class="sub">Tiger trout, rainbow trout and days on the water in Southern Utah.</p>
<a class="btn" href="./#contact"><span>Book a guided trip</span><i>&rarr;</i></a>
</div></section>
<section><div class="wrap"><div class="photogrid">{items}</div></div></section>
</main>
<footer><div class="wrap"><p><strong>Henrie Outfitters LLC</strong> &middot; Guided fishing and hunting in Southern Utah with James Henrie</p>
<p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{INSTAGRAM}">Instagram</a></p></div></footer>
<script>document.querySelector(".ddbtn").addEventListener("click",function(){{var d=this.parentNode,o=d.classList.toggle("open");this.setAttribute("aria-expanded",o)}});document.addEventListener("click",function(e){{var d=document.querySelector(".dd");if(d&&!d.contains(e.target)){{d.classList.remove("open")}}}});</script>
</body>
</html>
'''


# ---------- Southern Utah hub + species landing pages ----------
HUB = dict(slug="guided-fishing-southern-utah", label="Guided fishing in Southern Utah")
SPECIES_PAGES = [
 dict(slug="bass-fishing-southern-utah", h1="Guided Bass Fishing in Southern Utah", label="Bass fishing",
      short="bass", match=lambda s: "bass" in s.lower(),
      intro="Southern Utah has some of the most varied bass fishing in the West: largemouth in red rock reservoirs, striped bass schooling in the canyons of Lake Powell, and smallmouth in the big water. Henrie Outfitters guides bass trips at four lakes."),
 dict(slug="trout-fishing-southern-utah", h1="Guided Trout Fishing in Southern Utah", label="Trout fishing",
      short="trout", match=lambda s: "trout" in s.lower() or "splake" in s.lower(),
      intro="From cold mountain lakes to trophy trout water, Southern Utah offers rainbow, cutthroat, tiger and lake trout. Henrie Outfitters guides trout trips at three lakes."),
]

def lakes_with(match):
    return [l for l in LAKES if any(match(s) for s in l["species"])]

def species_table():
    order = []
    for l in LAKES:
        for s in l["species"]:
            if s not in order: order.append(s)
    rows = ""
    for s in order:
        links = ", ".join(f'<a href="lakes/{l["slug"]}.html">{E(l["name"])}</a>' for l in LAKES if s in l["species"])
        rows += f"<tr><th scope=\"row\">{E(s)}</th><td>{links}</td></tr>"
    return f'<div class="tablewrap"><table class="spt"><thead><tr><th>Fish</th><th>Where to catch it with a guide</th></tr></thead><tbody>{rows}</tbody></table></div>'

def root_page(slug, title, desc, h1, kicker, sub, body, graph, crumb_label, cta="Book a guided trip", photo=True):
    url = f"{BASE}{slug}.html"
    dd_items = "".join(f'<a href="lakes/{o["slug"]}.html">{E(o["name"])}</a>' for o in LAKES)
    g = graph + [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Henrie Outfitters", "item": BASE},
        {"@type": "ListItem", "position": 2, "name": crumb_label, "item": url}]}]
    crumbs = f'<a href="./">Home</a> / <span>{E(crumb_label)}</span>'
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Henrie Outfitters">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/hero.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/logo-96.webp" type="image/webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@500;600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/lake.css">
{"".join(jl(x) for x in g)}
</head>
<body>
<header class="nav"><a class="brand" href="./"><img src="assets/logo-96.webp" alt="Henrie Outfitters LLC logo" width="44" height="44">Henrie Outfitters</a>
<nav><div class="dd"><a class="ddlink" href="{HUB["slug"]}.html">Lakes</a><button class="ddbtn" type="button" aria-label="Show all lakes" aria-expanded="false">&#9662;</button><div class="ddmenu"><a href="{HUB["slug"]}.html">All lakes</a>{dd_items}</div></div><a href="tel:{PHONE_TEL}">Call {PHONE_DISPLAY}</a><a class="book" href="./#contact">Book now &rarr;</a></nav></header>
<main>
<section class="hero{" photo" if photo else ""}"><div class="wrap">
<nav class="crumbs" aria-label="Breadcrumb">{crumbs}</nav>
<p class="kicker">{E(kicker)}</p>
<h1>{E(h1)}</h1>
<p class="sub">{E(sub)}</p>
<a class="btn" href="./#contact"><span>{E(cta)}</span><i>&rarr;</i></a>
</div></section>
{body}
</main>
<footer><div class="wrap"><p><strong>Henrie Outfitters LLC</strong> &middot; Guided fishing and hunting in Southern Utah with James Henrie</p>
<p><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a> &middot; <a href="mailto:{EMAIL}">{EMAIL}</a> &middot; <a href="{INSTAGRAM}">Instagram</a></p></div></footer>
<script>document.querySelector(".ddbtn").addEventListener("click",function(){{var d=this.parentNode,o=d.classList.toggle("open");this.setAttribute("aria-expanded",o)}});document.addEventListener("click",function(e){{var d=document.querySelector(".dd");if(d&&!d.contains(e.target)){{d.classList.remove("open")}}}});</script>
</body>
</html>
'''

def lake_cards_html(lakes):
    out = ""
    for l in lakes:
        tags = "".join(f"<li>{E(s)}</li>" for s in l["species"])
        out += (f'<article class="lcard"><div class="lphoto">{lake_img(l["slug"])}</div><p class="eyebrow">{E(l["angle"])}</p>'
                f'<h3><a href="lakes/{l["slug"]}.html">Guided fishing at {E(l["name"])}</a></h3>'
                f'<p>{E(l["hook"])}</p><ul class="fish">{tags}</ul>'
                f'<p><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a></p></article>')
    return f'<div class="lgrid">{out}</div>'

HUB_FAQ = [
 ("Where does Henrie Outfitters guide fishing trips in Southern Utah?",
  "Henrie Outfitters guides fishing trips at six Southern Utah lakes: Panguitch Lake, Sand Hollow Reservoir, Lake Powell, Gunlock Reservoir, Quail Creek Reservoir and Fish Lake."),
 ("What is the best lake in Southern Utah for bass fishing?",
  "For numbers of largemouth bass in a red rock setting, start with Sand Hollow Reservoir. Gunlock Reservoir is a smaller, more intimate bass lake, Quail Creek Reservoir can produce big largemouth, and Lake Powell offers striped, smallmouth and largemouth bass."),
 ("Where can I catch trophy trout in Southern Utah?",
  "Panguitch Lake is built around trout, with rainbow, cutthroat and tiger trout. Fish Lake is the place to go deep for trophy lake trout (Mackinaw)."),
 ("Where can I catch striped bass in Southern Utah?",
  "Lake Powell. Guided trips run the canyons, find the bait and cast to striped bass, which can school and chase bait to the surface."),
 ("What is included on a guided fishing trip?",
  "A full 8 hour guided fishing trip, all fishing gear and equipment, lunch, customized start and end times to fit your schedule, and expert instruction and local knowledge. It suits beginners, families and experienced anglers."),
 ("How do I book a guided fishing trip in Southern Utah?",
  f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form on the Henrie Outfitters website. Customized trip packages are available."),
]

def faq_html_block(qa):
    return "".join(f"<details open><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in qa)

def faq_ld(qa):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}

def service_ld(name, desc, url, lakes):
    return {"@context": "https://schema.org", "@type": "Service", "name": name, "serviceType": "Guided fishing trip",
            "description": desc, "url": url,
            "areaServed": [{"@type": "AdministrativeArea", "name": "Southern Utah"}] + [{"@type": "Place", "name": f"{l['name']}, Utah"} for l in lakes],
            "provider": {**BUSINESS, "founder": {"@type": "Person", "name": "James Henrie"}}}

def hub_page():
    title = "Guided Fishing Trips in Southern Utah | 6 Lakes | Henrie Outfitters"
    desc = "Guided fishing in Southern Utah: bass, striped bass, trout and Mackinaw at Sand Hollow, Lake Powell, Panguitch Lake, Gunlock, Quail Creek and Fish Lake. Call (435) 592-0680."
    body = f'''<section><div class="wrap"><h2>Six lakes, one local guide</h2>
<p class="lead">Henrie Outfitters LLC runs guided fishing trips across Southern Utah with owner and guide James Henrie, who has 25 years of outdoor experience. Each lake is a different kind of fishing, so you can choose the experience that fits the fish you want.</p>
{lake_cards_html(LAKES)}</div></section>
<section class="alt"><div class="wrap"><h2>What you can catch, and where</h2>
{species_table()}
<p>Planning around where you are staying? See <a href="fishing-near-st-george-utah.html">fishing near St. George</a>, <a href="fishing-near-cedar-city-utah.html">fishing near Cedar City</a> and our <a href="fishing-trip-faqs.html">fishing trip FAQs</a>. Visiting a national park? See our <a href="fishing-utah-national-parks.html">national parks fishing guide</a>, or fishing near <a href="fishing-near-zion-national-park.html">Zion</a>, <a href="fishing-near-bryce-canyon.html">Bryce Canyon</a> and <a href="fishing-near-capitol-reef.html">Capitol Reef</a>.</p>
<p>Looking for one kind of fishing? See our guides to <a href="{SPECIES_PAGES[0]["slug"]}.html">bass fishing in Southern Utah</a> and <a href="{SPECIES_PAGES[1]["slug"]}.html">trout fishing in Southern Utah</a>.</p></div></section>
<section><div class="wrap"><h2>Which lake should I fish?</h2>
<ul class="know">
<li><strong>Numbers of largemouth bass:</strong> <a href="lakes/sand-hollow-reservoir.html">Sand Hollow Reservoir</a>, with year round bass fishing among red rock.</li>
<li><strong>A quieter bass lake:</strong> <a href="lakes/gunlock-reservoir.html">Gunlock Reservoir</a>, smaller water where you can slow down and learn where the bass hold.</li>
<li><strong>Big largemouth in clear water:</strong> <a href="lakes/quail-creek-reservoir.html">Quail Creek Reservoir</a>, where stocked trout help grow trophy bass.</li>
<li><strong>Striped bass and the most variety:</strong> <a href="lakes/lake-powell.html">Lake Powell</a>, an enormous canyon system.</li>
<li><strong>Trophy trout:</strong> <a href="lakes/panguitch-lake.html">Panguitch Lake</a>, built around trout including tiger trout and cutthroat.</li>
<li><strong>Trophy lake trout (Mackinaw):</strong> <a href="lakes/fish-lake.html">Fish Lake</a>, deep water fishing in Utah’s high country.</li>
</ul></div></section>
<section class="alt"><div class="wrap"><h2>How a guided trip works</h2>
<p>A guided fishing trip with Henrie Outfitters is a full 8 hour day on the water. All fishing gear and equipment and lunch are provided, start and end times are customized to fit your schedule, and you get expert instruction and local knowledge. Trips suit beginners, families and experienced anglers, and customized trip packages are available.</p>
<p><a class="btn" href="./#contact"><span>Book a guided fishing trip</span><i>&rarr;</i></a></p></div></section>
<section><div class="wrap"><h2>Southern Utah fishing questions</h2>{faq_html_block(HUB_FAQ)}</div></section>'''
    graph = [service_ld("Guided fishing trips in Southern Utah", desc, f"{BASE}{HUB['slug']}.html", LAKES), faq_ld(HUB_FAQ),
             {"@context": "https://schema.org", "@type": "ItemList", "name": "Southern Utah lakes with guided fishing trips",
              "itemListElement": [{"@type": "ListItem", "position": i, "name": l["name"], "url": f"{BASE}lakes/{l['slug']}.html"} for i, l in enumerate(LAKES, 1)]}]
    return root_page(HUB["slug"], title, desc, "Guided Fishing Trips in Southern Utah", "Six lakes · Bass, striped bass, trout and Mackinaw",
                     "Local expert James Henrie guides bass, striped bass, trout and Mackinaw trips at six Southern Utah lakes.", body, graph, HUB["label"])

def species_page(sp):
    lakes = lakes_with(sp["match"])
    names = ", ".join(l["name"] for l in lakes[:-1]) + " and " + lakes[-1]["name"]
    title = f"{sp['h1']} | Henrie Outfitters"
    desc = f"{sp['label']} with a local guide in Southern Utah: {names}. Call {PHONE_DISPLAY} to book."
    sections = ""
    for l in lakes:
        fish = [s for s in l["species"] if sp["match"](s)]
        sections += (f'<article class="spsec"><h2><a href="lakes/{l["slug"]}.html">{E(sp["short"].title())} fishing at {E(l["name"])}</a></h2>'
                     f'<p class="eyebrow">{E(l["tagline"])}</p><p>{E(l["experience"][0])}</p><p><strong>Why fish it:</strong> {E(l["why"])}</p>'
                     f'<ul class="fish">{"".join(f"<li>{E(s)}</li>" for s in fish)}</ul>'
                     f'<p><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a></p></article>')
    qa = [(f"Where can I go {sp['short']} fishing in Southern Utah with a guide?", f"Henrie Outfitters guides {sp['short']} fishing trips at {names}."),
          ("How do I book?", f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form on the Henrie Outfitters website.")]
    body = f'''<section><div class="wrap"><h2>{E(sp["label"])} at {len(lakes)} lakes</h2><p class="lead">{E(sp["intro"])}</p></div></section>
<section class="alt"><div class="wrap sps">{sections}</div></section>
<section><div class="wrap"><h2>Also see</h2><p><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a> &middot; <a href="{[x for x in SPECIES_PAGES if x is not sp][0]["slug"]}.html">{E([x for x in SPECIES_PAGES if x is not sp][0]["label"])} in Southern Utah</a></p>
<p><a class="btn" href="./#contact"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>'''
    graph = [service_ld(f"Guided {sp['short']} fishing in Southern Utah", desc, f"{BASE}{sp['slug']}.html", lakes), faq_ld(qa)]
    return root_page(sp["slug"], title, desc, sp["h1"], "Southern Utah", f"Guided {sp['short']} trips at {names}.", body, graph, sp["label"])


# ---------- National park trip pages (Zion, Bryce Canyon, Capitol Reef) ----------
TRIP_INCLUDES = ("A guided trip with Henrie Outfitters is a full 8 hour day on the water with owner and guide James Henrie. "
                 "All fishing gear and equipment and lunch are provided, start and end times are customized to fit your schedule, "
                 "and you get expert instruction and local knowledge. Beginners, families and experienced anglers are all welcome.")

PARKS = [
 dict(slug="fishing-near-zion-national-park", short="Zion", name="Zion National Park",
      title="Fishing Near Zion National Park | Guided Trips | Henrie Outfitters",
      desc="Guided fishing trips on lakes near Zion National Park: bass at Sand Hollow, Quail Creek and Gunlock. Call (435) 592-0680.",
      h1="Fishing Near Zion National Park", kicker="Zion region · Southern Utah",
      sub="Take a rest day from the trails with a guided day on a red rock reservoir.",
      outside=("Zion National Park is known for canyon hiking, not fishing. The guided fishing trips on this page are on lakes in the region around the park, "
               "not inside it. If you are planning a Zion trip, a guided fishing day gives you a slower day on the water between hikes. "
               "Check the National Park Service website for current rules about fishing inside the park."),
      lakes_intro="Many Zion visitors stay in or near St. George or Springdale. Three of our lakes are on the St. George side of Zion.",
      lakes=[("sand-hollow-reservoir", "The first lake to look at if you want numbers of largemouth bass and red rock scenery that matches the rest of your trip."),
             ("quail-creek-reservoir", "A very good option for bass, crappie, bluegill and rainbow trout, with good facilities and boat ramps."),
             ("gunlock-reservoir", "A smaller red rock lake that is quieter and easier to learn. When conditions are right, Gunlock Falls spills over the dam.")],
      rest=("After days of hiking and shuttle lines, a guided fishing day is a different pace: a boat, a lake, and someone else doing the planning. "
            "You can start with no experience and still catch fish, and the day is built around your group."),
      faq=[("Can you fish inside Zion National Park?", "This page covers guided trips on lakes near the park, not fishing inside it. Check the National Park Service website for current rules inside Zion."),
           ("Which lake is best for a Zion visitor?", "For bass and red rock scenery, start with Sand Hollow Reservoir. Gunlock Reservoir is smaller and quieter, and Quail Creek Reservoir offers bass, crappie, bluegill and rainbow trout."),
           ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included.")],
      also=["bass-fishing-southern-utah", "trout-fishing-southern-utah"]),
 dict(slug="fishing-near-bryce-canyon", short="Bryce Canyon", name="Bryce Canyon National Park",
      title="Fishing Near Bryce Canyon | Guided Trout Trips | Henrie Outfitters",
      desc="Guided trout fishing near Bryce Canyon National Park on Panguitch Lake, with rainbow, cutthroat and tiger trout. Call (435) 592-0680 to book a fishing day.",
      h1="Fishing Near Bryce Canyon", kicker="Bryce Canyon region · Southern Utah",
      sub="Trade the hoodoos for a day on a mountain trout lake with rainbow, cutthroat and tiger trout.",
      outside=("Bryce Canyon National Park is famous for its amphitheaters of hoodoos, not for fishing. Our guided fishing trips for Bryce visitors are on Panguitch Lake "
               "and other mountain lakes in the same part of Southern Utah, outside the park. Check the National Park Service website for current rules about fishing inside the park."),
      lakes_intro="Panguitch Lake is the lake we'd start with for a Bryce Canyon trip.",
      lakes=[("panguitch-lake", "Built around trout, with rainbow, cutthroat and tiger trout, good boat access, and a name that means ‘Big Fish’. This is where you go to look for a genuinely large Southern Utah trout.")],
      rest=("Bryce Canyon days are full of short hikes and viewpoints. A guided trout day on the water makes a slower, quieter contrast, and it works for families "
            "as well as for anglers who want to chase bigger fish."),
      faq=[("Can you fish in Bryce Canyon National Park?", "This page covers guided trips on lakes near the park, not fishing inside it. Check the National Park Service website for current rules."),
           ("What fish can I catch near Bryce Canyon?", "On Panguitch Lake, rainbow, cutthroat and tiger trout."),
           ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included.")],
      also=["trout-fishing-southern-utah"]),
 dict(slug="fishing-near-capitol-reef", short="Capitol Reef", name="Capitol Reef National Park",
      title="Fishing Near Capitol Reef National Park | Henrie Outfitters",
      desc="Guided fishing near Capitol Reef National Park: trophy lake trout at Fish Lake and variety on Lake Powell. Call (435) 592-0680 to book a fishing day.",
      h1="Fishing Near Capitol Reef", kicker="Capitol Reef region · Southern Utah",
      sub="Go deep for a trophy Mackinaw at Fish Lake, or add variety on Lake Powell.",
      outside=("Capitol Reef National Park is known for its red rock cliffs and the Waterpocket Fold, not for fishing. Our guided trips for Capitol Reef visitors are on lakes "
               "in the surrounding region, outside the park. Check the National Park Service website for current rules about fishing inside the park."),
      lakes_intro="Two of our lakes fit a Capitol Reef trip. They are very different days, so pick the one that matches what you want from the water.",
      lakes=[("fish-lake", "A serious trout destination, with lake trout (Mackinaw), splake, rainbow and cutthroat. This is deep-water hunting for a fish that can weigh tens of pounds, in Utah’s high country. In winter the lake becomes an ice fishing destination."),
             ("lake-powell", "The biggest variety in Southern Utah: striped bass, smallmouth and largemouth bass, walleye, crappie, catfish and bluegill. Best fished by boat. For Capitol Reef visitors it is a longer day, so ask us which fits your plans.")],
      rest=("Capitol Reef is one of the quieter national parks, and a guided fishing day fits that pace. Fish Lake is the trophy-hunting day, and Lake Powell is the "
            "canyon-variety day. Either one gives you a full day outdoors without the planning."),
      faq=[("Can you fish in Capitol Reef National Park?", "This page covers guided trips on lakes in the region, not fishing inside the park. Check the National Park Service website for current rules."),
           ("What can I catch at Fish Lake?", "Lake trout (Mackinaw), splake, rainbow trout, cutthroat trout and other trout."),
           ("Can I fish at Fish Lake in winter?", "In winter, Fish Lake becomes an ice fishing destination. Contact us to ask about winter trips.")],
      also=["trout-fishing-southern-utah"]),
]

def park_page(pk):
    lake = {l["slug"]: l for l in LAKES}
    cards = ""
    for slug, why in pk["lakes"]:
        l = lake[slug]
        tags = "".join(f"<li>{E(s)}</li>" for s in l["species"])
        cards += (f'<article class="lcard"><p class="eyebrow">{E(l["angle"])}</p>'
                  f'<h3><a href="lakes/{l["slug"]}.html">Guided fishing at {E(l["name"])}</a></h3>'
                  f'<p>{E(why)}</p><ul class="fish">{tags}</ul>'
                  f'<p><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a></p></article>')
    others = [x for x in PARKS if x is not pk]
    also = "".join(f'<li><a href="{x["slug"]}.html">Fishing near {E(x["short"])}</a></li>' for x in others)
    also += "".join(f'<li><a href="{s}.html">{E(next(sp["label"] for sp in SPECIES_PAGES if sp["slug"] == s))} in Southern Utah</a></li>' for s in pk["also"])
    also += f'<li><a href="{PARKS_HUB["slug"]}.html">Fishing on a Utah national parks trip</a></li>'
    also += f'<li><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a></li>'
    body = f"""<section><div class="wrap"><h2>Fishing outside the park</h2><p class="lead">{E(pk["outside"])}</p></div></section>
<section class="alt"><div class="wrap"><h2>Lakes that fit a {E(pk["short"])} trip</h2><p class="lead">{E(pk["lakes_intro"])}</p><div class="lgrid">{cards}</div></div></section>
<section><div class="wrap"><h2>A fishing day between park days</h2><p>{E(pk["rest"])}</p><p>{E(TRIP_INCLUDES)}</p>
<p><a class="btn" href="./#contact"><span>Book a guided fishing day</span><i>&rarr;</i></a></p></div></section>
<section class="alt"><div class="wrap"><h2>Questions about fishing near {E(pk["short"])}</h2>{faq_html_block(pk["faq"])}</div></section>
<section><div class="wrap"><h2>Keep planning</h2><ul class="others">{also}</ul></div></section>"""
    lakes_used = [lake[s] for s, _ in pk["lakes"]]
    graph = [service_ld(f"Guided fishing trips near {pk['name']}", pk["desc"], f"{BASE}{pk['slug']}.html", lakes_used), faq_ld(pk["faq"])]
    return root_page(pk["slug"], pk["title"], pk["desc"], pk["h1"], pk["kicker"], pk["sub"], body, graph, f"Fishing near {pk['short']}", photo=(pk["slug"] == "fishing-near-bryce-canyon"))

PARK_FOR_LAKE = {}
for _pk in PARKS:
    for _s, _ in _pk["lakes"]:
        PARK_FOR_LAKE.setdefault(_s, []).append(_pk)


# ---------- More landing pages: parks hub, St. George, Cedar City, FAQ ----------
PARKS_HUB = dict(slug="fishing-utah-national-parks", label="Fishing on a Utah national parks trip")
ST_GEORGE = dict(slug="fishing-near-st-george-utah", short="St. George")
CEDAR = dict(slug="fishing-near-cedar-city-utah", short="Cedar City")
FAQ_PAGE = dict(slug="fishing-trip-faqs", label="Fishing trip FAQs")

FAQ_ALL = [
 ("What is included on a guided fishing trip?", "A full 8 hour guided fishing trip, all fishing gear and equipment, lunch, customized start and end times to fit your schedule, and expert instruction and local knowledge."),
 ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included."),
 ("Can families and kids come along?", "Yes. Families are welcome, and the trip is built around your group."),
 ("Where do you guide fishing trips?", "At six Southern Utah lakes: Panguitch Lake, Sand Hollow Reservoir, Lake Powell, Gunlock Reservoir, Quail Creek Reservoir and Fish Lake."),
 ("What fish can I catch?", "Largemouth, smallmouth and striped bass, bluegill, crappie, catfish and walleye in the warm water lakes, and rainbow, cutthroat, tiger and lake trout (Mackinaw) and splake in the mountain lakes. Each lake page lists what is there."),
 ("Which lake should I choose?", "For numbers of largemouth bass, start with Sand Hollow. For striped bass and the widest variety, choose Lake Powell. For trophy trout, choose Panguitch Lake. For trophy lake trout (Mackinaw), choose Fish Lake."),
 ("I'm visiting a national park. Can I fit in a fishing day?", "Yes. Many visitors take one day out of a park trip to fish. See our pages for Zion, Bryce Canyon and Capitol Reef, and our guide to fishing on a Utah national parks trip. The fishing is on lakes outside the parks."),
 ("Do you guide hunting trips too?", "Yes. Henrie Outfitters offers guided fishing and guided hunting. Contact us to talk about hunting."),
 ("How do I book?", f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form on the Henrie Outfitters website. Customized trip packages are available."),
]

def parks_hub_page():
    title = "Fishing on a Utah National Parks Trip | Henrie Outfitters"
    desc = "Take a day out of your Utah national parks trip to fish. Guided trips near Zion, Bryce Canyon and Capitol Reef with Henrie Outfitters. Call (435) 592-0680."
    park_cards = ""
    for pk in PARKS:
        lakes = ", ".join(next(l["name"] for l in LAKES if l["slug"] == s) for s, _ in pk["lakes"])
        park_cards += (f'<article class="lcard"><p class="eyebrow">{E(pk["name"])}</p>'
                       f'<h3><a href="{pk["slug"]}.html">{E(pk["h1"])}</a></h3>'
                       f'<p>{E(pk["sub"])}</p><p class="note">Lakes: {E(lakes)}</p>'
                       f'<p><a class="more" href="{pk["slug"]}.html">See the trip &rarr;</a></p></article>')
    body = f"""<section><div class="wrap"><h2>A day on the water between park days</h2>
<p class="lead">Utah's five national parks are Zion, Bryce Canyon, Capitol Reef, Arches and Canyonlands. A road trip through them is a lot of hiking, driving and viewpoints. A guided fishing day gives you a slower, different kind of day: a lake, a boat, and a local guide doing the planning.</p>
<p>{E(TRIP_INCLUDES)}</p>
<p>The fishing is on lakes in the region, outside the parks. Check the National Park Service for the rules inside each park.</p></div></section>
<section class="alt"><div class="wrap"><h2>Which park pairs with which lake</h2>
<div class="lgrid">{park_cards}</div>
<h3>Arches and Canyonlands</h3>
<p>Arches and Canyonlands are in the Moab area, a long way from our lakes. Lake Powell is the closest of our six lakes. If your trip includes Moab, <a href="./#contact">contact us</a> and we'll tell you honestly whether a fishing day fits your plans.</p></div></section>
<section><div class="wrap"><h2>Planning your fishing day</h2>
<ul class="know">
<li>Pick the park you are visiting, then the lake that pairs with it. Each park page explains the options.</li>
<li>Choose a start time that fits your schedule. Start and end times are customized.</li>
<li>No fishing experience is needed, and families are welcome.</li>
<li>Book ahead. <a href="tel:{PHONE_TEL}">Call or text {PHONE_DISPLAY}</a>, or use the <a href="./#contact">booking form</a>.</li>
</ul>
<p><a class="btn" href="./#contact"><span>Book a fishing day</span><i>&rarr;</i></a></p></div></section>
<section class="alt"><div class="wrap"><h2>Questions about fishing on a parks trip</h2>{faq_html_block(PARKS_HUB_FAQ)}</div></section>
<section><div class="wrap"><h2>Keep planning</h2><ul class="others">
<li><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a></li>
<li><a href="{ST_GEORGE["slug"]}.html">Fishing near St. George</a></li>
<li><a href="{CEDAR["slug"]}.html">Fishing near Cedar City</a></li>
<li><a href="{FAQ_PAGE["slug"]}.html">Fishing trip FAQs</a></li></ul></div></section>"""
    graph = [service_ld("Guided fishing day for Utah national parks visitors", desc, f"{BASE}{PARKS_HUB['slug']}.html", LAKES), faq_ld(PARKS_HUB_FAQ)]
    return root_page(PARKS_HUB["slug"], title, desc, "Take a Day Out to Fish on Your Utah National Parks Trip", "Zion · Bryce Canyon · Capitol Reef",
                     "A guided fishing day between park days, on lakes near Zion, Bryce Canyon and Capitol Reef.", body, graph, PARKS_HUB["label"], photo=False)

PARKS_HUB_FAQ = [
 ("Is there fishing inside Utah's national parks?", "This page covers guided trips on lakes in the region, outside the parks. Check the National Park Service for current rules about fishing inside each park."),
 ("Which national parks can I pair with a fishing day?", "Zion, Bryce Canyon and Capitol Reef each have lakes in the region that fit a guided fishing day. Arches and Canyonlands are in the Moab area, a long way from our lakes."),
 ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included."),
 ("How do I book a fishing day?", f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form. Customized start and end times are available."),
]

def compare_table(slugs):
    lake = {l["slug"]: l for l in LAKES}
    rows = ""
    for s in slugs:
        l = lake[s]
        rows += (f'<tr><th scope="row"><a href="lakes/{l["slug"]}.html">{E(l["name"])}</a></th>'
                 f'<td>{E(l["angle"])}</td><td>{E(", ".join(l["species"]))}</td><td>{E(l["access"])}</td></tr>')
    return ('<div class="tablewrap"><table class="spt"><thead><tr><th>Lake</th><th>Best for</th><th>Fish</th><th>Setting</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>')

def st_george_page():
    lake = {l["slug"]: l for l in LAKES}
    slugs = ["sand-hollow-reservoir", "quail-creek-reservoir", "gunlock-reservoir"]
    title = "Fishing Near St. George, Utah | Guided Bass Trips | Henrie Outfitters"
    desc = "Guided fishing near St. George, Utah: compare Sand Hollow, Quail Creek and Gunlock for largemouth bass, crappie, bluegill and trout. Call (435) 592-0680."
    why = {"sand-hollow-reservoir": "Choose Sand Hollow if you want numbers of largemouth bass in red rock scenery, with a real chance at a big fish. It offers year round bass fishing.",
           "quail-creek-reservoir": "Choose Quail Creek for big largemouth in clear water, with stocked rainbow trout in the mix. It has good facilities and boat ramps.",
           "gunlock-reservoir": "Choose Gunlock if you want smaller, quieter water where you can slow down and learn where the bass hold. When conditions are right, Gunlock Falls spills over the dam."}
    sections = ""
    for s in slugs:
        l = lake[s]
        sections += (f'<article class="spsec"><h2><a href="lakes/{l["slug"]}.html">{E(l["name"])}</a></h2><p class="eyebrow">{E(l["tagline"])}</p>'
                     f'<p>{E(why[s])}</p><ul class="fish">{"".join(f"<li>{E(x)}</li>" for x in l["species"])}</ul>'
                     f'<p><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a></p></article>')
    qa = [("Which lake near St. George is best for bass?", "Sand Hollow Reservoir is the one to start with for numbers of largemouth bass. Quail Creek Reservoir can produce big largemouth in clear water, and Gunlock Reservoir is a smaller, quieter option."),
          ("Can I fish near St. George in winter?", "Sand Hollow offers year round bass fishing. Contact us to ask about winter trips at the other lakes."),
          ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included."),
          ("How do I book a guided trip near St. George?", f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form.")]
    body = f"""<section><div class="wrap"><h2>Three lakes, three different days</h2>
<p class="lead">St. George is the hub for Southern Utah's red rock bass fishing. Sand Hollow, Quail Creek and Gunlock are close to town, and each one is a different experience. This page helps you choose.</p>
{compare_table(slugs)}</div></section>
<section class="alt"><div class="wrap sps">{sections}</div></section>
<section><div class="wrap"><h2>Staying in St. George for Zion?</h2>
<p>Many visitors base themselves in St. George for Zion National Park. A guided fishing day on one of these lakes is an easy way to take a break from hiking. See <a href="{PARKS[0]["slug"]}.html">fishing near Zion National Park</a>.</p>
<p>{E(TRIP_INCLUDES)}</p>
<p><a class="btn" href="./#contact"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>
<section class="alt"><div class="wrap"><h2>Questions about fishing near St. George</h2>{faq_html_block(qa)}</div></section>
<section><div class="wrap"><h2>Keep planning</h2><ul class="others">
<li><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a></li>
<li><a href="{SPECIES_PAGES[0]["slug"]}.html">Bass fishing in Southern Utah</a></li>
<li><a href="{CEDAR["slug"]}.html">Fishing near Cedar City</a></li>
<li><a href="{PARKS_HUB["slug"]}.html">Fishing on a Utah national parks trip</a></li></ul></div></section>"""
    graph = [service_ld("Guided fishing trips near St. George, Utah", desc, f"{BASE}{ST_GEORGE['slug']}.html", [lake[s] for s in slugs]), faq_ld(qa)]
    return root_page(ST_GEORGE["slug"], title, desc, "Fishing Near St. George, Utah", "St. George region · Southern Utah",
                     "Compare Sand Hollow, Quail Creek and Gunlock, and pick the lake that fits your day.", body, graph, "Fishing near St. George", photo=False)

def cedar_page():
    lake = {l["slug"]: l for l in LAKES}
    slugs = ["panguitch-lake"]
    title = "Fishing Near Cedar City, Utah | Guided Trout Trips | Henrie Outfitters"
    desc = "Guided trout fishing near Cedar City, Utah at Panguitch Lake, with rainbow, cutthroat and tiger trout. Call (435) 592-0680."
    why = {"panguitch-lake": "Panguitch Lake is built around trout, with rainbow, cutthroat and tiger trout and good boat access. It is the lake to choose if you are looking for a large Southern Utah trout."}
    sections = ""
    for s in slugs:
        l = lake[s]
        sections += (f'<article class="spsec"><h2><a href="lakes/{l["slug"]}.html">{E(l["name"])}</a></h2><p class="eyebrow">{E(l["tagline"])}</p>'
                     f'<p>{E(why[s])}</p><ul class="fish">{"".join(f"<li>{E(x)}</li>" for x in l["species"])}</ul>'
                     f'<p><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a></p></article>')
    qa = [("What kind of fishing is near Cedar City?", "Mountain trout fishing. Panguitch Lake offers rainbow, cutthroat and tiger trout."),
          ("Is there bass fishing near Cedar City?", "Our bass lakes are on the St. George side of Southern Utah: Sand Hollow, Quail Creek and Gunlock. See our guide to fishing near St. George."),
          ("Do I need fishing experience?", "No. Trips suit beginners, families and experienced anglers, and expert instruction is included."),
          ("How do I book?", f"Call or text {PHONE_DISPLAY}, email {EMAIL}, or use the booking form.")]
    body = f"""<section><div class="wrap"><h2>Panguitch Lake for Cedar City visitors</h2>
<p class="lead">If you are staying in or passing through Cedar City, Panguitch Lake is where the trout fishing is. It is a high-country trout lake built around big fish.</p>
{compare_table(slugs)}</div></section>
<section class="alt"><div class="wrap sps">{sections}</div></section>
<section><div class="wrap"><h2>Want bass instead?</h2>
<p>Our warm water lakes are on the St. George side of Southern Utah. See <a href="{ST_GEORGE["slug"]}.html">fishing near St. George</a> for Sand Hollow, Quail Creek and Gunlock.</p>
<p>{E(TRIP_INCLUDES)}</p>
<p><a class="btn" href="./#contact"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>
<section class="alt"><div class="wrap"><h2>Questions about fishing near Cedar City</h2>{faq_html_block(qa)}</div></section>
<section><div class="wrap"><h2>Keep planning</h2><ul class="others">
<li><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a></li>
<li><a href="{SPECIES_PAGES[1]["slug"]}.html">Trout fishing in Southern Utah</a></li>
<li><a href="{PARKS[1]["slug"]}.html">Fishing near Bryce Canyon</a></li>
<li><a href="{PARKS_HUB["slug"]}.html">Fishing on a Utah national parks trip</a></li></ul></div></section>"""
    graph = [service_ld("Guided trout fishing near Cedar City, Utah", desc, f"{BASE}{CEDAR['slug']}.html", [lake[s] for s in slugs]), faq_ld(qa)]
    return root_page(CEDAR["slug"], title, desc, "Fishing Near Cedar City, Utah", "Cedar City region · Southern Utah",
                     "Panguitch Lake for rainbow, cutthroat and tiger trout.", body, graph, "Fishing near Cedar City", photo=False)

def faq_page():
    title = "Fishing Trip FAQs | Guided Fishing in Southern Utah | Henrie Outfitters"
    desc = "Answers about guided fishing trips in Southern Utah: what's included, who can come, which lake to pick, national park visitors and how to book. Call (435) 592-0680."
    body = f"""<section><div class="wrap"><h2>Common questions</h2>{faq_html_block(FAQ_ALL)}
<p><a class="btn" href="./#contact"><span>Book a guided trip</span><i>&rarr;</i></a></p></div></section>
<section class="alt"><div class="wrap"><h2>Keep planning</h2><ul class="others">
<li><a href="{HUB["slug"]}.html">All guided fishing trips in Southern Utah</a></li>
<li><a href="{PARKS_HUB["slug"]}.html">Fishing on a Utah national parks trip</a></li>
<li><a href="{ST_GEORGE["slug"]}.html">Fishing near St. George</a></li>
<li><a href="{CEDAR["slug"]}.html">Fishing near Cedar City</a></li></ul></div></section>"""
    graph = [faq_ld(FAQ_ALL)]
    return root_page(FAQ_PAGE["slug"], title, desc, "Fishing Trip FAQs", "Southern Utah",
                     "What's included, who can come, which lake to pick and how to book.", body, graph, FAQ_PAGE["label"], photo=False)

def dd_index():
    items = "".join(f'<a href="lakes/{l["slug"]}.html">{E(l["name"])}</a>' for l in LAKES)
    return ('<div class="dd"><a class="ddlink" href="#lakes">Lakes</a>'
            '<button class="ddbtn" type="button" aria-label="Show all lakes" aria-expanded="false">&#9662;</button>'
            f'<div class="ddmenu"><a href="#lakes">All lakes</a>{items}</div></div>')

def cards_html():
    out = []
    for n, l in enumerate(LAKES, 1):
        tags = "".join(f"<li>{E(s)}</li>" for s in l["species"])
        out.append(f'''    <article class="lakeitem reveal">
      <div class="lphoto">{lake_img(l["slug"])}<span class="num">{n:02d}</span></div>
      <div class="lbody"><span class="angle">{E(l["angle"])}</span><h3><a href="lakes/{l["slug"]}.html">{E(l["name"])}</a></h3><p class="hook">{E(l["hook"])}</p><ul class="fish">{tags}</ul><a class="more" href="lakes/{l["slug"]}.html">Lake details &rarr;</a><a class="btn" href="#contact" data-lake="{E(l["name"])}"><span>Book a trip here</span><i>&rarr;</i></a></div>
    </article>
''')
    return "".join(out)

def patch_index():
    p = ROOT / "index.html"
    s = p.read_text(encoding="utf-8")
    for a, z, body in (("<!-- LAKES:START -->", "<!-- LAKES:END -->", "\n" + cards_html() + "  "),
                       ("<!-- LAKENAV:START -->", "<!-- LAKENAV:END -->", dd_index())):
        if a in s:
            head, rest = s.split(a, 1); _, tail = rest.split(z, 1)
            s = head + a + body + z + tail
    p.write_text(s, encoding="utf-8")

def main():
    out = ROOT / "lakes"; out.mkdir(exist_ok=True)
    for l in LAKES:
        (out / f"{l['slug']}.html").write_text(lake_page(l), encoding="utf-8")
    (ROOT / f"{HUB['slug']}.html").write_text(hub_page(), encoding="utf-8")
    for sp in SPECIES_PAGES:
        (ROOT / f"{sp['slug']}.html").write_text(species_page(sp), encoding="utf-8")
    for pk in PARKS:
        (ROOT / f"{pk['slug']}.html").write_text(park_page(pk), encoding="utf-8")
    for d, fn in ((PARKS_HUB, parks_hub_page), (ST_GEORGE, st_george_page), (CEDAR, cedar_page), (FAQ_PAGE, faq_page)):
        (ROOT / f"{d['slug']}.html").write_text(fn(), encoding="utf-8")
    urls = [BASE, f"{BASE}{HUB['slug']}.html"] + [f"{BASE}{sp['slug']}.html" for sp in SPECIES_PAGES] + [f"{BASE}{pk['slug']}.html" for pk in PARKS] + [f"{BASE}{d['slug']}.html" for d in (PARKS_HUB, ST_GEORGE, CEDAR, FAQ_PAGE)] + [BASE + "photos.html"] + [f"{BASE}lakes/{l['slug']}.html" for l in LAKES]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>\n" for u in urls) + "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sm)
    bots = ["*", "GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-User", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
    (ROOT / "robots.txt").write_text("".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}sitemap.xml\n")
    lines = ["# Henrie Outfitters", "",
      "> Henrie Outfitters LLC offers guided fishing and hunting trips in Southern Utah, led by owner and local expert James Henrie (25 years of outdoor experience). Guided fishing trips are offered at six Southern Utah lakes: Panguitch Lake, Sand Hollow Reservoir, Lake Powell, Gunlock Reservoir, Quail Creek Reservoir and Fish Lake.", "",
      f"Book: call or text {PHONE_DISPLAY}, email {EMAIL}, or use the form at {BASE}#contact. Customized trip packages are available.", "",
      "## Guided fishing trips by lake", ""]
    for l in LAKES:
        lines.append(f"- [{l['name']}]({BASE}lakes/{l['slug']}.html): {l['tagline']}, {l['angle'].lower()}. {l['hook']}")
    lines += ["", "## Guides by fish", "", f"- [Guided fishing in Southern Utah]({BASE}{HUB['slug']}.html): all six lakes, what you can catch where, FAQ"] + [f"- [{sp['label']} in Southern Utah]({BASE}{sp['slug']}.html): {sp['intro']}" for sp in SPECIES_PAGES]
    lines += ["", "## Planning pages", "", f"- [Fishing on a Utah national parks trip]({BASE}{PARKS_HUB['slug']}.html): a guided fishing day between park days (Zion, Bryce Canyon, Capitol Reef)", f"- [Fishing near St. George]({BASE}{ST_GEORGE['slug']}.html): compare Sand Hollow, Quail Creek and Gunlock", f"- [Fishing near Cedar City]({BASE}{CEDAR['slug']}.html): mountain trout at Panguitch Lake", f"- [Fishing trip FAQs]({BASE}{FAQ_PAGE['slug']}.html): what is included, who can come, how to book"]
    lines += ["", "## National park trips", ""] + [f"- [Fishing near {pk['short']}]({BASE}{pk['slug']}.html): {pk['sub']}" for pk in PARKS]
    lines += ["", "## Main site", "", f"- [Henrie Outfitters home]({BASE}): trips, lakes, guide, booking", f"- [Photos]({BASE}photos.html): photos from guided fishing trips", f"- [Instagram]({INSTAGRAM})", ""]
    (ROOT / "llms.txt").write_text("\n".join(lines))
    (ROOT / "photos.html").write_text(photos_page(), encoding="utf-8")
    patch_index()
    print("built", len(LAKES), "lake pages")

if __name__ == "__main__":
    main()
