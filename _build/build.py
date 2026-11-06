#!/usr/bin/env python3
"""Generates the static familydoctor.sg site.

Edit the content below, then run:  python3 _build/build.py
Every page is written to <url-path>/index.html so the original WordPress URLs
(with trailing slashes) keep working on GitHub Pages.
"""
import json
import re
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://familydoctor.sg"
NAME = "The Family Doctor"
LEGAL = "The Family Doctor, Clinic & Surgery"
PHONE_DISPLAY = "+65 6453 4855"
PHONE = "+6564534855"
EMAIL = "doctor@familydoctor.sg"
MAILTO = "mailto:doctor@familydoctor.sg?subject=Question%20from%20a%20patient"
STREET = "215D Upper Thomson Road"
POSTAL = "574349"
LAT, LNG = 1.35232, 103.83491
MAPS = "https://www.google.com/maps/search/?api=1&query=The+Family+Doctor+215D+Upper+Thomson+Rd+Singapore+574349"
FACEBOOK = "https://www.facebook.com/thefamilydoctorsingapore/"
TWITTER = "https://twitter.com/thefamilydr"
CLOSED_ON = "2026-11-06"
TODAY = date.today().isoformat()
OG_IMAGE = f"{SITE}/assets/img/og-image.png"

ICONS = {
    "phone": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>',
    "mail": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>',
    "facebook": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M14 8V6.5c0-.7.2-1.2 1.2-1.2H17V2.2A24 24 0 0 0 14.6 2C12.2 2 10.6 3.5 10.6 6.1V8H8v3.4h2.6V22H14V11.4h2.7L17 8z"/></svg>',
    "x": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M17.8 3h3.1l-6.8 7.7 8 10.3h-6.2l-4.9-6.3L5.4 21H2.3l7.2-8.3L1.8 3h6.4l4.4 5.8zm-1.1 16.2h1.7L7.4 4.7H5.6z"/></svg>',
    "pin": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "arrow": '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M13 5l7 7-7 7-1.4-1.4 4.6-4.6H4v-2h12.2l-4.6-4.6z"/></svg>',
}

ADDRESS_LD = {
    "@type": "PostalAddress",
    "streetAddress": STREET,
    "addressLocality": "Singapore",
    "postalCode": POSTAL,
    "addressCountry": "SG",
}
ORG_ID = f"{SITE}/#clinic"
PERSON_ID = f"{SITE}/#dr-daniel-chia"
WEBSITE_ID = f"{SITE}/#website"


def crumbs_ld(items):
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
            for i, (n, p) in enumerate(items)
        ],
    }


def crumbs_html(items):
    lis = []
    for i, (n, p) in enumerate(items):
        if i == len(items) - 1:
            lis.append(f'<li aria-current="page">{escape(n)}</li>')
        else:
            lis.append(f'<li><a href="{p}">{escape(n)}</a></li>')
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'


