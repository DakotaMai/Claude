# King Will's Wills: new GHL website

Twelve ready-to-paste pages, rebuilt from the old kw-wills.co.uk site and the service leaflets. Brand colours: Blue `#37B3E7`, Grey `#C9C7D5`, Green `#5EECAF`, with a deep version of the logo grey for headings. Official logo and accreditation badges included.

Everything on the site comes from the leaflets, the brochure or the old website. Detail lives in FAQ sections (written once in `src/faqs.py`, shown on each service page and all together on the FAQs page) to keep pages light.

## Pages

| File | GHL page slug | Replaces old page(s) |
|---|---|---|
| `KWW-Home-GHL.html` | `/` | Home |
| `KWW-About-GHL.html` | `/about` | About |
| `KWW-Will-Writing-GHL.html` | `/will-writing` | Will Writing |
| `KWW-Trusts-GHL.html` | `/trusts` | Trusts |
| `KWW-Lasting-Powers-of-Attorney-GHL.html` | `/lasting-powers-of-attorney` | Health & Welfare, Property & Financial and Business LPA pages (now tabs on one page) |
| `KWW-Storage-and-Aftercare-GHL.html` | `/storage-and-after-care` | Storage and After Care |
| `KWW-Estate-Administration-GHL.html` | `/estate-administration-and-probate` | Estate Administration and Probate |
| `KWW-Your-Appointment-GHL.html` | `/your-appointment` | **New**: appointment guide + interactive checklist |
| `KWW-Intestacy-Checker-GHL.html` | `/intestacy` | **New**: interactive "who inherits without a Will?" tool |
| `KWW-Testimonials-GHL.html` | `/testimonials` | Testimonials |
| `KWW-Contact-GHL.html` | `/contact` | Contact |
| `KWW-FAQs-GHL.html` | `/faqs` | **New**: every FAQ, with search and topic filters |

The blog, privacy and copyright pages stay as GHL's own pages (`/blog`, `/privacy`). Funeral Planning has been removed.

## Putting a page into GHL

1. Sites → Websites → your site → add a page with the slug from the table above.
2. Add a full-width section, remove its padding, add one **Custom JS/HTML** element.
3. Open the `.html` file, copy **everything**, paste into the element, save.
4. In the page's SEO settings, copy in the `<title>` and `description` from the top of the file.

Each page is self-contained (header, footer, styles and scripts included), so pages don't depend on each other.

## Redirects (keep your Google rankings)

Add these 301 redirects in GHL (Sites → URL Redirects):

| Old URL | New URL |
|---|---|
| `/health-and-welfare-lasting-powers-of-attorney` | `/lasting-powers-of-attorney#health-and-welfare` |
| `/property-and-financial-lasting-powers-of-attorney` | `/lasting-powers-of-attorney#property-and-financial` |
| `/lasting-powers-of-attorney-for-your-business` | `/lasting-powers-of-attorney#business` |
| `/funeral-planning` | `/` |
| `/site-map`, `/copyright` | `/` |

The LPA page opens the right tab automatically from the `#…` part of the link.

## Before going live

- [ ] **Photos of Sevvy**: the pages currently borrow two photos from the old site (`/images/split/14_right.png` and `18_left.png`). Upload good photos of Sevvy to GHL Media, then change `SEVVY_PHOTO` / `SEVVY_PHOTO_2` at the top of `build.py` and re-run it. If a photo ever fails to load, a branded "SH" monogram shows instead, so nothing looks broken.
- [ ] **Contact form and calendar**: on the Contact page, replace the two dashed placeholder boxes with your GHL form and calendar embed codes (search the file for `GHL FORM` and `GHL CALENDAR`).
- [ ] **Review link**: on the Testimonials page, point the "Leave a review" button at your Google review link.
- [ ] **Check the facts**: the intestacy checker uses the current £322,000 spouse allowance (deaths from 26 July 2023). The printed Intestacy Chart leaflet still says £250,000 and should be updated. The LPA FAQ asks people to check the current OPG registration fee, because the leaflet's £82 is out of date.
- [ ] **Logo & badges**: the official logo and the IPW, Trading Standards and STEP badges are embedded directly in each page, so they work immediately. The full-size originals are in `assets/` for GHL Media, the favicon and social profiles. The footer also keeps IPW's live verification badge, which loads from IPW's site.

## Editing later

The pages are generated from `src/` by `build.py`. The shared header, footer, phone numbers, reviews and styling live in `build.py` and `src/base.css`. Change them once and run:

```
python3 build.py
```

The script rebuilds all twelve pages. Page content lives in `src/pages/`.
