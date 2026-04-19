# saurabhtripathi.in

Personal website for **Saurabh Tripathi**, Founder & CEO of Opus Momentum Digital LLP.

Plain HTML + CSS + JS. No build step. Deployed on GitHub Pages at the custom domain `saurabhtripathi.in`.

## Structure

```
.
├── index.html              # Home
├── about.html              # About
├── work.html               # Work (results / numbers)
├── opus-momentum.html      # The agency
├── writing.html            # Building Momentum newsletter
├── contact.html            # zcal embed + contact details
├── privacy.html            # Privacy notice
├── 404.html                # Branded not-found page
├── CNAME                   # Custom domain config for GitHub Pages
├── robots.txt
├── sitemap.xml
└── assets/
    ├── css/styles.css
    ├── js/
    │   ├── main.js         # Nav scroll, mobile menu, scroll-reveal, marquee
    │   ├── motion.js       # Hero word reveal, portrait parallax, cursor follower
    │   └── cookie-banner.js
    └── img/
        ├── portrait/       # 400/800/1200 JPG
        ├── logo/           # Wordmark + arrow
        ├── favicon/        # 32, 192, 512, apple-touch-icon
        ├── og/             # og-image.png (1200x630)
        ├── testimonials/   # 7 square photos, 400x400
        └── clients/        # 43 client logos, 600w PNG
```

## Local preview

```bash
python3 -m http.server 8000
```

Open http://localhost:8000.

## Deployment

1. Create a public repo on GitHub: `saurabhtripathi/saurabhtripathi.in`.
2. Commit everything in this folder as the repo root and push to `main`.
3. In Settings → Pages, set source to `main` branch, folder `/`.
4. DNS at the registrar for `saurabhtripathi.in`:
   - **A records** (apex) — point to GitHub Pages:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - **CNAME** for `www` → `saurabhtripathi.github.io`
5. Once DNS resolves, enable "Enforce HTTPS" in Settings → Pages.

## Before going live

- [ ] Replace the GA4 Measurement ID placeholder (`G-XXXXXXXXXX`) in `assets/js/cookie-banner.js`.
- [ ] Regenerate `assets/img/og/og-image.png` if the tagline or portrait is changed.
- [ ] Post-launch: submit the sitemap in Google Search Console.

## Stack / design

- **Type:** Fraunces (display) + Inter (body), Google Fonts.
- **Palette:** cream `#FAF7F2` background, ink `#1A1A1A` text, accent `#FF751F` (logo orange).
- **Motion:** hero text reveal, portrait parallax, CTA cursor follower, logo marquee. All gated behind `prefers-reduced-motion`.
- **Analytics:** GA4, loaded only after explicit consent via a cookie banner.
