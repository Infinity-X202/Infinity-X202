"""Build the Infinity X profile graphics.

Embeds OFL fonts and Simple Icons paths. Portrait PNGs are geometric
monograms until assets/id.png and assets/right_pointing.png are replaced
with the owner's images (see docs/ASSET_SOURCES.md).
"""

from __future__ import annotations

import base64
import io
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
ASSETS = ROOT / "assets"
ICONS = BUILD / "icons"
FONTS = BUILD / "fonts"

W = 960


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def font_css() -> str:
    faces = []
    for family, weight, filename in (
        ("Syne", 500, "syne-500.woff2"),
        ("Syne", 600, "syne-600.woff2"),
        ("Syne", 700, "syne-700.woff2"),
        ("IBM Plex Mono", 400, "plex-400.woff2"),
        ("IBM Plex Mono", 500, "plex-500.woff2"),
    ):
        raw = (FONTS / filename).read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        faces.append(
            f"""@font-face {{
  font-family: "{family}";
  font-style: normal;
  font-weight: {weight};
  src: url("data:font/woff2;base64,{b64}") format("woff2");
}}"""
        )
    return "\n".join(faces) + """
.display { font-family: Syne, "Segoe UI", sans-serif; font-weight: 700; fill: #F4F7FF; }
.mid { font-family: Syne, "Segoe UI", sans-serif; font-weight: 600; fill: #F4F7FF; }
.body { font-family: Syne, "Segoe UI", sans-serif; font-weight: 500; fill: #A7B2C8; }
.mono { font-family: "IBM Plex Mono", "Cascadia Mono", ui-monospace, monospace; font-weight: 400; fill: #A7B2C8; }
.kicker { font-family: "IBM Plex Mono", "Cascadia Mono", ui-monospace, monospace; font-weight: 500; fill: #C4B5FD; letter-spacing: 0.16em; }
@media (prefers-reduced-motion: reduce) {
  animate, animateTransform, animateMotion { display: none !important; }
}
"""


def load_icons() -> dict[str, tuple[list[str], str]]:
    found = {}
    for path in sorted(ICONS.glob("*.svg")):
        raw = path.read_text(encoding="utf-8")
        paths = re.findall(r"<path\b[^>]*\bd=\"([^\"]+)\"", raw)
        if not paths:
            raise SystemExit(f"No path in {path.name}")
        title = re.search(r"<title>([^<]+)</title>", raw)
        found[path.stem] = (paths, title.group(1) if title else path.stem)
    return found


