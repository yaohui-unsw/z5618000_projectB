# Finance lexicon candidate review

**Student review completed — 23 entries approved or edited, 4 entries rejected; frozen for later authorised implementation.**

## Review conditions and provenance

Codex proposed every term and score below. At the end of Stage 6A, none was approved: `student_decision` was `PENDING` and `student_final_value` was blank for all 27 candidates. Stage 6B preserves those AI proposals and records the student's later decision separately in the final two columns and the chronological record below.

The calibration corpus contains 36,955 cleaned headlines with inclusive UTC source dates from `2020-01-01` through `2020-12-31`, covering 50 tickers and 10 raw sectors. No 2021–2023 headline frequency, return, fund weight, portfolio performance, or fusion result was used.

Candidate counts use deterministic lowercase matching of token-shaped unigrams with the regex `(?<![A-Za-z0-9])[A-Za-z]+(?:['-][A-Za-z]+)*(?![A-Za-z0-9])`; source titles were never changed. A candidate required at least 25 token occurrences, 20 distinct headlines, and 5 tickers. Tickers, company/publisher/person names, URLs, numbers, dates, stopwords, and clearly ambiguous non-finance tokens were excluded. Values are conservative 0.5 increments in `[-3,+3]`.

Examples are not hand-picked. After matching rows were sorted by `source_timestamp` and `source_row_order`, example 1 is the earliest row and example 2 is the lower-median row at zero-based position `(n - 1) // 2`. Exact cleaned titles and zero-based source-row identifiers are retained. A fixed five-position context review (earliest, lower quartile, lower median, upper quartile, latest) informed the conflict flag, but only the required earliest and median examples are reproduced below.

Frequency does not establish polarity, and two examples do not prove stable meaning. Headline-level token polarity can be defeated by negation, questions, mixed clauses, an event concerning another company, or imprecise ticker tagging. Rejected terms must not be silently restored in implementation.

`ALL10` expands deterministically to: `Comm, Consumer, Energy, Financials, Healthcare, Industrials, Materials, RealEstate, Tech, Utilities`.

## Candidate table

Sorted by descending 2020 occurrences, then ascending term.

