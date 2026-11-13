import re
import sys
import urllib.request
from datetime import datetime

USER = "Valenciavm"
URL = f"https://github.com/users/{USER}/contributions"
OUT = "contributions.svg"

BG = "#000000"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
TEXT = "#8b949e"
CELL, GAP = 11, 3
PITCH = CELL + GAP
LEFT, TOP = 34, 30

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")

days = re.findall(
    r'data-date="([\d-]+)"\s+id="contribution-day-component-(\d+)-(\d+)"[^>]*data-level="(\d)"', html
)
if not days:
    sys.exit("No se encontraron datos de contribuciones.")

m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
total = m.group(1) if m else ""

cols = max(int(c) for _, _, c, _ in days) + 1
width = LEFT + cols * PITCH + 16
height = TOP + 7 * PITCH + 34

out = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="GitHub contributions of {USER}">',
    f'<rect width="{width}" height="{height}" rx="8" fill="{BG}"/>',
]

if total:
    out.append(
        f'<text x="{LEFT}" y="18" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="12">{total} contributions in the last year</text>'
    )

for label, row in (("Mon", 1), ("Wed", 3), ("Fri", 5)):
    out.append(
        f'<text x="4" y="{TOP + row * PITCH + 9}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="9">{label}</text>'
    )

last_month = None
for date, row, col, level in days:
    row, col, level = int(row), int(col), int(level)
    x, y = LEFT + col * PITCH, TOP + row * PITCH
    out.append(
        f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{LEVELS[level]}"><title>{date}</title></rect>'
    )
    if row == 0:
        month = datetime.strptime(date, "%Y-%m-%d").strftime("%b")
        if month != last_month:
            out.append(
                f'<text x="{x}" y="{TOP - 4}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="9">{month}</text>'
            )
            last_month = month

# leyenda
lx = width - 16 - 5 * PITCH - 60
ly = height - 14
out.append(f'<text x="{lx}" y="{ly + 9}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="9">Less</text>')
for i, c in enumerate(LEVELS):
    out.append(f'<rect x="{lx + 26 + i * PITCH}" y="{ly}" width="{CELL}" height="{CELL}" rx="2" fill="{c}"/>')
out.append(f'<text x="{lx + 30 + 5 * PITCH}" y="{ly + 9}" fill="{TEXT}" font-family="Segoe UI, Arial, sans-serif" font-size="9">More</text>')
out.append("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"OK: {len(days)} días, total: {total}")