def png_data(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


POSTER = Path(
    r"C:\Users\adilf\.cursor\projects\c-Users-adilf-Desktop-github\assets"
    r"\Infinity_X_Cyberpunk_Hacker_Poster-589c4648-35f3-4105-82d1-c92e4afa019e.jpg"
)


def jpeg_b64(image: Image.Image, longest: int, quality: int) -> str:
    frame = image.convert("RGB")
    frame.thumbnail((longest, longest), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    frame.save(buf, format="JPEG", quality=quality, optimize=True)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def make_portraits() -> tuple[str, str]:
    """Crop the supplied poster. Returns JPEG data for the hero and the face."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    src = Image.open(POSTER).convert("RGB")
    face = src.crop((328, 48, 712, 520))
    hero = src.crop((330, 8, 800, 548))
    face.save(ASSETS / "id.png", "PNG", optimize=True)
    hero.save(ASSETS / "right_pointing.png", "PNG", optimize=True)
    return jpeg_b64(hero, 720, 78), jpeg_b64(face, 520, 82)


def defs(prefix: str, width: int, height: int) -> str:
    return f"""<defs>
  <radialGradient id="{prefix}-glow-a" cx="82%" cy="18%" r="55%">
    <stop offset="0" stop-color="#3D7BFF" stop-opacity="0.42"/>
    <stop offset="1" stop-color="#3D7BFF" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="{prefix}-glow-b" cx="12%" cy="100%" r="50%">
    <stop offset="0" stop-color="#C026D3" stop-opacity="0.34"/>
    <stop offset="1" stop-color="#C026D3" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="{prefix}-rim" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#38BDF8" stop-opacity="0.95"/>
    <stop offset="0.5" stop-color="#E9D5FF" stop-opacity="0.35"/>
    <stop offset="1" stop-color="#E879F9" stop-opacity="0.95"/>
  </linearGradient>
  <linearGradient id="{prefix}-word" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#7DD3FC"/>
    <stop offset="0.45" stop-color="#F5F3FF"/>
    <stop offset="1" stop-color="#E879F9"/>
  </linearGradient>
  <linearGradient id="{prefix}-metal" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F4F7FF"/>
    <stop offset="0.45" stop-color="#8E9BB3"/>
    <stop offset="1" stop-color="#4C566B"/>
  </linearGradient>
  <pattern id="{prefix}-grid" width="48" height="48" patternUnits="userSpaceOnUse">
    <path d="M48 0 H0 V48" fill="none" stroke="#F4F7FF" stroke-opacity="0.045" stroke-width="1"/>
  </pattern>
  <pattern id="{prefix}-dots" width="18" height="18" patternUnits="userSpaceOnUse">
    <circle cx="1" cy="1" r="0.9" fill="#F4F7FF" fill-opacity="0.14"/>
  </pattern>
  <clipPath id="{prefix}-frame">
    <rect x="18" y="18" width="{width - 36}" height="{height - 36}" rx="28"/>
  </clipPath>
</defs>"""


def chrome(prefix: str, width: int, height: int) -> str:
    return f"""<g clip-path="url(#{prefix}-frame)">
  <rect width="{width}" height="{height}" fill="#05030C"/>
  <rect width="{width}" height="{height}" fill="url(#{prefix}-glow-a)"/>
  <rect width="{width}" height="{height}" fill="url(#{prefix}-glow-b)"/>
  <rect width="{width}" height="{height}" fill="url(#{prefix}-grid)"/>
  <rect width="{width}" height="{height}" fill="url(#{prefix}-dots)"/>
</g>
<rect x="18.5" y="18.5" width="{width - 37}" height="{height - 37}" rx="28" fill="none" stroke="url(#{prefix}-rim)" stroke-width="1.25"/>"""


def svg_doc(prefix: str, width: int, height: int, title: str, desc: str, body: str) -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="{prefix}-title {prefix}-desc">
<title id="{prefix}-title">{esc(title)}</title>
<desc id="{prefix}-desc">{esc(desc)}</desc>
<style><![CDATA[
{font_css()}
]]></style>
{defs(prefix, width, height)}
{chrome(prefix, width, height)}
{body}
</svg>
"""


def icon_group(icons: dict, slug: str, x: float, y: float, size: float) -> str:
    paths, title = icons[slug]
    parts = "".join(f'<path d="{p}" fill="#E8EEF9"/>' for p in paths)
    return f"""<svg x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" viewBox="0 0 24 24" role="img" aria-label="{esc(title)}">
  <title>{esc(title)}</title>
  {parts}
</svg>"""


def on_ellipse(cx, cy, rx, ry, phi, angle):
    p = math.radians(phi)
    t = math.radians(angle)
    x = cx + rx * math.cos(t) * math.cos(p) - ry * math.sin(t) * math.sin(p)
    y = cy + rx * math.cos(t) * math.sin(p) + ry * math.sin(t) * math.cos(p)
    return x, y


def ellipse_path(cx, cy, rx, ry, phi, n=120) -> str:
    pts = [on_ellipse(cx, cy, rx, ry, phi, i * 360 / n) for i in range(n + 1)]
    return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z"


def build_hero(icons_unused, hero_b64: str) -> str:
    roles = [
        "Cybersecurity &amp; Ethical Hacking",
        "Artificial Intelligence &amp; Machine Learning",
        "Digital Forensics",
        "Threat Intelligence &amp; Security Research",
    ]
    role_anim = [
        ('1;1;0;0;1', '0;0.249;0.25;0.999;1', '1'),
        ('0;0;1;1;0;0', '0;0.249;0.25;0.499;0.5;1', '0'),
        ('0;0;1;1;0;0', '0;0.499;0.5;0.749;0.75;1', '0'),
        ('0;0;1;1;0;0', '0;0.749;0.75;0.999;1', '0'),
    ]
    # Fourth keyTimes has 5 values and 5 times — fix to match.
    role_anim[3] = ('0;0;1;1;0', '0;0.749;0.75;0.999;1', '0')
    role_nodes = []
    for text, (values, times, base) in zip(roles, role_anim):
        role_nodes.append(
            f"""<text x="48" y="332" class="mid" font-size="20" opacity="{base}">{text}<animate attributeName="opacity" begin="0s" dur="12s" repeatCount="indefinite" calcMode="discrete" values="{values}" keyTimes="{times}"/></text>"""
        )
    body = f"""
<clipPath id="hx-portrait">
  <rect x="500" y="28" width="432" height="484" rx="26"/>
</clipPath>
<image href="data:image/jpeg;base64,{hero_b64}" x="470" y="28" width="492" height="484" preserveAspectRatio="xMidYMid slice" clip-path="url(#hx-portrait)"/>
<rect x="500.5" y="28.5" width="431" height="483" rx="26" fill="none" stroke="url(#hx-rim)" stroke-width="1.6"/>
<g>
  <text x="48" y="72" class="kicker" font-size="13">BLACK HAT  ·  INFINITY X</text>
  <clipPath id="hx-nameclip">
    <rect x="48" y="96" width="460" height="160">
      <animate attributeName="width" begin="0s" dur="1.05s" fill="freeze" values="0;460" keyTimes="0;1" calcMode="spline" keySplines="0.16 0.84 0.2 1"/>
    </rect>
  </clipPath>
  <g clip-path="url(#hx-nameclip)">
    <text x="48" y="168" class="display" font-size="62">INFINITY</text>
    <text x="48" y="236" class="display" font-size="62" fill="url(#hx-word)">X</text>
  </g>
  <text x="48" y="278" class="kicker" font-size="12">FOCUS</text>
  {''.join(role_nodes)}
  <text x="48" y="392" class="body" font-size="17">A black-hat eye for how systems break.</text>
  <text x="48" y="418" class="body" font-size="17">A builder's hand for what holds.</text>
  <text x="48" y="478" class="mono" font-size="13" fill="#E9D5FF">github.com/Infinity-X202</text>
</g>
"""
    return svg_doc(
        "hx",
        W,
        540,
        "Infinity X hero",
        "Infinity X in a black-hat neon style, with the supplied hooded portrait, the name, and four rotating areas of focus.",
        body,
    )


def build_about() -> str:
    left = [
        ("01", "Security research", "Defensive security and how systems are reviewed."),
        ("02", "Secure software development", "Web and backend software, built with care."),
        ("03", "AI and automation", "Machine learning where it helps a product."),
        ("04", "Digital investigation", "Forensics and threat analysis, as study."),
    ]
    rows = []
    for i, (num, title, line) in enumerate(left):
        y = 148 + i * 86
        rows.append(
            f"""<text x="56" y="{y}" class="kicker" font-size="13">{num}</text>
<text x="108" y="{y}" class="mid" font-size="22">{esc(title)}</text>
<text x="108" y="{y + 28}" class="body" font-size="16">{esc(line)}</text>"""
        )
    panels = [
        (
            "Ethical hacking, as study",
            "Interested in how attacks are understood",
            "so defenses can be designed. Not a claim",
            "of professional testing engagements.",
            "1",
            "1;1;0;0;1",
            "0;0.30;0.333;0.999;1",
        ),
        (
            "AI and machine learning",
            "Experimenting with models and automation,",
            "including a small public language-model",
            "service. Learning, not a lab credential.",
            "0",
            "0;0;1;1;0;0",
            "0;0.30;0.333;0.63;0.666;1",
        ),
        (
            "Forensics and intelligence",
            "Interested in how incidents are reconstructed",
            "and how public threat information is read",
            "without pretending to hold a case load.",
            "0",
            "0;0;1;1;0",
            "0;0.63;0.666;0.999;1",
        ),
    ]
    panel_xml = []
    for title, a, b, c, base, values, times in panels:
        panel_xml.append(
            f"""<g opacity="{base}">
  <animate attributeName="opacity" begin="0s" dur="12s" repeatCount="indefinite" calcMode="discrete" values="{values}" keyTimes="{times}"/>
  <text x="528" y="230" class="mid" font-size="26">{esc(title)}</text>
  <text x="528" y="278" class="body" font-size="16">{esc(a)}</text>
  <text x="528" y="304" class="body" font-size="16">{esc(b)}</text>
  <text x="528" y="330" class="body" font-size="16">{esc(c)}</text>
  <text x="528" y="390" class="mono" font-size="12">BLACK HAT  ·  FIELD OF STUDY</text>
</g>"""
        )
    bars = [
        (524, "118", "0;118;0;0", "0;0.333;0.334;1"),
        (660, "0", "0;0;118;0;0", "0;0.333;0.666;0.667;1"),
        (796, "0", "0;0;118", "0;0.666;1"),
    ]
    bar_xml = []
    for x, base, values, times in bars:
        bar_xml.append(
            f"""<rect x="{x}" y="168" width="118" height="4" rx="2" fill="#1C2740"/>
<rect x="{x}" y="168" width="{base}" height="4" rx="2" fill="#247BFF">
  <animate attributeName="width" begin="0s" dur="12s" repeatCount="indefinite" values="{values}" keyTimes="{times}"/>
</rect>"""
        )
    body = f"""
<text x="56" y="78" class="kicker" font-size="13">ABOUT  ·  AREAS OF FOCUS</text>
<text x="56" y="118" class="display" font-size="32">What I spend time on</text>
{''.join(rows)}
<rect x="504" y="132" width="408" height="300" rx="22" fill="#0C1322" stroke="url(#al-rim)" stroke-width="1.15"/>
<text x="528" y="160" class="kicker" font-size="12">INTERESTS  ·  4S</text>
{''.join(bar_xml)}
{''.join(panel_xml)}
"""
    return svg_doc(
        "al",
        W,
        500,
        "About Infinity X",
        "Two columns. The left lists four areas of focus. The right cycles three interest panels every four seconds.",
        body,
    )


def build_stack(icons: dict) -> str:
    # Three separate lanes. Icons are spaced on a fixed grid so labels cannot collide.
    xs = [176, 384, 592, 800]
    lanes = [
        ("st-orbit-a", 214, "#247BFF", 0.8, "16s", [
            ("python", "Python"),
            ("javascript", "JavaScript"),
            ("typescript", "TypeScript"),
            ("gnubash", "Bash"),
        ]),
        ("st-orbit-b", 324, "#9DB7DE", 0.7, "20s", [
            ("linux", "Linux"),
            ("windows", "Windows"),
            ("git", "Git"),
            ("github", "GitHub"),
        ]),
        ("st-orbit-c", 434, "#FF354F", 0.55, "24s", [
            ("react", "React"),
            ("nextdotjs", "Next.js"),
            ("fastapi", "FastAPI"),
            ("pytorch", "PyTorch"),
        ]),
    ]
    orbit_xml = []
    icon_xml = []
    centers = []
    for pid, cy, color, opacity, dur, items in lanes:
        d = ellipse_path(488, cy, 340, 14, -3)
        start = on_ellipse(488, cy, 340, 14, -3, 0)
        orbit_xml.append(
            f"""<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-opacity="{opacity}" stroke-width="1.25" stroke-dasharray="3 9">
  <animate attributeName="stroke-dashoffset" begin="0s" dur="{dur}" repeatCount="indefinite" values="0;-180" keyTimes="0;1"/>
</path>
<circle cx="{start[0]:.1f}" cy="{start[1]:.1f}" r="3.2" fill="{color}"/>
<circle cx="0" cy="0" r="4" fill="{color}" opacity="0">
  <animate attributeName="opacity" begin="0s" dur="0.01s" fill="freeze" values="0;1" keyTimes="0;1"/>
  <animateMotion begin="0s" dur="{dur}" repeatCount="indefinite" rotate="0" calcMode="linear">
    <mpath href="#{pid}" xlink:href="#{pid}"/>
  </animateMotion>
</circle>"""
        )
        for x, (slug, label) in zip(xs, items):
            centers.append((x, cy, label))
            icon_xml.append(
                f"""<g>
  <rect x="{x - 24:.1f}" y="{cy - 24:.1f}" width="48" height="48" rx="14" fill="#10182A" stroke="#243049" stroke-width="1"/>
  {icon_group(icons, slug, x - 13, cy - 18, 26)}
  <text x="{x:.1f}" y="{cy + 46:.1f}" text-anchor="middle" class="mono" font-size="13" fill="#F4F7FF">{esc(label)}</text>
</g>"""
            )
    for i, (x1, y1, lab1) in enumerate(centers):
        for x2, y2, lab2 in centers[i + 1 :]:
            dist = math.hypot(x1 - x2, y1 - y2)
            if dist < 96:
                raise SystemExit(f"Icon collision {lab1} / {lab2} dist={dist:.1f}")
    chips = """
<g>
  <rect x="40" y="508" width="880" height="168" rx="18" fill="#0C1322" stroke="#243049"/>
  <text x="64" y="542" class="kicker" font-size="12">PROGRAMMING</text>
  <text x="64" y="570" class="mid" font-size="16">Python · JavaScript · TypeScript · Bash</text>
  <text x="64" y="608" class="kicker" font-size="12">SYSTEMS</text>
  <text x="64" y="636" class="mid" font-size="16">Linux · Windows</text>

  <text x="430" y="542" class="kicker" font-size="12">DEVELOPMENT</text>
  <text x="430" y="570" class="mid" font-size="16">Git · GitHub</text>
  <text x="430" y="608" class="kicker" font-size="12">WEB</text>
  <text x="430" y="636" class="mid" font-size="16">React · Next.js · Tailwind CSS</text>

  <text x="700" y="542" class="kicker" font-size="12">AI IN PUBLIC CODE</text>
  <text x="700" y="570" class="mid" font-size="16">FastAPI · PyTorch</text>
  <text x="700" y="608" class="kicker" font-size="12">SECURITY INTERESTS</text>
  <text x="700" y="636" class="mid" font-size="16">Defense · Investigation</text>
</g>
"""
    body = f"""
<text x="48" y="72" class="kicker" font-size="13">TECHNOLOGY</text>
<text x="48" y="112" class="display" font-size="32">Stack in public work</text>
<text x="48" y="146" class="body" font-size="16">Icons name tools. They are not certifications or expertise claims.</text>
{''.join(orbit_xml)}
{''.join(icon_xml)}
{chips}
"""
    return svg_doc(
        "st",
        W,
        704,
        "Infinity X technology stack",
        "Three elliptical orbits with labelled technology icons and grouped chips for programming, systems, development, web, AI, and security interests.",
        body,
    )


def barcode() -> str:
    # Decorative widths only. This pattern is not derived from a name or URL.
    widths = [2, 1, 3, 1, 2, 2, 1, 4, 1, 2, 1, 3, 2, 1, 1, 2, 4, 1, 2, 1, 3, 1, 2, 2, 1, 3, 1, 2, 1, 4, 2, 1]
    x = 0
    parts = []
    for i, w in enumerate(widths):
        if i % 2 == 0:
            parts.append(f'<rect x="{x}" y="0" width="{w}" height="46" fill="#F4F7FF"/>')
        x += w + 1
    return f'<g transform="translate(392 470)">{"".join(parts)}</g>'


def build_id(id_b64: str) -> str:
    body = f"""
<text x="48" y="64" class="kicker" font-size="13">PROFILE CARD</text>
<text x="48" y="100" class="display" font-size="28">Identification</text>
<text x="48" y="132" class="body" font-size="15">Only facts already public on the GitHub profile.</text>
<g id="ixcard-swing">
  <animateTransform attributeName="transform" type="translate" additive="sum" begin="0s" dur="1.15s" fill="freeze" values="0 -34;0 6;0 0" keyTimes="0;0.72;1" calcMode="spline" keySplines="0.22 0.8 0.2 1;0.3 0 0.2 1"/>
  <animateTransform attributeName="transform" type="rotate" additive="sum" begin="1.15s" dur="2.4s" fill="freeze" values="-4.2 480 78;1.7 480 78;-1.2 480 78;0.5 480 78;0 480 78" keyTimes="0;0.28;0.52;0.75;1" calcMode="spline" keySplines="0.3 0 0.2 1;0.3 0 0.2 1;0.3 0 0.2 1;0.3 0 0.2 1"/>
  <animateTransform attributeName="transform" type="rotate" additive="sum" begin="3.55s" dur="3.6s" repeatCount="indefinite" values="-1.7 480 78;1.7 480 78;-1.7 480 78" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>
  <circle cx="480" cy="78" r="11" fill="#070B16" stroke="#C5CEDD" stroke-width="3"/>
  <circle cx="480" cy="78" r="3.5" fill="#E7EDF7"/>
  <path d="M480 78 C480 130 404 150 404 188" fill="none" stroke="url(#ixcard-metal)" stroke-width="5" stroke-linecap="round"/>
  <path d="M480 78 C480 130 556 150 556 188" fill="none" stroke="url(#ixcard-metal)" stroke-width="5" stroke-linecap="round"/>
  <rect x="352" y="196" width="256" height="392" rx="18" fill="#10182A" stroke="url(#ixcard-rim)" stroke-width="1.25"/>
  <clipPath id="ixcard-foil-clip">
    <rect x="352" y="196" width="256" height="392" rx="18"/>
  </clipPath>
  <g clip-path="url(#ixcard-foil-clip)">
    <rect x="250" y="196" width="70" height="392" fill="#F4F7FF" opacity="0.09" transform="skewX(-18)">
      <animate attributeName="x" begin="0s" dur="7s" repeatCount="indefinite" values="-180;-180;460;460" keyTimes="0;0.55;0.75;1"/>
    </rect>
  </g>
  <circle cx="404" cy="214" r="5" fill="none" stroke="#8E9BB3" stroke-width="1.5"/>
  <circle cx="556" cy="214" r="5" fill="none" stroke="#8E9BB3" stroke-width="1.5"/>
  <clipPath id="ixcard-face">
    <circle cx="480" cy="292" r="58"/>
  </clipPath>
  <circle cx="480" cy="292" r="60" fill="#0B0614" stroke="url(#ixcard-word)" stroke-width="2"/>
  <image href="data:image/jpeg;base64,{id_b64}" x="420" y="232" width="120" height="120" clip-path="url(#ixcard-face)" preserveAspectRatio="xMidYMid slice"/>
  <text x="480" y="368" text-anchor="middle" class="kicker" font-size="11">INFINITY X</text>
  <text x="480" y="396" text-anchor="middle" class="mid" font-size="20">Adil Fayyaz</text>
  <text x="480" y="422" text-anchor="middle" class="body" font-size="13">Security · AI · Software</text>
  <text x="480" y="452" text-anchor="middle" class="mono" font-size="11">github.com/Infinity-X202</text>
  {barcode()}
  <text x="480" y="536" text-anchor="middle" class="mono" font-size="10" fill="#A7B2C8">DECORATIVE  ·  NOT AN ID NUMBER</text>
  <text x="480" y="562" text-anchor="middle" class="mono" font-size="11">Since April 2025</text>
</g>
<g>
  <rect x="466" y="16" width="28" height="16" rx="3" fill="url(#ixcard-metal)"/>
  <rect x="474" y="28" width="12" height="70" rx="3" fill="url(#ixcard-metal)"/>
</g>
<text x="680" y="250" class="kicker" font-size="12">ON RECORD</text>
<text x="680" y="286" class="mid" font-size="18">Public profile name</text>
<text x="680" y="312" class="body" font-size="15">Adil Fayyaz</text>
<text x="680" y="352" class="mid" font-size="18">Display name</text>
<text x="680" y="378" class="body" font-size="15">InfinityX</text>
<text x="680" y="418" class="mid" font-size="18">No employer listed</text>
<text x="680" y="444" class="body" font-size="15">No certification claimed</text>
"""
    return svg_doc(
        "ixcard",
        W,
        660,
        "Infinity X identification card",
        "A hanging profile card with a metal clasp, monogram, public name, GitHub handle, decorative barcode, and a short swing.",
        body,
    )


def build_connect(point_b64: str) -> str:
    body = f"""
<text x="48" y="70" class="kicker" font-size="13">CONNECT</text>
<text x="48" y="108" class="display" font-size="32">Find Infinity X</text>
<clipPath id="cn-portrait">
  <rect x="36" y="128" width="360" height="320" rx="24"/>
</clipPath>
<image href="data:image/jpeg;base64,{point_b64}" x="16" y="128" width="400" height="320" preserveAspectRatio="xMidYMid slice" clip-path="url(#cn-portrait)"/>
<rect x="36.5" y="128.5" width="359" height="319" rx="24" fill="none" stroke="url(#cn-rim)" stroke-width="1.4"/>
<g>
  <animateTransform attributeName="transform" type="translate" additive="sum" begin="0s" dur="2.2s" repeatCount="indefinite" values="0 0;8 0;0 0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>
  <path d="M412 288 H500" stroke="#7DD3FC" stroke-width="1.6"/>
  <path d="M488 276 L508 288 L488 300" fill="none" stroke="#E879F9" stroke-width="1.6"/>
</g>
<rect x="548" y="168" width="364" height="196" rx="20" fill="#0C1322" stroke="url(#cn-rim)" stroke-width="1.2"/>
<rect x="576" y="196" width="44" height="44" rx="12" fill="#10182A" stroke="#243049"/>
<svg x="586" y="206" width="24" height="24" viewBox="0 0 24 24" aria-label="GitHub">
  <title>GitHub</title>
  <path fill="#E8EEF9" d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>
</svg>
<text x="636" y="214" class="kicker" font-size="12">GITHUB</text>
<text x="576" y="278" class="display" font-size="28">Infinity-X202</text>
<text x="576" y="314" class="body" font-size="15">The public profile and repositories.</text>
<text x="576" y="344" class="mono" font-size="13" fill="#F4F7FF">github.com/Infinity-X202</text>
<text x="548" y="408" class="mono" font-size="12">Other networks are omitted until a URL is confirmed.</text>
<text x="548" y="450" class="body" font-size="14">The card above is not a link. Use the README links.</text>
"""
    return svg_doc(
        "cn",
        W,
        500,
        "Connect with Infinity X",
        "A pointing monogram on the left and a GitHub card on the right. The only confirmed public profile URL is github.com/Infinity-X202.",
        body,
    )


def write_preview(svg_names: list[str]) -> None:
    imgs = "\n".join(
        f'<figure><img src="assets/{name}?v=1" alt="{name}"><figcaption>{name} via img</figcaption></figure>'
        for name in svg_names
    )
    mobile = "\n".join(f'<img src="assets/{name}?v=1" alt="">' for name in svg_names)
    inlined = []
    for name in svg_names:
        raw = (ASSETS / name).read_text(encoding="utf-8")
        raw = raw.replace('<?xml version="1.0" encoding="UTF-8"?>', "")
        inlined.append(f'<div class="inline-wrap" data-file="{name}">{raw}</div>')
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Infinity X profile preview</title>
  <style>
    :root {{ color-scheme: dark; }}
    body {{ margin: 0; background: #070B16; color: #F4F7FF; font: 16px/1.5 "Segoe UI", sans-serif; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 32px 20px 80px; }}
    h1 {{ font-weight: 650; letter-spacing: -0.03em; }}
    h2 {{ margin-top: 48px; font-size: 1.2rem; }}
    p {{ color: #A7B2C8; max-width: 68ch; }}
    figure {{ margin: 20px 0 32px; }}
    img, .inline-wrap svg {{ width: 100%; height: auto; display: block; }}
    figcaption {{ color: #A7B2C8; font-size: 13px; margin-top: 8px; }}
    .mobile {{ width: 360px; max-width: 100%; border: 1px solid #243049; padding: 8px; }}
    button {{ background: #10182A; color: #F4F7FF; border: 1px solid #247BFF; border-radius: 8px; padding: 8px 12px; margin: 0 8px 8px 0; cursor: pointer; }}
    .note {{ font-size: 14px; }}
  </style>
</head>
<body>
<main>
  <h1>Infinity X — local preview</h1>
  <p>This page is for review. GitHub will show the files under “Image embedding”, which is how a profile README loads SVG.</p>
  <h2>Image embedding</h2>
  {imgs}
  <h2>Mobile width (360px, via img)</h2>
  <div class="mobile">
    {mobile}
  </div>
  <h2>Inline SVG timing</h2>
  <p class="note">These copies are in the page so a browser can seek SMIL. Use the buttons, then inspect the frozen frame. GitHub does not promise the same motion.</p>
  <p>
    <button type="button" data-t="0">0s</button>
    <button type="button" data-t="2">2s</button>
    <button type="button" data-t="5">5s</button>
    <button type="button" data-t="9">9s</button>
    <button type="button" data-t="13">13s</button>
    <button type="button" id="play">Play</button>
    <button type="button" id="still">Animation off</button>
  </p>
  {''.join(inlined)}
</main>
<script>
const svgs = () => Array.from(document.querySelectorAll('.inline-wrap svg'));
function seek(t) {{
  svgs().forEach((svg) => {{
    if (svg.dataset.backup) svg.innerHTML = svg.dataset.backup;
    if (typeof svg.setCurrentTime === 'function') {{
      svg.setCurrentTime(t);
      svg.pauseAnimations();
    }}
  }});
}}
document.querySelectorAll('button[data-t]').forEach((btn) => {{
  btn.addEventListener('click', () => seek(Number(btn.dataset.t)));
}});
document.getElementById('play').addEventListener('click', () => {{
  svgs().forEach((svg) => {{
    if (svg.dataset.backup) svg.innerHTML = svg.dataset.backup;
    svg.unpauseAnimations();
  }});
}});
document.getElementById('still').addEventListener('click', () => {{
  svgs().forEach((svg) => {{
    if (!svg.dataset.backup) svg.dataset.backup = svg.innerHTML;
    svg.querySelectorAll('animate, animateTransform, animateMotion').forEach((n) => n.remove());
  }});
}});
const params = new URLSearchParams(location.search);
if (params.has('t')) seek(Number(params.get('t')));
if (params.get('still') === '1') document.getElementById('still').click();
</script>
</body>
</html>
"""
    (ROOT / "preview.html").write_text(html, encoding="utf-8")


def validate(files: list[Path]) -> None:
    for path in files:
        text = path.read_text(encoding="utf-8")
        if "<script" in text.lower() or "<foreignObject" in text:
            raise SystemExit(f"Forbidden element in {path.name}")
        allowed = ("http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink")
        for url in re.findall(r"https?://[^\"'\s<)]+", text):
            if url not in allowed:
                raise SystemExit(f"External URL in {path.name}: {url}")
        ET.fromstring(text)
        ids = re.findall(r'\bid="([^"]+)"', text)
        dupes = {i for i in ids if ids.count(i) > 1}
        if dupes:
            raise SystemExit(f"Duplicate ids in {path.name}: {dupes}")
        if 'viewBox="' not in text:
            raise SystemExit(f"Missing viewBox in {path.name}")
        print(f"OK {path.name}  {path.stat().st_size} bytes  ids={len(ids)}")


def main() -> None:
    hero_b64, face_b64 = make_portraits()
    icons = load_icons()
    id_b64 = face_b64
    point_b64 = hero_b64
    docs = {
        "hero.svg": build_hero(icons, hero_b64),
        "about-life.svg": build_about(),
        "stack.svg": build_stack(icons),
        "id-dashboard.svg": build_id(id_b64),
        "connect.svg": build_connect(point_b64),
    }
    paths = []
    for name, text in docs.items():
        path = ASSETS / name
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    validate(paths)
    write_preview(list(docs))
    for name in ("id.png", "right_pointing.png"):
        im = Image.open(ASSETS / name)
        print(name, im.mode, im.size)


if __name__ == "__main__":
    main()