| Term | Class | Occurrences | Headlines | Tickers | Sector coverage | Raw-sector list | Vanilla | Proposed | Direction | Student decision | Student final value |
|---|---|---:|---:|---:|---:|---|---:|---:|---|---|---|
| `shares` | reviewed_override | 1,922 | 1,893 | 48 | 10 | ALL10 | 1.2 | 0.0 | neutral | ACCEPT | 0.0 |
| `energy` | reviewed_override | 1,617 | 1,558 | 46 | 10 | ALL10 | 1.1 | 0.0 | neutral | ACCEPT | 0.0 |
| `alert` | reviewed_override | 399 | 399 | 50 | 10 | ALL10 | 1.2 | 0.0 | neutral | ACCEPT | 0.0 |
| `rally` | addition | 315 | 314 | 42 | 10 | ALL10 | NA | 1.0 | positive | ACCEPT | 1.0 |
| `active` | reviewed_override | 307 | 307 | 29 | 10 | ALL10 | 1.7 | 0.0 | neutral | ACCEPT | 0.0 |
| `beat` | addition | 295 | 295 | 45 | 10 | ALL10 | NA | 1.5 | positive | ACCEPT | 1.5 |
| `inflow` | addition | 243 | 243 | 42 | 10 | ALL10 | NA | 1.0 | positive | REJECT |  |
| `rebound` | addition | 235 | 232 | 44 | 10 | ALL10 | NA | 1.0 | positive | EDIT | 0.5 |
| `downgrades` | addition | 212 | 212 | 35 | 10 | ALL10 | NA | -1.5 | negative | EDIT | -1.0 |
| `asset` | reviewed_override | 207 | 206 | 35 | 10 | ALL10 | 1.5 | 0.0 | neutral | ACCEPT | 0.0 |
| `outflows` | addition | 207 | 207 | 44 | 10 | ALL10 | NA | -1.0 | negative | REJECT |  |
| `outflow` | addition | 205 | 205 | 45 | 10 | ALL10 | NA | -1.0 | negative | REJECT |  |
| `inflows` | addition | 197 | 197 | 44 | 10 | ALL10 | NA | 1.0 | positive | REJECT |  |
| `beats` | addition | 146 | 145 | 42 | 10 | ALL10 | NA | 1.5 | positive | ACCEPT | 1.5 |
| `outperform` | addition | 134 | 134 | 37 | 10 | ALL10 | NA | 1.5 | positive | EDIT | 1.0 |
| `miss` | reviewed_override | 128 | 128 | 45 | 10 | ALL10 | -0.6 | -1.5 | negative | EDIT | -1.0 |
| `overweight` | reviewed_override | 111 | 111 | 29 | 10 | ALL10 | -1.5 | 1.0 | positive | ACCEPT | 1.0 |
| `bullish` | addition | 101 | 101 | 41 | 10 | ALL10 | NA | 1.5 | positive | ACCEPT | 1.5 |
| `slump` | addition | 58 | 58 | 24 | 8 | Comm, Consumer, Energy, Financials, Healthcare, Industrials, Materials, Tech | NA | -1.5 | negative | ACCEPT | -1.5 |
| `misses` | reviewed_override | 46 | 46 | 32 | 10 | ALL10 | -0.9 | -1.5 | negative | ACCEPT | -1.5 |
| `plunge` | addition | 45 | 45 | 21 | 8 | Consumer, Energy, Financials, Healthcare, Industrials, Materials, Tech, Utilities | NA | -1.5 | negative | ACCEPT | -1.5 |
| `downgraded` | addition | 41 | 41 | 20 | 9 | Comm, Consumer, Energy, Financials, Healthcare, Industrials, Materials, Tech, Utilities | NA | -1.5 | negative | ACCEPT | -1.5 |
| `tumble` | addition | 32 | 32 | 16 | 6 | Consumer, Energy, Financials, Healthcare, Industrials, RealEstate | NA | -1.5 | negative | ACCEPT | -1.5 |
| `underweight` | addition | 31 | 31 | 10 | 7 | Energy, Financials, Healthcare, Industrials, RealEstate, Tech, Utilities | NA | -1.0 | negative | ACCEPT | -1.0 |
| `plunges` | addition | 30 | 29 | 13 | 7 | Consumer, Energy, Financials, Healthcare, Industrials, Materials, Tech | NA | -1.5 | negative | ACCEPT | -1.5 |
| `underperform` | addition | 28 | 28 | 16 | 8 | Consumer, Energy, Financials, Healthcare, Industrials, Materials, Tech, Utilities | NA | -1.5 | negative | EDIT | -1.0 |
| `layoffs` | addition | 27 | 27 | 11 | 5 | Comm, Consumer, Energy, Financials, Industrials | NA | -1.5 | negative | EDIT | -1.0 |

## Candidate rationales, audit examples, and risks

### `shares` — proposed 0.0

- Rationale: in financial headlines, “shares” normally names equity units; direction comes from surrounding words such as higher/lower, not the noun itself.
- Earliest: `2020-01-02T00:00:00+00:00`, row `8766`, AMD — “Advanced Micro Devices shares are trading higher after Nomura Instinet maintained a Buy rating on the stock and raised the price target from $40 to $58.”
- Lower median: `2020-04-08T00:00:00+00:00`, row `113248`, SHW — “Shares of several basic material companies are trading higher amid optimism that coronavirus cases around the world are potentially easing. Global slowing cases could raise hopes of a sooner return to spending, economic activity and investment.”
- Ambiguity/misuse risk: ordinary ownership uses are possible; neutralising the token could remove valid positive affect in rare non-finance phrases.
- Reviewed conflict with proposed polarity: no; reviewed uses treat it as a neutral noun.

### `energy` — proposed 0.0

- Rationale: “energy” usually identifies a sector, commodity theme, or company name component; the vanilla positive value can bias neutral sector headlines.
- Earliest: `2020-01-02T00:00:00+00:00`, row `27751`, COP — “Energy Sector Update for 01/02/2020: XOM, CVX, COP, SLB, OXY, CLB, WMB, SDRL”.
- Lower median: `2020-04-28T00:00:00+00:00`, row `114264`, SLB — “5 Energy Plays to Stand Out in Q1 Earnings Amid Crude Crash”.
- Risk: “energy” can be positive in ordinary language, but finance-sector usage dominates the reviewed examples.
- Conflict: no; reviewed finance uses are categorical rather than intrinsically positive.

### `alert` — proposed 0.0