def page(*, path, title, description, body, nav=None, og_type="website",
         ld=None, image=OG_IMAGE, image_alt=None, extra_head="", robots="index, follow, max-image-preview:large"):
    url = SITE + path
    graph = [
        {
            "@type": "WebSite",
            "@id": WEBSITE_ID,
            "url": SITE + "/",
            "name": NAME,
            "inLanguage": "en-SG",
            "publisher": {"@id": ORG_ID},
        }
    ] + (ld or [])
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    image_alt = image_alt or "The Family Doctor, clinic & surgery logo"

    def navlink(href, label, key):
        cur = ' aria-current="page"' if nav == key else ""
        return f'<a href="{href}"{cur}>{label}</a>'

    html = f"""<!doctype html>
<html lang="en-SG">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(description)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#800000">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta property="og:locale" content="en_SG">
<meta property="og:site_name" content="{NAME}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{escape(image_alt)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@thefamilydr">
<meta name="twitter:title" content="{escape(title)}">
<meta name="twitter:description" content="{escape(description)}">
<meta name="twitter:image" content="{image}">
<meta name="twitter:image:alt" content="{escape(image_alt)}">
{extra_head}<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap">
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">
{ld_json}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="notice-banner" role="note"><div class="wrap">The clinic closed permanently on 6 November 2026. <a href="/">Read Dr Chia&rsquo;s thank-you note</a></div></div>
<div class="topbar">
  <div class="wrap">
    <div class="contact">
      <a href="tel:{PHONE}">{ICONS['phone']}<span>{PHONE_DISPLAY}</span></a>
      <a href="{MAILTO}">{ICONS['mail']}<span>{EMAIL}</span></a>
    </div>
    <div class="social">
      <a href="{FACEBOOK}" rel="noopener" target="_blank">{ICONS['facebook']}<span>Facebook</span></a>
      <a href="{TWITTER}" rel="noopener" target="_blank">{ICONS['x']}<span>X (Twitter)</span></a>
    </div>
  </div>
</div>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="The Family Doctor home"><img src="/assets/img/logo.png" width="656" height="140" alt="The Family Doctor, clinic &amp; surgery"></a>
    <nav class="nav" aria-label="Main">
      {navlink('/blog/', 'Health Education', 'blog')}
      {navlink('/location/', 'Location', 'location')}
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <h2>{LEGAL}</h2>
        <address>{STREET}<br>Singapore {POSTAL}<br>Tel: <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></address>
        <p style="margin-top:12px">The clinic is permanently closed. Thank you for 35 years of support.</p>
      </div>
      <div>
        <h2>Pages</h2>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/blog/">Health Education</a></li>
          <li><a href="/location/">Location</a></li>
        </ul>
      </div>
      <div>
        <h2>Follow us</h2>
        <ul>
          <li><a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a></li>
          <li><a href="{TWITTER}" rel="noopener" target="_blank">X (Twitter)</a></li>
          <li><a href="{MAILTO}">Contact Dr Chia</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-base">
      <span>&copy; {NAME} 2017&ndash;2026</span>
      <span><a href="/terms-of-use/">Terms of Use</a> &middot; <a href="/privacy-policy/">Privacy Policy</a></span>
    </div>
  </div>
</footer>
</body>
</html>
"""
    # Relative links so pages also work when opened straight from disk.
    # 404.html stays root-absolute: GitHub Pages serves it at whatever URL was missing.
    if path != "/404.html":
        depth = path.strip("/").count("/") + 1 if path.strip("/") else 0
        prefix = "../" * depth or "./"
        html = re.sub(r'(href|src)="/(?!/)', lambda m: f'{m.group(1)}="{prefix}', html)
    out = ROOT / path.lstrip("/") / "index.html" if path.endswith("/") else ROOT / path.lstrip("/")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    return out


CLINIC_LD = {
    "@type": ["MedicalClinic", "MedicalBusiness"],
    "@id": ORG_ID,
    "name": LEGAL,
    "alternateName": NAME,
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/logo.png", "width": 656, "height": 140},
    "image": OG_IMAGE,
    "telephone": PHONE,
    "email": EMAIL,
    "address": ADDRESS_LD,
    "geo": {"@type": "GeoCoordinates", "latitude": LAT, "longitude": LNG},
    "hasMap": MAPS,
    "medicalSpecialty": "PrimaryCare",
    "description": "Family medical clinic and surgery on Upper Thomson Road, Singapore, run by Dr Daniel Chia for over 35 years. Permanently closed on 6 November 2026.",
    "sameAs": [FACEBOOK, TWITTER],
    "founder": {"@id": PERSON_ID},
    "employee": {"@id": PERSON_ID},
}
PERSON_LD = {
    "@type": "Physician",
    "@id": PERSON_ID,
    "name": "Dr Daniel Chia",
    "worksFor": {"@id": ORG_ID},
    "address": ADDRESS_LD,
    "telephone": PHONE,
}

