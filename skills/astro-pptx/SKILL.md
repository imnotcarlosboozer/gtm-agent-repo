---
name: astro-pptx
description: >
  Creates branded Astronomer PowerPoint presentations (.pptx) following the 2026 Astronomer Brand
  Guidelines. Use this skill whenever the user asks to make a slide deck, PowerPoint, presentation,
  or PPTX — especially for sales decks, customer-facing materials, prospect decks, QBRs, pitch decks,
  demo decks, or internal Astronomer presentations. Also trigger when the user says things like "make
  me a deck about X", "put together some slides for Y", "build a presentation for [account]", or
  "I have a meeting with [company] and need slides." Always save output to ~/Downloads/. Always run
  visual QA before declaring done.
---

# Astro PPTX

You're creating a branded Astronomer PowerPoint. The output must feel like it came from Astronomer's
marketing team — polished, on-brand, and ready to send to a customer.

## Step 1: Gather requirements

Ask the user these questions upfront in a single message:

1. **Mode**: Dark mode, light mode, or mixed (dark title/closing, light content slides)?
   Default to mixed if not specified.
2. **Title & purpose**: What's the deck title, and who's the audience?
   (e.g., "intro demo for Acme Corp's data engineering team")
3. **Specific slides or content**: Any sections or slides they definitely want?
   You'll fill the rest with good judgment.

Don't write a single line of code until you have at least the title and purpose.

---

## Step 2: Plan the slide structure

For sales/customer-facing decks, adapt this structure to the situation. Use judgment —
not every deck needs every slide.

| # | Slide | Mode |
|---|-------|------|
| 1 | Title (deck title, audience/account, date) | Dark |
| 2 | Agenda | Light |
| 3 | About Astronomer | Light |
| 4 | The problem / challenge | Light |
| 5 | The Astronomer platform | Light |
| 6 | How it works / architecture | Light |
| 7 | Key features or use cases (2–3) | Light |
| 8 | Customer proof / logos | Light |
| 9 | Next steps / CTA | Dark |
| 10 | Thank you + contact | Dark |

---

## Step 3: Build the deck with python-pptx

Install if needed:
```bash
python3 -m pip install python-pptx -q
# macOS with Homebrew Python: python3 -m pip install python-pptx --break-system-packages -q
```

Read `references/brand.md` before writing any code — it has all hex values, font names,
dark/light mode rules, and layout patterns.

If the user has provided a brand guidelines PPTX, you can also read it directly for additional context:
```bash
python3 -m markitdown "<path-to-brand-guidelines.pptx>"
```

### Slide setup
```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)
```

### Font notes
- **League Gothic** is the default headline font (Google Fonts: https://fonts.google.com/specimen/League+Gothic)
- All fonts are embedded by name in the XML — PowerPoint and Google Slides will render them
  correctly on machines where the fonts are installed. On machines without them, they'll
  substitute, which is expected behavior.
- Never fall back to Arial or Calibri for headlines. Keep League Gothic in the XML regardless.

### Every slide must have a visual element
Never produce a plain white slide with just text. Use at least one of:
- A colored header band or footer bar
- A background color fill (dark or light)
- Decorative arc/circle shapes (Orbit motif)
- A colored left column or side accent strip
- Icon placeholder shapes in brand colors

### Layout variety
Don't repeat the same layout on consecutive slides. `references/brand.md` has 8 named layouts
with exact specs — use them as your primary vocabulary. Quick reference:

| Layout | Best for |
|--------|----------|
| Gold top stripe | Almost every slide — thin brand header |
| Big statement (full purple bg) | Thesis, mission, bold section openers |
| Split: dark col left + card grid right | System overviews, feature breakdowns |
| Before / After split | Problem → solution, old vs. new |
| Giant stat left + content right | Key metrics, proof points |
| Dark callout on light bg | Examples, output callouts |
| 2×3 roadmap grid | What's next, feature roadmaps |
| Use case (numbered) | Use case walkthroughs, process flows |

A real example deck lives at `assets/all-hands-example.pptx` — read it for design inspiration.

---

## Step 4: Save and QA

Save to `~/Downloads/<deck-slug>.pptx` (kebab-case, descriptive name).

Visual QA is required. Convert to images and inspect:

```bash
cd ~/Downloads
# Convert to PDF with LibreOffice (install: brew install libreoffice)
soffice --headless --convert-to pdf <filename>.pptx

# Convert PDF to JPEG slides (install: brew install poppler)
pdftoppm -jpeg -r 150 <filename>.pdf slide
```

Inspect every slide image. Look for:
- Text cut off or overflowing its box
- Overlapping elements
- Low contrast (light text on light bg, or dark text on dark bg)
- Leftover placeholder text (`[COMPANY]`, `xxxx`, `lorem`, etc.)
- Inconsistent margins

Fix anything found, re-render, and re-check. Do not declare done until a full pass is clean.

---

## Step 5: Report

Tell the user:
- Full path to the saved file
- Brief summary of slides and design decisions
- Note if any fonts require installation for full fidelity (League Gothic, Roboto, Roboto Mono)

---

## Reference

| File | Contents | When to read |
|------|----------|--------------|
| `references/brand.md` | Colors, fonts, dark/light rules, layouts, logo rules | Always — before writing any code |
| `references/messaging.md` | Core positioning, stats, proof points, customer stories, narrative arcs, persona guide | For sales/customer-facing decks, or whenever you need accurate Astronomer claims |
