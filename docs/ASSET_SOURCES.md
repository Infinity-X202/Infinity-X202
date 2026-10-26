# Asset sources

Checked 26 October 2026. Nothing in the SVG files is loaded from the network. Fonts and icon paths are embedded. Licenses are in `docs/licenses/`.

## Fonts

| Family | Weights | Source | License |
| --- | --- | --- | --- |
| Syne | 500, 600, 700 | Latin WOFF2 from Fontsource 5.2.5 (`cdn.jsdelivr.net/fontsource/fonts/syne@5.2.5`) | SIL Open Font License 1.1. See `docs/licenses/OFL-Syne.txt`. |
| IBM Plex Mono | 400, 500 | Latin WOFF2 from Fontsource 5.2.5 | SIL Open Font License 1.1, copyright IBM Corp., reserved name “Plex”. See `docs/licenses/OFL-IBM-Plex.txt`. |

## Icons

Icon paths are from Simple Icons and are recolored to `#E8EEF9` so they stay visible on the navy background. Simple Icons is CC0 1.0. The shapes are trademarks of their owners and are used here only to name a technology.

Fetched from `https://cdn.simpleicons.org/{slug}` on 26 October 2026:

Python, JavaScript, TypeScript, GNU Bash (`gnubash`), Linux, Git, GitHub, React, Next.js (`nextdotjs`), FastAPI, PyTorch, Tailwind CSS, Hugging Face.

The Windows mark was not on that CDN. It is the four-square path from Simple Icons 11.14.0 (`simple-icons@11.14.0/icons/windows.svg`). It names the operating system. It is not a Microsoft partnership.

## Portraits

`assets/id.png` and `assets/right_pointing.png` were **not** supplied with the playbook. Both files in this package are generated geometric monograms:

- Transparent PNG (alpha 0 at the corners)
- `id.png` is 1024×1024
- `right_pointing.png` is 1200×900, with chevrons aimed to the viewer’s right

They are not a portrait of the owner and are not a traced face. To use a real portrait, replace both PNGs with the playbook exports (real alpha, not a painted checkerboard), then run:

```bash
python scripts/build_profile.py
```

The script embeds whatever PNGs are already in `assets/` and does not overwrite them.

## Profile facts

Taken from the public GitHub API for `Infinity-X202` and from that account’s existing profile README on 26 October 2026. No private data is embedded.
