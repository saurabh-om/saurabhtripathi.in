#!/usr/bin/env python3
"""Build the Building Momentum essay pages from _writing/*.md.

Each source file is a small header (title, date, source) above a `---` line,
then the issue body in a tiny Markdown subset: paragraphs, ### / #### headings,
"- " bullets, **bold**, *italic* and [links](url).

Running this script:
  - writes writing/<slug>.html for every issue
  - rewrites the archive list in writing.html (between ISSUES markers)
  - rewrites the essay entries in sitemap.xml (between WRITING markers)

Usage: python3 build-writing.py
"""
import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "_writing"
OUT = ROOT / "writing"
SITE = "https://saurabhtripathi.in"
NEWSLETTER = "https://www.linkedin.com/newsletters/building-momentum-7291532655647436800/"
GREETINGS = re.compile(r"^(hey there|namaskar)\b", re.I)


# ---------- parsing ----------

def parse(path):
    head, body = path.read_text(encoding="utf-8").split("\n---\n", 1)
    meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
    num, slug = path.stem.split("-", 1)
    meta.update(num=int(num), slug=slug, body=body.strip(),
                date=date.fromisoformat(meta["date"]))
    words = len(re.findall(r"\w+", body))
    meta["minutes"] = max(1, round(words / 230))
    meta["excerpt"] = excerpt(body)
    return meta


def excerpt(body, limit=160):
    for para in body.split("\n\n"):
        text = re.sub(r"[*#\[\]]|\(http[^)]*\)", "", para).strip()
        if not text or GREETINGS.match(text) or text.startswith("-"):
            continue
        if len(text) <= limit:
            return text
        cut = text[:limit].rsplit(" ", 1)[0].rstrip(",;:—-")
        return cut + "…"
    return ""


def inline(text):
    text = html.escape(text, quote=False)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)",
                  r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*(?!\s)(.+?)(?<!\s)\*(?!\*)", r"<em>\1</em>", text)
    return text


def render(body):
    out, first = [], True
    for block in body.split("\n\n"):
        block = block.strip()
        if block.startswith("#### "):
            out.append(f"<h4>{inline(block[5:])}</h4>")
        elif block.startswith("### "):
            out.append(f"<h2>{inline(block[4:])}</h2>")
        elif block.startswith("- "):
            items = [inline(l[2:]) for l in block.splitlines()]
            out.append("<ul>\n" + "\n".join(f"  <li>{i}</li>" for i in items) + "\n</ul>")
        else:
            cls = ""
            if first and not GREETINGS.match(block):
                cls, first = ' class="first-para"', False
            elif first:
                cls = ' class="greeting"'
            out.append(f"<p{cls}>{inline(block).replace(chr(10), '<br />')}</p>")
    return "\n".join(out)


def fmt(d):
    return f"{d.day} {d.strftime('%B %Y')}"


# ---------- page shell, borrowed from writing.html ----------

def shell():
    page = (ROOT / "writing.html").read_text(encoding="utf-8")
    head_end = page.index("  <!-- Phosphor icon sprite -->")
    sprite_to_main = page[head_end:page.index('  <main id="main">')]
    after_main = page[page.index("  </main>") + len("  </main>\n"):]
    head_links = page[page.index('  <link rel="icon"'):head_end]
    return head_links, sprite_to_main, after_main


def article_page(it, prev, nxt, parts):
    head_links, sprite_to_main, after_main = parts
    url = f"{SITE}/writing/{it['slug']}.html"
    title = html.escape(it["title"])
    desc = html.escape(it["excerpt"])
    ld = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": it["title"],
        "description": it["excerpt"],
        "datePublished": it["date"].isoformat(),
        "url": url,
        "mainEntityOfPage": url,
        "image": f"{SITE}/assets/img/og/og-image.png",
        "inLanguage": "en-IN",
        "isPartOf": {"@type": "Blog", "name": "Building Momentum", "url": f"{SITE}/writing.html"},
        "sameAs": it["source"],
        "author": {"@id": f"{SITE}/#person"},
        "publisher": {"@id": f"{SITE}/#person"},
    }
    nav = []
    if prev:
        nav.append(f'<a class="issue-nav-link prev" href="/writing/{prev["slug"]}.html"><span>Older</span><strong>{html.escape(prev["title"])}</strong></a>')
    if nxt:
        nav.append(f'<a class="issue-nav-link next" href="/writing/{nxt["slug"]}.html"><span>Newer</span><strong>{html.escape(nxt["title"])}</strong></a>')
    sprite_to_main = sprite_to_main.replace('class="is-active" href="/writing.html"', 'class="is-active" href="/writing.html" aria-current="page"')
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — Saurabh Tripathi</title>
  <meta name="description" content="{desc}" />
  <meta name="author" content="Saurabh Tripathi" />
  <link rel="canonical" href="{url}" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{url}" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{desc}" />
  <meta property="og:image" content="{SITE}/assets/img/og/og-image.png" />
  <meta property="og:image:width" content="1200" />
  <meta property="og:image:height" content="630" />
  <meta property="article:published_time" content="{it['date'].isoformat()}" />
  <meta property="article:author" content="Saurabh Tripathi" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{desc}" />
  <meta name="twitter:image" content="{SITE}/assets/img/og/og-image.png" />
{head_links}  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>

