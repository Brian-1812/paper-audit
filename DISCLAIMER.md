# Disclaimer - automated findings, not verified by any human

**Every finding in this repository is automated. No human has verified any of them.** They are in the process of
verification.

1. **What a finding is.** A finding is a possible discrepancy inside one paper: for example, a p value that does not
   seem to follow from its own test statistic, or a sentence that does not seem to agree with the paper's own table.
   A software pipeline with language models flagged it for checking.
2. **What a finding is not.** A finding is **not** a claim that a paper is wrong. It is **not** a statement about the
   quality of a paper, a journal or a publisher. It does **not** suggest misconduct by any author.
3. **Why a finding can be mistaken.** A model can misread the design, the unit of analysis, the test, or whether a
   value is a standard deviation or a standard error. The tool reads only the text and the tables. It does not see
   figures, supplements or raw data. "Confirmed" in this repository means that a second model agreed with a first
   model. Models of one family can share a blind spot.
4. **What we do not claim.** We do not claim that any finding is correct or valid. We publish the findings so that
   authors and readers can check them, and we treat every correction as part of the verification.
5. **Corrections.** If a finding is about your paper, or you see that a finding is not right, open an issue
   (template "Correction to a flagged paper") or write to the maintainer, Shohruh Toirov (contact details on
   [github.com/Brian-1812](https://github.com/Brian-1812)). We will re-run the check with your context, and we will
   correct or withdraw the finding in public. See [README: If this flags your paper](README.md#if-this-flags-your-paper).
6. **Paper content.** This repository holds no full paper text, no figure and no abstract. `FINDINGS.md` holds short
   quotations (each under 40 words) with the source, a link and the licence of each paper. The quoted words belong
   to the authors and stay under the paper's own licence. The MIT licence of this repository does not cover them.
7. **No error rate.** The run covers 500 papers from a narrow set of journals. Its counts are not an error rate for any
   field, journal or publisher.