- Rationale: “ETF Inflow Alert” and “Option Alert” are publication labels, not positive affect.
- Earliest: `2020-01-02T00:00:00+00:00`, row `18002`, BA — “ITOT, HD, BA, C: ETF Inflow Alert”.
- Lower median: `2020-04-23T00:00:00+00:00`, row `114249`, SLB — “Schlumberger Option Alert: May 15 $17.5 Calls Sweep (7) near the Ask: 500 @ $0.701 vs 3793 OI; Ref=$16.11”.
- Risk: a genuine risk alert can be negative; zero is proposed because direction must come from the event details.
- Conflict: no; reviewed uses are neutral labels.

### `rally` — proposed +1.0

- Rationale: commonly denotes a positive market-price advance; the score is restrained because a rally may concern another asset or be questioned.
- Earliest: `2020-01-02T00:00:00+00:00`, row `8768`, AMD — “2020 Vision: Rally Mode To Start Off Decade As Last Year's Strength Rolls Along”.
- Lower median: `2020-06-05T07:01:48+00:00`, row `110269`, SBUX — “What's Behind The Luckin Coffee Rally?”
- Risk: broad-market attribution, questions such as “rally over?”, and relief rallies can make issuer-level inference unreliable.
- Conflict: yes; reviewed interrogative/end-of-rally contexts can make the headline stance mixed.

### `active` — proposed 0.0

- Rationale: “most active” describes trading volume, not favourable performance.
- Earliest: `2020-01-03T00:00:00+00:00`, row `113913`, SLB — “Most Active Equity Options For Midday - Friday, Jan. 3”.
- Lower median: `2020-09-09T00:00:00+00:00`, row `51023`, GE — “After Hours Most Active for Sep 9, 2020 : AAPL, GE, IBN, MO, QQQ, INTC, NBL, BAC, GLNG, NYMT, GME, PFE”.
- Risk: non-finance “active” can be positive; the override is intended only for this finance corpus.
- Conflict: no.

### `beat` — proposed +1.5

- Rationale: earnings or revenue above a benchmark is favourable, although the surrounding headline may contain offsetting costs or guidance.
- Earliest: `2020-01-14T00:00:00+00:00`, row `126688`, USB — “First Republic (FRC) Q4 Earnings Beat Estimates, Costs Rise”.
- Lower median: `2020-05-01T00:00:00+00:00`, row `355`, ABBV — “Abbvie stands by 2020 profit forecast as Humira fuels quarterly beat”.
- Risk: “beat the market” is prospective or comparative; mixed clauses can offset the positive term.
- Conflict: yes; the earliest example also states that costs rose.

### `inflow` — proposed +1.0

- Rationale: fund inflow denotes positive net capital movement into the named vehicle.
- Earliest: `2020-01-02T00:00:00+00:00`, row `18002`, BA — “ITOT, HD, BA, C: ETF Inflow Alert”.
- Lower median: `2020-05-26T00:00:00+00:00`, row `27992`, COP — “XLE, PSX, COP, EOG: ETF Inflow Alert”.
- Risk: an ETF-level flow is not necessarily information about each tagged constituent; magnitude and motive are unknown.
- Conflict: no term-level conflict in the reviewed contexts.

### `rebound` — proposed +1.0

- Rationale: denotes recovery from an earlier decline, conservatively positive rather than proof of a durable trend.
- Earliest: `2020-01-03T00:00:00+00:00`, row `74842`, MRK — “After Lackluster 2019, Pfizer Stock Could Rebound in 2020”.
- Lower median: `2020-04-23T00:00:00+00:00`, row `106628`, QCOM — “Shares of several semiconductor companies are trading higher. Strength potentially related to earnings from notable names in the space this week as well as overall market strength amid a rebound in oil.”
- Risk: forecasts (“could rebound”), relief moves, and rebounds in another asset may not be issuer-positive.
- Conflict: yes; reviewed occurrences include prospective and cross-asset usage.

### `downgrades` — proposed -1.5

- Rationale: an analyst rating reduction is adverse information relative to the prior rating.
- Earliest: `2020-01-02T00:00:00+00:00`, row `131676`, WFC — “Baird Downgrades Wells Fargo to Underperform, Announces $50 Price Target”.
- Lower median: `2020-03-23T00:00:00+00:00`, row `25371`, CMCSA — “Baird Downgrades Comcast to Neutral, Lowers Price Target to $38”.
- Risk: digest headlines can mention both upgrades and downgrades without identifying the tagged issuer.
- Conflict: yes; fixed review included mixed “Top Upgrades, Downgrades” digests.

### `asset` — proposed 0.0

