#!/usr/bin/env python3
"""Builds the King Will's Wills GHL pages.

Each file in src/pages/ becomes one self-contained KWW-<Name>-GHL.html in this
folder, ready to paste into a GHL "Custom Code" element. Shared header, footer,
styles and scripts live in src/ and in this file, so edit them once here and
re-run:  python3 build.py
"""
import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

# ── Site settings ───────────────────────────────────────────────────────────
# Swap these for GHL media-library URLs once images are uploaded there.
# The photo URLs point at the current site, so they stop working once it's switched off.
def data_uri(name):
    return "data:image/webp;base64," + base64.b64encode((ROOT / "assets" / name).read_bytes()).decode()


# Official artwork, embedded so it works before anything is uploaded to GHL Media
LOGO_URL = data_uri("web-logo.webp")
IPW_BADGE = data_uri("web-ipw.webp")
TSI_BADGE = data_uri("web-tsi.webp")
STEP_BADGE = data_uri("web-step.webp")
SEVVY_PHOTO = "https://www.kw-wills.co.uk/images/split/14_right.png"
SEVVY_PHOTO_2 = "https://www.kw-wills.co.uk/images/split/18_left.png"

PHONE_1, PHONE_1_TEL = "01384 883 883", "+441384883883"   # Stourbridge
PHONE_2, PHONE_2_TEL = "01905 671 371", "+441905671371"   # Worcester
EMAIL = "enquiries@kw-wills.co.uk"
OFFICE_EMAIL = "office@kw-wills.co.uk"
ADDRESS = "136A King William Street, Stourbridge, DY8 4ES"

# Page slugs in GHL. Keep these matching the old site so Google rankings carry over.
LINKS = {
    "home": "/",
    "about": "/about",
    "wills": "/will-writing",
    "trusts": "/trusts",
    "lpa": "/lasting-powers-of-attorney",
    "storage": "/storage-and-after-care",
    "estate": "/estate-administration-and-probate",
    "appointment": "/your-appointment",
    "intestacy": "/intestacy",
    "testimonials": "/testimonials",
    "blog": "/blog",
    "contact": "/contact",
    "privacy": "/privacy",
}

ICONS = {
    "phone": '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "home": '<path d="m3 10 9-7 9 7v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><path d="M9 22V12h6v10"/>',
    "will": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h5"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "shieldcheck": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "hand": '<path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/><path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.8-2.8l-4.2 3.9"/><path d="m2 15 6 6"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.9M16 3.1a4 4 0 0 1 0 7.8"/>',
    "lock": '<rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "scale": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a4 4 0 0 0 6 0zM19 7l-3 7a4 4 0 0 0 6 0z"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "moon": '<path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "pound": '<path d="M18 7c0-5.3-8-5.3-8 0v10M6 13h8M6 21h12"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "award": '<circle cx="12" cy="8" r="6"/><path d="M15.5 13.5 17 22l-5-3-5 3 1.5-8.5"/>',
    "heart": '<path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1-1a5.5 5.5 0 0 0-7.8 7.8l1 1L12 21l7.8-7.8 1-1a5.5 5.5 0 0 0 0-7.6z"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "box": '<path d="M21 8v13H3V8M1 3h22v5H1zM10 12h4"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "zap": '<path d="M13 2 3 14h9l-1 8 10-12h-9z"/>',
    "folder": '<path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>',
    "map": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "tree": '<circle cx="12" cy="5" r="3"/><circle cx="5" cy="19" r="3"/><circle cx="19" cy="19" r="3"/><path d="M12 8v4M12 12 5 16M12 12l7 4"/>',
    "video": '<path d="m23 7-7 5 7 5z"/><rect x="1" y="5" width="15" height="14" rx="2"/>',
    "star": '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "chevron": '<path d="m6 9 6 6 6-6"/>',
    "menu": '<path d="M3 6h18M3 12h18M3 18h18"/>',
    "printer": '<path d="M6 9V2h12v7M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
    "x": '<path d="M4 4l16 16M20 4 4 20"/>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6zM2 9h4v12H2z"/><circle cx="4" cy="4" r="2"/>',
}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')


def photo(src, alt, mono="SH"):
    """Photo with a branded monogram behind it, so a missing image never looks broken."""
    return (f'<span class="mono" aria-hidden="true">{mono}</span>'
            f'<img src="{src}" alt="{alt}" loading="lazy" onerror="this.remove()">')


