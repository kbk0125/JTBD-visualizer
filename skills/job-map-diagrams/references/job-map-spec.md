# Structured job-map specification

The renderer accepts UTF-8 JSON with this shape:

```json
{
  "schema_version": 2,
  "representation": "time",
  "view": "compare",
  "title": "Comparison: Short map title",
  "job_executor": "Singular role",
  "core_job": "Verb + object + context or outcome",
  "sources": [
    {
      "id": "S1",
      "kind": "customer_evidence",
      "short_label": "Interview, checkout section",
      "label": "Source title or filename, section/page",
      "url": "https://optional-stable-link.example"
    },
    {
      "id": "S2",
      "kind": "proposal_evidence",
      "short_label": "Proposal, workflow section",
      "label": "Proposed intervention, workflow section",
      "url": "https://optional-stable-link.example/proposal"
    }
  ],
  "maps": [
    {
      "state": "status_quo",
      "stages": [
        {
          "id": "define",
          "duration": {"value": 0.5, "unit": "hours"},
          "outside_product_percent": 75,
          "activities": [
            {
              "text": "Determine the desired outcome and available time",
              "evidence": ["S1"],
              "confidence": "explicit"
            }
          ]
        }
      ]
    },
    {
      "state": "after",
      "stages": [
        {
          "id": "define",
          "duration": {"value": 0.25, "unit": "hours"},
          "outside_product_percent": 20,
          "activities": [
            {
              "text": "Use the proposed intervention to define the outcome",
              "evidence": ["S2"],
              "confidence": "explicit"
            }
          ]
        }
      ]
    }
  ]
}
```

The abbreviated example shows one stage per state for readability. Actual input must include all eight canonical stages in each map. Use `kind: "proposal_evidence"` for a source such as `S2` that supports the changed After workflow.

For a funnel map, set `"representation": "funnel"` and replace each stage's `duration` object with a conditional drop-off rate:

```json
{
  "id": "define",
  "dropoff_percent": 10,
  "outside_product_percent": 75,
  "activities": [
    {
      "text": "Determine the desired outcome and available time",
      "evidence": ["S1"],
      "confidence": "explicit"
    }
  ]
}
```

Rules enforced by `scripts/build_job_map.py`:

- `schema_version` is required and currently must be `2`. Future incompatible schema changes must increment it rather than silently reinterpreting existing specifications.
- `title`, `job_executor`, and `core_job` are non-empty strings. The title begins with `Status Quo:`, `After:`, or `Comparison:` according to the selected view.
- `view` is required and is `status_quo`, `after`, or `compare`.
- `representation` is required and is either `time` or `funnel`.
- `maps` contains exactly the states required by the view: only `status_quo`, only `after`, or `status_quo` followed by `after` for a comparison.
- Status Quo activities describe the existing workflow, workarounds, friction, and constraints. After activities describe the same job with the proposed intervention and preserve unaffected stages.
- `sources` contains unique internal IDs, a `kind` of `customer_evidence`, `proposal_evidence`, or `method`, a descriptive `short_label` of no more than 40 characters, and optional HTTP(S) URLs.
- Every map contains all eight canonical stage IDs exactly once and in canonical order.
- In time mode, every stage has a positive `duration.value` and a canonical `duration.unit` of `hours` or `weeks`. Percentage durations are not accepted. Hours and weeks may be mixed; the renderer treats one week as 168 elapsed hours when calculating proportions and the overall total.
- In funnel mode, every stage has a numeric `dropoff_percent` from 0 through 100 and no `duration`. The value is conditional: it describes the share of people who reached that stage and drop off there. Stage rates are independent and do not need to sum to 100.
- Funnel bar widths use the individual conditional drop-off rates. The final completion percentage is `100 × ∏(1 − dropoff_percent / 100)`, not 100 minus the sum of the rates. Thus two consecutive 50% drop-offs result in 25% reaching the end.
- Every stage has a numeric `outside_product_percent` from 0 through 100. This estimates how much of the user's work in that stage occurs outside the product. Values above 50 use Eraser's native watercolor style; values of exactly 50 or less remain crisp and plain. The numeric estimate remains in the specification and is not printed on the card.
- Each stage contains one to five activities.
- Each activity has non-empty text, valid evidence IDs, and confidence of `explicit` or `inferred`.
- Status Quo activity evidence may cite only `customer_evidence`. After activity evidence may cite `customer_evidence` for unchanged behavior and `proposal_evidence` for changed behavior. Frameworks, category definitions, and analysis methods belong in `method` sources and never appear as proof of behavior.
- User-visible text is length-limited to keep the cards readable.

An activity may cite multiple allowed evidence records. The card footer de-duplicates sources and renders each descriptive `short_label` as a Markdown link. Internal IDs such as `S1` remain in the structured data and do not appear on the diagram. Sources without URLs display their short label as plain text rather than pretending to be clickable. Method sources remain available for explaining how the map was constructed but are omitted from card footers.
