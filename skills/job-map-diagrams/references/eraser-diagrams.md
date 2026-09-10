# Eraser Diagrams implementation notes

This skill targets the open-source JSON format in [eraserlabs/eraser-diagrams](https://github.com/eraserlabs/eraser-diagrams), not Eraser's earlier diagram DSL or hosted rendering API.

The generated document uses:

- `Shape` entities for stage cards and separate proportional time or funnel bars;
- stock `Shape` fill and dashed-border properties to distinguish stages where more than half of the work occurs outside the product;
- plain `Textbox` entities for the consistently left-aligned Plan, Do, and Review headings;
- Eraser catalog SVG `Icon` entities paired with `Textbox` labels to form each card's title row;
- Markdown text runs for headings, durations, bullet lists, and evidence links;
- `Relationship` connections from each stage bar's bottom midpoint to its card's top midpoint, styled as thin light-gray lines without arrowheads;
- a fixed card width with no authored card height, allowing browser measurement to size each card to its content;
- two restrained card text styles: an unbolded stage title and one regular body style shared by activities and sources;
- a transparent final text run that creates consistent measured bottom padding without fixing card height;
- non-negative integer coordinates and unique entity IDs;
- both required top-level arrays: `entities` and `connections`.

Install and validate with Node.js 22.12 or newer:

```bash
npm install -D @eraserlabs/diagrams-cli
npx eraser-diagrams validate path/to/job-map-diagram.json --fail-on-warning
```

Render when a Chromium-family browser is available:

```bash
npx eraser-diagrams render path/to/job-map-diagram.json -o path/to/job-map-diagram.png --scale 2
```

Authoritative references:

- [Getting Started](https://github.com/eraserlabs/eraser-diagrams/blob/main/GETTING_STARTED.md)
- [Repository](https://github.com/eraserlabs/eraser-diagrams)

For watercolor output, use the workspace Python runtime with Pillow to trim renderer-added whitespace after rendering:

```bash
python3 scripts/crop_render.py path/to/job-map-diagram.png --padding 24
```

Because rendered dimensions depend on font measurement, inspect every preview. If a card overflows, shorten the activity wording before changing the shared layout.