# ── Reusable blocks, used in pages as {{> name}} ────────────────────────────
TESTIMONIALS = [
    ("Throughout the process we felt in good hands and there is no one else who could have dealt with our queries, circumstances and Wills in any better way than Sevvy did. Thank you for a fantastic service!", "Laura M", "Stourbridge"),
    ("Sevvy helped my parents with their Wills and dealing with a trust. He took the time to come out to my parents' house, explaining everything with great care and attention and ensured they fully understood all the implications.", "Jamie P", "Kidderminster"),
    ("Recently my father passed away, and I realised that we needed to quickly gain power of attorney over my mother's finances and healthcare. Sevvy really helped us deal with a potentially difficult situation. I would recommend him to anyone.", "Andy D", "Malvern"),
    ("I feel a sense of relief now, knowing that we have a Will in place and that Sevvy was able to take into account all of our wishes.", "Rachel D", "Droitwich"),
    ("We'd been planning on putting a Will together since our first son was born but it was one of those things we didn't get around to. Meeting Sevvy made us realise how important it was.", "Tracey M", "Worcester"),
    ("I would like to say how happy I am with the service you provided for me and my wife Tania in helping us sort out both our Wills. In just two very short meetings you made it very easy for us to understand all the pitfalls and implications of leaving things untouched with our current Will set-up. Thank you for explaining things in plain English.", "Leon Coppola", "Director, First Image Ltd"),
]


def quote_card(text, name, town, cls=""):
    return (f'<figure class="quote rv {cls}"><span class="stars" aria-label="5 stars">★★★★★</span>'
            f'<blockquote>“{text}”</blockquote><figcaption class="who"><span class="av">{name[0]}</span>'
            f'<span><b>{name}</b><span>{town}</span></span></figcaption></figure>')


def testimonials_block(n=3):
    cards = "".join(quote_card(*t) for t in TESTIMONIALS[:n])
    return f'''<section class="s s--pale" aria-labelledby="t-h">
  <div class="w">
    <div class="center"><span class="eyebrow">Kind words</span><h2 id="t-h">What our clients say about Sevvy</h2></div>
    <div class="grid g3 mt">{cards}</div>
    <div class="center mt"><a class="textlink" href="{LINKS["testimonials"]}">Read more client stories</a></div>
  </div>
</section>'''


BLOCKS = {
    "testimonials": testimonials_block(3),
    "testimonials_single": quote_card(*TESTIMONIALS[3]),
    "all_reviews": "".join(quote_card(*t) for t in TESTIMONIALS[1:]),
    "badges": f'''<section class="s s--sm s--tint" aria-label="Qualifications and memberships">
  <div class="w badges">
    <figure class="badge"><img src="{IPW_BADGE}" alt="Institute of Professional Willwriters member" width="180" height="65" loading="lazy"><figcaption>Fellow of the IPW</figcaption></figure>
    <figure class="badge"><img src="{TSI_BADGE}" alt="Trading Standards Institute Approved Code" width="150" height="69" loading="lazy"><figcaption>CTSI-approved code of practice</figcaption></figure>
    <figure class="badge"><img src="{STEP_BADGE}" alt="STEP Will Writing Code, England and Wales" width="72" height="71" loading="lazy"><figcaption>STEP Affiliate · Advanced Certificate</figcaption></figure>
    <figure class="badge"><span class="ico">{icon("lock")}</span><figcaption>Fully insured · £2m indemnity</figcaption></figure>
  </div>
</section>''',
    "cta": f'''<section class="s cta" aria-labelledby="cta-h">
  <div class="w">
    <div class="avatar">{photo(SEVVY_PHOTO, "Sevvy Hasan")}</div>
    <div>
      <h2 id="cta-h">Let's have a friendly chat</h2>
      <p>No obligation, no jargon, no pressure. Sevvy will listen, explain your options in plain English and give you a fixed price up front, at home, by Zoom, or in the evening or at weekends.</p>
      <p class="cta-phones">Stourbridge <a href="tel:{PHONE_1_TEL}">{PHONE_1}</a> &nbsp;·&nbsp; Worcester <a href="tel:{PHONE_2_TEL}">{PHONE_2}</a></p>
    </div>
    <div class="btn-row">
      <a class="btn btn--primary" href="{LINKS["contact"]}">{icon("calendar")} Book a free consultation</a>
      <a class="btn btn--ghost-light" href="tel:{PHONE_1_TEL}">{icon("phone")} Call {PHONE_1}</a>
    </div>
  </div>
</section>''',
}


# ── Header / footer ─────────────────────────────────────────────────────────
SERVICES = [
    ("wills", "Will Writing", "Make sure your wishes are carried out"),
    ("trusts", "Trusts", "Protect your home and your family's inheritance"),
    ("lpa", "Lasting Powers of Attorney", "Health & welfare, property & finance, business"),
    ("storage", "Storage & Aftercare", "Safe storage and free advice for life"),
    ("estate", "Estate Administration & Probate", "Support for executors when the time comes"),
]
GUIDES = [
    ("appointment", "Your Appointment", "What to expect and how to prepare"),
    ("intestacy", "No Will? Who Inherits", "Interactive intestacy checker"),
]