# ---------------------------------------------------------------- Home
home_body = f"""
<section class="page-head">
  <div class="narrow">
    <p class="eyebrow">Notice</p>
    <h1>Thank you for 35 years</h1>
    <p class="lede">After more than three and a half decades on Upper Thomson Road, The Family Doctor clinic has closed for good. A message from Dr Daniel Chia and the nurses.</p>
  </div>
</section>
<section class="narrow" aria-labelledby="letter-title">
  <article class="letter">
    <h2 id="letter-title">A deep-felt thank you</h2>
    <p>Well, after 35 and a half years, we are sad to announce that our clinic has finally closed for good.</p>
    <p>We&rsquo;ve had an incredible run&hellip; many of our patients have grown up with us and we were already seeing the third and fourth generations in families that have continued to trust us all these years.</p>
    <p>Words cannot ever adequately express how much of an honour and privilege it has been for me and my faithful nurses, Christine, Helen and Jeannie, to have had your trust in us for all these almost 36 years, and I am personally deeply grateful to you all, our beloved patients and now friends, for all these incredible years of friendship and support that you have given me.</p>
    <p>You all know how to reach me. I may not be able to be your family doctor any more, but I would love for our friendship to continue. Please keep in touch with me and let me know how you and your family do in the years to come. I will miss you all deeply.</p>
    <p class="sign">With all our heart,<strong>Dr Daniel Chia</strong>Christine, Helen and Jeannie</p>
    <time datetime="{CLOSED_ON}">6th November 2026</time>
    <div class="actions">
      <a class="btn btn-light" href="{MAILTO}">{ICONS['mail']} Contact Dr Chia</a>
      <a class="btn btn-ghost" href="/location/">{ICONS['pin']} Clinic location</a>
    </div>
  </article>

  <div class="grid">
    <div class="card">
      <p class="kicker">Consultation hours</p>
      <p class="status">Permanently closed</p>
      <p>The clinic is permanently closed. Thank you for 35 years of support.</p>
    </div>
    <div class="card">
      <p class="kicker">Where we were</p>
      <h3>{NAME}</h3>
      <address>{LEGAL}<br>{STREET}<br>Singapore {POSTAL}<br>Tel: <a href="tel:{PHONE}">{PHONE_DISPLAY}</a></address>
      <p style="margin-top:10px"><a href="{MAPS}" rel="noopener" target="_blank">View on Google Maps</a></p>
    </div>
    <div class="card">
      <p class="kicker">Stay in touch</p>
      <p>For the latest announcements and updates, follow us on <a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a> and <a href="{TWITTER}" rel="noopener" target="_blank">X (Twitter)</a>.</p>
    </div>
  </div>
</section>
"""
page(
    path="/",
    title="The Family Doctor | Clinic and Surgery",
    description="Dr Daniel Chia's family clinic at 215D Upper Thomson Road, Singapore, has closed after 35 years. A heartfelt thank-you to our patients.",
    body=home_body,
    ld=[CLINIC_LD, PERSON_LD, {
        "@type": "WebPage", "@id": SITE + "/#webpage", "url": SITE + "/",
        "name": "The Family Doctor | Clinic and Surgery", "isPartOf": {"@id": WEBSITE_ID},
        "about": {"@id": ORG_ID}, "datePublished": CLOSED_ON, "dateModified": TODAY,
    }],
)

