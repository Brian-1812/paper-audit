# Results

Every count here is a count of **possible discrepancies that no human has checked**. They are in the process of
verification, and they are not claims that any paper is wrong. All labels come from models.
This file gives only aggregate counts. The 40 per-paper findings of the strict sample, all unverified, are in
[`FINDINGS.md`](../FINDINGS.md). This file gives no rate per field. The sample cannot carry such a rate (see "Limits" below).

## 1. Pilot: swarm against a fixed pipeline (100 psychology papers)

Before the main run, we compared designs on 100 open-access psychology papers (Europe PMC, papers with 5 or more
APA-format tests). All arms used the same papers and the same judge. "Real" means the judge gave tier A or B and
its own sandbox output showed the error.

A deterministic statcheck-style rule (`pipeline/psystat.py`) gave a reference set for p values only: the judge
kept 64 of its material hits as distinct real errors.

| arm | claims judged | real | judged-real share | distinct real errors | tier A | repeats | recall of the 64 | explore $ | judge $ | $ per real error |
|---|---|---|---|---|---|---|---|---|---|---|
| swarm (Sonnet) | 166 | 109 | 66% | 108 | 14 | 1% | 34% | 18.83 | 6.03 | 0.23 |
| fixed pipeline (Sonnet) | 261 | 115 | 44% | 96 | 25 | 17% | 36% | 18.77 | 10.15 | 0.30 |
| fixed pipeline (Haiku) | 480 | 205 | 43% | 170 | 33 | 17% | 52% | 1.78 | 19.61 | 0.13 |
| rule only (no model read) | 157 | 68 | 43% | 64 | 7 | 6% | 100% (by definition) | 0 | 4.78 | 0.07 |

What this shows:
1. At an equal explorer budget, the swarm was more precise than the fixed Sonnet pipeline (66% vs 44%) and
   repeated itself less (1% vs 17%). The lease board worked: no two explorers did the same cell.
2. The swarm did not find new kinds of error. Explorers proposed no new check type in the pilot.
3. The cheap Haiku pipeline found the most errors (170) at the lowest cost per error of the model arms. Most of its cost was the
   judge, because it sends many more claims.
4. The scheduler over-used one check type ("text against table": 90 of 168 cells; p-value recomputation: 6).
5. The evidence gate costs recall. 25 real errors were in findings that the gate dropped, because the explorer
   did not run its check in the sandbox.

Not proved: the swarm and the pipeline differ in more than the board (the explorers also have a sandbox and focused
cells). We did not run the ablation without the board. One run per arm.

## 2. Main run: 500 papers, 5 fields

Paper list and rule: `selection/`. 24 Sonnet explorers, the evidence gate, and one judge call per paper
(about 70% Opus, 30% Fable, by paper hash). 11 batches.

| item | value |
|---|---|
| papers explored | 500 of 500 (every paper with an evidenced finding judged, 0 left unjudged, 0 failed cells, 0 double leases) |
| explorer cells done | 881 (2,650 more cells were open and never claimed within the budget) |
| evidenced findings, judged as claims | 872 |
| judge tiers on the 872 claims | A 206, B 586, C 65, D 15 |
| real findings in the register | **542** issue records, claims about the same error merged (tier A 197, tier B 345) |
| papers with one or more real finding | 261 of 500 (134 with a tier-A finding) |
| judged A or B, but no logged code check (not counted) | 245 |
| error types of the 542 | text against table 226, p value 107, claim against result 105, effect size or interval 57, df or sample size 36, other 8, GRIM 3 |
| list-price cost | explorers $95.08 + judge $97.30 = $192.38; $0.355 per real finding |
| judge calls | Opus 248, Fable 103 |
| new check types proposed by explorers | 6 (for example: power analysis n, total equals the sum of subscales) |

Warnings:
- The judge rejected only 7% of claims as tier C. In the psychology pilot it rejected about a third. Either the
  gate and these fields give cleaner claims, or the judge was lenient here. Section 3 suggests it was lenient in
  specific ways.
- The scheduler again favoured "text against table" (402 cells) and "claim against result" (300) over p-value
  recomputation (34). Each paper got about 1.8 cells.
- 25% of the 6,834 tests that our selector counted are in the APA text format that statcheck-type rules read
  (estimate from our own regular expressions). Most of the 542 findings are of types that a rule cannot read: 331
  are "text against table" or "claim against result".

## 3. Strict blind verification of 40 tier-A findings