def header(active):
    def cls(key):
        return ' class="is-active" aria-current="page"' if key == active else ""

    svc = "".join(f'<li><a href="{LINKS[k]}"{cls(k)}>{t}<span>{d}</span></a></li>' for k, t, d in SERVICES)
    gd = "".join(f'<li><a href="{LINKS[k]}"{cls(k)}>{t}<span>{d}</span></a></li>' for k, t, d in GUIDES)
    svc_active = " is-active" if active in dict((k, 1) for k, *_ in SERVICES) else ""
    gd_active = " is-active" if active in dict((k, 1) for k, *_ in GUIDES) else ""
    d_svc = "".join(f'<a class="sub" href="{LINKS[k]}"{cls(k)}>{t}</a>' for k, t, _ in SERVICES)
    d_gd = "".join(f'<a class="sub" href="{LINKS[k]}"{cls(k)}>{t}</a>' for k, t, _ in GUIDES)
    return f'''<div class="topbar"><div class="w">
  <span class="tb-left">Friendly, qualified Will writing across England &amp; Wales · Home visits, Zoom, evenings &amp; weekends</span>
  <span class="tb-right"><a href="tel:{PHONE_1_TEL}"><span class="tb-lbl">Stourbridge </span>{PHONE_1}</a><a href="tel:{PHONE_2_TEL}"><span class="tb-lbl">Worcester </span>{PHONE_2}</a></span>
</div></div>
<header class="hdr" id="kww-hdr"><div class="w">
  <a class="logo" href="{LINKS["home"]}" aria-label="King Will's Wills home"><img src="{LOGO_URL}" alt="King Will's Wills, Estate Planning Specialists" width="262" height="52"></a>
  <nav aria-label="Main"><ul class="nav">
    <li><a href="{LINKS["about"]}"{cls("about")}>About Sevvy</a></li>
    <li class="has-dd{svc_active}"><button type="button" aria-expanded="false" aria-haspopup="true">Services {icon("chevron")}</button><ul class="dd">{svc}</ul></li>
    <li class="has-dd{gd_active}"><button type="button" aria-expanded="false" aria-haspopup="true">Guides {icon("chevron")}</button><ul class="dd">{gd}</ul></li>
    <li><a href="{LINKS["testimonials"]}"{cls("testimonials")}>Reviews</a></li>
    <li><a href="{LINKS["blog"]}"{cls("blog")}>Blog</a></li>
    <li><a href="{LINKS["contact"]}"{cls("contact")}>Contact</a></li>
  </ul></nav>
  <div class="hdr-cta">
    <a class="btn btn--primary" href="{LINKS["contact"]}">Book a free chat</a>
    <button class="burger" type="button" aria-label="Open menu" aria-controls="kww-drawer" aria-expanded="false">{icon("menu")}</button>
  </div>
</div></header>
<div class="drawer" id="kww-drawer" aria-hidden="true">
  <div class="scrim" data-close></div>
  <div class="sheet" role="dialog" aria-label="Menu">
    <button class="close" type="button" aria-label="Close menu" data-close>×</button>
    <a href="{LINKS["home"]}"{cls("home")}>Home</a>
    <a href="{LINKS["about"]}"{cls("about")}>About Sevvy</a>
    <span class="grp">Services</span>{d_svc}
    <span class="grp">Guides</span>{d_gd}
    <a href="{LINKS["testimonials"]}"{cls("testimonials")}>Reviews</a>
    <a href="{LINKS["blog"]}"{cls("blog")}>Blog</a>
    <a href="{LINKS["contact"]}"{cls("contact")}>Contact</a>
    <a class="btn btn--primary" href="{LINKS["contact"]}">{icon("calendar")} Book a free chat</a>
    <a class="btn btn--ghost" href="tel:{PHONE_1_TEL}">{icon("phone")} {PHONE_1}</a>
  </div>
</div>'''


