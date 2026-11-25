# Method

> Every finding of this tool is automated. No human has verified any of them; they are in the process of verification.
> A finding is a possible discrepancy flagged for checking. It is not a claim that a paper is wrong. See [`DISCLAIMER.md`](../DISCLAIMER.md).

This file explains each stage, the rule that it enforces, and the code that holds the rule.

## 1. What the tool looks for

We look only for **internal** possible discrepancies: a number or a statement that does not follow from other numbers in the same
paper. Examples: a p value that does not follow from its test statistic and df; a mean that is impossible for its
n (GRIM); degrees of freedom that do not fit the stated sample; an effect size or interval that does not follow
from its test; a number in the text that differs from the same number in a table; a claim ("no significant
difference") that the paper's own statistics contradict. We do not judge the methods, the data or the conclusions.

Tiers (given by the judge):
- **A**: a possible discrepancy that, in the judge model's reading, changes a reported result or conclusion.
- **B**: a possible discrepancy that, in the judge model's reading, changes no reported result.
- **C**: not a discrepancy, in the judge model's reading.
- **D**: cannot be decided from the text.

## 2. Papers

`pipeline/select_papers.py` and `pipeline/fetch_epmc.py` fetch candidates from the Europe PMC search API and
full text as JATS XML from NCBI (one request at a time, with delays). The rule is in `selection/rule.md`. We save
the list before any model call, and models see an opaque id, never the PMCID.

## 3. Explorers and the lease board

`swarm/swarm.py`, `swarm/board.py`, `swarm/explorer.txt`, `swarm/checks.json`.

- **Cells.** The search space is a grid: one paper times one check type. The seed check types are
  `stat_recompute`, `grim_grimmer`, `df_sample`, `effect_size_ci`, `text_table`, `claim_result` and `open`.
- **Lease board.** One SQLite file in WAL mode. A cell has `UNIQUE(paper, check)`, and an explorer claims it in
  one transaction, so two explorers never work on the same cell. A lease that expires (a lost explorer) returns
  the cell to the board. The board also holds an append-only findings log, notes and leads.
- **Scheduler.** With probability 0.3 an explorer takes a random open cell. Otherwise it takes the cell with the
  best score: the yield of its check type (a bandit), times a bonus for papers that already show evidenced
  findings, divided by the cells already done on that paper, times 1.5 for a cell that another explorer proposed.
- **One explorer call.** One `claude -p` call per cell. It gets the paper, the check type, an angle and a BOARD
  block (findings and notes on this paper). Its only tools are the sandbox and a read of the board.
- **Leads.** An explorer may propose a new check type for all papers (at most 6) or one more cell on this paper.

## 4. Evidence gate

When an explorer call ends, a program checks every finding:
1. Its quote must occur in the paper text (whitespace-normalised).
2. Its evidence output must occur in the sandbox log of that call.

A finding that fails stays in the log, but it does not go to the judge. A program also marks duplicates.
This gate stops a model from reporting a calculation that it did not run.

## 5. Judge and register

`swarm/pool.py`, `prompts/judge_pool.txt`, `prompts/tool_sbx.txt`, `swarm/register.py`.

- One judge call per paper reads all evidenced findings of that paper together. The model (Opus or Fable) is
  chosen by a hash of the paper id.
- The judge gives each claim a tier, an error type and an issue number (claims about the same error share it),
  and it must run its own check in the sandbox.
- **Register rule.** A finding is real only when all three hold: the judge gave A or B; the judge said its code
  confirms the error; and the output that the judge reports appears in the judge's own sandbox log (a run with
  exit code 0, numbers matched at the reported rounding). Findings that fail only the last two go to a separate
  "unconfirmed" file and are never counted.

## 6. Strict blind verification

`verify/sample.py`, `verify/strict.py`, `verify/verifier.txt`, `verify/tool_sbx_strict.txt`, `verify/control.py`,
`verify/analyze.py`.

1. **Sample before review.** `sample.py` draws k findings per field with a fixed seed and saves only their ids and
   the hash of the register file. Nobody reads the findings before the sample is saved.
2. **Partly blind.** The verifier gets the full paper and a location pointer (the section and a verbatim quote).
   It does not get the claim, the judge's statement, the tier or the error type.
3. **Default "consistent".** "Inconsistent" needs all five rules in `verify/verifier.txt`: R1 reproduced in sandbox
   code; R2 every input quoted from the paper; R3 no explanation elsewhere in the paper (a correction, a different
   n, a one-tailed test, an adjustment, a different test, model-based values, a different definition); R4 the
   formula applies to the design (repeated measures, multilevel, adjusted models, non-parametric tests); R5 the
   difference is larger than rounding allows.