# ---------------------------------------------------------------- Location
DIRECTIONS = [
    ("Bishan MRT", "Bishan+MRT+Station"),
    ("AMK Hub", "AMK+Hub"),
    ("Toa Payoh MRT", "Toa+Payoh+MRT+Station"),
    ("MacRitchie Reservoir bus stop", "MacRitchie+Reservoir+Bus+Stop"),
]
dest = f"{LAT},{LNG}"
dir_items = "\n".join(
    f'<li><a href="https://www.google.com/maps/dir/?api=1&amp;origin={o}&amp;destination={dest}" rel="noopener" target="_blank">From {escape(n)} {ICONS["arrow"]}</a></li>'
    for n, o in DIRECTIONS
)
loc_crumbs = [("Home", "/"), ("Location", "/location/")]
loc_body = f"""
<section class="page-head">
  <div class="wrap">
    {crumbs_html(loc_crumbs)}
    <p class="eyebrow">Location</p>
    <h1>Clinic location</h1>
    <p class="lede">The Family Doctor, Clinic &amp; Surgery, 215D Upper Thomson Road, Singapore.</p>
  </div>
</section>
<section class="wrap">
  <div class="callout" role="note"><strong>The clinic is permanently closed.</strong> After 35 years, The Family Doctor closed on 6 November 2026. Thank you for 35 years of support. <a href="/">Read Dr Chia&rsquo;s note</a>.</div>
  <div class="grid" style="margin-top:0">
    <div class="card">
      <p class="kicker">Address</p>
      <h2 style="margin-top:0;font-size:1.35rem">{LEGAL}</h2>
      <address>{STREET}<br>Singapore {POSTAL}</address>
      <p style="margin-top:14px"><a class="btn btn-primary" href="{MAPS}" rel="noopener" target="_blank">{ICONS['pin']} View on Google Maps</a></p>
    </div>
    <div class="card">
      <p class="kicker">Contact</p>
      <p><a href="tel:{PHONE}">{PHONE_DISPLAY}</a><br><a href="{MAILTO}">{EMAIL}</a></p>
      <p>For announcements and updates, follow us on <a href="{FACEBOOK}" rel="noopener" target="_blank">Facebook</a> and <a href="{TWITTER}" rel="noopener" target="_blank">X (Twitter)</a>.</p>
    </div>
    <div class="card">
      <p class="kicker">Consultation hours</p>
      <p class="status">Permanently closed</p>
      <p>The clinic no longer sees patients.</p>
    </div>
  </div>
  <h2>Directions</h2>
  <ul class="directions">
{dir_items}
  </ul>
</section>
"""
page(
    path="/location/",
    title="Location | The Family Doctor",
    description="Where The Family Doctor clinic was located: 215D Upper Thomson Road, Singapore 574349. The clinic closed permanently on 6 November 2026 after 35 years.",
    body=loc_body,
    nav="location",
    ld=[CLINIC_LD, crumbs_ld(loc_crumbs), {
        "@type": "WebPage", "url": SITE + "/location/", "name": "Location | The Family Doctor",
        "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": ORG_ID},
    }],
)

# ---------------------------------------------------------------- Ideal weight article
POST_DATE = "2017-04-20"
BMI = [
    ("Below 18.5", "Risk of nutritional deficiency diseases and osteoporosis", "risk-mod"),
    ("18.5 &ndash; 22.9", "Low risk (healthy range)", "risk-low"),
    ("23.0 &ndash; 27.4", "Moderate risk", "risk-mod"),
    ("27.5 and above", "High risk", "risk-high"),
]
bmi_rows = "\n".join(f'<tr><td>{b}</td><td class="{c}">{r}</td></tr>' for b, r, c in BMI)

# height cm: (men small, medium, large) or None, (women small, medium, large) or None
WEIGHTS = [
    (145, None, ("46-50", "49-55", "53-59")),
    (147, None, ("46-51", "50-56", "54-61")),
    (150, None, ("47-52", "51-57", "55-62")),
    (152, None, ("48-53", "52-58", "56-63")),
    (155, ("57-60", "58-63", "61-67"), ("49-55", "53-60", "58-65")),
    (157, ("58-61", "59-64", "62-68"), ("50-56", "55-61", "59-66")),
    (160, ("59-61", "60-65", "63-70"), ("51-57", "56-62", "61-68")),
    (163, ("60-62", "61-66", "64-71"), ("53-59", "57-64", "62-70")),
    (165, ("61-63", "62-67", "65-73"), ("54-60", "59-65", "53-72")),
    (168, ("61-65", "63-69", "66-75"), ("56-61", "60-66", "65-74")),
    (170, ("62-66", "65-70", "68-77"), ("57-63", "61-68", "66-76")),
    (173, ("63-67", "66-71", "69-79"), ("58-64", "63-69", "67-77")),
    (175, ("64-69", "66-73", "71-81"), ("60-66", "64-71", "69-78")),
    (178, ("65-70", "69-74", "72-82"), ("61-67", "66-72", "70-80")),
    (180, ("66-71", "70-76", "73-84"), ("62-68", "67-73", "71-81")),
    (183, ("68-73", "71-78", "75-86"), None),
    (185, ("69-75", "73-80", "77-88"), None),
    (188, ("71-77", "75-81", "79-91"), None),
    (190, ("72-79", "76-84", "81-93"), None),
]