- Rationale: “asset” is normally a neutral finance noun; transaction direction and quality come from surrounding language.
- Earliest: `2020-01-03T00:00:00+00:00`, row `142996`, XOM — “Dow Jones News: Apple Price Targets Raised; Exxon Expects Big Gain From Norway Asset Sale”.
- Lower median: `2020-05-04T00:00:00+00:00`, row `39097`, DIS — “Granite Springs Asset Management LLC Buys Science Applications International Corp, Accenture ...”.
- Risk: “asset” occurs in organisation names and positive phrases such as valuable asset; zero may remove rare ordinary-language affect.
- Conflict: no; reviewed uses are nouns/name components.

### `outflows` — proposed -1.0

- Rationale: denotes net capital leaving a fund, a restrained adverse flow indicator.
- Earliest: `2020-01-02T00:00:00+00:00`, row `48957`, EA — “Noteworthy ETF Outflows: XLC, CHTR, ATVI, EA”.
- Lower median: `2020-06-15T00:00:00+00:00`, row `75320`, MRK — “XLV, MRK, PFE, CVS: Large Outflows Detected at ETF”.
- Risk: ETF-level flows do not establish adverse issuer information for every constituent.
- Conflict: no term-level conflict in the reviewed contexts.

### `outflow` — proposed -1.0

- Rationale: singular form of the adverse capital-flow concept.
- Earliest: `2020-01-02T00:00:00+00:00`, row `3102`, ABT — “SPDR Portfolio S&P 500 Growth ETF Experiences Big Outflow”.
- Lower median: `2020-06-18T00:00:00+00:00`, row `55001`, GILD — “Notable ETF Outflow Detected - IVE, C, WFC, GILD”.
- Risk: constituent attribution and investor motivation remain unknown.
- Conflict: no.

### `inflows` — proposed +1.0

- Rationale: plural form of positive net capital movement into a fund.
- Earliest: `2020-01-02T00:00:00+00:00`, row `2`, ABBV — “NOBL, TGT, ABBV, ADM: Large Inflows Detected at ETF”.
- Lower median: `2020-06-22T00:00:00+00:00`, row `83058`, NEE — “SPLG, ACN, NEE, UNP: Large Inflows Detected at ETF”.
- Risk: ETF flow is not issuer-specific and can reflect mechanical allocation.
- Conflict: no.

### `beats` — proposed +1.5

- Rationale: normally reports performance above earnings, sales, or revenue expectations.
- Earliest: `2020-01-15T00:00:00+00:00`, row `56994`, GS — “Goldman Sachs Q4 Profit Misses View, But Revenue Beats”.
- Lower median: `2020-05-01T00:00:00+00:00`, row `100075`, O — “Cousins Properties (CUZ) Beats on Q1 FFO, Scraps '20 View”.
- Risk: mixed headlines can contain a beat in one measure and a miss, weak outlook, or withdrawn view elsewhere.
- Conflict: yes; both mandatory examples contain offsetting negative information.

### `outperform` — proposed +1.5

- Rationale: favourable analyst rating or explicit relative-performance expectation.
- Earliest: `2020-01-03T00:00:00+00:00`, row `82635`, NEE — “Credit Suisse Maintains Outperform on NextEra Energy, Raises Price Target to $250”.
- Lower median: `2020-03-26T00:00:00+00:00`, row `14796`, AMGN — “Oppenheimer Maintains Outperform on Amgen, Lowers Price Target to $240”.
- Risk: it can describe another company or coexist with a lower target; “maintains” contains less new information than an upgrade.
- Conflict: yes; the median example lowers the target despite the positive rating.

### `miss` — proposed -1.5

- Rationale: an earnings/revenue miss is materially adverse relative to expectations; vanilla `-0.6` appears understated in this domain.
- Earliest: `2020-01-14T00:00:00+00:00`, row `131716`, WFC — “Wells Fargo Trades Lower On Q4 Earnings Miss”.
- Lower median: `2020-04-22T00:00:00+00:00`, row `38947`, DIS — “Netflix's (NFLX) Q1 Earnings Miss, Coronavirus Aids User Growth”.
- Risk: ordinary “miss out” usage is not an earnings shortfall; one fixed-review example used that construction.
- Conflict: yes; “Did You Miss Out ...?” is contextually different and can make the proposed negative value wrong.

### `overweight` — proposed +1.0

