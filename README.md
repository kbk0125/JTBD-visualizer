# JTBD Visualizer

Turn customer evidence into a living, visual problem statement.

JTBD Visualizer is a Codex skill for product managers. It investigates how customers accomplish an important workflow, organizes the evidence into an eight-stage Jobs-to-be-Done map, and renders the result with [Eraser Diagrams](https://github.com/eraserlabs/eraser-diagrams).

Use it while you are still learning—not only after you have decided what to build. The same diagram can begin as a Status Quo view of customer problems, become a deeper research artifact as evidence accumulates, and end as a before-and-after feature narrative for your team. This avoids repackaging the same research into a separate problem statement, PRD, and presentation.

![Comparison of Status Quo and After job maps](skills/job-map-diagrams/examples/prodpad-adaptive-learning.png)

## When to use it

### Research your customers' most important problems

Ask how customers accomplish a workflow today. Give the skill a written summary, interview notes, or access to evidence such as customer-call transcripts through your company's connected tools. It creates an initial Status Quo map that gives you a structured place to start investigating.

This is useful when you are not yet sure what to build and want to find recurring friction across several customers.

```text
Use $job-map-diagrams to investigate how customers complete [workflow] today.
Review the attached interview notes and call transcripts, then create a Status Quo map.
Separate direct evidence from inference and tell me what I should investigate next.
```

The connected-research workflow is vendor-neutral. It can work with Gong, Zoom, Fathom, Chorus, Fireflies, Grain, or another authorized tool that can search calls and retrieve transcripts. The skill adapts to the capabilities exposed by the integration rather than relying on vendor-specific commands.

### Investigate one important problem deeply

Keep the diagram open as a working research artifact. Add interviews, transcripts, and your own review of the evidence over time, then regenerate the map. The fixed stages make gaps visible and help you determine which related problems must be solved together to unblock the customer's workflow.

```text
Update this Status Quo job map using the new evidence I attached.
Preserve supported findings, revise anything contradicted by the evidence,
and identify stages where our understanding is still mostly inferred.
```

### Pitch a feature to your team

Once a problem and proposed intervention are credible, generate a Comparison view. It shows how the customer works before and after the feature, how much friction changes at each stage, and which parts of the job still happen outside your product. Use the rendered diagram—or a screenshot of the relevant section—as the problem-statement summary in a review or presentation.

```text
Create a Comparison job map for this customer problem and proposed feature.
Keep the core job consistent across both states, show the measured improvement,
and distinguish work completed inside our product from work completed outside it.
```

For the reasoning behind these workflows, read [Unbundling the Product Requirement Doc with AI: Problem Statements](https://productiongradesaas.substack.com/p/unbundling-the-product-requirement).

## How it works

1. **Investigate:** Provide a customer-problem summary, source documents, or connected customer evidence.
2. **Choose the story:** Generate the **Status Quo**, the proposed **After** state, or a **Comparison** of both.
3. **Measure the pain:** Supply a duration or conditional funnel drop-off for every stage. Bar length makes the relative friction visible.
4. **Map the product boundary:** Estimate how much of each stage happens outside your product. Watercolor bars call attention to stages that are mostly external.
5. **Generate the artifact:** Receive editable Eraser JSON and a rendered, source-linked diagram.

The skill asks a short set of follow-up questions when these inputs are incomplete. It does not invent quantitative measurements.

When researching through a connected call tool, it samples distinct calls and accounts, retrieves transcript evidence rather than relying on search snippets, preserves contradictions, reports corpus coverage, and identifies evidence gaps before rendering. If the integration cannot return usable transcripts, you can provide transcript exports or files instead.

## What the diagram communicates

- The customer's work across **Define, Locate, Prepare, Confirm, Execute, Monitor, Modify, and Conclude**.
- Three scannable phases: **Plan, Do, and Review**.
- Relative pain through proportional **time** or **funnel drop-off** bars.
- Where the workflow leaves your product through prominent watercolor bars.
- Direct evidence, source links, and clearly marked inferences.
- A shared scale across Status Quo and After maps so improvements remain visually comparable.

## Install the skill

Clone the repository and copy the skill folder into your personal Codex skills directory:

```bash
git clone https://github.com/kevinkononenko/JTBD-visualizer.git
mkdir -p ~/.codex/skills
cp -R JTBD-visualizer/skills/job-map-diagrams ~/.codex/skills/job-map-diagrams
```

Restart Codex after installation so it discovers the skill.

## Choose a view and measurement

### Available views

| View | Output |
| --- | --- |
| Status Quo | The job as customers accomplish it today |
| After | The job after the proposed intervention |
| Comparison | Status Quo and After maps in one diagram |

### Available measurements

| Representation | Stage input | Total shown |
| --- | --- | --- |
| Time | Positive hours or weeks | Total elapsed time |
| Funnel | Conditional percentage dropping off at each stage | Percentage reaching the end |

Funnel completion is calculated multiplicatively because each stage's drop-off applies only to the people who reached that stage.

## Example

The included fixture begins with the fictional adaptive-learning problem in ProdPad's [PRD example](https://www.prodpad.com/blog/prd-example/). Its Status Quo map adds supporting workplace-learning evidence from [360Learning's survey of 600 U.S. employees](https://360learning.com/blog/best-practices-in-training-and-development/) and [TalentLMS's survey of 1,000 U.S. employees](https://www.talentlms.com/research/learning-development-report-2026). It compares a 10-hour Status Quo flow with a proposed After flow where Execute becomes 50% faster and the other stage durations remain unchanged. The stage durations and product-boundary percentages are illustrative assumptions added to demonstrate comparison scaling and the plain and watercolor bar treatments; they are not measurements reported by those sources.

- [Input specification](skills/job-map-diagrams/examples/prodpad-adaptive-learning-spec.json)
- [Editable Eraser JSON](skills/job-map-diagrams/examples/prodpad-adaptive-learning.json)
- [Rendered PNG](skills/job-map-diagrams/examples/prodpad-adaptive-learning.png)

The eight-stage structure follows Strategyn's [customer-centered innovation map](https://strategyn.com/jobs-to-be-done/customer-centered-innovation-map/). Method sources guide organization but are not presented as evidence for customer behavior.

## Generate a diagram directly

The deterministic builder can also be run without invoking the conversational workflow:

```bash
cd skills/job-map-diagrams
python3 scripts/build_job_map.py \
  examples/prodpad-adaptive-learning-spec.json \
  examples/prodpad-adaptive-learning.json
```

The input schema is documented in [job-map-spec.md](skills/job-map-diagrams/references/job-map-spec.md).

## Validate and render

The builder itself uses the Python standard library. Rendering requires Node.js 22.12 or newer and the Eraser Diagrams CLI:

```bash
npx @eraserlabs/diagrams-cli validate \
  skills/job-map-diagrams/examples/prodpad-adaptive-learning.json \
  --fail-on-warning

npx @eraserlabs/diagrams-cli render \
  skills/job-map-diagrams/examples/prodpad-adaptive-learning.json \
  -o skills/job-map-diagrams/examples/prodpad-adaptive-learning.png \
  --scale 2
```

Cropping the near-white margins from watercolor renders is optional and requires Pillow:

```bash
python3 skills/job-map-diagrams/scripts/crop_render.py \
  skills/job-map-diagrams/examples/prodpad-adaptive-learning.png \
  --padding 24
```

## Repository structure

```text
skills/job-map-diagrams/
├── SKILL.md                 Skill workflow and behavior
├── agents/openai.yaml       Codex display metadata
├── examples/                Canonical specification, Eraser JSON, and preview
├── references/              JTBD method, schema, layout, and Eraser notes
└── scripts/                 Validator, metrics, layout, and renderer builder
```

## Current scope

- The stage taxonomy and Plan/Do/Review grouping are fixed in schema version 2.
- A comparison uses the same representation and shared bar scale for both states.
- Time values accept hours or weeks; percentage-based duration inputs are intentionally rejected.
- Funnel inputs are conditional stage drop-off rates from 0% through 100%.
- Every stage includes an outside-product estimate from 0% through 100%; bars use watercolor styling only above 50%. The percentages remain in the source specification rather than appearing on cards.

## License

Released under the [MIT License](LICENSE).

Eraser Diagrams is a separate open-source project maintained by Eraser Labs. This repository is not affiliated with or endorsed by Strategyn or ProdPad.