def footer():
    svc = "".join(f'<li><a href="{LINKS[k]}">{t}</a></li>' for k, t, _ in SERVICES)
    return f'''<footer class="ftr"><div class="w">
  <div>
    <a class="flogo" href="{LINKS["home"]}"><img src="{LOGO_URL}" alt="King Will's Wills" width="222" height="44"></a>
    <p>Friendly, professional estate planning from a qualified, insured and regulated Will writer. Founded by Sevvy Hasan in 2014.</p>
    <div class="social">
      <a href="https://www.facebook.com/KingWillsWills/" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a>
      <a href="https://twitter.com/KingWillsWills" target="_blank" rel="noopener" aria-label="X (Twitter)">{icon("x")}</a>
      <a href="https://www.linkedin.com/in/sevvy-hasan-step-affiliate-mipw-ab04099/" target="_blank" rel="noopener" aria-label="LinkedIn">{icon("linkedin")}</a>
    </div>
  </div>
  <div><h4>Services</h4><ul>{svc}</ul></div>
  <div><h4>Helpful guides</h4><ul>
    <li><a href="{LINKS["appointment"]}">Your appointment</a></li>
    <li><a href="{LINKS["intestacy"]}">Who inherits without a Will?</a></li>
    <li><a href="{LINKS["about"]}">About Sevvy</a></li>
    <li><a href="{LINKS["testimonials"]}">Client reviews</a></li>
    <li><a href="{LINKS["blog"]}">Blog</a></li>
  </ul></div>
  <div><h4>Get in touch</h4><ul>
    <li>Stourbridge <a href="tel:{PHONE_1_TEL}"><b>{PHONE_1}</b></a></li>
    <li>Worcester <a href="tel:{PHONE_2_TEL}"><b>{PHONE_2}</b></a></li>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li>{ADDRESS}</li>
  </ul>
  <div class="ftr-badges">
    <div class="ipw"><div style="position:relative;padding-bottom:36.8%;height:0;overflow:hidden"><iframe title="IPW / CTSI Approved Code badge" style="border:0;position:absolute;inset:0;width:100%;height:100%" src="https://cdn.yoshki.com/iframe/55068r.html" loading="lazy" scrolling="no"></iframe></div></div>
    <img src="{STEP_BADGE}" alt="STEP Will Writing Code, England and Wales" width="64" height="63" loading="lazy">
  </div>
  </div>
</div>
<div class="legal"><span>© <span data-year>2026</span> King Will's Wills Ltd. A member of the Institute of Professional Willwriters. This firm is compliant with the IPW code of practice.</span><span><a href="{LINKS["privacy"]}">Privacy</a><a href="{LINKS["contact"]}">Contact</a></span></div>
</footer>
<div class="mbar"><a class="btn btn--navy" href="tel:{PHONE_1_TEL}">{icon("phone")} Call us</a><a class="btn btn--primary" href="{LINKS["contact"]}">{icon("calendar")} Book a chat</a></div>'''


# ── Assembly ────────────────────────────────────────────────────────────────
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,600;1,500&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">')


def render(text):
    text = re.sub(r"\{\{>\s*(\w+)\s*\}\}", lambda m: BLOCKS[m.group(1)], text)
    text = re.sub(r"\{\{icon:(\w+)\}\}", lambda m: icon(m.group(1)), text)
    text = re.sub(r"\{\{link:(\w+)\}\}", lambda m: LINKS[m.group(1)], text)
    text = re.sub(r"\{\{photo:(\w+)\}\}", lambda m: photo(globals()[m.group(1)], "Sevvy Hasan, founder of King Will's Wills"), text)
    for k in ("PHONE_1", "PHONE_1_TEL", "PHONE_2", "PHONE_2_TEL", "EMAIL", "OFFICE_EMAIL", "ADDRESS"):
        text = text.replace("{{" + k + "}}", globals()[k])
    left = re.findall(r"\{\{[^}]*\}\}", text)
    if left:
        raise SystemExit(f"Unresolved tokens: {left}")
    return text


def build():
    css = (SRC / "base.css").read_text()
    js = (SRC / "site.js").read_text()
    head_ftr = footer()
    for page in sorted((SRC / "pages").glob("*.html")):
        raw = page.read_text()
        meta, body = raw.split("\n---\n", 1)
        m = dict(line.split(":", 1) for line in meta.strip().splitlines())
        m = {k.strip(): v.strip() for k, v in m.items()}
        html = f'''<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{m["title"]}</title>
<meta name="description" content="{m["description"]}">
{FONTS}
<style>
{css}
</style>
</head>
<body style="margin:0">
<div class="kww">
<a href="#main" style="position:absolute;left:-9999px" onfocus="this.style.left='8px'" onblur="this.style.left='-9999px'">Skip to content</a>
{header(m["active"])}
<main id="main">
{render(body)}
</main>
{head_ftr}
</div>
<script>
{js}
</script>
</body>
</html>
'''
        out = ROOT / f'KWW-{m["out"]}-GHL.html'
        out.write_text(html)
        print(f"built {out.name}  ({len(html)//1024} KB)")


if __name__ == "__main__":
    build()