{sprite_to_main}  <main id="main">

    <section class="bold-hero issue-hero">
      <div class="container">
        <span class="bg-num" aria-hidden="true">{it['num']:02d}</span>
        <div class="tag"><a href="/writing.html">Building Momentum</a> · Issue {it['num']:02d}</div>
        <h1 class="title">{title}</h1>
        <div class="meta">
          <div><span>Published</span><strong><time datetime="{it['date'].isoformat()}">{fmt(it['date'])}</time></strong></div>
          <div><span>Reading time</span><strong>{it['minutes']} min</strong></div>
          <div><span>Written by</span><strong>Saurabh Tripathi</strong></div>
        </div>
      </div>
    </section>

    <section class="section-sm">
      <div class="narrow">
        <article class="prose issue-body">
{render(it['body'])}
        </article>

        <aside class="issue-origin">
          <p>First published in <strong>Building Momentum</strong>, Saurabh's newsletter on LinkedIn.</p>
          <div class="issue-origin-actions">
            <a class="btn btn-primary" href="{NEWSLETTER}" target="_blank" rel="noopener"><svg width="16" height="16" aria-hidden="true"><use href="#i-linkedin"/></svg> Subscribe on LinkedIn</a>
            <a class="btn btn-ghost" href="{html.escape(it['source'])}" target="_blank" rel="noopener">Comment on the original <svg width="14" height="14" aria-hidden="true"><use href="#i-arrow-ur"/></svg></a>
          </div>
        </aside>

        <nav class="issue-nav" aria-label="More issues">
          {chr(10).join('          ' + n for n in nav).strip()}
        </nav>
        <p class="issue-all"><a href="/writing.html">All issues →</a></p>
      </div>
    </section>

    <!-- CTA BAND -->
    <section class="cta-band">
      <div class="container">
        <div class="eyebrow">Got something to talk about</div>
        <h2>Got something to <span class="italic-serif">talk about</span>?</h2>
        <p>Thirty minutes, direct with Saurabh. No slides, no sales pitch.</p>
        <a class="cta-btn" href="https://zcal.co/opusmomentum/meet" target="_blank" rel="noopener">
          Book a 30-min call
          <span class="chip" aria-hidden="true"><svg><use href="#i-arrow-ur"/></svg></span>
        </a>
        <div class="small-note">Thirty minutes <span class="dot"></span> Direct with Saurabh <span class="dot"></span> No slides</div>
      </div>
    </section>

  </main>
{after_main}"""


def archive(items):
    rows = []
    for it in items:
        rows.append(f"""          <li>
            <a class="issue-row" href="/writing/{it['slug']}.html">
              <span class="ir-num">{it['num']:02d}</span>
              <span class="ir-main">
                <span class="ir-date"><time datetime="{it['date'].isoformat()}">{fmt(it['date'])}</time> · {it['minutes']} min read</span>
                <span class="ir-title">{html.escape(it['title'])}</span>
                <span class="ir-excerpt">{html.escape(it['excerpt'])}</span>
              </span>
              <span class="ir-arrow" aria-hidden="true"><svg width="18" height="18"><use href="#i-arrow-ur"/></svg></span>
            </a>
          </li>""")
    return "\n".join(rows)


def replace_between(text, start, end, new):
    a, b = text.index(start) + len(start), text.index(end)
    return text[:a] + "\n" + new + "\n" + text[b:]


def main():
    items = sorted((parse(p) for p in SRC.glob("*.md")), key=lambda i: i["num"])
    OUT.mkdir(exist_ok=True)
    parts = shell()
    for i, it in enumerate(items):
        prev = items[i - 1] if i > 0 else None
        nxt = items[i + 1] if i + 1 < len(items) else None
        (OUT / f"{it['slug']}.html").write_text(article_page(it, prev, nxt, parts), encoding="utf-8")

    newest_first = list(reversed(items))
    w = ROOT / "writing.html"
    w.write_text(replace_between(w.read_text(encoding="utf-8"),
                 "<!-- ISSUES:START -->", "          <!-- ISSUES:END -->",
                 archive(newest_first)), encoding="utf-8")

    entries = "\n".join(f"""  <url>
    <loc>{SITE}/writing/{it['slug']}.html</loc>
    <lastmod>{it['date'].isoformat()}</lastmod>
    <priority>0.7</priority>
  </url>""" for it in newest_first)
    s = ROOT / "sitemap.xml"
    s.write_text(replace_between(s.read_text(encoding="utf-8"),
                 "<!-- WRITING:START -->", "  <!-- WRITING:END -->", entries), encoding="utf-8")
    print(f"Built {len(items)} issues.")


if __name__ == "__main__":
    main()
