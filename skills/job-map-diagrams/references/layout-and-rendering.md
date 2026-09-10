# Layout and rendering

Read this reference when generating or visually revising an Eraser job-map artifact.

## Composition

- Each displayed state contains three rows with fixed membership:
  - Plan: Define, Locate, Prepare, Confirm
  - Do: Execute, Monitor
  - Review: Modify, Conclude
- A single-state diagram shows one complete map. A comparison stacks Status Quo above After and gives both prominent state headings.
- Use one shared bar scale across every displayed state so equal values have equal widths. Calculate each state's total separately.
- Align every phase title, bar row, and first card to the Plan row's left edge. Keep the four Plan cards evenly spaced. Place the two Do cards and two Review cards as left-aligned adjacent pairs.

## Metric bars

- Replace continuous timelines and numbered nodes with one separate horizontal bar per stage: four for Plan, two for Do, and two for Review.
- In time mode, width represents elapsed duration.
- In funnel mode, width represents the stage's conditional drop-off rate. A longer bar signals greater loss. Funnel phase totals and the sum across stages may exceed 100%.
- Derive a common scale from the largest displayed phase total. The longest phase fills the available width; shorter phases stop proportionally earlier.
- Use 18px-high bars with a small gap between stages and 28px of visible space from the bar's lower edge to its cards.
- Draw a thin, light-gray, arrowless connector from the midpoint beneath each bar to the midpoint at the top of its corresponding card. Keep connectors visually subordinate to both bars and cards.
- Keep the lane color on every bar. Add a subtle, lighter diagonal texture when `outside_product_percent` is greater than 50; leave the bar solid at 50 or below.
- Include a compact legend beneath the header explaining solid as mostly in-product and textured as mostly outside-product.

## Content-aware vertical placement

- Estimate the tallest card in each lane from its rendered text width, wrapped activity lines, source labels, and bottom clearance.
- Position the following lane from that estimated height rather than fixed absolute lane coordinates.
- Position each `Total:` line below the tallest Review card, then position the next comparison state from the preceding total. This prevents longer cards from colliding with later sections.
- Eraser ultimately measures auto-height cards in the browser, so inspect the rendered preview. If the estimate leaves too little clearance, fix the estimator or shorten overly verbose content; do not add a one-off absolute offset for a specific example.

## Cards and labels

- Put each Plan, Do, or Review label on its own row closely above the bar. Render state and phase labels as large, left-aligned black text on white—not colored cards.
- Plan cards are 320px wide. Do and Review cards are 480px wide. Omit authored card heights so Eraser sizes cards to content.
- Put a small semantic Eraser SVG icon and unbolded stage title on the first row. Use the stage name without its sequence number.
- Put `Time:` or `Drop-off:` directly beneath the title, then `Outside product:` with the exact percentage. Follow with one to five literal bullet glyphs and a Sources line. Separate Sources from activities by one blank line.
- Render activities and Sources in one visible text block at the same 24px left inset. Keep a modest fixed bottom inset beneath Sources without vertically redistributing content.
- Use invisible text copies inside each card only for auto-height measurement.

## Typography and color

- Use Eraser's `rough` typeface for the map title, state headings, phase labels, card titles, and totals.
- Use `clean` for executor, core job, metrics, activities, and Sources.
- Use 29px phase labels and totals; use a slightly larger 34px state heading in comparisons.
- Render stage cards with watercolor style. Keep bars crisp, icons crisp, and the summary header plain with a white surface and subtle gray border. Textured bars use lighter lines from the same lane color family.
- Plan: border/bar `#4F76A8`, wash `#E4EDF7`.
- Do: border/bar `#8A5B9E`, wash `#F1E4F4`.
- Review: border/bar `#A9752A`, wash `#F7E9CF`.

## Totals

- Time mode: show weeks only when every value uses weeks; otherwise convert the total to elapsed hours.
- Funnel mode: show the percentage reaching the end using `100 × ∏(1 − dropoff_percent / 100)`. Never use 100 minus the sum of drop-offs.
- Style totals exactly like phase labels.

## Validation and preview

Read [eraser-diagrams.md](eraser-diagrams.md) for format and CLI details. Validate the specification, generate JSON, validate the Eraser artifact, and render a preview when Chromium is available. Inspect for clipping, collisions, broken links, and misleading cross-state scaling.

Watercolor output can add near-white margins. Use `scripts/crop_render.py` with 24px padding after rendering and confirm that watercolor edges remain intact.