def wtable(idx, who):
    rows = []
    for h, men, women in WEIGHTS:
        v = (men, women)[idx]
        if v:
            rows.append(f"<tr><td>{h}</td>" + "".join(f"<td>{x.replace('-', '&ndash;')}</td>" for x in v) + "</tr>")
    return f"""<div class="table-wrap"><table>
<caption>{who}: desirable weight (kg, in light clothing)</caption>
<thead><tr><th scope="col">Height (cm)</th><th scope="col">Small frame</th><th scope="col">Medium frame</th><th scope="col">Large frame</th></tr></thead>
<tbody>
{chr(10).join(rows)}
</tbody></table></div>"""


post_crumbs = [("Home", "/"), ("Health Education", "/category/health-education/"), ("Ideal weight", "/ideal-weight/")]
post_img_alt = "A pair of running shoes beside two green 0.5 kg hand weights"
post_body = f"""
<article>
<section class="page-head">
  <div class="narrow">
    {crumbs_html(post_crumbs)}
    <a class="tag" href="/category/health-education/">Health Education</a>
    <h1 style="margin-top:10px">Ideal weight</h1>
    <p class="meta"><time datetime="{POST_DATE}">20 April 2017</time></p>
  </div>
</section>
<div class="narrow prose">
  <figure class="post-hero" style="margin:0 0 32px">
    <img src="/assets/img/ideal-weight.webp" width="640" height="400" alt="{post_img_alt}">
  </figure>
  <h2>Is my weight ideal?</h2>
  <p>There are two ways to check whether your weight is in a healthy range.</p>

  <h3>1. Body Mass Index (BMI)</h3>
  <p>BMI is an index of obesity in adults, based on your height and weight. It is calculated as:</p>
  <p class="formula">BMI = weight (kg) &divide; [height (m) &times; height (m)]</p>
  <div class="table-wrap"><table class="wrap-cells">
    <caption>BMI for adults and risk of heart disease and diabetes</caption>
    <thead><tr><th scope="col">BMI (kg/m&sup2;)</th><th scope="col">Risk category</th></tr></thead>
    <tbody>
{bmi_rows}
    </tbody>
  </table></div>

  <h3>2. Desirable body weight range</h3>
  <p>You can also compare your weight against the desirable range for your height and body frame (small, medium or large). Weights are in kilograms in light clothing, with height in centimetres.</p>
  {wtable(0, "Men")}
  {wtable(1, "Women")}

  <p style="margin-top:2em"><a href="/category/health-education/">&larr; More health education articles</a></p>
</div>
</article>
"""
page(
    path="/ideal-weight/",
    title="Ideal weight | The Family Doctor",
    description="Is your weight ideal? Check it two ways: BMI risk categories, and desirable weight ranges by height and body frame for men and women.",
    body=post_body,
    nav="blog",
    og_type="article",
    image=f"{SITE}/assets/img/ideal-weight.jpg",
    image_alt=post_img_alt,
    extra_head=f'<meta property="article:published_time" content="{POST_DATE}T08:00:00+08:00">\n<meta property="article:section" content="Health Education">\n',
    ld=[CLINIC_LD, PERSON_LD, crumbs_ld(post_crumbs), {
        "@type": "BlogPosting",
        "@id": SITE + "/ideal-weight/#article",
        "mainEntityOfPage": SITE + "/ideal-weight/",
        "headline": "Ideal weight",
        "description": "How to check whether your weight is ideal using BMI and desirable body weight ranges.",
        "image": [f"{SITE}/assets/img/ideal-weight.jpg"],
        "datePublished": f"{POST_DATE}T08:00:00+08:00",
        "dateModified": f"{POST_DATE}T08:00:00+08:00",
        "author": {"@id": ORG_ID},
        "publisher": {"@id": ORG_ID},
        "articleSection": "Health Education",
        "inLanguage": "en-SG",
    }],
)

