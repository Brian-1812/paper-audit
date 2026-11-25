# Disclaimer

Every finding in this repository is automated. No human has verified any of them. They are in the process of
verification.

## What a finding is

A finding is a possible discrepancy inside one paper. For example: a p value that does not seem to follow from its
own test statistic, or a sentence that does not seem to agree with the paper's own table. A software pipeline with
language models flagged it for checking.

## What a finding is not

- A finding is **not** a claim that a paper is wrong.
- It is **not** a statement about the quality of a paper, a journal or a publisher.
- It does **not** suggest misconduct by any author.

## Why a finding can be mistaken

- A model can misread the design, the unit of analysis, the test, or whether a value is a standard deviation or a
  standard error.
- The tool reads only the text and the tables. It does not see figures, supplements or raw data.
- "Confirmed" in this repository means that a second model agreed with a first model. Models of one family can share
  a blind spot.

We do not claim that any finding is correct or valid.

## Why we publish unverified findings

A private list helps nobody check it. We publish the findings so that authors and readers can check them and tell us
where the tool is wrong. Each correction goes back into the tool as context, and we re-run the check. That loop is
part of the verification.

## If this flags your paper

**What we did.** Software read the open-access text of your paper from PubMed Central. Language models extracted
numbers and statements. Code in a sandbox recomputed statistics from your paper's own numbers. A second model, which
did not see the first claim, checked the same place again. Every step was automatic.

**What we did not do.** No human read your paper for this project. The tool did not see figures, supplements or raw
data. We did not contact you before we published this list.

**How to tell us we are wrong.**

- Open an issue in this repository with the template "Correction to a flagged paper". Give the finding number (for
  example F07) and your explanation.
- Or write to the maintainer, Shohruh Toirov. The contact details are on the GitHub profile
  [github.com/Brian-1812](https://github.com/Brian-1812).

**What we promise.** We re-run the check with your context. Then we correct or withdraw the finding in public: we
change its entry in [`FINDINGS.md`](FINDINGS.md), add a line with the date and the reason to "Corrections and
withdrawals" in that file, and answer in the issue. A withdrawn finding stays visible as "withdrawn", with the reason,
so that the record is honest.

## Paper content

This repository holds no full paper text, no figure and no abstract. `FINDINGS.md` holds short quotations (each under
40 words) with the source, a link and the licence of each paper. The quoted words belong to the authors and stay under
the paper's own licence. The MIT licence of this repository does not cover them.

## No error rate

The run covers 500 papers from a narrow set of journals. Its counts are not an error rate for any field, journal or
publisher.
