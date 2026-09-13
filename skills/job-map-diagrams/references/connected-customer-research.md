# Connected customer research

Read this reference when the user asks the skill to discover or investigate a customer workflow using connected call-recording or transcript tools. The protocol is vendor-neutral: apply it to any authorized integration that can find customer calls and return transcripts or transcript excerpts.

## Capability contract

Use the available tools by capability rather than vendor-specific name. Look for:

- search or list calls using text, account, participant, owner, date, or similar filters;
- retrieve call metadata and the full transcript, or the largest relevant excerpt available;
- expose speaker attribution and participant roles;
- return a stable call URL or ID;
- identify transcript timestamps or another precise source location when possible.

Not every integration exposes every capability. Use what is available, disclose important limitations, and offer user-provided transcript exports as a fallback. Never imply that the skill itself grants access to a call system.

## Establish the research scope

Before searching, identify:

- the workflow or desired customer progress being investigated;
- the relevant customer segment, persona, or job executor;
- a date range appropriate to the question;
- any accounts, products, regions, or call types that should be included or excluded.

Ask only for missing choices that would materially change the corpus. Do not broaden the user's authorized scope.

## Research loop

1. Create several concise search concepts from the job, desired outcome, behaviors, obstacles, and completion signal. Do not search only for the proposed feature name.
2. Search broadly enough to find distinct calls and accounts. Use metadata to remove obvious duplicates, internal-only meetings, and calls outside the requested segment.
3. Retrieve the full transcript or relevant sections for promising calls. A search snippet alone cannot support `confidence: "explicit"`.
4. Extract atomic observations about the executor, context, behavior, friction, workaround, desired outcome, completion signal, time, drop-off, and product boundary. Keep each observation attached to its call and transcript location.
5. Compare observations across calls. Track corroboration by unique call and, when available, unique account; repeated statements within one call are not independent evidence.
6. Actively retain contradictions and meaningful variation by segment. Do not collapse different workflows merely to fill one canonical card.
7. Continue until the relevant results are exhausted, the requested limit is reached, or additional calls stop materially changing the map. Aim for at least five relevant calls across multiple accounts when available, and disclose when the corpus is smaller or concentrated.

## Evidence normalization

Register each relevant call as `customer_evidence`. Make its full `label` identify the call, date, participant role or segment, and transcript location. Keep `short_label` concise enough for a card footer, and use the stable call URL when the tool returns one.

Do not place customer names, email addresses, or unnecessary sensitive details in the rendered diagram. Use role, segment, or account-safe descriptions unless the user explicitly needs named attribution. Paraphrase findings; use short quotations only when exact wording materially matters.

For each synthesized activity:

- use `explicit` only when one or more retrieved transcript passages directly support it;
- use `inferred` when combining or interpreting evidence beyond what customers directly stated;
- cite every call that genuinely supports the activity, without padding the footer with merely related sources;
- distinguish frequency in the retrieved corpus from prevalence in the broader customer population.

## Quantitative measurements

Do not convert qualitative language such as “slow,” “often,” or “many customers” into a duration or percentage. Accept a time, conditional drop-off rate, or outside-product percentage only when it is directly supported by the evidence or explicitly supplied by the user.

If the calls establish the workflow but not all required measurements, finish the qualitative synthesis, show which values are missing, and ask the user for the measurements before rendering. Do not fabricate values to complete the diagram.

## Research handoff

Before generating the final artifact, summarize:

- corpus coverage: number of relevant calls, unique accounts when available, roles or segments, and date range;
- the proposed executor and stable core job;
- strongest recurring behaviors and friction;
- conflicting evidence or important segment differences;
- stages supported mainly by inference;
- missing time, funnel, or product-boundary measurements.

The summary makes the limits of the research visible and gives the user a chance to correct scope or interpretation before the diagram becomes a presentation artifact.
