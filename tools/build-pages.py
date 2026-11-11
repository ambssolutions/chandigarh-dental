#!/usr/bin/env python3
"""Build the inner pages (services.html, about.html) from index.html.

The head (styles, fonts, theme bootstrap), header, phone menu and footer are copied from index.html,
so the inner pages always match the home page. Run after changing index.html:

    python3 tools/build-pages.py
"""
import html, json, os, re, sys, urllib.parse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
from content import STRINGS, DOCTORS  # noqa: E402

src = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
SITE = 'https://chandigarh-dental.vercel.app'  # the live address; change here if the clinic gets its own domain
WA = 'https://wa.me/919915510261'
TEL = 'tel:+919915510261'
MAP = 'https://www.google.com/maps/search/?api=1&amp;query=Chandigarh+Multispeciality+Dental+Clinic+Chamkaur+Sahib'


def cut(start, end, s=src, inclusive=True):
    a = s.index(start)
    b = s.index(end, a) + (len(end) if inclusive else 0)
    return s[a:b]


# ---------- shared pieces from index.html ----------
head = src[:src.index('</head>')]
head = re.sub(r'<script type="application/ld\+json">\s*\{"@context":"https://schema.org","@type":"FAQPage".*?</script>\n?', '', head, flags=re.S)

top = cut('<div class="progress"', '</aside>')
footer = cut('<footer>', '</footer>')
callbar = cut('<nav class="callbar', '</nav>')


def localise_links(chunk, current):
    chunk = chunk.replace('href="#top"', 'href="/"')
    chunk = re.sub(r'href="#([\w-]+)"', r'href="/#\1"', chunk)
    chunk = chunk.replace('class="btn solid pinbook" href="#book"', 'class="btn solid pinbook" href="/#book"')
    if current:
        chunk = chunk.replace(f'<a href="{current}">', f'<a href="{current}" aria-current="page">')
    return chunk