- Rationale: finance usage is a favourable relative-allocation/rating term; vanilla `-1.5` has the wrong sign for this context.
- Earliest: `2020-01-07T00:00:00+00:00`, row `8794`, AMD — “Wells Fargo Maintains Overweight on Advanced Micro Devices, Raises Price Target to $55”.
- Lower median: `2020-03-30T00:00:00+00:00`, row `113240`, SHW — “Morgan Stanley Maintains Overweight on Sherwin-Williams, Lowers Price Target to $550”.
- Risk: a downgrade *from* overweight is adverse, and the body-weight meaning remains negative outside finance.
- Conflict: yes; reviewed occurrences include downgrade-from-overweight and lower-target contexts.

### `bullish` — proposed +1.5

- Rationale: expresses positive market or analyst direction.
- Earliest: `2020-01-02T00:00:00+00:00`, row `128178`, V — “Does Visa Deserve Its Bullish Valuation?”
- Lower median: `2020-05-19T00:00:00+00:00`, row `91167`, NVDA — “NVIDIA shares are trading higher after Susquehanna and RBC Capital maintained their bullish ratings on the company's stock along with raising their price targets.”
- Risk: questions, negation, “bullish but...”, and valuation warnings can reverse or weaken the headline stance.
- Conflict: yes; the earliest example is interrogative, and fixed review included a bullish/forecast-fall paradox.

### `slump` — proposed -1.5

- Rationale: denotes a sustained adverse decline in market, demand, or activity.
- Earliest: `2020-02-27T00:00:00+00:00`, row `38349`, DIS — “3 Stocks to Buy if the Market's Coronavirus-Induced Slump Continues”.
- Lower median: `2020-04-21T00:00:00+00:00`, row `143550`, XOM — “U.S. energy companies' quarterly reports to show depths of slump”.
- Risk: a slump may create a buying opportunity or concern a broad market/another entity.
- Conflict: yes; the earliest headline frames the slump as a buying setup.

### `misses` — proposed -1.5

- Rationale: earnings, sales, or goal failure is adverse; vanilla `-0.9` is conservatively strengthened.
- Earliest: `2020-01-07T00:00:00+00:00`, row `74853`, MRK — “Merck's Keytruda Misses an Important Lung Cancer Goal”.
- Lower median: `2020-04-16T00:00:00+00:00`, row `78876`, MS — “Morgan Stanley Misses On EPS, But Shows Strong Trading Results For Q1 As Banks Wrap Up”.
- Risk: an offsetting “but” clause may dominate; grammatical ordinary-language uses also exist.
- Conflict: yes; the median headline explicitly offsets the miss with strong trading results.

### `plunge` — proposed -1.5

- Rationale: denotes a sharp adverse decline, but the score is kept below the most extreme VADER values.
- Earliest: `2020-01-16T00:00:00+00:00`, row `78613`, MS — “Mid-Day Market Update: Crude Oil Up Over 1%; Qudian Shares Plunge”.
- Lower median: `2020-04-20T00:00:00+00:00`, row `38917`, DIS — “Dow Jones Dips As Oil Prices Plunge, But Coronavirus Stock Market Rally Still Has Bullish Tone”.
- Risk: the plunging object can be oil or another company; mixed clauses can offset the negative movement.
- Conflict: yes; the median headline also contains rally and bullish language.

### `downgraded` — proposed -1.5

- Rationale: past-tense analyst rating reduction is adverse relative to the previous recommendation.
- Earliest: `2020-01-21T00:00:00+00:00`, row `78652`, MS — “Morgan Stanley shares are trading lower after Citigroup downgraded the stock from Buy to Neutral.”
- Lower median: `2020-04-13T00:00:00+00:00`, row `22218`, CAT — “Caterpillar shares are trading lower after analysts at Bank of America downgraded the company's stock from Neutral to Underperform.”
- Risk: a headline may discuss a different issuer or an already-priced action.
- Conflict: no in the reviewed contexts.

### `tumble` — proposed -1.5

- Rationale: denotes a sharp negative market or operating decline.
- Earliest: `2020-01-27T00:00:00+00:00`, row `74899`, MRK — “A Peek Into The Markets: US Stock Futures Down; Dow Futures Tumble Over 400 Points”.
- Lower median: `2020-04-01T00:00:00+00:00`, row `38653`, DIS — “Stocks Tumble As Data Reveals Worsening Coronavirus Impact”.
- Risk: broad-market use can be weakly related to the tagged ticker.
- Conflict: no term-level conflict in reviewed contexts.

