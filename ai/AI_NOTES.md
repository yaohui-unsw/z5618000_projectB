# AI Workflow Reflection

## Why I used a staged workflow

I organised Project B into separate design, implementation, validation and
review stages. Working in stages made each part easier to inspect and prevented
the AI from modifying methodologies after observing the outcomes. Important
modelling choices were frozen before their corresponding outputs were
generated.

## Decisions I retained

I retained responsibility for the main methodological decisions and final
approvals. These included the portfolio design, the 5-bps transaction-cost
assumption, the final finance-lexicon terms and values, and the requirement that
sentiment be lagged by one trading day before affecting portfolio weights.

I also decided to retain both favourable and unfavourable results rather than
repeatedly changing the specification.

## Errors, risks and corrections

The workflow encountered time-out errors, an overly strict output-order
validator, and overlapping or clipped chart labels. These issues were
identified through command logs, failed tests, output inspection and manual
visual review.

I worked with ChatGPT to inspect the methodology, evidence, figures and
application behaviour. Codex implemented the authorised technical corrections.
I made the final decisions and approved each correction only after confirming
that it did not alter the frozen data, methodology, parameters or analytical
results.

## How I verified AI output

I did not treat successful code execution as sufficient evidence. I used
automated tests, manual cross-checking, schema validation, date-boundary and
look-ahead checks, file hashing, output reconciliation and visual inspection.
I also audited the complete set of 24 sentiment-fusion comparisons so that
negative results were not selectively omitted.

## How I treated an unexpected result

The evidence-aware sentiment approach reduced turnover but underperformed the
naive Finance-VADER variant in all paired comparisons. I did not continue
adjusting the reliability rule, tilt strength or other parameters after
observing this result because doing so could amount to data-mining.

The negative result was retained and interpreted as evidence of a trade-off
between signal selectivity, turnover and performance.

## What I would improve

In future work, I would break tasks down more explicitly and define testing and
acceptance criteria earlier. This would reduce redundant runs and make the
distinction between methodological decisions, implementation checks and
presentation corrections even clearer.