Code: `verify/`. Method: `docs/method.md`, section 6.

- Sample: 8 random tier-A findings per field (seed fixed, sample saved before anyone read the findings).
- The verifier (Opus) got the full paper and the place of the finding, but not the claim, the tier or the type.
  Its default answer is "consistent".

| measure | k/n | estimate | 95% exact interval |
|---|---|---|---|
| confirmed / all sampled (unresolved counts as not confirmed) | 33/40 | 82.5% | 67.2% - 92.7% |
| confirmed / decided (unresolved left out) | 33/36 | 91.7% | 77.5% - 98.2% |
| confirmed and the verifier says a reported result changes | 29/40 | 72.5% | 56.1% - 85.4% |
| confirmed by a recomputation (not only a text comparison) | 24/40 | 60.0% | 43.3% - 75.1% |

Why 7 findings did not hold:

| outcome | reason | n |
|---|---|---|
| rejected | a second symptom of an error that another finding already holds | 1 |
| rejected | the arithmetic is right under a valid different denominator (a reporting weakness, not an error) | 1 |
| rejected | not reproduced blind (the verifier tested a different reading) | 1 |
| unresolved | a premise that the paper does not state: SD or SE | 1 |
| unresolved | a premise that the paper does not state: the unit of analysis | 1 |
| unresolved | the wording has two readings | 1 |
| unresolved | two claims in one finding; only the second reproduced | 1 |

Four more findings were confirmed but change no reported result. They are real slips, but they belong in tier B.

**Control.** The same verifier, run on 20 random statistical sentences in the same papers that no finding cites,
flagged 1 of 20 (exact 95% interval 0.1% - 24.9%). So the verifier does not confirm whatever it is pointed at.

**Mechanical checks of the 33 confirmations.** Every input quote of every confirmed item occurs verbatim in its
paper. We ran the verifier's logged sandbox code again: 29 of 33 print the item's numbers in the same order, and for
the other 4 the numbers are in the logged runs, split over runs or abbreviated in the item. This
proves the arithmetic and the quotes. (The 4 were checked by the model session that prepared this
release, by reading the logs. No human did it.) It does not prove the model's reading of the paper.

**What the 40 do not prove.** No human checked a verdict. The verifier is from the same model family as most of the
judge calls, so they can share a blind spot. The place of the finding is a strong hint. n = 40 gives wide intervals.
36 distinct papers: four papers gave two findings each.

## 4. Judge v2 and the blind gate (tested on the same 40 findings only)

The strict pass showed where the first judge was lenient. The v2 judge adds five fixes:

1. **Unstated premise.** Compute the check under every reading that the paper leaves open (SD or SE, unit of
   analysis, n, which test). Tier A only when the error holds under all of them.
2. **Root-cause dedup.** A symptom of an error that another claim holds gets the issue number and tier of that root.
3. **Materiality gate.** Tier A must name the reported result that flips, from what to what.
4. **Blind second gate.** Every tier-A finding goes to the blind verifier. Confirmed stays A; not material goes
   to B; unresolved goes to B and a human queue; rejected leaves the register.
5. **No `#` comments in sandbox code.** The permission check of the CLI denied every sandbox command with a `#`
   comment line. In the main run, 29 denied sandbox commands in 28 judge calls lost a check this way.

On the same 40 findings:
- All 7 rejected or unresolved findings left tier A.
- 14 of the 29 confirmed-and-material findings stayed in tier A. The others went to tier B (6 to the human queue,
  5 because the judge named no flip) or dropped out (3 with no logged code check, 1 as tier D).
- A re-run of the old judge on the same claims kept 5 of the 7 bad findings in tier A. So the drop of the bad
  findings comes from the fixes, not from run-to-run noise. But the old judge itself also lost 7 of 29 good
  findings on a re-run, so part of any change is noise.
- Sandbox denials fell from 7 of 36 calls (old judge re-run) to 0 of 36.

This is an in-sample test: the fixes came from these 40 findings. A run on new papers is the real test, and we
have not done it.

## Limits

- No human labels. Nothing here is a measured precision.
- No recall: we do not know how many errors the run missed.
- The sample is 500 papers from 20 large open-access journals, about two thirds from two publishers.
- One run. Model output varies between runs.
- Cost is not an advantage: BARS (Kosakovsky Pond and others, 2026, https://github.com/veg/BARS) reports $0.04 to $0.09 per paper for a single-model review,
  and our run cost about $0.38 per paper at list price.