### `underweight` — proposed -1.0

- Rationale: unfavourable relative-allocation or analyst-rating term.
- Earliest: `2020-01-06T00:00:00+00:00`, row `126674`, USB — “Wells Fargo Downgrades U.S. Bancorp to Underweight, Announces $61 Price Target”.
- Lower median: `2020-04-09T00:00:00+00:00`, row `22207`, CAT — “Stephens & Co. Maintains Underweight on Caterpillar, Lowers Price Target to $80”.
- Risk: “maintains” is not new information, and the ordinary body-weight meaning differs.
- Conflict: no in the reviewed finance usages.

### `plunges` — proposed -1.5

- Rationale: inflected form of a sharp negative decline.
- Earliest: `2020-01-31T00:00:00+00:00`, row `62866`, INTC — “Dow Jones Plunges 600 Points As U.S. Declares Coronavirus Public Health Emergency”.
- Lower median: `2020-04-27T00:00:00+00:00`, row `39001`, DIS — “Oil Plunges, BP Reports Steep Slide In Profits”.
- Risk: broad index, commodity, or another issuer may be the declining object.
- Conflict: no term-level conflict in reviewed contexts, but attribution risk is high.

### `underperform` — proposed -1.5

- Rationale: unfavourable analyst rating or relative-performance expectation.
- Earliest: `2020-01-02T00:00:00+00:00`, row `131676`, WFC — “Baird Downgrades Wells Fargo to Underperform, Announces $50 Price Target”.
- Lower median: `2020-03-30T00:00:00+00:00`, row `72724`, MMM — “Gordon Haskett Downgrades 3M to Underperform”.
- Risk: comparisons may identify another company as the underperformer; maintained ratings may add little new information.
- Conflict: no in the two mandatory examples; attribution remains a broader risk.

### `layoffs` — proposed -1.5

- Rationale: workforce reductions usually indicate organisational stress and adverse employee impact.
- Earliest: `2020-01-28T00:00:00+00:00`, row `72580`, MMM — “Dow Jones News: 3M Announces Layoffs; Apple Has a Lot to Prove Today”.
- Lower median: `2020-07-24T00:00:00+00:00`, row `30593`, CVX — “Chevron diversity ratio to improve as layoffs progress”.
- Risk: investors may interpret cost reductions positively; voluntary or restructuring contexts differ from distress.
- Conflict: yes; the median example frames a potentially positive diversity effect alongside layoffs.

## Rejected-candidate audit

The table records representative high-frequency or conceptually relevant terms considered but not proposed. It is not an exhaustive dump of the 1,755 tokens that met the mechanical frequency/ticker thresholds.

| Term | Occurrences | Headlines | Tickers | Vanilla | Exclusion reason |
|---|---:|---:|---:|---:|---|
| `buy` | 3,314 | 3,310 | 50 | NA | Recommendation, acquisition verb, insider transaction, or imperative; not a stable headline polarity. |
| `earnings` | 2,143 | 2,128 | 50 | NA | Neutral topic noun; surprise and guidance modifiers carry direction. |
| `dividend` | 1,283 | 1,272 | 49 | NA | Payment, yield description, increase, cut, or suspension have different signs. |
| `target` | 1,035 | 1,034 | 50 | NA | Neutral valuation noun; raise/lower and comparison to market price matter. |
| `lower` | 828 | 805 | 47 | -1.2 | Already valenced and highly object/context dependent; no justified override. |
| `growth` | 517 | 510 | 49 | 1.6 | Vanilla value is directionally reasonable; no material finance-specific correction shown. |
| `raises` | 388 | 388 | 46 | NA | Raising a target/dividend is positive, but raising costs/debt/risk is negative. |
| `sell` | 279 | 279 | 46 | NA | Rating, transaction, sale instruction, or quotation; issuer meaning is unstable. |
| `profit` | 268 | 264 | 41 | 1.9 | Existing VADER value is directionally suitable; no override needed. |
| `hold` | 267 | 267 | 47 | NA | Neutral analyst rating or ordinary verb; adding zero would not alter VADER. |
| `cuts` | 256 | 251 | 32 | -1.2 | Dividend/job cuts can be adverse, while cost/tax cuts may be positive; existing value retained. |
| `upgrades` | 199 | 199 | 36 | NA | Mixes analyst actions, combined upgrade/downgrade digests, and product/software upgrades. |
| `surge` | 184 | 184 | 34 | NA | The surging object may be price, demand, infections, costs, or claims; sign is not stable. |
| `guidance` | 116 | 115 | 35 | NA | Neutral topic; raise/cut/withdrawal and magnitude establish direction. |
| `upgrade` | 94 | 94 | 32 | NA | Mixes analyst/strategy upgrades with product and technology changes. |
| `lawsuit` | 41 | 41 | 17 | -0.9 | Already negative in vanilla; outcome and plaintiff/defendant attribution vary. |
| `plunged` | 25 | 25 | 16 | NA | Meets the threshold boundary but reviewed market/object attribution was too unstable for this conservative proposal. |
| `bankruptcy` | 24 | 24 | 12 | NA | Fails the minimum 25-occurrence threshold; threshold was not lowered. |
| `bearish` | 20 | 20 | 14 | NA | Fails the minimum 25-occurrence threshold; threshold was not lowered. |
| `fraud` | 14 | 14 | 7 | -2.8 | Fails occurrence/headline thresholds and already has strong vanilla valence. |
| `downgrade` | 6 | 6 | 3 | NA | Fails occurrence, headline, and five-ticker thresholds. |

