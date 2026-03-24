# Astronomer 2026 Brand Guidelines

## Colors

### Primary Palette

| Name | Hex | Use |
|------|-----|-----|
| New Moon 80 | `#343247` | Primary dark background |
| New Moon 70 | `#555261` | Secondary dark, body text on light |
| Purple 60 | `#872DED` | Accent, links/CTAs on light bg |
| Gold 40 | `#FFB32D` | Accent, links/CTAs on dark bg |
| New Moon 10 | `#F0ECE5` | Light background, body text on dark |

### Supporting Colors

| Name | Hex | Use |
|------|-----|-----|
| Red 50 | `#F03A47` | Alerts, emphasis |
| Blue 50 | `#2676FF` | Data, technical |
| Green 50 | `#19BA5A` | Success, positive metrics |
| Teal 50 | `#13BDD7` | Data pipelines, integrations |

### Logo Colors
- On light backgrounds: `#2B215B` (deep purple)
- On dark backgrounds: `#FFFFFF` (white)

---

## Dark Mode Rules

Use for: title slide, closing slide, CTA slide, section dividers.

| Element | Color |
|---------|-------|
| Background | New Moon 80 `#343247` or New Moon 70 `#555261` |
| Slide title | White `#FFFFFF` |
| Eyebrow / label | Gold 40 `#FFB32D` |
| Body copy | New Moon 10 `#F0ECE5` |
| Accent / CTA / links | Gold 40 `#FFB32D` |
| Decorative shapes | New Moon 70 `#555261` or Purple 60 `#872DED` |

---

## Light Mode Rules

Use for: content slides, feature slides, data slides.

| Element | Color |
|---------|-------|
| Background | White `#FFFFFF` or New Moon 10 `#F0ECE5` |
| Slide title | New Moon 80 `#343247` |
| Eyebrow / label | Purple 60 `#872DED` |
| Body copy | New Moon 70 `#555261` |
| Accent / CTA / links | Purple 60 `#872DED` |
| Decorative shapes | New Moon 10 `#F0ECE5` or Purple 60 `#872DED` |

---

## Typography

### Fonts (all from the brand PPTX, all available on Google Fonts)

| Font | Use | Google Fonts URL |
|------|-----|-----------------|
| **League Gothic** | ALL headers and titles — default font | https://fonts.google.com/specimen/League+Gothic |
| **Roboto** | Body copy and paragraphs | https://fonts.google.com/specimen/Roboto |
| **Roboto Mono** | Eyebrows, labels, captions, code | https://fonts.google.com/specimen/Roboto+Mono |

These are the three canonical brand fonts. Do not use Inter, Albert Sans, or any other font
unless the user explicitly requests it.

### Font Sizes

| Element | Font | Size | Notes |
|---------|------|------|-------|
| Slide title | League Gothic | 40–48pt | League Gothic has no bold variant — weight comes from the letterform |
| Section header | League Gothic | 28–36pt | |
| Eyebrow / label | Roboto Mono | 9–11pt | ALL CAPS |
| Body text | Roboto | 13–15pt | Regular |
| Stat callout number | League Gothic | 60–72pt | |
| Caption / fine print | Roboto | 10–11pt | Muted color |
| Code / DAG names | Roboto Mono | 11–13pt | |

---

## Writing Style

- **Sentence case with punctuation** for all headers longer than 4 words.
  - Good: "The future of data orchestration is here."
  - Good: "Why Astronomer?"  ← under 4 words, Title Case OK, no punctuation
- **Oxford comma** required.
- Tone: professional, confident, data-forward. Avoid buzzwords and filler.
- Never use exclamation points in headers.

---

## Logo Rules

- Clear space: use the "A" rule — minimum padding equal to the height of the "A" in "Astronomer"
- One color only: never two-tone or gradient
- Approved colors: `#2B215B` on light, `#FFFFFF` on dark
- Never stretch, rotate, add shadow, or change color
- Never place on busy backgrounds or photography
- Never use the icon and wordmark together on the same slide

---

## Design Elements

These are the visual motifs from the Astronomer brand. Use them as decorative elements,
not as literal images (since we're building programmatically with python-pptx shapes).

- **Space Math / Grid**: Use evenly-spaced lines or dot grids as subtle background texture
- **Orbits**: Arc and circle shapes in New Moon colors — great for title slide backgrounds
- **Textures**: Semi-transparent rectangle overlays to add depth
- **Iconography**: Simple line-style icons (use text characters or Unicode symbols as proxies)
- **ASCII graphics**: For technical/architecture slides, monospaced text art works well

### python-pptx: Creating Orbit decorative elements
```python
from pptx.util import Inches, Pt, Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE
import pptx.oxml.ns as nsmap
from lxml import etree

# Add a circle arc as orbit decoration
# Use MSO_SHAPE.OVAL for full circles, adjust size/position for partial overlap effect
from pptx.util import Inches
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR

def add_orbit_circle(slide, left, top, width, height, color_hex, line_width_pt=1.5, fill=False):
    shape = slide.shapes.add_shape(
        1,  # MSO_SHAPE_TYPE.OVAL = 9, but add_shape uses autoshape type. Use 9 for oval.
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.line.color.rgb = RGBColor.from_string(color_hex.lstrip('#'))
    shape.line.width = Pt(line_width_pt)
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor.from_string(color_hex.lstrip('#'))
    else:
        shape.fill.background()
    return shape
```

---

## python-pptx: Text box with eyebrow + title pattern

This is the core pattern for most slides:

```python
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

def add_eyebrow_title(slide, eyebrow_text, title_text, left, top, width,
                       eyebrow_color, title_color, dark_mode=False):
    # Eyebrow
    tb_eye = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.4))
    tf_eye = tb_eye.text_frame
    tf_eye.word_wrap = False
    p_eye = tf_eye.paragraphs[0]
    run_eye = p_eye.add_run()
    run_eye.text = eyebrow_text.upper()
    run_eye.font.name = "Roboto Mono"
    run_eye.font.size = Pt(10)
    run_eye.font.color.rgb = RGBColor.from_string(eyebrow_color.lstrip('#'))

    # Title
    tb_title = slide.shapes.add_textbox(Inches(left), Inches(top + 0.45), Inches(width), Inches(1.5))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    run_title = p_title.add_run()
    run_title.text = title_text
    run_title.font.name = "League Gothic"
    run_title.font.size = Pt(44)
    run_title.font.color.rgb = RGBColor.from_string(title_color.lstrip('#'))
```