# ---------------------------------------------------------------- Blog + category listings
card = f"""<a class="post-card" href="/ideal-weight/">
  <img src="/assets/img/ideal-weight.webp" width="640" height="400" alt="{post_img_alt}" loading="lazy">
  <div class="body">
    <span class="tag">Health Education</span>
    <h2>Ideal weight</h2>
    <p>Two ways to tell whether your weight is healthy: Body Mass Index and the desirable weight range for your height and frame.</p>
    <p class="meta" style="margin-top:12px"><time datetime="{POST_DATE}">20 April 2017</time></p>
  </div>
</a>"""
item_list = {
    "@type": "ItemList",
    "itemListElement": [{"@type": "ListItem", "position": 1, "url": SITE + "/ideal-weight/"}],
}
for path, title, h1, desc, crumbs in [
    ("/blog/", "Blog | The Family Doctor", "Health Education",
     "Health education articles from Dr Daniel Chia of The Family Doctor, Singapore, including how to check your ideal weight with BMI and desirable weight ranges.",
     [("Home", "/"), ("Health Education", "/blog/")]),
    ("/category/health-education/", "Health Education | The Family Doctor", "Health Education",
     "Health Education articles from The Family Doctor clinic in Singapore: practical guidance from Dr Daniel Chia on weight, BMI and everyday family health.",
     [("Home", "/"), ("Health Education", "/category/health-education/")]),
]:
    body = f"""
<section class="page-head">
  <div class="wrap">
    {crumbs_html(crumbs)}
    <p class="eyebrow">Blog</p>
    <h1>{h1}</h1>
    <p class="lede">Practical health guidance from Dr Daniel Chia.</p>
  </div>
</section>
<section class="wrap"><div class="post-list">{card}</div></section>
"""
    page(path=path, title=title, description=desc, body=body, nav="blog",
         ld=[crumbs_ld(crumbs), {"@type": "CollectionPage", "url": SITE + path, "name": title,
                                 "isPartOf": {"@id": WEBSITE_ID}, "mainEntity": item_list}])

