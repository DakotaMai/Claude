# Brief: Facebook & Instagram posts for Ember

Paste this into the design session that made the two months of social posts.

## What's changed
LinkedIn posts stay as they are. Facebook and Instagram need their own treatment: an even
mix of two post types.

1. **Story posts (keep the existing style).** Image-led, personal, "building in public"
   posts like the current LinkedIn ones: what I'm doing, what I'm noticing, real life
   alongside the business. Tighter captions than LinkedIn, and no CTA on most of them.
2. **Text posts (new).** Bold graphic posts in the same style as the Health Check ads.
   Each makes one sharp point and sends people somewhere: the free Systems Health Check
   or the website.

Alternate them, so roughly half of each over the two months.

## Text post style (match the Health Check ads exactly)
- Background: dark chocolate `#2a140c`. Text: cream `#f2e1cd`. Accent: burnt orange `#c75c33`.
- Headline: Chivo, weight 900, tight letter-spacing (-0.025em), two short lines. The second
  line, the payoff, is in orange. Example: "It works. / Because you do."
- Body: Livvic 500, one or two lines, cream at about 80% opacity.
- Small outlined orange pill at the top, uppercase with letter-spacing, e.g. "FREE SYSTEMS HEALTH CHECK".
- Optional visual borrowed from the quiz results: the orange score ring ("50 / 100") or the
  six result bars with "LOOK HERE FIRST" tags.
- Orange button-style block at the bottom ("Take the 3-minute check →"), with "EMBER / BY
  VICTORIA LEWIS" bottom right.
- Sizes: 1080×1350 for the feed, 1080×1920 for Stories.
- Reference images: `ads/health-check-ignite-feed.png` and `ads/health-check-inferno-feed.png`
  in the DakotaMai/Claude repo, branch `claude/cool-dirac-ywj4hh`. The render script is
  `ads/render-ads.js`.

## What the text posts can say
Hooks that already work, taken from the site and the quiz:
- "Your business shouldn't rely on you for everything."
- "It's not a you problem. It's a systems problem."
- "The numbers are good. The picture isn't."
- "It works because of who, not how."
- "Every yes creates a pile of admin."
- "People who aren't ready yet just disappear."
- "Nobody owns the plumbing."

## Where they link
- **Health Check:** `[health check page URL]?utm_source=meta&utm_medium=organic&utm_campaign=health-check&utm_content=[post-name]`
- **Website:** victorialewis.co.uk. Use the Ignite page for small-business posts and the
  Inferno page for growing-team posts.

## Rules
- **Two audiences.** Ignite & Build is for solo owners and micro businesses who want the
  business set up behind them to free up their time. Inferno is for growing businesses with
  a team, messy processes, no tech person, and systems not used to their fullest.
- **Prices.** Never show small-business prices in anything aimed at larger businesses.
  Ignite is £750 and Build is a further £1,500 (£2,250 total), and those only appear in
  Ignite content.
- **Voice.** British English, warm and direct, no hype, dashes written as " - ". CTAs are
  soft ("if that's you, you know where I am").
