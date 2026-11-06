# familydoctor.sg — static site

Static rebuild of familydoctor.sg for GitHub Pages. Every original WordPress URL is kept
(`/`, `/location/`, `/blog/`, `/ideal-weight/`, `/category/health-education/`,
`/terms-of-use/`, `/privacy-policy/`), and the old image URLs under `/wp-content/uploads/`
still resolve, so existing links and image search entries keep working.

## Deploy
1. Create a GitHub repo and push the contents of this folder to the `main` branch.
2. Repo **Settings → Pages**: Source = "Deploy from a branch", branch `main`, folder `/ (root)`.
3. Custom domain is set by the `CNAME` file (`familydoctor.sg`). At your DNS provider, point the
   apex domain at GitHub Pages with A records 185.199.108.153, 185.199.109.153, 185.199.110.153,
   185.199.111.153, and add a `www` CNAME to `<your-user>.github.io`. Then tick **Enforce HTTPS**.
4. In Google Search Console, submit `https://familydoctor.sg/sitemap.xml`.

## Editing
Content lives in `_build/build.py`. Edit it and run `python3 _build/build.py` to regenerate the
HTML, `sitemap.xml`, `robots.txt` and `feed.xml`. The `_build` folder is not published
(GitHub Pages' Jekyll step skips folders starting with `_`), so don't add a `.nojekyll` file.

## SEO included
Unique title and meta description per page, canonical URLs, Open Graph and Twitter cards,
JSON-LD (MedicalClinic, Physician, WebSite, BlogPosting, BreadcrumbList), image sitemap,
robots.txt, RSS feed, alt text on every image, custom 404, favicon set and web manifest.