4. **Mechanical provenance.** `strict.py check` then checks that the printed numbers of each "inconsistent" item
   appear in that call's sandbox log, and that every input quote occurs in the paper.
5. **Matching.** Only after the run, the operator compares each finding with the verifier's items and assigns
   CONFIRMED, REJECTED or UNRESOLVED (the verifier saw the same discrepancy but could not decide because a fact
   is missing from the paper). In our run a separate model session did this matching by reading. No human did it.
6. **Control.** `control.py` picks random prose sentences with a test statistic or p value that share no
   25-character window with any finding, and runs the identical verifier on them.

## 7. Judge v2 and the blind second gate

`prompts/judge_pool_v2.txt`, `prompts/tool_sbx_v2.txt`, `prompts/schemas_v2.json`, `swarm/judge_rules.py`,
`swarm/gate.py`, `swarm/register_v2.py`, tests in `swarm/testing/test_judge_rules.py`.

| fix | in the prompt | enforced in code |
|---|---|---|
| unstated premise | compute under every open reading; fields `premise_readings`, `holds_under_all_readings` | tier A that does not hold under all readings becomes D |
| root-cause dedup | a symptom names its root in `root_cause_of` | the symptom takes the root's issue and tier |
| materiality gate | tier A must fill `flip` with result, from, to | tier A without a full flip becomes B |
| blind second gate | the strict verifier, unchanged | `gate.py`: Opus verify, then a Sonnet matcher, then a decision table in code |
| no `#` in sandbox code | no comments, one command per call, retry a denied call | (the denial is in the CLI permission check) |

Gate decisions: CONFIRMED keeps tier A; confirmed but not material goes to B; UNRESOLVED goes to B and a human
queue; REJECTED leaves the register (`blind_rejected.jsonl`).

## 8. Safety of the model calls

- Every call is `claude -p` with `--safe-mode`, `--strict-mcp-config`, `--no-session-persistence`, JSON output and
  a fixed `--json-schema`. Calls with no tool use `--tools ""`. Calls with a tool may run only the sandbox
  `Bash(python3 -I <abs>/pipeline/sbx.py *)` (or `calc.py` in the first pipeline; explorers may also run
  `board.py read`), with `--permission-mode dontAsk`, so every other command is denied.
- `pipeline/sbx.py` runs the code in new network, mount, PID, IPC and UTS namespaces, with no network, as user
  `nobody`, with no new privileges, with /root, /srv, /home, /tmp, /var and /mnt hidden, and with limits of 1 GiB
  memory, 30 s CPU, 64 processes, 5 MB files, 60 s wall time and 20,000 characters of output. It logs every call.
- `pipeline/calc.py` is a smaller calculator. It walks the Python syntax tree over an allow list and never calls
  `eval`.
- Paper text is untrusted. It goes inside a random nonce fence with a guard sentence.

## 9. Parallelism and usage limits

`pipeline/coordinator.py` (the runner used by every stage), `pipeline/meter.py`, `swarm/run.py`.

- The runner starts with a few parallel calls and adds more after a run of successes. It stops adding when memory
  or CPU would pass the limits you give it.
- On a rate-limit error it halves the parallelism and pauses (60 s, doubling to 15 min).
- `meter.py` reads the account's 5-hour and 7-day usage windows from one tiny call. The swarm and the judge pause
  near a ceiling and resume by themselves. `swarm/run.py` runs the papers in batches and saves its state after each
  step, so a stopped run resumes without redoing work.

## 10. Earlier stages that this repository includes

`pipeline/exp.py`, the skim prompts (`prompts/skim*.txt`) and `prompts/judge.txt`, `judge_equations.txt`, `verify.txt`,
`recheck.txt` come from a first, fixed pipeline: a cheap model skims each paper, a strong model verifies the flags.
The swarm reuses its runner and sandbox code. The pilot in `docs/results.md` section 1 compares the two designs.

These files are kept as they ran. Some of them describe earlier corpora (arXiv HTML with LaTeX math; computational
biology, neuroscience and ML benchmark papers), and some code paths in `exp.py`, `screen0.py` and `coordinator.py`
(arXiv versions, LaTeX abstracts, a rule-screen input) serve only that first pipeline. The swarm does not use them.
Where a prompt says "HTML-to-text", read "the paper converted to plain text": the main run used JATS XML from PMC.