## Required student action — Stage 6A historical status

For each candidate, the student must record `ACCEPT`, `REJECT`, or `EDIT`, provide a short reason, and enter a final value for accepted/edited terms. An accepted final value must remain in `[-3,+3]` on a 0.5 increment. No candidate is operational until that review is complete and a later implementation stage is explicitly authorised.

**Stage 6A historical status:** All candidate decisions remained `PENDING`; no finance-lexicon entry had yet been approved.

## Final student decision record

### Confirmation context and provenance

Before the Stage 6B prompt, ChatGPT reviewed `docs/finance_lexicon_review.md`, `docs/sentiment_innovation_design.md`, and `ai/07_sentiment_design_and_lexicon_candidates.md` with the student. ChatGPT explained every candidate, displayed example, ambiguity warning, proposed value, and design choice, then recommended 17 unchanged acceptances, six value edits, and four rejections. The student reviewed that assistance and replied exactly:

> “我确认了，给我提示词”

By sending the Stage 6B prompt, the student then confirmed exactly:

> I have reviewed the Stage 6A methodology, all 27 AI-proposed candidates, the audit examples, and the stated ambiguity risks. I accept the 17 unchanged decisions listed below, approve the six edited final values, and reject `inflow`, `inflows`, `outflow`, and `outflows`.
>
> I agree that repeated ETF-flow template headlines present material ticker-attribution and repeated-reporting risks. ETF-level inflows and outflows therefore should not automatically alter the sentiment score of every tagged constituent.
>
> I accept the proposed sentiment and fusion methodology, including the separation of raw evidence-aware diagnostics from the tradable evidence-aware signal. I also accept preserving the exact required `sector_sentiment_index.csv` schema while storing the sector-level custom-term hit-share diagnostic in `sentiment_diagnostics.csv`.
>
> These are my final pre-implementation lexicon decisions. Stage 6B is authorised only to record these decisions, freeze the approved lexicon and accepted design, and preserve the AI-workflow evidence. No sentiment implementation, full-corpus scoring, sector-index generation, fusion, portfolio regeneration, output generation, figure creation, app work, or report work is authorised.

Codex generated the original 27 proposals; ChatGPT provided the described review assistance; the student reviewed that material and exercised final authority. This record does not claim that the student independently performed Codex's extraction or ChatGPT's technical review.

### Complete decision matrix

