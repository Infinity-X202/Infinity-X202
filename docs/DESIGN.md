# Design

Infinity X uses a dark cyber-technical system built for a GitHub README, where each graphic is a single SVG image. The page does not reflow inside the SVG. Markdown under each image carries the same facts in normal text so the profile stays readable when the image is scaled down on a phone.

## Color

| Role | Hex |
| --- | --- |
| Background | `#070B16` |
| Electric blue | `#247BFF` |
| Crimson | `#FF354F` |
| Main text | `#F4F7FF` |
| Muted text | `#A7B2C8` |
| Card | `#0C1322` |

Blue and crimson are limited to borders, small labels, the infinity mark, and one or two orbit strokes. Body copy stays off-white or muted.

## Type

- Syne (500, 600, 700) for headings and sentences
- IBM Plex Mono (400, 500) for kickers, handles, and chip labels

Both are embedded as Latin WOFF2 so the graphic does not request a font server. If a viewer strips `@font-face`, the fallback is Segoe UI and Cascadia Mono.

## The five graphics

All boards are 960 units wide, with a 28-unit corner radius and a hairline gradient stroke.

1. **Hero** (`assets/hero.svg`, 960×540). Greeting, a clip reveal of the name, four interest labels on a 12-second loop, a two-line mission, and the monogram.
2. **About** (`assets/about-life.svg`, 960×500). Four focus rows on the left. Three interest panels on the right, changing every 4 seconds, with a segment bar for each panel.
3. **Stack** (`assets/stack.svg`, 960×704). Three elliptical lanes. Each lane holds four labelled icons. A chip band underneath groups the same tools and states that icons are not expertise claims.
4. **ID card** (`assets/id-dashboard.svg`, 960×660). A fixed stem, a ring that moves with the card, straps, a foil sweep, a decorative barcode, and only public profile facts.
5. **Connect** (`assets/connect.svg`, 960×500). The pointing monogram on the left and one GitHub card on the right. The only confirmed profile URL is GitHub.

## Motion

Motion is SMIL, started at `0s`, with `keyTimes` for the delays.

| Graphic | Behavior |
| --- | --- |
| Hero name | Width clip from 0 to full over 1.05s, then frozen |
| Hero labels | Discrete swap every 3 seconds |
| About panels | Discrete swap every 4 seconds |
| About bars | Linear fill during that panel's 4 seconds |
| Orbits | Dashed stroke drift and a dot on the path |
| ID card | Drop for 1.15s, damped settle for 2.4s, then ±1.7° every 3.6s |
| Connect | A short arrow nudge every 2.2s |

Base attributes are the readable resting state: the name is fully visible, the first interest is shown, the first progress segment is filled, and the card hangs straight. Removing every `animate`, `animateTransform`, and `animateMotion` element leaves that state.

A `@media (prefers-reduced-motion: reduce)` rule hides those animation elements. In an Edge test on 26 October 2026, `--force-prefers-reduced-motion` did not change the inline frame, so this reduced-motion rule is not confirmed. The no-animation state was confirmed by deleting the animation elements.

## GitHub rendering

Inline SVG in Edge played the timeline. The same hero file loaded with an HTML `img` matched the no-animation frame exactly. GitHub profile images are closer to `img` than to inline SVG, so visitors may see the resting state. The resting state is designed to stand alone.

## What the card is allowed to say

Public facts used on 26 October 2026:

- Profile name already published in the previous README: Adil Fayyaz
- GitHub display name: InfinityX
- Handle: Infinity-X202
- Account created: 29 April 2025, shown as “Since April 2025”

No employer, location, certification, clearance, follower count, or star count is drawn. The barcode widths are a fixed decorative sequence. They are not derived from a name or URL.
