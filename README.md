# paper-audit

> **Read this first. Every finding in this repository is automated, and NO human has verified any of them.**
> The findings are in the process of verification. They are **not** claims that any paper is wrong, and they do **not** suggest misconduct.
> Each one is a possible discrepancy that a language-model pipeline flagged for checking. If it flags your paper, see [If this flags your paper](#if-this-flags-your-paper).

A research tool that reads published papers and looks for **possible internal discrepancies**: a p value that does
not seem to follow from its own test statistic, a percentage that does not seem to match its own counts, a sentence
that does not seem to agree with the paper's own table. Language models do the reading. Code in a sandbox does every
calculation. The output is a list of **possible discrepancies, flagged for checking**. It is not a verdict about any
paper or any author. Full disclaimer: [`DISCLAIMER.md`](DISCLAIMER.md).

We ran it once on 500 open-access papers from 2025-26 in five applied fields: ecology and environment;
agriculture, food and veterinary science; sports and exercise science; nursing and public health; and wet-lab
biology. This repository holds the code, the prompts, the method, the list of papers, our aggregate results, and
**[`FINDINGS.md`](FINDINGS.md): 40 findings in 36 papers, with their evidence** (33 that our own second automated pass
confirmed, and 7 that it did not confirm, in a separate section). It holds no full paper text. The section "Data" says why.

## Why we publish unverified findings

Keeping the findings private helps nobody check them. We publish them so that authors and readers can check them,
and tell us where the tool is wrong. Each correction goes back into the tool as context, and we re-run the check.
That loop is part of the verification. So we say clearly, everywhere: these findings are **not verified**, and we
do **not** claim that they are correct.

## If this flags your paper

**What we did.** Software read the open-access text of your paper from PubMed Central. Language models extracted
numbers and statements. Code in a sandbox recomputed statistics from your paper's own numbers. A second model, which
did not see the first claim, checked the same place again. Every step was automatic.

**What we did not do.** No human read your paper for this project. The tool did not see figures, supplements or raw
data. We did not contact you before we published this list. We do not claim that your paper is wrong, and we do not
suggest misconduct. A model can misread a design, a unit, a test or a sentence.

**How to tell us we are wrong.**
- Open an issue in this repository with the template "Correction to a flagged paper". Give the finding number (for
  example F07) and your explanation.
- Or write to the maintainer, Shohruh Toirov. The contact details are on the GitHub profile
  [github.com/Brian-1812](https://github.com/Brian-1812).

**What we promise.** We will re-run the check with your context. Then we will correct or withdraw the finding in
public: we change its entry in `FINDINGS.md`, add a line to "Corrections and withdrawals" with the date and the
reason, and answer in the issue. A withdrawn finding stays visible as "withdrawn", with the reason, so that the
record is honest.

## The honest result, first

- The run logged **542 possible discrepancies in 261 of the 500 papers** (after merging claims about the same issue). A model judge put 197 of them in tier A
  (in its reading, it changes a reported result) and 345 in tier B (in its reading, a possible small slip that changes no result).
- **No human has checked any of these findings.** Every label in this repository comes from a model.
- `FINDINGS.md` publishes the 40 findings of the strict sample (below) with their evidence: 33 confirmed by the
  second pass, 7 not confirmed. The other records of the run are not published: no second pass checked them.
- A second, stricter model pass re-checked a random sample of 40 tier-A findings. It saw the paper and the place,
  but not the claim. It reproduced **33 of 40** (82.5%, 95% CI 67-93%). On 20 random statistical sentences with no
  known finding, it flagged 1 (5%). So the pass does not confirm whatever it is pointed at. But two models of the
  same family can share a blind spot, so 33 of 40 is model agreement. It is not a measured precision.
- In a 100-paper pilot, the swarm design was **more precise** than a fixed two-pass pipeline at the same budget
  (66% vs 44% of claims judged real). It **did not find more possible discrepancies** than a cheap fixed pipeline with a small
  model, which found the most at the lowest cost of the model arms. The swarm is a design that works. It is not a proven win.
- This is a pilot. It is not an error rate for any field, journal or publisher.

## How it works

```
papers.tsv ──► explorers (N identical agents) ──► evidence gate ──► judge ──► register ──► blind verifier
              claim cells on a lease board         (program)       (model +    (rules)     (second model,
              (paper x check type)                                  sandbox)                 sandbox, control)
```

1. **Select.** `pipeline/select_papers.py` draws the paper list by a fixed rule and saves it before any model
   call (`selection/rule.md`). Full text comes from PMC as JATS XML.
2. **Explore.** `swarm/swarm.py` runs N identical explorer agents (Claude Sonnet, 24 in our run). The search space
   is a grid of cells: one paper times one check type (recompute p values, GRIM, degrees of freedom against sample
   size, effect sizes and intervals, text against table, claims against results, and an open type).
   `swarm/board.py` is a lease board in one SQLite file. An explorer claims a cell in one transaction, so two
   explorers never do the same cell. A scheduler picks the next cell: a bandit over check types, a bonus for
   papers that already show a finding, and 30% random picks. Explorers leave notes and leads for each other.
3. **Evidence gate.** A program accepts a finding only when its quote is verbatim in the paper and its numbers were
   printed by the explorer's own sandbox run. Findings without this evidence are dropped.
4. **Judge.** `swarm/pool.py judge` sends all accepted findings of one paper to one strong model call (Opus or
   Fable, split by paper hash). The judge gives a tier (A, B, C, D) and must run its own check in the sandbox.
5. **Register.** `swarm/register.py` keeps a finding as real only when the judge gave A or B, said its code
   confirms the discrepancy, AND the judge's own sandbox log holds the output that the judge reports.
6. **Blind verifier.** `verify/strict.py` gives a fresh model the paper and the place of a finding, but not the
   claim. Its default answer is "consistent". It may say "inconsistent" only with a sandbox check that prints the
   paper's value and the recomputed value. A program then checks that every input quote is in the paper and every
   printed number is in the sandbox log. `verify/control.py` runs the same verifier on random statistical
   sentences, to measure how often it flags text with no known error.

**The sandbox.** `pipeline/sbx.py` is the only command that the judge and the verifier may run (explorers may
also read the board; the first pipeline used the smaller `pipeline/calc.py`). It runs Python in new Linux namespaces
with no network, as user `nobody`, with memory, CPU, process and output limits, and it logs every call. Paper text
is untrusted: it goes to the model inside a random fence with a guard sentence. Every model call runs with
`--safe-mode`, no MCP servers, no web tools and a fixed JSON schema.

After the strict pass we wrote a **v2 judge** (`prompts/judge_pool_v2.txt`, `swarm/judge_rules.py`) and a
**blind second gate** (`swarm/gate.py`, `swarm/register_v2.py`). They fix what the strict pass found. We tested
them only on the same 40 findings, so they are not yet measured on new papers. Details: `docs/method.md`.

## Results

All numbers and their limits are in `docs/results.md`. Short form:

| item | value |
|---|---|
| papers explored | 500 of 500 (every paper with an evidenced finding was judged; 0 left unjudged) |
| findings judged | 872 claims; tiers A 206, B 586, C 65, D 15 |
| findings in the register | 542 issue records (claims about the same issue merged): tier A 197, tier B 345, in 261 papers |
| judged A or B but no logged code check (not counted) | 245 |
| types of the 542 | text against table 226, p value 107, claim against result 105, effect size or interval 57, df or sample size 36, other 8, GRIM 3 |
| strict blind pass on 40 random tier-A findings | 33 confirmed, 3 rejected, 4 unresolved |
| control: 20 random sentences with no known finding | 1 flagged |
| list-price cost of the run | $192 ($0.355 per real finding) |

## What it cannot do

- It cannot tell you that a paper is wrong. It tells you where a number does not follow from the paper's own
  numbers, and a human must check each case.
- It reads only what is in the text and tables. It does not see figures, supplements or raw data.
- It does not find problems that are consistent inside the paper, such as a poor choice of method or model, or bad data.
- It cannot say how many discrepancies it missed. We have no recall number for this run.

## LIMITATIONS

- **No human checked any finding.** All labels come from models: the explorers, the judge, the verifier and the
  matcher. The strict pass is model against model.
- **The strict pass is not fully blind.** It gets the place of the finding, which is a strong hint.
- **Small samples.** 40 findings in the strict pass give wide intervals (about plus or minus 13 points). 20
  control sentences give a 95% interval of 0.1% to 25% for the flag rate.
- **Some confirmations are weak.** For 9 of the 33, the sandbox code only compares two sentences or a value with a
  threshold. Only 24 of 40 were confirmed by a real recomputation.
- **"Tier A" is a model's reading.** Whether a discrepancy changes a result is the model's judgment. No code proves it.
- **The sample is narrow.** 500 papers from 20 large open-access journals, about two thirds of them from two publishers.
  The results are not an error rate for any field.
- **The judge was lenient in known ways.** It accepted premises that the paper does not state (SD or SE, the unit
  of analysis), counted one issue twice as two symptoms, and gave tier A to slips that change no result. The v2
  judge fixes these, but we tested it only on the same 40 findings.
- **The scheduler is biased.** It gave many more cells to "text against table" than to p-value recomputation, and
  2,650 of the 3,531 cells were never explored within the budget.
- **One run, no repeats.** A re-run of the same judge moved about 7 of 29 good findings by itself.
- **The method is not new.** The design follows Casey Handmer's "Physics, audited". See "Credits".

## Data: what is here and what is not

We processed other people's papers. The papers are open access, but their licences differ: of the 500, 418 are
CC BY 4.0, 75 are CC BY-NC-ND 4.0 and 7 are CC BY-NC 4.0. So:

- **Here:** `selection/papers.tsv` (PMCID, DOI, journal, year, field and our two test counts per paper), our own
  code, prompts, method and aggregate results.
- **Here, as short quotations:** for each of the 40 findings in `FINDINGS.md`, the short passages of the paper that
  the finding rests on. Each quotation is under 40 words, marked as a quotation, and comes with the paper's
  identifier, a link and its licence. The quoted words belong to the authors and stay under the paper's own licence.
- **Not here:** paper full text, figures, abstracts, any longer passage and the cached XML. Each paper is open access in PMC
  under its PMCID. No script here rebuilds our exact 500-paper set from `papers.tsv`: `select_papers.py` runs a new
  search, which finds newer papers. To audit the same papers, fetch each PMCID's JATS XML from NCBI efetch
  (`db=pmc`) and write `data/<run>/list.tsv`, `key.json` and `papers/<id>/paper.txt` in the format that
  `select_papers.py finalize` writes.
- **Not here:** the other per-paper records of the run (542 in total). No second pass checked them.

## Run it

Requirements:
- Linux, Python 3.12, `lxml`, and the `unshare`, `setpriv` and `prlimit` tools (util-linux).
- `pipeline/sbx.py` creates namespaces and mounts, so it must run as **root**. Use a disposable VM or
  container for this.
- A directory with `sympy`, `mpmath` and `numpy` for the sandbox. Set `SBX_SITE` to it (default: `sandbox/site`).
- The Claude Code CLI (`claude`) on the PATH. Every model call is `claude -p` with a fixed JSON schema.
  The published run used a Claude subscription through the CLI, and `pipeline/meter.py` read the account's 5-hour
  and 7-day usage windows so that the run paused near the limit. For a new run we suggest an API key. Then the
  meter reads nothing: the swarm resumes after its error backoff, and the batch driver retries the judge every 10
  minutes. We have not tested the API-key path.

```bash
# self-tests (no model call)
python3 -I pipeline/calc.py '17*23' 'p_t(2.20, 28)' 'grim(3.47, 20, 2)'
python3 -I pipeline/psystat.py --selftest
python3 -I swarm/testing/test_judge_rules.py
sudo SBX_SITE=/path/to/site python3 -I pipeline/sbx.py --selftest

# 1. paper list and full text (network; polite delays; a new search finds newer papers, see selection/rule.md)
python3 -I pipeline/select_papers.py data/run1 search
python3 -I pipeline/select_papers.py data/run1 select
python3 -I pipeline/select_papers.py data/run1 finalize      # writes data/run1/list.tsv

# 2. the whole swarm run, in batches; run the same command again to resume
python3 -I swarm/run.py --data data/run1 --run runs/run1

# 3. strict blind verification of a sample, then the mechanical provenance check
#    (after "check", a person matches each finding with the verifier's items and writes verify/verdicts.json:
#     {"verdicts": [{"fid", "verdict": CONFIRMED|REJECTED|UNRESOLVED, "item", "code_kind": recompute|text, "material"}]})
python3 -I verify/sample.py data/register/findings.jsonl runs/verify/sample.json --seed 399 --per-field 8
python3 -I verify/strict.py run   --sample runs/verify/sample.json --register data/register/findings.jsonl --data data/run1 --run runs/verify
python3 -I verify/strict.py check --sample runs/verify/sample.json --register data/register/findings.jsonl --data data/run1 --run runs/verify
python3 -I verify/control.py runs/verify/sample.json data/register data/run1 runs/verify/control --seed 399 --n 20
python3 -I verify/analyze.py verify/verdicts.json runs/verify/sample.json

# 4. v2: blind second gate on the tier-A records, then the v2 register (tested on 40 findings only)
python3 -I swarm/register_v2.py data/run1 runs/run1 data/register-v2   # writes gate_candidates.jsonl
python3 -I swarm/gate.py run --register data/register-v2 --data data/run1 --run runs/run1
python3 -I swarm/gate.py decide --run runs/run1
python3 -I swarm/register_v2.py data/run1 runs/run1 data/register-v2   # again, now with the gate verdicts
```
`swarm/run.py` uses the v1 judge. The v2 judge is `swarm/pool.py judge --judge-version v2`.

Costs: our 500-paper run was $192 at list price for the explorers and the judge, and the strict pass was about
$0.21 per finding. Model output varies from run to run, so a re-run gives different findings.

## Credits and related work

- The design follows Casey Handmer, "Physics, audited": a cheap read for breadth, a strong model with tools
  to recompute, and a blind re-check of 40 random findings (https://science.caseyhandmer.com/physics/). His
  method page says that a fresh session, given the paper and where to look, "found 33 of 40 wrong", and that
  "No person has checked them." Our 33 of 40 is a separate run on other papers; the equal count is a coincidence.
- statcheck (Nuijten et al. 2016) recomputes APA-format p values with rules. `pipeline/psystat.py` uses the same
  rule as a baseline. It is our own code, not statcheck's.
- GRIM (Brown and Heathers 2017) tests whether a mean is possible for its n.
- Bianchi, Kwon, Izzo, Zhang and Zou, "To Err Is Human" (2025), had humans check 316 model flags in ML papers
  (83% precision). That is the standard our work does not yet meet (https://arxiv.org/abs/2512.05925).
- van Aert et al. (2023) checked 40,633 statistics in 1,066 biomedical preprints by hand. Their data is a natural
  answer key for a tool like this one (https://osf.io/tdfgq/). We have not run it.

## Licence

MIT, copyright 2026 Shohruh Toirov. See `LICENSE`. The licence covers our code and our own text only. It does not
cover the papers that the tool reads, or the short quotations from them in `FINDINGS.md`: those stay under each
paper's own licence (CC BY 4.0, CC BY-NC 4.0 or CC BY-NC-ND 4.0, named in each entry).