# ---------------------------------------------------------------- Terms of Use
TERMS = [
    ("Terms of Use Agreement",
     "<p>Your access to this website is conditional on your acceptance of these Terms of Use and our <a href=\"/privacy-policy/\">Privacy Policy</a>. By using the site in any way you agree to them, including any later changes. You must be 18 or older to use this site, and it is not intended for anyone covered by the US Children&rsquo;s Online Privacy Protection Act. We may refuse access to anyone for any reason, and we may collect data as described in the Privacy Policy. It is your responsibility to stay informed of changes to these terms.</p>"),
    ("Parties to the Terms of Use Agreement",
     "<p>&ldquo;Visitors&rdquo; includes anyone who views or uses the site, including users, subscribers, members, affiliates, resellers and customers. The other party is the owner and operator of this website. This agreement takes precedence over any terms a visitor publishes on their own site. Disputes are governed by this agreement and applicable law, and are resolved by binding arbitration or in a court of the website&rsquo;s choosing. Any contract with the website cannot be terminated without the website&rsquo;s written consent.</p>"),
    ("Use of Information From This Website",
     "<p>Unless you have a written agreement with us, you may not use, copy, save, print, sell, broadcast or publish content from this site for commercial or public purposes. Breach of this term carries liquidated damages of US$100,000 plus costs.</p>"),
    ("Ownership of Website or Right to Use, Sell, Publish Contents of This Website",
     "<p>The content of this website is owned or licensed by the website and is presumed to be proprietary and protected by copyright. Visitors have no rights in it without express permission.</p>"),
    ("Hyperlinking to Site, Co-Branding, &ldquo;Framing&rdquo; and Referencing Site Prohibited",
     "<p>You may not link to this site, reference its address, or display it within a frame without permission. Breach of this term carries the same liquidated damages of US$100,000 plus costs.</p>"),
    ("Disclaimer for Contents of Site",
     "<p>We do not guarantee the accuracy of anything on this website, and you rely on its contents at your own risk. Nothing on the site is a promise or guarantee of any outcome. Information on this site is general in nature and is not a substitute for personal medical advice.</p>"),
    ("Disclaimer for Harm Caused to Your Computer or Software From Interacting With This Website or Its Contents",
     "<p>We are not responsible for any virus or harmful code that affects your device as a result of using this website or anything displayed on it.</p>"),
    ("Disclaimer for Harm Caused by Downloads",
     "<p>Anything you download from this site is downloaded at your own risk. We do not guarantee that downloads are free of viruses or other harmful code.</p>"),
    ("Limitation of Liability",
     "<p>By using this website you waive any claim for harm of any kind, whether physical, emotional, personal or business-related, arising from your use of the site.</p>"),
    ("Indemnification",
     "<p>You agree to reimburse the website for any damages it is required to pay as a result of your actions.</p>"),
    ("Submissions",
     "<p>Anything you send to the website becomes its property and may be used for any purpose, including commercially, without compensation to you.</p>"),
    ("Notice",
     "<p>You waive any right to receive notice of any kind.</p>"),
    ("Disputes",
     "<p>Any claim against the website must be resolved by binding arbitration. You waive the right to go to court, to a jury trial, to pre-trial discovery and to take part in a class action. The website may bring proceedings in a court of its choosing.</p>"),
    ("Jurisdiction and Venue",
     "<p>Any court proceedings will be heard in the jurisdiction listed in the website&rsquo;s contact information, or another court chosen by the website.</p>"),
    ("Billing Model and Cancellation / Refund Policy",
     "<p>Unless an offer states otherwise, refund requests should be made using the contact details below.</p>"),
    ("Applicable Law",
     "<p>These terms are governed by the law of the jurisdiction listed in the website&rsquo;s contact information.</p>"),
    ("Contact Information",
     f"<p>{LEGAL}, {STREET}, Singapore {POSTAL}. Email <a href=\"{MAILTO}\">{EMAIL}</a>.</p>"),
]
for path, title, h1, desc, sections in [
    ("/terms-of-use/", "Terms of Use | The Family Doctor", "Terms of Use",
     "Terms of Use for familydoctor.sg, the website of The Family Doctor clinic and surgery in Singapore: content ownership, disclaimers and limitation of liability.",
     TERMS),
    ("/privacy-policy/", "Privacy Policy | The Family Doctor", "Privacy Policy",
     "Privacy Policy for familydoctor.sg: what information The Family Doctor website collects, how cookies are used, and how you can control them.",
     [
        ("Our commitment",
         "<p>The Family Doctor values the privacy of everyone who visits this website. This policy explains what personal information the site receives and collects, and how it is safeguarded. We never sell your personal information to third parties.</p>"),
        ("Log files",
         "<p>Like most websites, this site&rsquo;s hosting provider records standard server log data, such as your IP address, internet service provider, browser type, the time of your visit and the pages you view.</p>"),
        ("Cookies and web beacons",
         "<p>Cookies may be used to remember your preferences, for example so that a message is only shown once per visit.</p>"),
        ("Advertising cookies",
         "<p>Google may use DoubleClick DART cookies to serve ads based on browsing history. These cookies use non-personally identifiable information and do not record your name, contact details or financial account numbers. You can opt out of personalised advertising through <a href=\"https://adssettings.google.com/\" rel=\"noopener\" target=\"_blank\">Google Ads Settings</a>.</p>"),
        ("Managing cookies",
         "<p>You can disable cookies entirely, or block them selectively, through your browser settings or security software. Doing so may affect how some websites work. Your browser vendor&rsquo;s website has detailed instructions.</p>"),
        ("Contact us",
         f"<p>Questions about this policy can be sent to <a href=\"{MAILTO}\">{EMAIL}</a>.</p>"),
     ]),
]:
    crumbs = [("Home", "/"), (h1, path)]
    secs = "\n".join(f"<h2>{h}</h2>\n{b}" for h, b in sections)
    body = f"""
<section class="page-head">
  <div class="narrow">
    {crumbs_html(crumbs)}
    <p class="eyebrow">Legal</p>
    <h1>{h1}</h1>
  </div>
</section>
<div class="narrow"><div class="panel prose">
{secs}
</div></div>
"""
    page(path=path, title=title, description=desc, body=body,
         ld=[crumbs_ld(crumbs), {"@type": "WebPage", "url": SITE + path, "name": title, "isPartOf": {"@id": WEBSITE_ID}}])