| Term | AI-proposed value | Student decision | Student final value | Student-confirmed reason |
|---|---:|---|---:|---|
| `shares` | 0.0 | ACCEPT | 0.0 | In financial headlines it is normally a neutral noun referring to equity units. |
| `energy` | 0.0 | ACCEPT | 0.0 | It normally identifies a sector, commodity theme, or name component rather than positive affect. |
| `alert` | 0.0 | ACCEPT | 0.0 | In this corpus it is mainly a publication, ETF-flow, option, or trading-alert label. |
| `rally` | +1.0 | ACCEPT | +1.0 | It normally denotes a positive market-price movement, with a conservative magnitude retained for attribution and question risk. |
| `active` | 0.0 | ACCEPT | 0.0 | “Most active” describes trading activity or volume rather than favourable performance. |
| `beat` | +1.5 | ACCEPT | +1.5 | An earnings, revenue, or estimate beat is materially favourable; other words can represent offsetting clauses. |
| `inflow` | +1.0 | REJECT |  | ETF-level flow cannot be reliably attributed to every tagged constituent, and repeated template headlines could dominate the signal. |
| `rebound` | +1.0 | EDIT | +0.5 | It is directionally positive, but can be prospective, temporary, or refer to another asset, so a weaker value is more defensible. |
| `downgrades` | -1.5 | EDIT | -1.0 | Rating downgrades are negative, but this plural form often appears in mixed analyst-action digests. |
| `asset` | 0.0 | ACCEPT | 0.0 | It is generally a neutral finance noun or organisation-name component. |
| `outflows` | -1.0 | REJECT |  | ETF-level flow cannot be reliably attributed to every tagged constituent, and repeated template headlines could dominate the signal. |
| `outflow` | -1.0 | REJECT |  | ETF-level flow cannot be reliably attributed to every tagged constituent, and repeated template headlines could dominate the signal. |
| `inflows` | +1.0 | REJECT |  | ETF-level flow cannot be reliably attributed to every tagged constituent, and repeated template headlines could dominate the signal. |
| `beats` | +1.5 | ACCEPT | +1.5 | It normally reports performance above expectations; mixed clauses remain visible through other headline terms. |
| `outperform` | +1.5 | EDIT | +1.0 | It is a favourable rating, but maintained ratings and simultaneous target cuts justify a more conservative magnitude. |
| `miss` | -1.5 | EDIT | -1.0 | It frequently denotes an earnings or revenue shortfall but also occurs in ordinary constructions such as “miss out.” |
| `overweight` | +1.0 | ACCEPT | +1.0 | In financial ratings it is positive and corrects the inappropriate negative vanilla-VADER sign. |
| `bullish` | +1.5 | ACCEPT | +1.5 | It directly expresses a positive market or analyst view, while existing VADER rules and other words retain some contextual qualification. |
| `slump` | -1.5 | ACCEPT | -1.5 | It denotes a material adverse decline in markets, demand, or activity. |
| `misses` | -1.5 | ACCEPT | -1.5 | In this finance corpus it usually reports failure to meet earnings, sales, or operating expectations. |
| `plunge` | -1.5 | ACCEPT | -1.5 | It denotes a sharp adverse decline, with the magnitude kept below extreme VADER values. |
| `downgraded` | -1.5 | ACCEPT | -1.5 | It directly reports an adverse analyst-rating reduction. |
| `tumble` | -1.5 | ACCEPT | -1.5 | It denotes a substantial negative market or operating movement. |
| `underweight` | -1.0 | ACCEPT | -1.0 | In finance it is an unfavourable relative-allocation or analyst-rating term. |
| `plunges` | -1.5 | ACCEPT | -1.5 | It is the inflected form of a sharp adverse decline. |
| `underperform` | -1.5 | EDIT | -1.0 | It is an unfavourable rating, but a symmetric conservative value with `outperform` reduces overstatement and maintained-rating risk. |
| `layoffs` | -1.5 | EDIT | -1.0 | Workforce reductions are generally adverse, but cost-reduction and restructuring interpretations justify a weaker value. |

The decision reconciliation is `17 ACCEPT + 6 EDIT + 4 REJECT = 27`; 23 entries have approved numeric values and four do not.

### Frozen operational and rejected lists

The 23 operational entries, frozen for a later separately authorised implementation, are:

`shares`, `energy`, `alert`, `rally`, `active`, `beat`, `rebound`, `downgrades`, `asset`, `beats`, `outperform`, `miss`, `overweight`, `bullish`, `slump`, `misses`, `plunge`, `downgraded`, `tumble`, `underweight`, `plunges`, `underperform`, and `layoffs`.

The four rejected, non-operational ETF-flow entries are:

`inflow`, `inflows`, `outflow`, and `outflows`.

They must not enter `finance_vader` or a future `finance_lexicon.csv`. The original AI proposals, counts, examples, rationales, conflict warnings, and earlier rejected-candidate audit remain visible above. No return, portfolio, fusion result, or post-2020 frequency influenced the decisions; no candidate was added after viewing results; and the rejected ETF-flow terms remain excluded because of attribution and repeated-template risk.

**Student review completed; the 23 approved or edited entries are frozen for a later authorised implementation stage. The four rejected ETF-flow entries are non-operational. No sentiment or fusion result has been generated.**