def page(slug, title, title_key, desc, body):
    h = head
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)}</title>', h, flags=re.S)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc)}">', h)
    h = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{html.escape(title)}">', h)
    if slug == '404':
        h = re.sub(r'<link rel="canonical" href="[^"]*">\n?', '<meta name="robots" content="noindex">\n', h)
    else:
        h = h.replace(f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/{slug}">')
    h = h.replace(f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/{slug}">')
    h = h.replace('</head>', '')
    h += f'<meta name="page-title-key" content="{html.escape(title_key)}">\n'
    # the build stamp is added to the shared files so phones fetch the new copy after each release
    ver = re.search(r'<meta name="build" content="([^"]*)">', h).group(1).replace(':', '').replace('-', '')
    h += f'<link rel="stylesheet" href="/pages.css?v={ver}">\n</head>\n'
    cur = '/' + slug
    out = (h + f'<body class="page-inner page-{slug}">\n' + localise_links(top, cur) + '\n<div class="navspace" aria-hidden="true"></div>\n'
           + '<main id="main" class="page">\n' + body + '\n</main>\n\n'
           + localise_links(footer, cur) + '\n' + callbar.replace('callbar glass away', 'callbar glass').replace('href="#book"', 'href="/#book"') + '\n'
           + f'<script src="/site.js?v={ver}" defer></script>\n</body>\n</html>\n')
    open(os.path.join(ROOT, slug + '.html'), 'w', encoding='utf-8').write(out)
    return out


# ---------- services ----------
def tile(name):
    """Return (art svg, tag, description) for a treatment tile on the home page."""
    m = re.search(r'<article class="tile[^"]*">(.*?)</article>', src[:0] or src, flags=re.S)
    for art in re.finditer(r'<article class="tile[^"]*">(.*?)</article>', src, flags=re.S):
        block = art.group(1)
        if f'<h3>{html.escape(name)}</h3>' in block or f'<h3>{name}</h3>' in block:
            svg = re.search(r'<svg class="art".*?</svg>', block, flags=re.S)
            tag = re.search(r'<span class="tag">(.*?)</span>', block)
            p = re.search(r'</h3><p>(.*?)</p>', block, flags=re.S)
            return (svg.group(0) if svg else ''), (tag.group(1) if tag else ''), (p.group(1) if p else '')
    raise SystemExit('tile not found: ' + name)


MIRROR = ('<svg class="art" viewBox="0 0 300 120" aria-hidden="true"><path class="fill" d="M150 16c-16-12-44-6-44 22 0 18 10 26 12 44 2 14 6 22 12 22 8 0 7-24 20-24s12 24 20 24c6 0 10-8 12-22 2-18 12-26 12-44 0-28-28-34-44-22z"/>'
          '<g><line x1="196" y1="40" x2="246" y2="96" stroke="var(--tooth-line)" stroke-width="5" stroke-linecap="round"/><circle cx="190" cy="34" r="13" fill="var(--enamel)" stroke="var(--aqua)" stroke-width="3"/></g></svg>')

SERVICES = [
    # slug, name on home page tile, booking-form option, bullets
    ('checkup', None, 'General check-up', [
        'A regular check-up finds decay, gum problems and worn fillings early, while they are simpler to treat.',
        'The dentist looks at each tooth and your gums, and explains anything that needs attention.',
        'It is a good time to ask about cleaning, sensitivity or any tooth that has been bothering you.']),
    ('root-canal', 'Root canal (RCT)', 'Root canal (RCT)', [
        'Needed when the soft tissue inside a tooth is infected or inflamed, often after deep decay or a crack.',
        'The dentist cleans the canals inside the tooth, disinfects them and seals them.',
        'Most teeth then need a filling or a crown to protect them. The dentist will advise which.']),
    ('laser', 'Laser dentistry', 'Laser dentistry', [
        'A dental laser can be used for some gum and soft-tissue treatments.',
        'It is precise, which can mean less bleeding and quicker healing in suitable cases.',
        'The dentist will tell you whether a laser suits your treatment.']),
    ('braces', 'Straightening', 'Braces / straightening', [
        'Braces and alignment help with crowding, gaps and a bite that does not close well.',
        'Treatment is planned after an examination and usually takes months, with regular visits.',
        'Ask about the options and how long your treatment might take.']),
    ('reshaping', 'Tooth reshaping', 'Tooth reshaping', [
        'Small changes to the shape of a tooth can fix chips, uneven edges and minor gaps.',
        'The dentist smooths the tooth or builds it up with tooth-coloured material.',
        'It is often done in a single visit.']),
    ('fillings', 'Dental fillings', 'Dental fillings', [
        'A filling repairs a tooth after the decay is cleaned out.',
        'Treating a cavity early helps stop it reaching the nerve.',
        'Tooth-coloured fillings can be matched to your teeth.']),
    ('implants', 'Dental implants', 'Dental implants', [
        'An implant replaces a missing tooth with a post set in the jaw and a crown on top.',
        'It needs healthy gums and enough bone, which the dentist checks first.',
        'Treatment takes place over several visits while the implant settles.']),
    ('whitening', 'Teeth whitening', 'Teeth whitening', [
        'Whitening lightens stains from tea, food and tobacco.',
        "It is done under the dentist's care, after checking your teeth and gums.",
        'Results vary from person to person, and the dentist will explain what to expect.']),
    ('surgery', 'Oral & maxillofacial surgery', 'Oral surgery / extraction', [
        'Covers extractions, wisdom teeth and other surgical care of the mouth and jaw.',
        'The dentist explains the procedure and the aftercare before anything starts.',
        'Maxillofacial prosthetics are also offered. Ask the clinic about your case.']),
]


PHOTO_ALT = {
    'checkup': 'A dentist showing a smiling patient his check-up results on a tablet',
    'root-canal': 'A dentist with magnifying loupes treating a back tooth',
    'laser': 'A dentist holding a dental laser above an instrument tray',
    'braces': 'A smiling teenager wearing clear braces',
    'reshaping': 'A patient checking her reshaped front teeth in a hand mirror',
    'fillings': 'A tooth-colour shade guide held next to a tooth model',
    'implants': 'A model of a dental implant with a crown, set in the jaw',
    'whitening': 'A smiling man with naturally bright teeth in the dental chair',
    'surgery': 'A dental surgeon explaining a jaw X-ray to an older patient',
}

cards, chips = [], []
for i, (slug, name, option, bullets) in enumerate(SERVICES, 1):
    if name:
        art, tag, desc = tile(name)
        title = html.escape(name)
    else:
        art, tag, desc, title = MIRROR, 'Routine care', 'A full look at your teeth and gums, with anything that needs attention explained.', 'Check-ups'
    ask = '/?svc=' + urllib.parse.quote(option) + '#book'
    wa = WA + '?text=' + urllib.parse.quote(f'Hello, I would like to ask about {option}.')
    chips.append(f'<li><a href="#{slug}">{title}</a></li>')
    lis = ''.join(f'<li>{html.escape(b)}</li>' for b in bullets)
    cards.append(f'''  <article class="svc glass{" svc-flip" if i % 2 == 0 else ""}" id="{slug}">
    <figure class="svc-photo"><img src="/img/svc-{slug}-v2-800.webp" srcset="/img/svc-{slug}-v2-800.webp 800w, /img/svc-{slug}-v2-1536.webp 1536w" sizes="(min-width: 861px) 560px, 100vw" width="1536" height="1024" {"" if i==1 else "loading=\"lazy\" "}decoding="async" alt="{PHOTO_ALT[slug]}"></figure>
    <div class="svc-main">
      <span class="tag">{tag}</span><h2>{title}</h2><p class="svc-desc">{desc}</p>
      <div class="svc-know"><h3>Good to know</h3><ul class="ticks">{lis}</ul></div>
    </div>
  </article>''')

services_body = f'''<section class="phead"><div class="wrap">
  <span class="kicker">Services</span>
  <h1>Treatments at the clinic</h1>
  <p>Nine treatments under one roof in Chamkaur Sahib, explained in plain words.</p>
  <ul class="chips" aria-label="Treatments">{''.join(chips)}</ul>
  <p class="ainote">Photos on this page are AI-generated illustrations, not photos of the clinic.</p>
</div></section>
<section class="svcs" style="padding-top:0"><div class="wrap">
{chr(10).join(cards)}
  <p class="note">General guide only. The dentist decides after examining you.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="cta-band glass"><span class="kicker">Not sure what you need?</span><h2>Start with a check-up.</h2>
    <div class="acts"><a class="btn solid" href="/?svc={urllib.parse.quote('General check-up')}#book">Book a check-up</a></div></div>
</div></section>'''

page('services', 'Treatments | Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib', 'Services',
     'Root canal, laser dentistry, braces, tooth reshaping, fillings, implants, whitening, oral surgery and check-ups at Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib.',
     services_body)


# ---------- dentists (About page) ----------
if DOCTORS:
    cards_d = []
    for d in DOCTORS:
        initials = ''.join(w[0] for w in d['name'].replace('Dr.', '').split()[:2]).upper()
        pic = (f'<img src="/{d["photo"]}" alt="{html.escape(d["name"])}" width="400" height="400" loading="lazy" decoding="async">'
               if d.get('photo') else f'<span class="doc-initials" aria-hidden="true">{initials}</span>')
        bio = f'<p>{html.escape(d["bio"])}</p>' if d.get('bio') else ''
        cards_d.append(f'<article class="doc glass"><div class="doc-pic">{pic}</div><h3>{html.escape(d["name"])}</h3>'
                       f'<span class="doc-q">{html.escape(d.get("quals", ""))}</span><span class="doc-r">{html.escape(d.get("role", ""))}</span>{bio}</article>')
    team = f'''<section style="padding-top:0"><div class="wrap">
  <div class="head"><span class="kicker">Your dentists</span><h2>Meet the dentists</h2></div>
  <div class="docs">{''.join(cards_d)}</div>
</div></section>'''
else:
    team = '''<section style="padding-top:0"><div class="wrap">
  <div class="team-gen glass">
    <div class="team-art" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><linearGradient id="tmg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2de2d0"/><stop offset="1" stop-color="#6cb8ff"/></linearGradient></defs><circle cx="60" cy="60" r="56" fill="none" stroke="url(#tmg)" stroke-width="2.5" opacity=".6"/><circle cx="60" cy="46" r="17" fill="url(#tmg)"/><path d="M28 96c4-18 17-28 32-28s28 10 32 28" fill="url(#tmg)"/><path d="M52 74l8 10 8-10" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></div>
    <span class="kicker">Your dentists</span><h2>Meet the dentists</h2>
    <p>Treatment is carried out by the clinic's dentists, who explain each step in plain words before anything starts.</p>
    <ul class="team-pts"><li>15+ years of experience</li><li>Explained in plain words</li><li>You choose before anything starts</li><li>Follow-up advice for home</li></ul>
  </div>
</div></section>'''

# ---------- about ----------
stats = cut('<div class="wrap stats">', '</div>\n</section>', inclusive=False).replace(' rv"', '"') + '</div>'
steps = cut('<ol class="steps">', '</ol>').replace(' rv"', '"')
about_body = f'''<section class="phead"><div class="wrap">
  <span class="kicker">About the clinic</span>
  <h1>Dental care in Chamkaur Sahib</h1>
  <p>Chandigarh Multispeciality Dental Clinic is on Morinda Road in Chamkaur Sahib, opposite the bus stand.</p>
  <p style="margin-top:.8rem">It brings check-ups, root canals, laser dentistry, braces, implants and oral surgery under one roof, so there is no second trip to Ropar or Chandigarh for a specialist.</p>
  <p class="allsvc"><a class="btn" href="/services">See all treatments</a></p>
</div></section>
<section style="padding-block:0">{stats}
</section>
<section><div class="wrap">
  <div class="head"><h2>How a visit works</h2></div>
  {steps}
</div></section>
{team}
<section style="padding-top:0"><div class="wrap">
  <div class="about-find glass">
    <h2>Find the clinic</h2>
    <address><span>Morinda Road, Opposite Bus Stand</span><br><span>Chamkaur Sahib, Punjab 140112</span></address>
    <p class="hrs"><span>Mon–Sat · 10 AM – 7 PM</span><br><span>Sunday</span> · <span>Closed</span></p>
    <div class="acts"><a class="btn" href="{MAP}" target="_blank" rel="noopener">Open in Google Maps</a></div>
  </div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="cta-band glass"><h2>Ready when you are</h2><p>Call, send a WhatsApp message or request an appointment, and the clinic will get back to you.</p>
    <div class="acts"><a class="btn solid" href="/#book">Book an appointment</a></div></div>
</div></section>'''

page('about', 'About | Chandigarh Multispeciality Dental Clinic, Chamkaur Sahib', 'About the clinic',
     'About Chandigarh Multispeciality Dental Clinic on Morinda Road, Chamkaur Sahib: treatments under one roof, opening hours and how to find the clinic.',
     about_body)

# ---------- 404 ----------
page('404', 'Page not found | Chandigarh Multispeciality Dental Clinic', 'Page not found',
     'This page does not exist or has moved.',
     '''<section class="phead" style="min-height:52vh;display:grid;align-content:center"><div class="wrap">
  <span class="kicker">404</span>
  <h1>Page not found</h1>
  <p>This page does not exist or has moved.</p>
  <p class="allsvc"><a class="btn solid" href="/">Back to home</a> <a class="btn" href="/services">See all treatments</a></p>
</div></section>''')

# ---------- sitemap and robots ----------
import datetime
today = datetime.date.today().isoformat()
open(os.path.join(ROOT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{SITE}/{u}</loc><lastmod>{today}</lastmod></url>\n' for u in ['', 'services', 'about']) + '</urlset>\n')
open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')

# ---------- translations ----------
ipath = os.path.join(ROOT, 'i18n.json')
j = json.load(open(ipath, encoding='utf-8'))
added = 0
for en, hi, pa in STRINGS:
    if en not in j['hi']:
        j['hi'][en], j['pa'][en] = hi, pa
        added += 1
json.dump(j, open(ipath, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('built services.html, about.html; translations added:', added)