# ---------------------------------------------------------------- 404
nf = """
<section class="page-head"><div class="narrow">
  <p class="eyebrow">Error 404</p>
  <h1>Page not found</h1>
  <p class="lede">The page you were looking for isn&rsquo;t here. The clinic has closed, but its health education articles and contact details are still available.</p>
  <p><a class="btn btn-primary" href="/">Go to the home page</a> &nbsp; <a href="/blog/">Health Education</a> &middot; <a href="/location/">Location</a></p>
</div></section>
"""
page(path="/404.html", title="Page not found | The Family Doctor",
     description="This page could not be found on familydoctor.sg.", body=nf, robots="noindex, follow")

# ---------------------------------------------------------------- sitemap / robots / feed
URLS = [
    ("/", TODAY, "1.0"),
    ("/location/", TODAY, "0.8"),
    ("/blog/", TODAY, "0.6"),
    ("/ideal-weight/", TODAY, "0.7"),
    ("/category/health-education/", TODAY, "0.5"),
    ("/terms-of-use/", TODAY, "0.2"),
    ("/privacy-policy/", TODAY, "0.2"),
]
IMAGES = {
    "/": [f"{SITE}/assets/img/logo.png"],
    "/ideal-weight/": [f"{SITE}/assets/img/ideal-weight.webp"],
}
entries = []
for p, lm, pr in URLS:
    imgs = "".join(f"\n    <image:image><image:loc>{u}</image:loc></image:image>" for u in IMAGES.get(p, []))
    entries.append(f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{lm}</lastmod>\n    <priority>{pr}</priority>{imgs}\n  </url>")
(ROOT / "sitemap.xml").write_text(
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    + "\n".join(entries) + "\n</urlset>\n", encoding="utf-8")

(ROOT / "robots.txt").write_text(
    f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

(ROOT / "feed.xml").write_text(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
  <title>{NAME}</title>
  <link>{SITE}/</link>
  <atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>
  <description>Health education from The Family Doctor, Singapore</description>
  <language>en-SG</language>
  <item>
    <title>Ideal weight</title>
    <link>{SITE}/ideal-weight/</link>
    <guid>{SITE}/ideal-weight/</guid>
    <pubDate>Thu, 20 Apr 2017 08:00:00 +0800</pubDate>
    <category>Health Education</category>
    <description>Two ways to check whether your weight is ideal: BMI and desirable body weight ranges.</description>
  </item>
</channel>
</rss>
""", encoding="utf-8")

print("built", len(URLS), "pages + 404, sitemap.xml, robots.txt, feed.xml")
