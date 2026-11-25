# Findings - automated, NOT verified by any human

> **Read this first.** Everything in this file comes from software that uses language models.
> **No human has verified any of these findings.** They are in the process of verification.
> A finding here is a **possible discrepancy that was flagged for checking**. It is **not** a claim that a paper is wrong,
> and it does **not** suggest misconduct by any author. The model can misread a paper; the paper can be right.
> If this file flags your paper, see [If this flags your paper](#if-this-flags-your-paper). We will re-check it with your context
> and correct or withdraw the finding in public.

Date of this list: 2026-11-25. Run: one run over 500 open-access papers (see `docs/results.md`).
Full disclaimer: [`DISCLAIMER.md`](DISCLAIMER.md).

## What is in this file

- **Section A - 33 findings that our own second automated pass confirmed.** They are in four groups, from the
  strongest automated bar to the weakest. "Confirmed" means one model agreed with another model. It does not mean true.
- **Section B - 7 flags that our own second pass did NOT confirm.** They are listed only so that the sample of 40 is
  complete and nothing is hidden. Read them as "not confirmed by our own second pass".
- The 40 are a random sample (8 per field) of the 197 tier-A records of the run. The other records of the run
  (542 in total) are not published here: no second pass checked them.

## How to read one entry

- **Paper**: the PMC identifier and the DOI, with links to the open-access paper. Read the paper itself.
- **What the tool checked** and **the numbers it extracted**: each number comes with the short passage of the paper
  that it was read from.
- **What the tool flagged**: a summary written by the model. We changed words such as "wrong" or "error" to neutral words.
  We did not change any number.
- **If the flag holds**: the model's reading of what would change. No code proves this part.
- **Automatic checks**: which steps of the pipeline the finding passed. All of them are automatic. None is a human check.
- **Sandbox runs**: the Python code that the second pass ran, and what it printed, as logged.

**Quotations.** Passages in `>` quote blocks are short quotations from the paper, each under 40 words, with the
source above them. The words belong to the paper's authors. They stay under the paper's own licence (named in each entry).
The MIT licence of this repository does not cover them. Three dots (...) inside a quote mark words that we left out;
[...] marks a cut at the 40-word limit. A `|` inside a quote separates the cells of one table row.
This file holds no full text, no figure and no abstract.

**The automatic checks, in plain words.**

1. *Evidence gate (program)*: the quote of the first finding is word for word in the paper, and its numbers were printed by a sandbox run.
2. *First judge (model)*: a strong model gave tier A (a reported result changes) and ran its own check in the sandbox.
3. *Strict blind pass (second model)*: a fresh model got the paper and the place, but not the claim. Its default answer
   is "consistent". It said "inconsistent" with a sandbox check. "Recomputed" means it recomputed a statistic;
   "text comparison" means its code only compared statements or a threshold.
4. *v2 judge and blind second gate (models)*: a stricter judge written after the strict pass, then the blind check again.
   It was tested only on these 40 findings.
5. *Mechanical checks (program, 2026-11-25)*: every quote is word for word in the paper text; the logged sandbox code was run again.

## Corrections and withdrawals

None yet (2026-11-25). When an author or a reader shows that a finding is not right, we write it here with the date,
and we mark the entry itself.

## If this flags your paper

See the section of the same name in [`README.md`](README.md#if-this-flags-your-paper). In short: open an issue in
this repository (template "Correction to a flagged paper"), or write to the maintainer. We will re-run the check
with your context and correct or withdraw the finding in public.

## Section A - 33 findings confirmed by our own second automated pass (not verified by a human)

Counts: group 1: 11, group 2: 10, group 3: 8, group 4: 4.

### Group 1 - recomputed, changes a reported result, and passed the v2 judge and blind gate (11)

The strongest automated bar. The second pass recomputed the number from the paper's own numbers. In its reading, a reported result changes. The finding also stayed in tier A under the stricter v2 judge and the blind second gate. This is still not a human check.

#### F01 · PMC12070029 · Nurs Open (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12070029](https://pmc.ncbi.nlm.nih.gov/articles/PMC12070029/) · DOI [10.1002/nop2.2204](https://doi.org/10.1002/nop2.2204) · *Nurs Open* (2025) · field: nursing_public_health · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q5358133c-2`
- **Where in the paper**: Abstract Results vs Results section
- **What the tool checked**: Other Abstract correlations (total, emotional, informational) vs Table 3
- **Value as reported in the paper**: Abstract: total 0.415 (p<0.001), emotional 0.328 (p=0.004), informational 0.311 (p=0.006); Table 3: 0.236 (0.009), 0.314 (0.001), 0.161 (0.094)
- **What the tool computed**: With n = 120, the Table 3 values give p = 0.0095, 0.0005 and 0.079. The Abstract r values give p = 2e-6, 0.00026 and 0.00055, which do not match the Abstract's 0.004 and 0.006
- **What the tool flagged** (model summary): The Abstract reports r = 0.415 for total support and r = 0.311, p = 0.006 (significant) for informational support. The Results and Table 3 report r = 0.236 and r = 0.161, p = 0.094 (not significant). The Abstract p-values also do not fit n = 120: r = 0.328 gives p ≈ 0.0003, and r = 0.197 gives p ≈ 0.031.
- **If the flag holds, what would change** (model reading, not proven): The informational dimension is significant in the Abstract (p = 0.006) but not significant in the Results (p = 0.094). The Abstract's conclusion for this dimension is the opposite of the Results.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12070029, CC BY 4.0):

- `0.415, 0.328, 0.311`, from:

  > "(r = 0.415, p < 0.001) and the emotional (r = 0.328, p = 0.004) and informational (r = 0.311, p = 0.006)"

- `0.236, 0.314, 0.161`, from:

  > "(r = 0.236, p = 0.009) and the emotional support subscale (r = 0.314, p = 0.001) ... informational (r = 0.161, p = 0.094)"

- The passage that the first finding rests on:

  > "this relationship was not significant in the instrumental dimension (r = 0.197, p = 0.081)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p(r,n):
    df=n-2
    t=r*m.sqrt(df)/m.sqrt(1-r*r)
    return float(t), float(m.betainc(df/2.0,0.5,0,df/(df+t*t),regularized=True))
for r,pp in [(0.197,0.081),(0.1965,0.081),(0.1975,0.081),(0.132,0.173),(0.236,0.009),(0.314,0.001),(0.161,0.094),(0.415,0.001),(0.328,0.004),(0.311,0.006)]:
    print("r",r,"paper p",pp,"t,p n=120",p(r,120))
for n in [80,90,100,110]:
    print("n",n,"r=0.197",p(0.197,n))
```
```text
r 0.197 paper p 0.081 t,p n=120 (2.1827418834803303, 0.03103530608246504)
r 0.1965 paper p 0.081 t,p n=120 (2.1769791336132154, 0.03147330678504408)
r 0.1975 paper p 0.081 t,p n=120 (2.188506405268663, 0.030602481203553952)
r 0.132 paper p 0.173 t,p n=120 (1.4465447014077824, 0.15067561054727216)
r 0.236 paper p 0.009 t,p n=120 (2.6381354631192777, 0.009460361163372)
r 0.314 paper p 0.001 t,p n=120 (3.5926169226346327, 0.00047859689842747025)
r 0.161 paper p 0.094 t,p n=120 (1.7720247744198756, 0.07897143373912568)
r 0.415 paper p 0.001 t,p n=120 (4.954877791520776, 2.442929051066057e-06)
r 0.328 paper p 0.004 t,p n=120 (3.77164816638463, 0.00025502101479939687)
r 0.311 paper p 0.006 t,p n=120 (3.5545975390788755, 0.0005455693794763134)
n 80 r=0.197 (1.7746335170293384, 0.07986018532586305)
n 90 r=0.197 (1.8849624989101914, 0.06273514992794733)
n 100 r=0.197 (1.989181521337756, 0.049468766956677186)
n 110 r=0.197 (2.088205599878859, 0.03913054330820811)
```

</details>

#### F02 · PMC12565232 · Insects (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12565232](https://pmc.ncbi.nlm.nih.gov/articles/PMC12565232/) · DOI [10.3390/insects16101013](https://doi.org/10.3390/insects16101013) · *Insects* (2025) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qbbf35f1b-1`
- **Where in the paper**: Results 3.1
- **What the tool checked**: 2.4-fold higher ATP at 5000 lux vs 200 lux at 12 °C
- **Value as reported in the paper**: 2.4-fold
- **What the tool computed**: 3.13-fold (12.165/3.885)
- **What the tool flagged** (model summary): In Section 3.1, ATP is 12.165 μmol/g at 5000 lux versus 3.885 μmol/g at 200 lux. That is a 3.13-fold ratio, a 213% increase. The paper instead reports '2.4-fold' (3.1) and a '240%' increase (Summary, Abstract, 4.1), and these two figures also disagree with each other.
- **If the flag holds, what would change** (model reading, not proven): The headline effect size changes. The reported means give a 3.1-fold (213%) increase, not 2.4-fold or 240%. The direction and significance stay the same.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12565232, CC BY 4.0):

- `12.165`, from:

  > "5000 lux: 12.165 ± 0.42 μmol/g"

- `3.885`, from:

  > "200 lux: 3.885 ± 0.21 μmol/g; p < 0.001"

- The passage that the first finding rests on:

  > "reaching a 2.4-fold higher level under high light (5000 lux: 12.165 ± 0.42 μmol/g) compared to low light (200 lux: 3.885 ± 0.21 μmol/g; p < 0.001)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
hi=12.165
lo=3.885
print("fold", hi/lo, "paper 2.4")
print("pct increase", (hi/lo-1)*100, "paper 240")
print("fold bounds", 12.1645/3.8855, 12.1655/3.8845)
print("22C reduction pct", (1-6.304/11.118)*100, "paper 43")
```
```text
fold 3.131274131274131 paper 2.4
pct increase 213.1274131274131 paper 240
fold bounds 3.130742504182216 3.1318058952246104
22C reduction pct 43.299154524194996 paper 43
```

</details>

#### F03 · PMC12696897 · BMC Nurs (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12696897](https://pmc.ncbi.nlm.nih.gov/articles/PMC12696897/) · DOI [10.1186/s12912-025-03932-x](https://doi.org/10.1186/s12912-025-03932-x) · *BMC Nurs* (2025) · field: nursing_public_health · licence: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Run id**: `R1-q9130c5da-1`
- **Where in the paper**: Table 3, Humanistic Care Training, cognitive dimension
- **What the tool checked**: Table 3, humanistic care training, cognitive dimension: t = 3.331, P = 0.505 (independent samples t-test, Yes n=158 vs No n=23)
- **Value as reported in the paper**: t = 3.331, P = 0.505
- **What the tool computed**: Two-tailed p = 0.0011 (df 179) or 0.0027–0.0030 (Welch-type df 22–25)
- **What the tool flagged** (model summary): In Table 3 (training, cognitive dimension), t = 3.331 with df ≈ 179 gives p ≈ 0.001, but the paper reports P = 0.505 and treats training as non-significant. It is therefore left out of the cognitive regression in Table 8.
- **If the flag holds, what would change** (model reading, not proven): Training would change from a non-significant to a significant factor for the cognitive dimension (P≈0.001–0.003 instead of 0.505). The univariate Results text, which lists only marital status and professional title for cognition, and the choice of variables for the Table 8 cognitive model would change.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12696897, CC BY-NC-ND 4.0):

- `3.331`, from:

  > "Yes | 3.331(0.505)a | 5.603(< 0.001**)a | 1.934(0.124)a"

- `n = 158 / 23`, from:

  > "Yes | 158(87.3) | 179.50 ± 16.97 | 5.236a | 0.031* / No | 23(12.7) | 147.57 ± 28.27"

- The passage that the first finding rests on:

  > "Humanistic Care Training |  |  |  / Yes | 3.331(0.505)a | 5.603(< 0.001**)a | 1.934(0.124)a"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p(t,df):
    t=abs(t); return m.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
for t in [3.331,3.3305,3.3315,5.603,1.934]:
    for df in [179,25,22]:
        print("t",t,"df",df,"p2",m.nstr(p(t,df),4))
```
```text
t 3.331 df 179 p2 0.001051
t 3.331 df 25 p2 0.002691
t 3.331 df 22 p2 0.003031
t 3.3305 df 179 p2 0.001053
t 3.3305 df 25 p2 0.002694
t 3.3305 df 22 p2 0.003034
t 3.3315 df 179 p2 0.001049
t 3.3315 df 25 p2 0.002687
t 3.3315 df 22 p2 0.003027
t 5.603 df 179 p2 7.838e-8
t 5.603 df 25 p2 7.901e-6
t 5.603 df 22 p2 1.24e-5
t 1.934 df 179 p2 0.05469
t 1.934 df 25 p2 0.06451
t 1.934 df 22 p2 0.06608
```

</details>

#### F04 · PMC13136085 · Front Sports Act Living (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13136085](https://pmc.ncbi.nlm.nih.gov/articles/PMC13136085/) · DOI [10.3389/fspor.2026.1806303](https://doi.org/10.3389/fspor.2026.1806303) · *Front Sports Act Living* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q21025977-3`
- **Where in the paper**: Results, Participant characteristics vs Table 1
- **What the tool checked**: No significant sex difference in RHR (p > 0.05), checked against Table 1 male vs female means and SDs
- **Value as reported in the paper**: p > 0.05 (no significant difference); Table 1 RHR male 47 ± 5 (n = 3,280), female 50 ± 6 (n = 1,091)
- **What the tool computed**: Welch t = -14.9, p ≈ 4.5e-47; at the rounding bound that gives the smallest difference, t = -9.1, p ≈ 1.9e-19
- **What the tool flagged** (model summary): The Results and Abstract say there were no significant sex differences in RHR, HRmax or HRR (all p > 0.05). But Table 1 gives RHR 47±5 vs 50±6 and HRR 135±11 vs 130±15 with n = 3,280 vs 1,091, which yields t ≈ −16.3 and 11.8 (p < 0.001).
- **If the flag holds, what would change** (model reading, not proven): The statement 'No significant sex differences in RHR' (Results and Abstract) would become: females had a significantly higher RHR (about 3 bpm, p < 0.001).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13136085, CC BY 4.0):

- `47 ± 5`, from:

  > "RHR (bpm) | 47 ± 5 | 50 ± 6 | 51 ± 7 | 48 ± 6"

- `50 ± 6`, from:

  > "RHR (bpm) | 47 ± 5 | 50 ± 6 | 51 ± 7 | 48 ± 6"

- `3,280 / 1,091`, from:

  > "Male (n = 3,280) | Female (n = 1,091)"

- The passage that the first finding rests on:

  > "No statistically significant sex differences were observed in RHR, HRmax, or HRR (all p > 0.05)."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as mp
def welch(m1,s1,n1,m2,s2,n2):
    se=mp.sqrt(s1**2/n1+s2**2/n2)
    t=(m1-m2)/se
    df=(s1**2/n1+s2**2/n2)**2/((s1**2/n1)**2/(n1-1)+(s2**2/n2)**2/(n2-1))
    p=mp.betainc(df/2,0.5,0,df/(df+t**2),regularized=True)
    return float(t),float(df),float(p)
print("RHR", welch(47,5,3280,50,6,1091))
print("RHR min diff bound", welch(47.5,5.5,3280,49.5,6.5,1091))
print("HRmax", welch(183,10,3280,182,10,1091))
print("HRmax min bound", welch(182.5,10.5,3280,182.5,10.5,1091))
print("HRR", welch(135,11,3280,130,15,1091))
print("HRR min diff bound", welch(134.5,11.5,3280,130.5,15.5,1091))
```
```text
RHR (-14.885230499670135, 1622.9252395026424, 4.514958131733916e-47)
RHR min diff bound (-9.133610362365706, 1640.0648995985891, 1.8948670849256618e-19)
HRmax (2.8612703461214815, 1867.0446041166974, 0.004266448176179641)
HRmax min bound (0.0, 1867.0446041166974, 1.0)
HRR (10.140443034006832, 1498.885116465552, 2.040585271916364e-23)
HRR min diff bound (7.83664800164918, 1508.8799522741704, 8.673048312038116e-15)
```

</details>

#### F05 · PMC13168142 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13168142](https://pmc.ncbi.nlm.nih.gov/articles/PMC13168142/) · DOI [10.3389/fphar.2026.1801073](https://doi.org/10.3389/fphar.2026.1801073) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q8022901e-2`
- **Where in the paper**: Results, NTT paragraph
- **What the tool checked**: Distance traveled ANOVA F(3,36)=2.78, p<0.01
- **Value as reported in the paper**: F(3,36)=2.78, p < 0.01
- **What the tool computed**: p = 0.055 (0.0547–0.0553 within rounding bounds of F); not significant at 0.05
- **What the tool flagged** (model summary): Results, NTT: F(3,36)=2.78 (distance) gives p=0.055, not the reported p<0.01, and F(3,36)=3.14 (velocity) gives p=0.037, not p<0.01. The distance ANOVA is therefore not significant at 0.05, which goes against the claim of 'a significant overall effect of treatment across all measured parameters'.
- **If the flag holds, what would change** (model reading, not proven): The overall treatment effect on distance traveled changes from significant (p<0.01) to non-significant (p≈0.055). This contradicts the claim of 'a significant overall effect of treatment across all measured parameters' and weakens the reported RA-induced reduction in locomotion (p<0.05).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13168142, CC BY 4.0):

- `2.78`, from:

  > "total distance traveled [F (3,36) = 2.78, p < 0.01; Figure 1C]"

- `3,36`, from:

  > "F (3,36) = 2.78"

- The passage that the first finding rests on:

  > "total distance traveled [F (3,36) = 2.78, p < 0.01; Figure 1C], and swimming velocity [F (3,36) = 3.14, p < 0.01; Figure 1D]"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
def p(F,d1,d2):
    x=d2/(d2+d1*F)
    return mpmath.betainc(d2/2.0,d1/2.0,0,x,regularized=True)
for F in [2.78,2.775,2.785,3.14,3.135,3.145,8.02,7.85]:
    print("F",F,"p",p(F,3,36))
```
```text
F 2.78 p 0.0549838045839098
F 2.775 p 0.0552879551877355
F 2.785 p 0.0546813819423672
F 3.14 p 0.0370621918231467
F 3.135 p 0.0372643616510197
F 3.145 p 0.0368611597707375
F 8.02 p 0.000320222924249526
F 7.85 p 0.000371235243250844
```

</details>

#### F06 · PMC13300515 · Insects (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13300515](https://pmc.ncbi.nlm.nih.gov/articles/PMC13300515/) · *Insects* (2026) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qd54b31d2-1`
- **Where in the paper**: 3.1.2, northern slope regression
- **What the tool checked**: p < 0.01 reported for F(2,4)=0.40, and the claim that quadratic models gave 'strong fits'
- **Value as reported in the paper**: p < 0.01
- **What the tool computed**: p = 0.694 (0.692 to 0.697 when F is rounded to 0.395 or 0.405)
- **What the tool flagged** (model summary): In Section 3.1.2, the northern-slope Simpson quadratic fit is reported as R2=0.17, F(2,4)=0.40, p<0.01. F(2,4)=0.40 actually gives p≈0.69. The fit is not significant and not 'strong', which also matches the earlier finding of no Simpson differences on the northern slope.
- **If the flag holds, what would change** (model reading, not proven): The northern-slope Simpson quadratic fit changes from significant (p < 0.01, a 'strong fit') to non-significant (p about 0.69). So the claim that quadratic models gave strong fits for all four indices on the northern slope does not hold for Simpson's index.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13300515, CC BY 4.0):

- `F(2,4) =0.40`, from:

  > "Simpson index (R2 = 0.17, F(2,4) =0.40, p < 0.01)"

- `df 2,4`, from:

  > "Simpson index (R2 = 0.17, F(2,4) =0.40, p < 0.01)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p(F,d1,d2):
    x=d2/(d2+d1*F)
    return m.betainc(d2/2.0,d1/2.0,0,x,regularized=True)
print("F_from_R2", (0.17/2)/((1-0.17)/4))
print("F_bounds", (0.165/2)/((1-0.165)/4), (0.175/2)/((1-0.175)/4))
print("p_paper_F0.40", p(0.40,2,4))
print("p_F0.395", p(0.395,2,4), "p_F0.405", p(0.405,2,4))
print("Fcrit_p0.01_check p(18)", p(18,2,4))
```
```text
F_from_R2 0.4096385542168675
F_bounds 0.3952095808383234 0.42424242424242425
p_paper_F0.40 0.694444444444445
p_F0.395 0.697347030391255 p_F0.405 0.691559943119195
Fcrit_p0.01_check p(18) 0.01
```

</details>

#### F07 · PMC13389739 · Front Vet Sci (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13389739](https://pmc.ncbi.nlm.nih.gov/articles/PMC13389739/) · DOI [10.3389/fvets.2026.1839557](https://doi.org/10.3389/fvets.2026.1839557) · *Front Vet Sci* (2026) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qa620ee35-1`
- **Where in the paper**: Table 4 / Results fecal DM
- **What the tool checked**: Day-21 fecal dry matter: C 32.42 ± 1.95 vs Lb.-FM 42.06 ± 1.54 (mean ± SD, n = 6/group), reported p = 0.980 (C × Lb.-FM) and 0.979 (diet)
- **Value as reported in the paper**: p = 0.980 / 0.979
- **What the tool computed**: t-test with n=6/group: t = 9.50, p ≈ 2.5e-6 (rounding extremes: t = 9.47). Even if ± were SE: t = 3.88, p ≈ 0.003
- **What the tool flagged** (model summary): Table 4 reports fecal dry matter of 32.42 ± 1.95 (C) vs 42.06 ± 1.54 (Lb.-FM) on day 21 with p = 0.980, and 30.91 ± 1.89 vs 39.11 ± 1.70 on day 61 with p = 0.601 (n = 6 per group). A Welch-type t-test on these numbers gives t ≈ −9.5, p ≈ 2.5e-6 (day 21) and t ≈ −7.9, p ≈ 1.3e-5 (day 61). Even if the ± values were SEs, p would be ≈ 0.003 and 0.009. So the means/SDs and the p-values do not fit together, and the stated 'no difference in dry matter' does not follow from the table.
- **If the flag holds, what would change** (model reading, not proven): The claim of no significant difference in fecal dry matter at day 21 (in the Results and Discussion: 'no significant effect on ... dry matter content') would change to a highly significant group difference (p < 0.001). This also makes the groups look non-comparable at baseline.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13389739, CC BY 4.0):

- `32.42 ± 1.95`, from:

  > "Dry matter (%) | 21 | 32.42 ± 1.95a | 42.06 ± 1.54a | 0.980 | 0.979"

- `42.06 ± 1.54`, from:

  > "Dry matter (%) | 21 | 32.42 ± 1.95a | 42.06 ± 1.54a | 0.980 | 0.979"

- `n = 6`, from:

  > "The data are presented as the mean ± standard deviation (n = 6/group)."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as mp
def welch(m1,s1,m2,s2,n=6):
    se=mp.sqrt(s1**2/n+s2**2/n); t=(m2-m1)/se; df=2*n-2
    p=mp.betainc(df/2,0.5,0,df/(df+t**2),regularized=True)
    return float(t),float(p)
print("DM21 SD", welch(32.42,1.95,42.06,1.54))
print("DM21 SD worst rounding", welch(32.425,1.955,42.055,1.545))
print("DM21 if SE", welch(32.42,1.95*6**0.5,42.06,1.54*6**0.5))
print("DM61 SD", welch(30.91,1.89,39.11,1.70))
print("pH21 SD", welch(6.36,0.17,6.12,0.08))
print("tex21 SD", welch(0.60,0.06,0.34,0.03))
print("paper p DM21 0.980 diet 0.979")
```
```text
DM21 SD (9.503111599662427, 2.530867229502504e-06)
DM21 SD worst rounding (9.46649770082748, 2.621168624352732e-06)
DM21 if SE (3.8796290646494924, 0.003060781192804368)
DM61 SD (7.901374389536323, 1.3124252410745535e-05)
pH21 SD (-3.128956418992551, 0.01070949179495745)
tex21 SD (-9.493857663422878, 2.5533655899521802e-06)
paper p DM21 0.980 diet 0.979
```

</details>

#### F08 · PMC13451341 · Nurs Open (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13451341](https://pmc.ncbi.nlm.nih.gov/articles/PMC13451341/) · DOI [10.1002/nop2.70731](https://doi.org/10.1002/nop2.70731) · *Nurs Open* (2026) · field: nursing_public_health · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qbd0e9f5a-1`
- **Where in the paper**: Results, Exploratory Subgroup Analyses (text vs Table 2)
- **What the tool checked**: Table 2 F = 2.48, p = 0.088 for Relationship versus the same group statistics and the text
- **Value as reported in the paper**: F = 2.48, p = 0.088 (Table 2); text says F = 3.17, p = 0.045
- **What the tool computed**: F = 3.17 (range over all rounding bounds 2.97–3.38), p = 0.045
- **What the tool flagged** (model summary): The text and Table 2 disagree on the relationship-to-patient ANOVA. The Results text gives F = 3.17, p = 0.045 but calls the result non-significant. Table 2 gives F = 2.48, p = 0.088. Recomputing the one-way ANOVA from Table 2's own data (spouse n = 67, 4.28 ± 0.76; child n = 49, 3.92 ± 0.95; other n = 12, 3.85 ± 0.82) gives F(2,125) = 3.17, p = 0.045 and η² ≈ 0.048. So the table values do not fit together, and the 'not significant' conclusion does not follow at α = 0.05.
- **If the flag holds, what would change** (model reading, not proven): Table 2 reports the relationship comparison as non-significant (p = 0.088). The summary data and the text give p = 0.045, which is significant at α = 0.05.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13451341, CC BY 4.0):

- `2.48, 0.088`, from:

  > "Spouse | 67 (52.3) | 4.28 ± 0.76 | 2.48 | 0.088 | η / 2 = 0.04"

- `F = 3.17, p = 0.045`, from:

  > "spouses reported higher needs than children (4.28 ± 0.76 vs. 3.92 ± 0.95, F = 3.17, p = 0.045, η / 2 = 0.04)"

- The passage that the first finding rests on:

  > "spouses reported higher needs than children (4.28 ± 0.76 vs. 3.92 ± 0.95, F = 3.17, p = 0.045, η / 2 = 0.04), although this difference did not reach statistical significance"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as mp
n=[67,49,12]; m=[4.28,3.92,3.85]; s=[0.76,0.95,0.82]
N=sum(n); gm=sum(a*b for a,b in zip(n,m))/N
ssb=sum(a*(b-gm)**2 for a,b in zip(n,m)); ssw=sum((a-1)*c**2 for a,c in zip(n,s))
F=(ssb/2)/(ssw/(N-3))
def p(F,d1,d2): return mp.betainc(d2/2.,d1/2.,0,d2/(d2+d1*F),regularized=True)
print("F recomputed",F,"p",p(F,2,N-3),"eta2",ssb/(ssb+ssw))
print("text F 3.17 p",p(3.17,2,125)); print("table F 2.48 p",p(2.48,2,125))
```
```text
F recomputed 3.171468009185263 p 0.0453373153753375 eta2 0.048292936115600156
text F 3.17 p 0.0454007017828243
table F 2.48 p 0.0878555892551141
```

```python
import itertools
n=[67,49,12]; M=[4.28,3.92,3.85]; S=[0.76,0.95,0.82]
r=[]
for dm in itertools.product([-0.005,0.005],repeat=3):
  for ds in itertools.product([-0.005,0.005],repeat=3):
    m=[a+b for a,b in zip(M,dm)]; s=[a+b for a,b in zip(S,ds)]
    N=sum(n); gm=sum(a*b for a,b in zip(n,m))/N
    ssb=sum(a*(b-gm)**2 for a,b in zip(n,m)); ssw=sum((a-1)*c**2 for a,c in zip(n,s))
    r.append(((ssb/2)/(ssw/122*0+ssw/125), ssb/(ssb+ssw)))
print("F range",min(x[0] for x in r),max(x[0] for x in r))
print("eta2 range",min(x[1] for x in r),max(x[1] for x in r))
```
```text
F range 2.9706492406809373 3.38140062808733
eta2 range 0.04537375564675308 0.0513255728604794
```

</details>

#### F09 · PMC13607948 · Insects (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13607948](https://pmc.ncbi.nlm.nih.gov/articles/PMC13607948/) · DOI [10.3390/insects17090974](https://doi.org/10.3390/insects17090974) · *Insects* (2026) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qd89f8d28-1`
- **Where in the paper**: Section 3.3, hour-0 ANOVA
- **What the tool checked**: F(2,42)=0.88 at hour 0 compared with the reported hour-0 means ± SE (n=15 per group)
- **Value as reported in the paper**: F2,42 = 0.88, p = 0.422 (not significant)
- **What the tool computed**: F ≈ 3.60, p ≈ 0.036 (range 3.45–3.76 within rounding, p 0.031–0.041) if ± is SE; F ≈ 54 if ± is SD
- **What the tool flagged** (model summary): In Section 3.3, the hour-0 egg densities are 57.5 ± 2.6, 53.3 ± 4.1 and 44.4 ± 3.7 (n = 15 per group). A one-way ANOVA on these gives F2,42 ≈ 3.60, p ≈ 0.036, not the reported F2,42 = 0.88, p = 0.422. Reading ± as SE is supported because the same reading reproduces the paper's 48 h, tomato and eggplant F values. So the claim of no initial difference among groups does not seem to fit the paper's own numbers.
- **If the flag holds, what would change** (model reading, not proven): The statement that initial egg densities did not differ (F=0.88, p=0.422) changes to a significant baseline difference (F≈3.6, p≈0.036). The control started with fewer eggs, which weakens the claim that the groups were comparable at baseline.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13607948, CC BY 4.0):

- `57.5 ± 2.6`, from:

  > "from an initial density of 57.5 ± 2.6 eggs per plant at hour 0"

- `53.3 ± 4.1`, from:

  > "starting from an initial density of 53.3 ± 4.1 eggs per plant at hour 0"

- `44.4 ± 3.7`, from:

  > "egg counts increased from an initial baseline density of 44.4 ± 3.7 eggs per plant at hour 0"

- `n = 15`, from:

  > "Each treatment was replicated 15 times (n = 15)"

- `45.3 ± 6.7, 143.5 ± 11.2, 165.7 ± 13.0; F2,42 = 36.46`, from:

  > "A one-way ANOVA revealed highly significant differences ... (F2,42 = 36.46, p < 0.001)"

- The passage that the first finding rests on:

  > "Initial egg densities showed no significant differences among treatment groups at hour 0 (F2,42 = 0.88, p = 0.422)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 5/5 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): partly: the numbers are in the logged runs, but split over runs or abbreviated. A model session checked this by reading the logs, not a human

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as mp
def F(m,s,n):
    k=len(m); g=sum(m)/k
    ssb=n*sum((x-g)**2 for x in m); msb=ssb/(k-1)
    msw=sum((si**2)*n for si in s)/k
    f=msb/msw; d2=k*(n-1)
    p=mp.betainc(d2/2,(k-1)/2,0,d2/(d2+(k-1)*f),regularized=True)
    return f,p
def pF(f,d1,d2): return mp.betainc(d2/2,d1/2,0,d2/(d2+d1*f),regularized=True)
print("paper hour0 F=0.88 p=0.422; p from F:",pF(0.88,2,42))
print("hour0 SE-based",F([57.5,53.3,44.4],[2.6,4.1,3.7],15))
print("hour48 SE-based (paper F=36.46)",F([45.3,143.5,165.7],[6.7,11.2,13.0],15))
lo=F([57.5-0.05,53.3,44.4+0.05],[2.65,4.15,3.75],15); hi=F([57.5+0.05,53.3,44.4-0.05],[2.55,4.05,3.65],15)
print("hour0 bounds",lo,hi)
```
```text
paper hour0 F=0.88 p=0.422; p from F: 0.422290701311755
hour0 SE-based (3.602522812667741, mpf('0.035977640897524012'))
hour48 SE-based (paper F=36.46) (36.295405652314855, mpf('7.0159973955249251e-10'))
hour0 bounds (3.452913920250606, mpf('0.040894244520304449')) (3.7596439169139435, mpf('0.031475519289863502'))
```

```python
import mpmath as mp
m=[57.5,53.3,44.4]; s=[2.6,4.1,3.7]; n=15
g=sum(m)/3; msb=n*sum((x-g)**2 for x in m)/2
msw=sum(x**2 for x in s)/3
print("hour0 if +- were SD: F",msb/msw)
print("MSB",msb,"MSW needed for F=0.88",msb/0.88,"implied pooled SD",(msb/0.88)**0.5,"implied SE",(msb/0.88/15)**0.5)
```
```text
hour0 if +- were SD: F 54.03784219001611
MSB 671.1500000000001 MSW needed for F=0.88 762.6704545454546 implied pooled SD 27.616488816383857 implied SE 7.130546751105204
```

</details>

#### F10 · PMC13631009 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13631009](https://pmc.ncbi.nlm.nih.gov/articles/PMC13631009/) · DOI [10.3389/fphar.2026.1848763](https://doi.org/10.3389/fphar.2026.1848763) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q59bdd494-1`
- **Where in the paper**: Conclusion
- **What the tool checked**: Conclusion claim that 'most participants expressed positive attitudes' versus the attitude-level distribution (Figure 5 text, Table 7)
- **Value as reported in the paper**: most participants expressed positive attitudes
- **What the tool computed**: Positive attitude 47/508 = 9.3%; neutral 315 = 62.0%; negative 146 = 28.7%
- **What the tool flagged** (model summary): The Conclusion says "most participants expressed positive attitudes", but Figure 5 and Table 7 give 47/508 = 9.3% positive, 315/508 = 62.0% neutral and 146/508 = 28.7% negative. The paper's own numbers contradict the conclusion.
- **If the flag holds, what would change** (model reading, not proven): The Conclusion's statement that most participants had positive attitudes would say that only 9.3% had positive attitudes, while the majority (62.0%) were neutral and 28.7% were negative.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13631009, CC BY 4.0):

- `62.0%, 28.7%, 9.3%`, from:

  > "most respondents, 62.0%, maintain a neutral position... 28.7% of participants expressed negative attitudes... only a small fraction, 9.3%, display a positive attitude"

- `Male 21/73/13, Female 125/242/34`, from:

  > "Male | 21 | 14.4 | 73 | 23.2 | 13 | 27.7 ... Female | 125 | 85.6 | 242 | 76.8 | 34 | 72.3"

- The passage that the first finding rests on:

  > "Although most participants expressed positive attitudes, many relied on social media"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
neg=21+125; neu=73+242; pos=13+34; N=508
print("neg,neu,pos,total", neg, neu, pos, neg+neu+pos)
print("pct neg", round(100*neg/N,1), "paper 28.7")
print("pct neu", round(100*neu/N,1), "paper 62.0")
print("pct pos", round(100*pos/N,1), "paper 9.3")
print("pos is majority?", pos/N > 0.5)
print("pos+neu share", round(100*(pos+neu)/N,1))
```
```text
neg,neu,pos,total 146 315 47 508
pct neg 28.7 paper 28.7
pct neu 62.0 paper 62.0
pct pos 9.3 paper 9.3
pos is majority? False
pos+neu share 71.3
```

</details>

#### F11 · PMC13763532 · Foods (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13763532](https://pmc.ncbi.nlm.nih.gov/articles/PMC13763532/) · DOI [10.3390/foods15213998](https://doi.org/10.3390/foods15213998) · *Foods* (2026) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q2539bf5f-3`
- **Where in the paper**: 3.6 Pearson correlation analysis
- **What the tool checked**: Significance of fucoidan–Pb correlation in salted samples (r = −0.18, p < 0.05)
- **Value as reported in the paper**: r = −0.18, p < 0.05
- **What the tool computed**: Two-tailed p = 0.64 with n = 9 harvest dates and 0.37 with n = 27 (9 dates × 3 replicates). |r| = 0.18 reaches p < 0.05 only with n ≥ 120.
- **What the tool flagged** (model summary): Section 3.6 reports the salted fucoidan-Pb correlation as r = -0.18, p < 0.05. With n <= 27 (9 harvest times x 3 replicates) the two-sided p is about 0.37 (0.64 if n = 9); p < 0.05 would need n >= 120, so the 'shift to negative' is not statistically supported.
- **If the flag holds, what would change** (model reading, not proven): The negative fucoidan–Pb correlation after salting is reported as significant, but it is not significant (p ≈ 0.37 or higher). So the claim that Na+ displaced Pb from fucoidan, or that salting degraded fucoidan, has no statistical support. The same problem affects the blanched alginate–Pb correlation (r = 0.23, p < 0.05).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13763532, CC BY 4.0):

- `-0.18`, from:

  > "The fucoidan–Pb correlation shifted from positive to negative (r = −0.18, p < 0.05)."

- `9 time points`, from:

  > "Sampling was conducted at nine 7-day intervals from mid-to-late February to early May 2025"

- `3 replicates`, from:

  > "Data are expressed as the mean ± standard deviation (SD) of three independent replicates."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p(r,n):
    df=n-2
    t=abs(r)*m.sqrt(df/(1-r*r))
    return m.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
for n in [9,27,30,120,270]:
    print("n",n,"r=-0.18 p",m.nstr(p(-0.18,n),4),"r=0.23 p",m.nstr(p(0.23,n),4))
for n in range(9,300):
    if p(0.18,n)<0.05:
        print("min n for r=0.18 sig",n);break
```
```text
n 9 r=-0.18 p 0.6431 r=0.23 p 0.5516
n 27 r=-0.18 p 0.369 r=0.23 p 0.2485
n 30 r=-0.18 p 0.3412 r=0.23 p 0.2214
n 120 r=-0.18 p 0.04915 r=0.23 p 0.0115
n 270 r=-0.18 p 0.002995 r=0.23 p 0.0001373
min n for r=0.18 sig 120
```

</details>

### Group 2 - recomputed and changes a reported result, but did not stay in tier A under v2 (10)

The second pass recomputed the number, and in its reading a reported result changes. The stricter v2 judge or the blind second gate did not keep it in tier A. Each entry says why.

#### F12 · PMC12295857 · Insects (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12295857](https://pmc.ncbi.nlm.nih.gov/articles/PMC12295857/) · DOI [10.3390/insects16070732](https://doi.org/10.3390/insects16070732) · *Insects* (2025) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q78b8dfda-3`
- **Where in the paper**: Results 3.4.1
- **What the tool checked**: Orchard 1 vs orchard 2 immature-female comparison: χ2 = 5.86, df = 1, reported p = 0.119
- **Value as reported in the paper**: χ2 = 5.86, df = 1, p = 0.119
- **What the tool computed**: p = 0.0155 for χ2 = 5.86 with df = 1 (rounding range 5.855–5.865 gives 0.01544–0.01553); a p of 0.119 would need χ2 ≈ 2.43
- **What the tool flagged** (model summary): Section 3.4.1: 'The overall percentage of immature females was also similar between orchard 1 (73 ± 4%) and orchard 2 (89 ± 3%) (chi2 = 5.86, df = 1, p = 0.119)'. Chi2 = 5.86 with df = 1 gives p = 0.015, and the stated means ± SE give z of about 3.2, so, in the model's reading, the difference is significant, not 'similar'.
- **If the flag holds, what would change** (model reading, not proven): The statement that the share of immature females was 'similar' in orchard 1 and orchard 2 (non-significant, p = 0.119) would change to a significant difference (p ≈ 0.016) if the χ2 value is correct.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12295857, CC BY 4.0):

- `5.86`, from:

  > "(mean 89 ± 3%) (χ2 = 5.86, df = 1, p = 0.119)"

- `df = 1`, from:

  > "(χ2 = 5.86, df = 1, p = 0.119)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
for x in [5.855,5.86,5.865]:
    print("chi2",x,"p",mpmath.gammainc(0.5,x/2,mpmath.inf,regularized=True))
print("chi2 for p=0.119", mpmath.findroot(lambda c: mpmath.gammainc(0.5,c/2,mpmath.inf,regularized=True)-0.119, 2.4))
```
```text
chi2 5.855 p 0.0155328580295606
chi2 5.86 p 0.0154887940092
chi2 5.865 p 0.0154448587590173
chi2 for p=0.119 2.430433314079
```

</details>

#### F13 · PMC12797519 · BMC Nurs (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12797519](https://pmc.ncbi.nlm.nih.gov/articles/PMC12797519/) · DOI [10.1186/s12912-025-04180-9](https://doi.org/10.1186/s12912-025-04180-9) · *BMC Nurs* (2025) · field: nursing_public_health · licence: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Run id**: `R1-qa4b8bf75-1`
- **Where in the paper**: Table 3 vs Table 1 / Methods
- **What the tool checked**: Table 3 n for Technical Institute (36) and the total n of the education Kruskal-Wallis analysis, compared with Table 1 and the study n = 160
- **Value as reported in the paper**: Table 3: TI n=36; group ns 36+149+28+22 = 235
- **What the tool computed**: Table 1: TI n=24; group ns 24+106+19+11 = 160. The mean ranks in Table 3 average to 118.001 ≈ (235+1)/2, so the test was actually run on 235 observations
- **What the tool flagged** (model summary): In Table 3 the group ns of every Kruskal-Wallis block sum to 235 (e.g. education 36/149/28/22), and the mean ranks average to 118 = (235+1)/2. Table 1 gives 160 nurses (education 24/106/19/11; exposure 65/7/32/56), so the Table 3 tests do not describe the stated sample.
- **If the flag holds, what would change** (model reading, not proven): The education Kruskal-Wallis result (H=12.702, p=0.005) and the other Table 3 tests rest on 235 observations, while the study has 160 nurses. The group sizes (for example TI 36 vs 24) do not seem to fit the sample description, so these factor analyses would need checking.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12797519, CC BY-NC-ND 4.0):

- `36`, from:

  > "Technical Institute | 36 | 95.875 | 12.702 (3) | 0.005"

- `149`, from:

  > "Bachelor’s in Nursing Sciences | 149 | 115.36"

- `28`, from:

  > "University Diploma | 28 | 128.25"

- `22`, from:

  > "Higher Education | 22 | 159.05"

- `24`, from:

  > "Technical Institute | 24 (15%)"

- `106`, from:

  > "Bachelor’s in Nursing Sciences | 106 (66.3%)"

- `19`, from:

  > "University Diploma | 19 (11.9%)"

- `11`, from:

  > "Higher Education | 11 (6.9%)"

- The passage that the first finding rests on:

  > "Technical Institute | 36 | 95.875"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 8/8 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
n3=[36,149,28,22]; r=[95.875,115.36,128.25,159.05]; n1=[24,106,19,11]; N=sum(n3); print("T3 total",N,"T1 total",sum(n1)); print("T3 TI n",36,"T1 TI n",24); print("weighted mean rank",sum(a*b for a,b in zip(n3,r))/N,"expected (N+1)/2",(N+1)/2); print("other T3 totals",sum([68,60,27,5,54,21]),sum([101,11,56,67]),sum([21,94,81,20,19]))
```
```text
T3 total 235 T1 total 160
T3 TI n 36 T1 TI n 24
weighted mean rank 118.00102127659574 expected (N+1)/2 118.0
other T3 totals 235 235 235
```

</details>

#### F14 · PMC12821694 · J Funct Morphol Kinesiol (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12821694](https://pmc.ncbi.nlm.nih.gov/articles/PMC12821694/) · DOI [10.3390/jfmk11010003](https://doi.org/10.3390/jfmk11010003) · *J Funct Morphol Kinesiol* (2025) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q1f88b004-1`
- **Where in the paper**: Results 3.2
- **What the tool checked**: Mean daily energy deficit of males (~2981 kcal/day) and females (~2228 kcal/day) in Results 3.2, checked against daily EE, NI and the Results 3.1 energy balance
- **Value as reported in the paper**: males ~2981 kcal deficit per day; females ~2228 kcal deficit per day
- **What the tool computed**: EE − NI = 1420.8 (males) and 972.67 (females) kcal/day. Section 3.1 reports −1350 ± 674 and −975 ± 671. The largest possible daily deficit (NI = 0) is 2540.8 and 1942.67 kcal, and both are smaller than the reported deficits.
- **What the tool flagged** (model summary): Section 3.2 reports mean daily deficits against EE of about 2981 kcal for males and 2228 kcal for females. These values do not seem possible, because they are larger than the reported mean EE (2540.8 and 1942.67 kcal/day). It also contradicts Section 3.1 (−1350 and −975 kcal) and intake minus EE (−1421 and −973).
- **If the flag holds, what would change** (model reading, not proven): The reported daily deficits (~2981 and ~2228 kcal) contradict the 3.1 values (−1350 and −975) and are larger than total daily expenditure. The size of the energy deficit would be too large by roughly a factor of 2.2. The conclusion that a deficit exists stays the same.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12821694, CC BY 4.0):

- `2540.8`, from:

  > "male cadets expended 2540.8 ± 638.9 kcal/day, while female cadets expended 1942.67 ± 368.58 kcal/day"

- `1942.67`, from:

  > "female cadets expended 1942.67 ± 368.58 kcal/day"

- `1120 / 970`, from:

  > "Mean total energy intake was 1120 ± 486 kcal for male cadets and 970 ± 422 kcal for female cadets"

- `−1350 / −975`, from:

  > "male cadets demonstrated an energy deficit of −1350 ± 674 kcal, while female cadets exhibited a deficit of −975 ± 671 kcal"

- `2981 / 2228`, from:

  > "males averaging a deficit of approximately 2981 kcal and females with an approximate deficit of 2228 kcal per day"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 5/5 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
EEm=2540.8
EEf=1942.67
NIm=1120
NIf=970
print("male EE-NI", EEm-NIm, "reported 3.1", -1350, "passage", 2981)
print("female EE-NI", EEf-NIf, "reported 3.1", -975, "passage", 2228)
print("max possible daily deficit male (NI=0)", EEm, "female", EEf)
print("ratio passage/3.1 male", 2981/1350, "female", 2228/975)
```
```text
male EE-NI 1420.8000000000002 reported 3.1 -1350 passage 2981
female EE-NI 972.6700000000001 reported 3.1 -975 passage 2228
max possible daily deficit male (NI=0) 2540.8 female 1942.67
ratio passage/3.1 male 2.208148148148148 female 2.285128205128205
```

</details>

#### F15 · PMC13003745 · BMC Sports Sci Med Rehabil (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13003745](https://pmc.ncbi.nlm.nih.gov/articles/PMC13003745/) · DOI [10.1186/s13102-026-01545-8](https://doi.org/10.1186/s13102-026-01545-8) · *BMC Sports Sci Med Rehabil* (2026) · field: sports_exercise · licence: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Run id**: `R1-qcf65dfaa-1`
- **Where in the paper**: Discussion paragraph 4 vs Table 3
- **What the tool checked**: Discussion claim of significant CKCUEST improvement within the experimental (mace) group, p < 0.001
- **Value as reported in the paper**: significant improvements in upper extremity stabilization ... CKCUEST in the experimental group (p < 0.001)
- **What the tool computed**: Mace group mean change = +0.09 reps (25.83 to 25.92). Even under the most favourable assumption (pre-post r = 1, so SD of change = |2.59-2.39|), the paired t is at most 1.62 (p = 0.13). At the rounding extremes it is 1.90 (p = 0.082). Neither reaches p < 0.05, let alone p < 0.001. The control group fell by 2.00 reps, and that decline drives the interaction.
- **What the tool flagged** (model summary): Table 3 gives CKCUEST 25.83→25.92 for mace and 25.80→23.80 for control, and push-ups 43.00→43.17 for mace and 42.60→39.33 for control. The significant interactions therefore come from a decline in the control group. This contradicts the Results text ('improved over time in both groups') and the Discussion claim of significant CKCUEST improvement in the experimental group (p<0.001).
- **If the flag holds, what would change** (model reading, not proven): The Discussion's statement that CKCUEST significantly improved in the experimental group (p < 0.001) changes to: no meaningful change in the mace group (+0.09 reps, at best p ≈ 0.08–0.13). The significant interaction reflects a 2-rep decline in the control group, not a gain from mace training.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13003745, CC BY-NC-ND 4.0):

- `25.83 ± 2.59 | 25.92 ± 2.39`, from:

  > "CKCUEST (rep. num) | 25.83 ± 2.59 | 25.92 ± 2.39 | 25.80 ± 1.74 | 23.80 ± 1.66 | 0.660*"

- `25.80 ± 1.74 | 23.80 ± 1.66`, from:

  > "CKCUEST (rep. num) | 25.83 ± 2.59 | 25.92 ± 2.39 | 25.80 ± 1.74 | 23.80 ± 1.66 | 0.660*"

- `n = 13`, from:

  > "assigned to either a mace training group (n = 13) or a control group (n = 14)"

- The passage that the first finding rests on:

  > "significant improvements in upper extremity stabilization, as indicated by the Closed Kinetic Chain Upper Extremity Stability Test (CKCUEST) in the experimental group (p < 0.001)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
n=13
def p2(t,df):
    return m.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
d=25.92-25.83
sdmin=2.59-2.39
t=d/(sdmin/m.sqrt(n))
print("mace change",d,"control change",23.80-25.80)
print("best case paired t (r=1)",t,"p",p2(t,n-1))
dmax=25.925-25.825
sdmin2=2.585-2.395
t2=dmax/(sdmin2/m.sqrt(n))
print("rounding extreme t",t2,"p",p2(t2,n-1))
print("interaction F=48.495 df(1,25) p",p2(m.sqrt(48.495),25))
```
```text
mace change 0.09000000000000341 control change -2.0
best case paired t (r=1) 1.62249807395886 p 0.130657894109446
rounding extreme t 1.89765856603371 p 0.0820559845722077
interaction F=48.495 df(1,25) p 2.67288860443337e-7
```

</details>

#### F16 · PMC13168142 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13168142](https://pmc.ncbi.nlm.nih.gov/articles/PMC13168142/) · DOI [10.3389/fphar.2026.1801073](https://doi.org/10.3389/fphar.2026.1801073) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q8022901e-4`
- **Where in the paper**: Results, Y-maze paragraph
- **What the tool checked**: Time spent in each arm: F(3,36)=2.85 reported with p < 0.01
- **Value as reported in the paper**: F(3,36)=2.85, p < 0.01
- **What the tool computed**: p = 0.051 (range 0.0506–0.0512 across the rounding bounds of F)
- **What the tool flagged** (model summary): Results, Y-maze: F(3,36)=3.22 (spontaneous alternation) gives p=0.034, not p<0.01. F(3,36)=2.85 (arm time) gives p=0.051, which is not significant, not p<0.01.
- **If the flag holds, what would change** (model reading, not proven): The overall treatment effect on arm time (novel-arm exploration) changes from significant (p<0.01) to not significant (p≈0.051 > 0.05). This undermines the claim that RA and 3-HT increased novel-arm time, which also appears in the Abstract.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13168142, CC BY 4.0):

- `2.85`, from:

  > "time spent in each arm [F (3, 36) = 2.85, p < 0.01] (Figure 2B)"

- `3, 36`, from:

  > "time spent in each arm [F (3, 36) = 2.85, p < 0.01] (Figure 2B)"

- The passage that the first finding rests on:

  > "spontaneous alternation [F (3, 36) = 3.22, p < 0.01] (Figure 2A), time spent in each arm [F (3, 36) = 2.85, p < 0.01]"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
def p(F,d1,d2):
    x=d2/(d2+d1*F)
    return mpmath.betainc(d2/2,d1/2,0,x,regularized=True)
for F in [3.22,3.215,3.225,2.85,2.845,2.855,19.48,1.59,8.02,7.85,2.78,3.14,7.71]:
    print("F",F,"p",mpmath.nstr(p(F,3,36),6))
```
```text
F 3.22 p 0.0339778
F 3.215 p 0.0341626
F 3.225 p 0.0337941
F 2.85 p 0.0509027
F 2.845 p 0.0511835
F 2.855 p 0.0506234
F 19.48 p 1.1279e-7
F 1.59 p 0.208728
F 8.02 p 0.000320223
F 7.85 p 0.000371235
F 2.78 p 0.0549838
F 3.14 p 0.0370622
F 7.71 p 0.000419656
```

</details>

#### F17 · PMC13291109 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13291109](https://pmc.ncbi.nlm.nih.gov/articles/PMC13291109/) · DOI [10.3389/fphar.2026.1776775](https://doi.org/10.3389/fphar.2026.1776775) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q7a98d23d-1`
- **Where in the paper**: Table 4 clinical remission column vs Results/Abstract
- **What the tool checked**: Overall clinical remission 67/101 (66.34%) vs sum of Table 4 remission counts across severity strata
- **Value as reported in the paper**: 67/101 (66.34%)
- **What the tool computed**: 17+29+1 = 47/101 (46.53%)
- **What the tool flagged** (model summary): Table 4 clinical remission counts by severity (17/24, 29/61, 1/16) sum to 47/101 = 46.5%, but the Abstract and Results report 67/101 = 66.34%. The response and mucosal healing columns sum correctly to 95 and 77.
- **If the flag holds, what would change** (model reading, not proven): The headline clinical remission rate (66.34%, 67/101) in the Abstract, Results and Discussion conflicts with the stratified table, which gives 47/101 (46.53%). The 47/101 figure would weaken the claim that remission beats the historical budesonide/vedolizumab rates (about 47–54%).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13291109, CC BY 4.0):

- `67/101`, from:

  > "a clinical remission rate of 66.34% (67/101)"

- `17/24`, from:

  > "Mild | 24 | 24/24 (100.00) | 17/24 (70.83) | 21/24 (87.50)"

- `29/61`, from:

  > "Moderate | 61 | 59/61 (96.72) | 29/61 (47.54) | 48/61 (78.68)"

- `1/16`, from:

  > "Severe | 16 | 12/16 (75.00) | 1/16 (6.25) | 8/16 (50.00)"

- The passage that the first finding rests on:

  > "clinical remission rate of 66.34% (67/101)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: left the v2 register: the v2 judge logged no code check for it
- Quotes word for word in the paper text (program): 4/4 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): partly: the numbers are in the logged runs, but split over runs or abbreviated. A model session checked this by reading the logs, not a human

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
def chi(a,n):
    t=sum(a);N=sum(n);s=0
    for x,m in zip(a,n):
        e1=m*t/N;e0=m*(N-t)/N
        s+=(x-e1)**2/e1+((m-x)-e0)**2/e0
    return s, mpmath.gammainc(1,s/2,mpmath.inf,regularized=True)
n=[24,61,16]
print("response sum",24+59+12,"paper 95")
print("remission sum",17+29+1,"paper 67")
print("healing sum",21+48+8,"paper 77")
print("pct 67/101",round(67/101*100,2),"47/101",round(47/101*100,2))
print("chi resp",chi([24,59,12],n),"paper 12.691")
print("chi remis",chi([17,29,1],n),"paper 26.094")
print("chi heal",chi([21,48,8],n),"paper 7.963")
print("pcts",17/24*100,29/61*100,1/16*100)
```
```text
response sum 95 paper 95
remission sum 47 paper 67
healing sum 77 paper 77
pct 67/101 66.34 47/101 46.53
chi resp (12.691084268047168, mpf('0.0017545512828850814')) paper 12.691
chi remis (16.156666887355907, mpf('0.00031018754992116488')) paper 26.094
chi heal (7.962749937903627, mpf('0.01865996481867677')) paper 7.963
pcts 70.83333333333334 47.540983606557376 6.25
```

```python
def chi(a,n):
    t=sum(a);N=sum(n);s=0
    for x,m in zip(a,n):
        e1=m*t/N;e0=m*(N-t)/N
        s+=(x-e1)**2/e1+((m-x)-e0)**2/e0
    return s
n=[24,61,16]
for a in range(0,25):
    for b in range(0,62):
        for c in range(0,17):
            if 0<a+b+c<101:
                v=chi([a,b,c],n)
                if abs(v-26.094)<0.0006: print(a,b,c,a+b+c,round(v,3))
```
```text
1 19 13 33 26.094
3 43 12 58 26.094
5 47 13 65 26.094
9 18 16 43 26.094
15 43 0 58 26.094
19 14 3 36 26.094
21 18 4 43 26.094
23 42 3 68 26.094
```

</details>

#### F18 · PMC13513319 · Insects (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13513319](https://pmc.ncbi.nlm.nih.gov/articles/PMC13513319/) · DOI [10.3390/insects17080828](https://doi.org/10.3390/insects17080828) · *Insects* (2026) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q9f09ff6c-2`
- **Where in the paper**: Section 3.2 vs Section 2.3/2.5
- **What the tool checked**: Significance claim p < 0.05 for larval Cd (Cd vs control) under a Mann–Whitney U test with 3 replicates per group
- **Value as reported in the paper**: p < 0.05
- **What the tool computed**: Smallest possible exact two-sided Mann–Whitney p for 3 vs 3 = 0.1. Normal approximation with continuity correction: 0.081. Uncorrected normal approximation: 0.0495.
- **What the tool flagged** (model summary): Section 2.3 says larval, female pupal and female adult Cd were measured with three biological replicates per group. Section 2.5 says these were compared with Mann–Whitney U tests. For 3 vs 3, the smallest possible exact two-sided p is 2/C(6,3) = 0.10. The 'p < 0.05' reported in Section 3.2 for all three stages therefore cannot come from the test described. The egg comparison (5 vs 5) could reach p < 0.05.
- **If the flag holds, what would change** (model reading, not proven): The larval Cd difference cannot reach p < 0.05 with the stated test and n. The reported significance would change to non-significant (p ≥ 0.1). The same limit applies to the female pupa and female adult comparisons, which also used n = 3 per group.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13513319, CC BY 4.0):

- `n = 3 per group (larvae)`, from:

  > "Notably, five replicates were prepared for egg Cd detection instead of three replicates used for larval, pupal and adult samples from Cd treatment and control."

- `Mann–Whitney U, GraphPad Prism`, from:

  > "For whole-body Cd concentration data across developmental stages, the data deviated from normal distribution; thus, non-parametric Mann–Whitney U tests were adopted for pairwise comparisons between treatments (p < 0.05)."

- `p < 0.05`, from:

  > "Larval Cd concentration reached 38.07 ± 3.22 mg/kg in the Cd treatment group, markedly higher than the control level of 0.08 ± 0.01 mg/kg (Table 1, p < 0.05)."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: the v2 judge gave tier D (not a real discrepancy, in its reading)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import itertools, mpmath
n1=3
n2=3
vals=list(range(6))
cnt=0
tot=0
for c in itertools.combinations(vals,n1):
    tot+=1
    U=sum(1 for a in c for b in vals if b not in c and a>b)
    if U==0 or U==9: cnt+=1
print("exact two-sided min p n=3v3", cnt/tot)
sd=mpmath.sqrt(n1*n2*(n1+n2+1)/mpmath.mpf(12))
z=4.5/sd
print("normal approx no cc p", mpmath.erfc(z/mpmath.sqrt(2)))
z2=4.0/sd
print("normal approx with cc p", mpmath.erfc(z2/mpmath.sqrt(2)))
print("paper p", "< 0.05")
```
```text
exact two-sided min p n=3v3 0.1
normal approx no cc p 0.0495346134356267
normal approx with cc p 0.0808555983700523
paper p < 0.05
```

</details>

#### F19 · PMC13587494 · BMC Sports Sci Med Rehabil (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13587494](https://pmc.ncbi.nlm.nih.gov/articles/PMC13587494/) · DOI [10.1186/s13102-026-01816-4](https://doi.org/10.1186/s13102-026-01816-4) · *BMC Sports Sci Med Rehabil* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q34dcb204-2`
- **Where in the paper**: Table 1, BMI row
- **What the tool checked**: Table 1 BMI means vs height and body-weight means of the same groups
- **Value as reported in the paper**: BMI IWU 24.77, Control 23.73 kg/m2
- **What the tool computed**: Weight/height^2 from the group means: IWU 25.78, Control 25.88 kg/m2
- **What the tool flagged** (model summary): Table 1: mean weight / mean height² gives BMI 25.78 (IWU: 84.35 kg, 180.90 cm) and 25.88 (control: 83.33 kg, 179.44 cm), but the table reports 24.77 and 23.73. A t-test on the reported BMI means and SDs (24.77 ± 1.35 vs 23.73 ± 0.63) gives t of about 2.1–2.2 and p of about 0.04–0.05, not 0.089, while the other three p-values in the table reproduce (with control n = 9).
- **If the flag holds, what would change** (model reading, not proven): The reported BMI means are about 1.0 (IWU) and 2.15 (Control) kg/m2 lower than the height and weight data imply. The BMI group comparison and its p value therefore rest on inconsistent numbers. The conclusion of homogeneous groups probably does not change.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13587494, CC BY 4.0):

- `180.90 / 84.35 / 24.77`, from:

  > "Height (cm) | 180.90 | 4.89 | 179.44 | 4.07 | 0.493 ... Body weight (kg) | 84.35 | 6.25 | 83.33 | 3.20 | 0.667 ... BMI (kg/m2) | 24.77 | 1.35 | 23.73 | 0.63 | 0.089"

- `179.44 / 83.33 / 23.73`, from:

  > "Height (cm) | 180.90 | 4.89 | 179.44 | 4.07 | 0.493"

- The passage that the first finding rests on:

  > "BMI (kg/m2) | 24.77 | 1.35 | 23.73 | 0.63 | 0.089"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as mp
def tp(t,df):
    return mp.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
m1,s1,m2,s2=24.77,1.35,23.73,0.63
for n1,n2 in [(10,10),(10,9)]:
    sp=((n1-1)*s1**2+(n2-1)*s2**2)/(n1+n2-2)
    t=(m1-m2)/mp.sqrt(sp*(1/n1+1/n2))
    v1,v2=s1**2/n1,s2**2/n2
    tw=(m1-m2)/mp.sqrt(v1+v2)
    dfw=(v1+v2)**2/(v1**2/(n1-1)+v2**2/(n2-1))
    print(n1,n2,"student t",t,"p",tp(t,n1+n2-2),"welch t",tw,"df",dfw,"p",tp(tw,dfw))
print("paper p 0.089")
print("BMI from means IWU",84.35/1.809**2,"paper 24.77")
print("BMI from means CON",83.33/1.7944**2,"paper 23.73")
for lo,hi in [(24.765,24.775)]:
    pass
print("BMI IWU range",84.345/1.80905**2,84.355/1.80895**2)
print("BMI CON range",83.325/1.79445**2,83.335/1.79435**2)
```
```text
10 10 student t 2.20757541304696 p 0.0404922983670261 welch t 2.20757541304696 df 12.742503677441254 p 0.0462496433139461
10 9 student t 2.10921776035979 p 0.0500579841443978 welch t 2.18596442521403 df 13.024581091863787 p 0.04767340156665
paper p 0.089
BMI from means IWU 25.77555072130289 paper 24.77
BMI from means CON 25.879915898255017 paper 23.73
BMI IWU range 25.772598121293402 25.77850360838046
BMI CON range 25.87692092786477 25.882911162286835
```

```python
import mpmath as mp
def tp(t,df):
    return mp.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
rows=[("height",180.90,4.89,179.44,4.07,0.493),("weight",84.35,6.25,83.33,3.20,0.667),("age",23.10,2.56,22.78,1.39,0.742),("bmi",24.77,1.35,23.73,0.63,0.089)]
for nm,m1,s1,m2,s2,pp in rows:
    for n1,n2 in [(10,10),(10,9)]:
        sp=((n1-1)*s1**2+(n2-1)*s2**2)/(n1+n2-2)
        t=(m1-m2)/mp.sqrt(sp*(1/n1+1/n2))
        print(nm,n1,n2,"paper",pp,"student p",mp.nstr(tp(t,n1+n2-2),4))
```
```text
height 10 10 paper 0.493 student p 0.4774
height 10 9 paper 0.493 student p 0.4918
weight 10 10 paper 0.667 student p 0.6515
weight 10 9 paper 0.667 student p 0.6657
age 10 10 paper 0.742 student p 0.7323
age 10 9 paper 0.742 student p 0.7433
bmi 10 10 paper 0.089 student p 0.04049
bmi 10 9 paper 0.089 student p 0.05006
```

</details>

#### F20 · PMC13637671 · Front Public Health (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13637671](https://pmc.ncbi.nlm.nih.gov/articles/PMC13637671/) · DOI [10.3389/fpubh.2026.1927794](https://doi.org/10.3389/fpubh.2026.1927794) · *Front Public Health* (2026) · field: nursing_public_health · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q33e96d6d-5`
- **Where in the paper**: Q11 post hoc text / Table 31
- **What the tool checked**: Claim that the Student–Public post hoc difference for Q11 is statistically significant (Table 31: t=1.7935, P=3.7%)
- **Value as reported in the paper**: t=1.7935, P=3.7% → 'Different' / 'statistically significant'
- **What the tool computed**: Two-tailed p for t=1.7935 with df=347 is 0.0738 (7.4%). The reported 3.7% is the one-tailed p (3.69%). The other rows of Table 31 are one-tailed too (35.6, 11.0).
- **What the tool flagged** (model summary): The Q11 text claims a significant Student-Public difference (Table 31: t=1.7935, P=3.7%). The two-tailed p for df=347 is about 0.074, and the omnibus ANOVA is non-significant (p=0.1907). The reported significance comes from an unstated one-tailed p and should not be claimed.
- **If the flag holds, what would change** (model reading, not proven): With the standard two-tailed test, the Student–Public difference for Q11 is not significant (p≈0.074). The conclusion changes from 'a statistically significant difference only between students and the general public' to 'no pairwise difference is significant', which matches the non-significant omnibus ANOVA.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13637671, CC BY 4.0):

- `t=1.7935, P=3.7`, from:

  > "Student-Public | 1.0063 | 48.7 | Equal variance | 1.7935 | 3.7 | Different"

- `n=204, 145`, from:

  > "comprising 204 students (41.5%), 145 members of the general public (29.5%)"

- `Public-Seafarer t −0.3696 P 35.6; Student-Seafarer t 1.2273 P 11.0`, from:

  > "Public-Seafarer | 0.7365 | 3.4 | Unequal variance | −0.3696 | 35.6 | Same"

- The passage that the first finding rests on:

  > "Post hoc comparisons for Q11 revealed a statistically significant difference only between students and members of the general public"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
m1,s1,n1=4.3333,0.4696,204
m2,s2,n2=4.2000,0.4666,145
df=n1+n2-2
sp2=((n1-1)*s1**2+(n2-1)*s2**2)/df
t=(m1-m2)/m.sqrt(sp2*(1/n1+1/n2))
p1=m.betainc(df/2,0.5,0,df/(df+t**2),regularized=True)/2
print("t paper 1.7935 recomputed",t)
print("one-tailed p",p1,"two-tailed p",2*p1, "paper P 3.7 percent")
tp=1.7935
pp=m.betainc(df/2,0.5,0,df/(df+tp**2),regularized=True)
print("two-tailed p at paper t",pp)
F=1.6625
p=m.betainc(244,1,0,488/(488+2*F),regularized=True)
print("omnibus p paper 0.1907 recomputed",p)
```
```text
t paper 1.7935 recomputed 2.62022844363238
one-tailed p 0.0045866113130476 two-tailed p 0.00917322262609521 paper P 3.7 percent
two-tailed p at paper t 0.0737636411615649
omnibus p paper 0.1907 recomputed 0.190736601272968
```

```python
ms=[4.3333,4.2000,4.2323]
sd=[0.4696,0.4666,0.6335]
n=[204,145,142]
N=sum(n)
g=sum(a*b for a,b in zip(ms,n))/N
ssb=sum(b*(a-g)**2 for a,b in zip(ms,n))
ssw=sum((b-1)*s**2 for s,b in zip(sd,n))
print("SSB paper 1.7161 recomputed",ssb)
print("SSW paper 251.8643 recomputed",ssw)
print("F paper 1.6625 recomputed",(ssb/2)/(ssw/488))
```
```text
SSB paper 1.7161 recomputed 1.7160645118126308
SSW paper 251.8643 recomputed 132.70388237
F paper 1.6625 recomputed 3.155293827160408
```

```python
import mpmath as m
def p2(t,df):
    return m.betainc(df/2,0.5,0,df/(df+t**2),regularized=True)
for name,t,df,pp in [("Stud-Pub",1.7935,347,3.7),("Pub-Sea",0.3696,285,35.6),("Stud-Sea",1.2273,344,11.0)]:
    print(name,"paper P%",pp,"one-tailed %",100*p2(t,df)/2,"two-tailed %",100*p2(t,df))
for t in [1.79345,1.79355]:
    print("bounds t",t,"two-tailed",p2(t,347))
print("t from pooled MSW", 0.1333/m.sqrt(0.5161*(1/204+1/145)))
```
```text
Stud-Pub paper P% 3.7 one-tailed % 3.68818205807825 two-tailed % 7.37636411615649
Pub-Sea paper P% 35.6 one-tailed % 35.597751210071 two-tailed % 71.195502420142
Stud-Sea paper P% 11.0 one-tailed % 11.0274540507401 two-tailed % 22.0549081014803
bounds t 1.79345 two-tailed 0.0737716458686058
bounds t 1.79355 two-tailed 0.0737556371677737
t from pooled MSW 1.70824276979368
```

</details>

#### F21 · PMC13731344 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13731344](https://pmc.ncbi.nlm.nih.gov/articles/PMC13731344/) · DOI [10.3389/fphar.2026.1965339](https://doi.org/10.3389/fphar.2026.1965339) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qd372f837-2`
- **Where in the paper**: Table 1, column 'Prescriptions with ≥1 pDDI', by number of concomitant drugs
- **What the tool checked**: pDDI counts summed across concomitant-drug groups compared with the total of 684 pDDI prescriptions
- **Value as reported in the paper**: 622 + 172 + 13 = 807 (total stated as 684)
- **What the tool computed**: 807 vs 684. Gender (240+444) and age (85+330+269) both sum to 684, and the group denominators sum to 3476
- **What the tool flagged** (model summary): In Table 1 the pDDI-positive prescriptions by number of concomitant drugs (622 + 172 + 13) sum to 807, not the 684 reported in the text and obtained from the gender (240 + 444) and age (85 + 330 + 269) rows. The stratum denominators sum correctly to 3476, so at least one drug-count cell does not fit (for example 622 (19.93%) would need to be 499 (15.99%)).
- **If the flag holds, what would change** (model reading, not proven): The 2–3 drug count and percentage (622, 19.93%) cannot be reconciled with the overall 684/3476 (19.68%). Both the size of the polypharmacy contrast and the chi-square of 200.79 depend on which value is correct (622 gives 186.4; 499 gives 264.5).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13731344, CC BY 4.0):

- `622`, from:

  > "2–3 | 3121 (89.79) | 622 (19.93)"

- `172`, from:

  > "4–6 | 334 (9.61) | 172 (51.50)"

- `13`, from:

  > "≧7 | 21 (0.60) | 13 (61.90)"

- `684`, from:

  > "A total of 684 prescriptions (19.68%, 684/3476) were identified with 1404 pDDIs"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 4/4 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import numpy as np
print("622/3121", 622/3121*100, "172/334", 172/334*100, "13/21", 13/21*100)
print("sum drug", 622+172+13, "sum gender", 240+444, "sum age", 85+330+269, "total rows", 3121+334+21)
def chi(a,n):
    a=np.array(a,float);n=np.array(n,float);b=n-a;O=np.array([a,b]);E=np.outer(O.sum(1),O.sum(0))/O.sum();return ((O-E)**2/E).sum()
print("chi drug 622", chi([622,172,13],[3121,334,21]))
print("chi drug 499", chi([499,172,13],[3121,334,21]))
print("chi gender", chi([240,444],[1417,2059]), "chi age", chi([85,330,269],[421,1318,1737]))
```
```text
622/3121 19.929509772508812 172/334 51.49700598802395 13/21 61.904761904761905
sum drug 807 sum gender 684 sum age 684 total rows 3476
chi drug 622 186.39901221687657
chi drug 499 264.5184478555322
chi gender 11.367694165454008 chi age 43.33409388408917
```

</details>

### Group 3 - text comparison only, changes a reported result (8)

The second pass did not recompute a statistic. Its code only compares statements, or a value with a threshold. In its reading, a reported result changes. A text comparison depends more on how the model reads the paper.

#### F22 · PMC11670870 · Nurs Open (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC11670870](https://pmc.ncbi.nlm.nih.gov/articles/PMC11670870/) · DOI [10.1002/nop2.70099](https://doi.org/10.1002/nop2.70099) · *Nurs Open* (2025) · field: nursing_public_health · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q54daeea1-2`
- **Where in the paper**: Abstract / Objective II overestimation regression (Table 6)
- **What the tool checked**: Statement that patients with education at or below year 11 were MORE likely to overestimate, together with anticoagulant use
- **Value as reported in the paper**: Both anticoagulant use and education ≤ year 11 increase the likelihood of overestimation
- **What the tool computed**: The two predictors have opposite signs in the same model (anticoagulant +0.528, std +0.364; education < year 11 −0.490, std −0.345), and the Table 5 correlations also have opposite signs (+0.33 vs −0.32). So they cannot both point toward more overestimation.
- **What the tool flagged** (model summary): Table 6 gives anticoagulant use B = +0.528 (β = 0.364) and education < year 11 B = −0.490 (β = −0.345) for the same outcome. Table 5 shows the same pattern (+0.33 vs −0.32, with postgraduate +0.29). Yet the Abstract and Results say both factors make patients more likely to overestimate their falls risk. One of these two directional claims contradicts the paper's own coefficients.
- **If the flag holds, what would change** (model reading, not proven): The Abstract, Impact and Results conclusion that lower education (≤ year 11) predicts overestimation would instead read that it is associated with less overestimation (or, under the other coding, the anticoagulant finding reverses).

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC11670870, CC BY 4.0):

- `0.528 / 0.364`, from:

  > "Anticoagulant medication use | 0.528 | 0.176 | 0.174 | 0.882 | 0.364 | 0.004"

- `−0.490 / −0.345`, from:

  > "Highest Education attained (< year 11) | −0.490 | 0.173 | −0.837 | −0.143 | −0.345 | 0.007"

- `0.33, −0.32`, from:

  > "Anticoagulant medication use | 0.33** ... Highest education attained (< year 11) | −0.32*"

- The passage that the first finding rests on:

  > "patients were more likely to overestimate their falls risk if they used anticoagulant medication and if their highest education level was less than or equal year 11."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): partly: the numbers are in the logged runs, but split over runs or abbreviated. A model session checked this by reading the logs, not a human

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p2(t,df):
    return m.betainc(df/2,0.5,0,df/(df+t*t),regularized=True)
F=8.841;k=2;d2=50
R2=F*k/(F*k+d2);n=k+d2+1
print("R2",R2,"adjR2",1-(1-R2)*(n-1)/(n-k-1),"paper 0.232")
print("pF",p2(1,1)*0+m.betainc(d2/2,k/2,0,d2/(d2+k*F),regularized=True))
for name,b,se,lo,hi,pp in [("anticoag",0.528,0.176,0.174,0.882,0.004),("edu<11",-0.490,0.173,-0.837,-0.143,0.007)]:
    t=b/se;tc=2.0085591
    print(name,"t",t,"p",p2(t,50),"paper",pp,"CI",b-tc*se,b+tc*se,"paper",lo,hi,"sign",m.sign(b))
print("Table5 rho signs: anticoag 0.33, edu<11 -0.32")
```
```text
R2 0.2612511450607251 adjR2 0.2317011908631541 paper 0.232
pF 0.000515727771394724
anticoag t 3.0000000000000004 p 0.00420170318706824 paper 0.004 CI 0.17449359840000006 0.8815064016 paper 0.174 0.882 sign 1.0
edu<11 t -2.832369942196532 p 0.00664267601539219 paper 0.007 CI -0.8374807243 -0.14251927570000006 paper -0.837 -0.143 sign -1.0
Table5 rho signs: anticoag 0.33, edu<11 -0.32
```

</details>

#### F23 · PMC12648369 · Glob Chang Biol (2025)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12648369](https://pmc.ncbi.nlm.nih.gov/articles/PMC12648369/) · DOI [10.1111/gcb.70623](https://doi.org/10.1111/gcb.70623) · *Glob Chang Biol* (2025) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q30ebd430-3`
- **Where in the paper**: Abstract
- **What the tool checked**: Abstract claim that total abundance increases more rapidly in wintering than in breeding communities
- **Value as reported in the paper**: Abstract: abundance is 'increasing more rapidly in wintering compared to breeding communities'
- **What the tool computed**: Results: abundance difference not significant, p = 0.077 > 0.05
- **What the tool flagged** (model summary): The Abstract says taxonomic and functional richness 'along with total abundance' increase more rapidly in wintering than breeding Baltic communities. The Results (wintering vs breeding section) say there was no significant difference in abundance (R2 = 0.011; p = 0.077), and the Discussion names only taxonomic and functional richness.
- **If the flag holds, what would change** (model reading, not proven): The abstract presents abundance as increasing faster in wintering communities. The paper's own result (p = 0.077) shows no significant seasonal difference in abundance, so the abstract claim should cover only taxonomic and functional richness.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12648369, CC BY 4.0):

- `0.077`, from:

  > "we did not find significant differences in Shannon diversity (R² < 0.001; p = 0.647), abundance (R² = 0.011; p = 0.077) and functional diversity trends (R² = 0.008; p = 0.132) between the two sampling seasons"

- The passage that the first finding rests on:

  > "taxonomic and functional richness, along with total abundance, are increasing more rapidly in wintering compared to breeding communities"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 1/1 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
r={"taxonomic richness":0.019,"functional richness":0.016,"abundance":0.077,"Shannon":0.647,"FEve":0.132}
for k,v in r.items(): print(k,"p =",v,"significant at 0.05:",v<0.05)
```
```text
taxonomic richness p = 0.019 significant at 0.05: True
functional richness p = 0.016 significant at 0.05: True
abundance p = 0.077 significant at 0.05: False
Shannon p = 0.647 significant at 0.05: False
FEve p = 0.132 significant at 0.05: False
```

</details>

#### F24 · PMC12975460 · Front Vet Sci (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12975460](https://pmc.ncbi.nlm.nih.gov/articles/PMC12975460/) · DOI [10.3389/fvets.2026.1692050](https://doi.org/10.3389/fvets.2026.1692050) · *Front Vet Sci* (2026) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q22b450dc-1`
- **Where in the paper**: Discussion paragraph 2
- **What the tool checked**: Discussion claim that CK in Groups A and B normalized by T3
- **Value as reported in the paper**: Groups A and B showed CK normalization by T3
- **What the tool computed**: According to the Results, CK was significantly above T0 at T3 in Group A (where it also peaked) and in Group B (elevated from T1 through T4). Group B was also higher than Group A at T3 and T4.
- **What the tool flagged** (model summary): Discussion paragraph 2 says "Groups A and B showed CK normalization by T3, suggesting reversible damage". The Results (time-course biomarkers) say Group A's CK was significantly elevated at T2 and T3 and peaked at T3, and Group B's CK was significantly elevated from T1 through T4. The paper's own results contradict the normalization claim and the reversibility inference drawn from it.
- **If the flag holds, what would change** (model reading, not proven): The conclusion that short compression (4 h and 8 h) gave reversible damage with CK back to normal by 24 h is not supported. The Results show CK at its peak (Group A) or still significantly elevated (Group B, through 72 h) at T3.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC12975460, CC BY 4.0):

- `Group A elevated at T2, T3, peak T3`, from:

  > "Group A exhibited significantly elevated CK at T2 and T3 compared to baseline (T0), peaking at T3."

- `Group B elevated T1–T4, peak T2`, from:

  > "Group B showed sustained increases from T1 through T4, reaching its highest level at T2"

- `B > A at T3, T4`, from:

  > "For CK, Group B surpassed Group A at T3 and T4"

- The passage that the first finding rests on:

  > "Groups A and B showed CK normalization by T3, suggesting reversible damage after short compression"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: left the v2 register: the v2 judge logged no code check for it
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
tp=["T0","T1","T2","T3","T4"]
A_sig=["T2","T3"]; A_peak="T3"
B_sig=["T1","T2","T3","T4"]; B_peak="T2"
print("Discussion claim: A and B normalized by T3")
print("Results Group A peak", A_peak, "sig elevated", A_sig, "T3 elevated:", "T3" in A_sig)
print("Results Group B peak", B_peak, "sig elevated", B_sig, "T3 elevated:", "T3" in B_sig, "T4 elevated:", "T4" in B_sig)
print("Claim consistent:", ("T3" not in A_sig) and ("T3" not in B_sig))
```
```text
Discussion claim: A and B normalized by T3
Results Group A peak T3 sig elevated ['T2', 'T3'] T3 elevated: True
Results Group B peak T2 sig elevated ['T1', 'T2', 'T3', 'T4'] T3 elevated: True T4 elevated: True
Claim consistent: False
```

</details>

#### F25 · PMC13180824 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13180824](https://pmc.ncbi.nlm.nih.gov/articles/PMC13180824/) · DOI [10.3389/fphar.2026.1761852](https://doi.org/10.3389/fphar.2026.1761852) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qd258bbf0-1`
- **Where in the paper**: Results, RA disease related indicators vs Table 5
- **What the tool checked**: Direction of the DAS28-CRP change in the SHG group from baseline to Week 4 (text says 'increased')
- **Value as reported in the paper**: DAS28-CRP increased significantly from baseline to Week 4 (0.30 ± 0.10)
- **What the tool computed**: Table 5 EMMs go from 3.39 to 3.09, a decrease of 0.30. The table defines a positive change as baseline minus follow-up, which marks improvement.
- **What the tool flagged** (model summary): In the Results (RA indicators), the text says SHG DAS28-CRP 'increased significantly' (0.30 ± 0.10). Table 5 shows it fell from 3.39 to 3.09, and a positive value means improvement. The same text calls the hs-CRP change a 'reduction', but Table 5 shows SHG hs-CRP rising significantly from 2.84 to 4.56 mg/L (change −1.72, P = 0.036, about +61%). That rise undercuts the conclusion that SHG addresses the 'inflammatory' dimension of pain.
- **If the flag holds, what would change** (model reading, not proven): The text reports that disease activity in the SHG group got significantly worse (DAS28-CRP increased) by Week 4. The paper's own table shows a significant improvement (a 0.30 decrease), which is below the 0.6 MCID.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13180824, CC BY 4.0):

- `3.39`, from:

  > "SHG | Week 0 | 3.39 ± 0.29 | — | −0.71 ± 0.45 (P = 0.126)"

- `3.09`, from:

  > "Week 4 | 3.09 ± 0.31 | 0.30 ± 0.10 (P = 0.004) | −0.24 ± 0.48 (P = 0.628)"

- `0.30`, from:

  > "DAS28-CRP increased significantly from baseline to Week 4 (0.30 ± 0.10, P = 0.004)."

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
b=3.39
w4=3.09
print("baseline_minus_week4", round(b-w4,2), "paper_change", 0.30)
print("direction", "decrease" if w4<b else "increase")
for d in [24,25,26]:
    t=mpmath.mpf(0.30)/0.10
    p=mpmath.betainc(d/2,0.5,0,d/(d+t*t),regularized=True)
    print("df",d,"t",t,"p",p)
print("z p", mpmath.erfc(3/mpmath.sqrt(2)))
```
```text
baseline_minus_week4 0.3 paper_change 0.3
direction decrease
df 24 t 3.0 p 0.00620573661652474
df 25 t 3.0 p 0.00603817956514349
df 26 t 3.0 p 0.00588545385039899
z p 0.00269979606326019
```

</details>

#### F26 · PMC13295250 · Animals (Basel) (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13295250](https://pmc.ncbi.nlm.nih.gov/articles/PMC13295250/) · DOI [10.3390/ani16121847](https://doi.org/10.3390/ani16121847) · *Animals (Basel)* (2026) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qa2d7bb65-1`
- **Where in the paper**: Discussion 4.4 vs Results 3.1
- **What the tool checked**: Discussion says inner-bay Hg (0.06 μg/L) has not exceeded the Class I standard; Results say NW Hg surpassed the Class I standard (0.05 μg/L)
- **Value as reported in the paper**: 0.06 μg/L, 'has not yet exceeded the first-class seawater quality standard'
- **What the tool computed**: 0.06 > 0.05 (ratio 1.2), so the value exceeds the Class I standard
- **What the tool flagged** (model summary): Section 4.4 says inner-bay Hg (0.06 μg/L) 'has not yet exceeded the first-class seawater quality standard', but Section 3.1 gives the Class I standard as 0.05 μg/L and says NW Hg surpassed it. Since 0.06 > 0.05, the Discussion statement does not match the paper's own numbers.
- **If the flag holds, what would change** (model reading, not proven): The exceedance conclusion flips. Results say inner-bay Hg is above the Class I standard; Discussion 4.4 says it is not. Given 0.05 μg/L, the Discussion statement would say the standard was exceeded.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13295250, CC BY 4.0):

- `0.06`, from:

  > "The mercury concentration in the inner bay (0.06 μg/L) was three times that of the outer bay. Although it has not yet exceeded the first-class seawater quality standard"

- `0.05`, from:

  > "Mercury (Hg) at the inner-bay margin (NW) surpassed the Class I standard (0.05 μg/L)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
std=0.05
hg=0.06
print("inner_bay_Hg", hg, "ClassI_std", std, "exceeds", hg>std, "ratio", round(hg/std,2))
```
```text
inner_bay_Hg 0.06 ClassI_std 0.05 exceeds True ratio 1.2
```

</details>

#### F27 · PMC13587494 · BMC Sports Sci Med Rehabil (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13587494](https://pmc.ncbi.nlm.nih.gov/articles/PMC13587494/) · DOI [10.1186/s13102-026-01816-4](https://doi.org/10.1186/s13102-026-01816-4) · *BMC Sports Sci Med Rehabil* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q34dcb204-1`
- **Where in the paper**: Conclusions
- **What the tool checked**: Claim that the hypothesis that IWU increases the pressure-generating capacity of the inspiratory muscles (MIP) was confirmed
- **Value as reported in the paper**: Hypothesis that IWU increases inspiratory pressure-generating capacity 'was confirmed'
- **What the tool computed**: MIP group x time interaction: F=0.598, p≈0.450, ηp²≈0.034 (df 1,17). Not significant. MIP rose about equally in both groups (IWU +7.21%, CON +6.32%).
- **What the tool flagged** (model summary): The Conclusions state that the hypothesis that IWU increases inspiratory pressure-generating capacity and so improves 1RM 'was confirmed'. Table 2 gives a non-significant MIP group × time interaction (F = 0.598, p = 0.450, ηp² = 0.034; IWU +7.20% vs control +6.32%), and the Results say no superiority of IWU can be inferred for MIP.
- **If the flag holds, what would change** (model reading, not proven): The Conclusions would say that the 'increase in inspiratory pressure-generating capacity' part of the hypothesis was not supported (the MIP interaction was non-significant, p=0.450). The 1RM part is supported. The claim that the primary hypothesis was 'confirmed' would be too strong.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13587494, CC BY 4.0):

- `F = 0.598, p = 0.450, ηp² = 0.034`, from:

  > "However, the absence of a significant group × time interaction (F = 0.598, p = 0.450, ηp² = 0.034) indicates that the magnitude of improvement was comparable between groups. Consequently, no superiority of the IWU intervention can be [...]"

- `126.3, 135.4, 128.44, 136.56`, from:

  > "MIP | IWU | 126.3 ± 11.57 | 135.4 ± 1.64 | 7.2 | ... CG | 128.44 ± 9.13 | 136.56 ± 9.79 | 6.32"

- The passage that the first finding rests on:

  > "IWU would lead to an increase in the pressure-generating capacity of the inspiratory muscles and consequently result in improved 1RM performance, was confirmed"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: moved to tier B: the blind second gate marked it "unresolved" (queue for a human check)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath as m
def p(F,d1,d2): return m.betainc(d2/2,d1/2,0,d2/(d2+d1*F),regularized=True)
for d2 in (17,18):
    print("df2",d2,"MIP interaction p",p(0.598,1,d2),"etap2",0.598/(0.598+d2))
    print("df2",d2,"1RM interaction p",p(141.560,1,d2),"etap2",141.560/(141.560+d2))
print("paper MIP p 0.450 etap2 0.034; 1RM p<0.001 etap2 0.893")
print("MIP pct IWU",(135.4-126.3)/126.3*100,"CG",(136.56-128.44)/128.44*100)
```
```text
df2 17 MIP interaction p 0.449961958542774 etap2 0.033981134219797704
df2 17 1RM interaction p 1.1466253631861e-9 etap2 0.8927850655903128
df2 18 MIP interaction p 0.449379070568258 etap2 0.03215399505323153
df2 18 1RM interaction p 5.79002009472737e-10 etap2 0.8871897718726498
paper MIP p 0.450 etap2 0.034; 1RM p<0.001 etap2 0.893
MIP pct IWU 7.205067300079183 CG 6.322018062908755
```

</details>

#### F28 · PMC13608439 · J Funct Morphol Kinesiol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13608439](https://pmc.ncbi.nlm.nih.gov/articles/PMC13608439/) · DOI [10.3390/jfmk11030358](https://doi.org/10.3390/jfmk11030358) · *J Funct Morphol Kinesiol* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qcb80f115-2`
- **Where in the paper**: Results, Table 6 paragraph
- **What the tool checked**: Claim that the analysis of variations (Δ) showed significant between-group differences for Satisfaction with Life
- **Value as reported in the paper**: statistically significant differences between the groups in the Satisfaction with Life variable (analysis of the variations)
- **What the tool computed**: Δ-based Kruskal–Wallis for SWL: H(2)=4.452 gives p=0.108, which is not significant. The only significant Δ-based psychosocial result is for quality of life (H=11.356, p=0.0034).
- **What the tool flagged** (model summary): In the Results paragraph after Table 6, the paper says the analysis of the variations revealed statistically significant between-group differences in satisfaction with life. Its own Δ Kruskal–Wallis test gives H(2)=4.452, p=0.108, which the earlier Results and the Discussion describe as non-significant.
- **If the flag holds, what would change** (model reading, not proven): The statement that SWL change differed significantly between groups changes to no significant Δ difference for SWL (p=0.108). The significant Δ psychosocial result is for quality of life. The same possible discrepancy appears in the Conclusions.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13608439, CC BY 4.0):

- `4.452`, from:

  > "For satisfaction with life, the Δ-based omnibus test was not significant, H(2) = 4.452, p = 0.108"

- `11.356`, from:

  > "a significant between-group difference was observed for quality of life, H(2) = 11.356, p = 0.003"

- The passage that the first finding rests on:

  > "The analysis of the variations revealed statistically significant differences between the groups in the Satisfaction with Life variable"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: stayed in tier A (passed the v2 judge and the blind second gate)
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
for name,H,p in [("SWL_delta",4.452,0.108),("QoL_delta",11.356,0.003),("SWL_post",9.037,0.011)]:
    print(name,"H",H,"paper_p",p,"recomputed_p",mpmath.nstr(mpmath.gammainc(1,H/2,mpmath.inf)/mpmath.gamma(1),4),"significant_at_0.05",float(mpmath.exp(-H/2))<0.05)
```
```text
SWL_delta H 4.452 paper_p 0.108 recomputed_p 0.108 significant_at_0.05 False
QoL_delta H 11.356 paper_p 0.003 recomputed_p 0.00342 significant_at_0.05 True
SWL_post H 9.037 paper_p 0.011 recomputed_p 0.01091 significant_at_0.05 True
```

</details>

#### F29 · PMC13682915 · Ecol Evol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13682915](https://pmc.ncbi.nlm.nih.gov/articles/PMC13682915/) · DOI [10.1002/ece3.74556](https://doi.org/10.1002/ece3.74556) · *Ecol Evol* (2026) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q55558b43-2`
- **Where in the paper**: Discussion, paragraph 3 (precipitation and NDVI)
- **What the tool checked**: Discussion claim that NDVI has a significant link to beta diversity turnover
- **Value as reported in the paper**: NDVI has a 'significant link to beta diversity turnover'
- **What the tool computed**: The only NDVI–beta diversity result reported is from the db-RDA: NDVI marginal contribution 0.49%, p = 0.4139, which is not significant. No partial Mantel result for NDVI is reported.
- **What the tool flagged** (model summary): Discussion paragraph 1, finding (ii), calls NDVI a primary correlate of beta diversity, and paragraph 3 says it has a 'significant link to beta diversity turnover'. The only beta-diversity result reported for NDVI is the dbRDA marginal test, where NDVI explains 0.49% with p = 0.4139, which is not significant. Only Bio12 and latitude were significant, and no partial Mantel statistics are reported for NDVI.
- **If the flag holds, what would change** (model reading, not proven): The Discussion's claim that NDVI is a significant correlate of beta diversity turnover, and its broader claim that precipitation and NDVI are the primary correlates of both alpha and beta diversity, are not supported. The reported results show NDVI as non-significant for beta diversity (p = 0.4139). Only precipitation and latitude were significant.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13682915, CC BY 4.0):

- `0.4139`, from:

  > "NDVI (0.49%, p = 0.4139)"

- `0.0001`, from:

  > "Latitude (F = 4.91, p = 0.0001) and Bio12 (F = 6.61, p = 0.0001) as the only significant predictors"

- The passage that the first finding rests on:

  > "and its significant link to beta diversity turnover"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: yes
- v2 judge and blind second gate: left the v2 register: the v2 judge logged no code check for it
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
p_ndvi=0.4139
p_bio12=0.0001
print("NDVI dbRDA p", p_ndvi, "significant at 0.05:", p_ndvi<0.05)
print("Bio12 dbRDA p", p_bio12, "significant at 0.05:", p_bio12<0.05)
print("NDVI marginal pct", 0.49)
```
```text
NDVI dbRDA p 0.4139 significant at 0.05: False
Bio12 dbRDA p 0.0001 significant at 0.05: True
NDVI marginal pct 0.49
```

</details>

### Group 4 - confirmed, but no reported result changes (4)

The second pass found the same possible discrepancy, but in its reading no reported result or conclusion changes. These are possible small reporting slips.

#### F30 · PMC13079375 · Front Sports Act Living (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13079375](https://pmc.ncbi.nlm.nih.gov/articles/PMC13079375/) · DOI [10.3389/fspor.2026.1770227](https://doi.org/10.3389/fspor.2026.1770227) · *Front Sports Act Living* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q2c278b5f-3`
- **Where in the paper**: Table 9 / text
- **What the tool checked**: Residual df 97 compared with the sample size N=116
- **Value as reported in the paper**: df2 = 97 (implies n = 100)
- **What the tool computed**: With N=116 and 2 predictors, df2 = 113, and F would be about 40.9 for R2=.42
- **What the tool flagged** (model summary): Table 9 reports F(2,97) = 35.64. Residual df of 97 implies n = 100, but N = 116. With N = 116 and R² = .42, F(2,113) = 40.9. Even at df 97, R² = .42 gives F = 35.1.
- **If the flag holds, what would change** (model reading, not proven): The reported denominator df (97) does not match the reported sample (116). Significance does not change. The F statistic would be about 40.9 rather than 35.64. Table 14 also reports a different R2 (.46, F=29.87) for what looks like the same model.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13079375, CC BY 4.0):

- `97`, from:

  > "[F(2,97) = 35.64, p < .001]"

- `116`, from:

  > "Self-efficacy | 116 | 2.30 | 5.00 | 3.87 | 0.54"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-opus-5-5): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: no
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): partly: the numbers are in the logged runs, but split over runs or abbreviated. A model session checked this by reading the logs, not a human

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
import mpmath
for r2 in [0.415,0.42,0.425]:
    print("R2",r2,"F df97",r2/2/((1-r2)/97),"F df113",r2/2/((1-r2)/113))
print("implied n from df2=97:",97+2+1)
F=35.64
print("p",mpmath.betainc(97/2,1,0,97/(97+2*F),regularized=True))
print("R2 from t: R=0.65 R2", 0.65**2)
```
```text
R2 0.415 F df97 34.4059829059829 F df113 40.08119658119658
R2 0.42 F df97 35.120689655172406 F df113 40.91379310344827
R2 0.425 F df97 35.84782608695652 F df113 41.76086956521739
implied n from df2=97: 100
p 2.4880133119133e-12
R2 from t: R=0.65 R2 0.42250000000000004
```

</details>

#### F31 · PMC13149103 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13149103](https://pmc.ncbi.nlm.nih.gov/articles/PMC13149103/) · DOI [10.3389/fphar.2026.1745737](https://doi.org/10.3389/fphar.2026.1745737) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-qcb676891-1`
- **Where in the paper**: Results, Patient characteristics / Table 1
- **What the tool checked**: Loading dose percentage: 175 patients (65.1%) of the 281-patient cohort
- **Value as reported in the paper**: 175 (65.1%); Table 1: None loading dose 94 (34.9), Loading dose 175 (65.1); total 281
- **What the tool computed**: 175/281 = 62.28%. 65.1% matches only 175/269, and 94+175 = 269, not 281
- **What the tool flagged** (model summary): In Table 1 and the Patient characteristics text, loading dose 175 (65.1%) plus no loading dose 94 (34.9%) gives 269, not the stated cohort of 281. The percentages only reproduce with base 269 (175/281 = 62.3%), so 12 patients have no loading-dose status even though the inclusion criteria assign every patient to one of the two groups.
- **If the flag holds, what would change** (model reading, not proven): Only a descriptive result changes. The share of patients who received a loading dose is 62.3% of the stated cohort, not 65.1%, and 12 patients (281 − 269) have no loading-dose category. The n used in the loading-dose analyses is also unclear. No inferential conclusion changes.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13149103, CC BY 4.0):

- `175`, from:

  > "A total of 175 patients (65.1%) received loading dose therapy."

- `281`, from:

  > "A total of 281 patients were included in this study after screening."

- `94`, from:

  > "None loading dose | 94 (34.9)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: no
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
print("paper_pct", 65.1)
print("175/281", round(175/281*100,2))
print("sum_groups", 94+175)
print("175/269", round(175/269*100,2))
print("94/269", round(94/269*100,2))
print("94/281", round(94/281*100,2))
print("check_sex", round(191/281*100,2), round(90/281*100,2))
```
```text
paper_pct 65.1
175/281 62.28
sum_groups 269
175/269 65.06
94/269 34.94
94/281 33.45
check_sex 67.97 32.03
```

</details>

#### F32 · PMC13534047 · Front Public Health (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13534047](https://pmc.ncbi.nlm.nih.gov/articles/PMC13534047/) · DOI [10.3389/fpubh.2026.1926848](https://doi.org/10.3389/fpubh.2026.1926848) · *Front Public Health* (2026) · field: nursing_public_health · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q321101e6-3`
- **Where in the paper**: Results, Circumstances and types of violent incidents
- **What the tool checked**: Number exposed to any violence (323) compared with the number reporting verbal violence (333)
- **Value as reported in the paper**: 323 reported experiencing violence; 333 reported verbal violence
- **What the tool computed**: The number exposed to any violence must be at least 333. 323 is 10 too few.
- **What the tool flagged** (model summary): The Results give 333 participants reporting verbal violence, yet state that 323 healthcare workers reported experiencing violence, and the Abstract and PTSD section give the exposed group as n = 305. A subset (333) cannot exceed its total (323 or 305), so the denominator of the 64.9% PTSD prevalence (198/305) is uncertain.
- **If the flag holds, what would change** (model reading, not proven): The exposed denominator is unclear (323 vs at least 333 vs 305). The prevalence counts and the shift/day percentages rest on an inconsistent base. The main associations are not directly changed.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13534047, CC BY 4.0):

- `333`, from:

  > "Physical assault was reported by 184 participants, verbal violence by 333 participants"

- `323`, from:

  > "Among the 323 healthcare workers who reported experiencing violence"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: text comparison · a reported result changes, in its reading: no
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 2/2 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
n=323
print("shift answered", n-2, 133+188)
print("day pct paper 41.4 recomputed", round(100*133/321,2))
print("night pct paper 58.6 recomputed", round(100*188/321,2))
print("weekday answered", n-4, 211+108)
print("working day paper 66.0 recomputed", round(100*211/319,2))
print("nonworking paper 33.9 recomputed", round(100*108/319,2))
print("verbal violence count", 333, "vs total exposed", 323, "excess", 333-323)
print("PCL-5 n", 305, "vs exposed", 323, "diff", 323-305)
```
```text
shift answered 321 321
day pct paper 41.4 recomputed 41.43
night pct paper 58.6 recomputed 58.57
weekday answered 319 319
working day paper 66.0 recomputed 66.14
nonworking paper 33.9 recomputed 33.86
verbal violence count 333 vs total exposed 323 excess 10
PCL-5 n 305 vs exposed 323 diff 18
```

</details>

#### F33 · PMC13585511 · Front Pharmacol (2026)

**Status: unverified. Flagged for checking by an automated pipeline. No human has checked it. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13585511](https://pmc.ncbi.nlm.nih.gov/articles/PMC13585511/) · DOI [10.3389/fphar.2026.1918438](https://doi.org/10.3389/fphar.2026.1918438) · *Front Pharmacol* (2026) · field: wetlab_biology · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q64b528a1-3`
- **Where in the paper**: Results, adverse events paragraph
- **What the tool checked**: Results text says no dizziness occurred in males; Table 3 reports male dizziness 2 (6.90%)
- **Value as reported in the paper**: Text: no dizziness in male cohort; Table 3: Dizziness male 2 (6.90%), P = 0.600
- **What the tool computed**: 2/29 = 6.90% and Fisher p = 0.600 both match 2 cases. With 0 male cases Fisher p would be 1.000. The table is internally consistent with 2 cases, so the text contradicts it.
- **What the tool flagged** (model summary): The Results text says no dizziness occurred in males, and the Discussion likewise lists none, but Table 3 reports male dizziness 2 (6.90%) with P=0.600, which Fisher's exact test reproduces for 2/29 vs 1/32. The two do not fit together: male dizziness is either 0% with P=1.000 or 6.90% with P=0.600.
- **If the flag holds, what would change** (model reading, not proven): The reported number of male dizziness cases is either 0 (text) or 2 (Table 3). This changes the description of the male adverse-event profile. The sex comparison stays non-significant either way.

**Numbers the tool extracted, and the passages they come from** (quotations; source: PMC13585511, CC BY 4.0):

- `0 dizziness in males`, from:

  > "no instances of vomiting, dizziness, or fatigue were reported"

- `2 (6.90%) vs 1 (3.13%), P 0.600`, from:

  > "Dizziness, n (%) | 2 (6.90%) | 1 (3.13%) | 0.600"

- `29, 32`, from:

  > "Male (n = 29) | Female (n = 32)"

**Automatic checks** (all automatic, none by a human):

- Evidence gate (program): passed
- First judge (model, claude-fable-5-2): tier A, with a logged code check
- Strict blind pass (second model): confirmed · kind: recomputed · a reported result changes, in its reading: no
- v2 judge and blind second gate: moved to tier B: the v2 judge did not name a reported result that changes
- Quotes word for word in the paper text (program): 3/3 input quotes; quote of the first finding: yes
- Logged sandbox code run again (program): yes, the code prints the numbers of the finding

<details><summary>Sandbox runs of the second pass (code and output, as logged)</summary>

```python
from math import comb
def fisher(a,n1,c,n2):
    K=a+c;N=n1+n2
    p0=comb(n1,a)*comb(n2,c)/comb(N,K)
    s=0
    for x in range(max(0,K-n2),min(K,n1)+1):
        p=comb(n1,x)*comb(n2,K-x)/comb(N,K)
        if p<=p0*(1+1e-9): s+=p
    return s
print("male dizziness pct table 6.90 recomputed", round(200/29,2))
print("Fisher p dizziness 2/29 vs 1/32 table 0.600 recomputed", round(fisher(2,29,1,32),3))
print("text male dizziness count 0 -> Fisher p", round(fisher(0,29,1,32),3))
print("female fatigue 1/32 pct", round(100/32,2), "Fisher", round(fisher(0,29,1,32),3))
```
```text
male dizziness pct table 6.90 recomputed 6.9
Fisher p dizziness 2/29 vs 1/32 table 0.600 recomputed 0.6
text male dizziness count 0 -> Fisher p 1.0
female fatigue 1/32 pct 3.12 Fisher 1.0
```

</details>

## Section B - Not confirmed by our own second pass (7 flags)

> These 7 flags came from the first pass. **Our own second pass did not confirm them**: it rejected 3 and could not decide on 4.
> No human has checked them either. We list them so that the random sample of 40 is complete. Do not read them as confirmed findings.

#### N1 · PMC12807936 · Front Vet Sci (2025) - not confirmed: rejected (the second pass tested a different comparison)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12807936](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807936/) · DOI [10.3389/fvets.2025.1707434](https://doi.org/10.3389/fvets.2025.1707434) · *Front Vet Sci* (2025) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q28cc1bbc-1`
- **Where in the paper**: Results, Dispensing patterns by premise type; Discussion para 1; Table 2
- **What the first pass flagged** (model summary): Results ('Dispensing patterns') and Discussion para 1 say the volume of antibiotics did not differ between premise types (chi-square 1.25, p = 0.263) and that pharmacies dispensed slightly more. That statistic is the Table 3 outlet comparison (40/46 vs 45/48); Table 2's 'Quantity of antibiotics dispensed' row gives 51 agrovet vs 49 pharmacy products with p < 0.001 (recomputed chi-square 24.8).
- **Why the second pass did not confirm it**: The second pass tested the chi-square value 1.25 against a different table (the outlet counts of Table 3). There it found the value consistent (1.252, p = 0.263). It did not test the point of this flag: that the text presents this test as a test of antibiotic volume, while Table 2 gives p < 0.001 for volume. So the second pass neither confirmed nor cleared this flag.

Passage (quotation; source: PMC12807936, CC BY 4.0):

> "retail pharmacies dispensed a slightly higher volume of antibiotics, the difference was not statistically significant (χ2 = 1.25, p = 0.263)"

#### N2 · PMC12807936 · Front Vet Sci (2025) - not confirmed: rejected (a valid different denominator)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12807936](https://pmc.ncbi.nlm.nih.gov/articles/PMC12807936/) · DOI [10.3389/fvets.2025.1707434](https://doi.org/10.3389/fvets.2025.1707434) · *Front Vet Sci* (2025) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q28cc1bbc-6`
- **Where in the paper**: Abstract, Results
- **What the first pass flagged** (model summary): The Abstract gives prior-treatment 8.5%, progression 19.1%, route 74.5%, dose frequency 63.8% and duration 58.5% (counts 8, 18, 70, 60, 55 over 94), but referral 12.3% and symptoms 53.2% over 220, with no denominator stated. Results and Table 2 report the same counts as 3.6%, 8.2%, 31.8%, 27.3% and 25.0% of 220.
- **Why the second pass did not confirm it**: The second pass recomputed all six Abstract percentages. Each one is exact for its own denominator (94 dispensing outlets or 220 premises). Two denominators in one Abstract sentence is a reporting choice. In this reading, no number is inconsistent and no result changes.

Passage (quotation; source: PMC12807936, CC BY 4.0):

> "Few inquired about prior treatment (8.5%), advised on disease progression (19.1%), or referred the simulated farmer to a veterinarian (12.3%). While 74.5% communicated the correct route of administration, only 63.8% mentioned dosage frequency, and 58.5% specified treatment duration."

#### N3 · PMC12797519 · BMC Nurs (2025) - not confirmed: rejected (a second symptom of another finding)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC12797519](https://pmc.ncbi.nlm.nih.gov/articles/PMC12797519/) · DOI [10.1186/s12912-025-04180-9](https://doi.org/10.1186/s12912-025-04180-9) · *BMC Nurs* (2025) · field: nursing_public_health · licence: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Run id**: `R1-qa4b8bf75-3`
- **Where in the paper**: Results, Factors impacting KPA scores
- **What the first pass flagged** (model summary): The Spearman correlations with age and experience (Results and Table 3) give p-values that match N=235, not 160. For example, r=0.18 gives p=0.023 at N=160 but 0.0057 at N=235 (reported 0.006). Likewise r=0.23 gives 0.0034 vs 0.0004 (reported <0.001).
- **Why the second pass did not confirm it**: The second pass found r = 0.18, p = 0.006 consistent at n = 235, the analysis size that Table 3 implies. The flag describes the same question as finding F13 (analysis size against the stated sample), so it is not a separate finding.

Passage (quotation; source: PMC12797519, CC BY-NC-ND 4.0):

> "attitude (r = 0.18, p = 0.006)"

#### N4 · PMC13292676 · Poult Sci (2026) - not confirmed: unresolved (the wording has two readings)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13292676](https://pmc.ncbi.nlm.nih.gov/articles/PMC13292676/) · DOI [10.1016/j.psj.2026.107253](https://doi.org/10.1016/j.psj.2026.107253) · *Poult Sci* (2026) · field: agri_food_vet · licence: [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)
- **Run id**: `R1-q40b15963-5`
- **Where in the paper**: Abstract
- **What the first pass flagged** (model summary): The abstract says the Mix group "consistently outperformed" NC and O2 in richness. The genus-level Results show Mix had the lowest richness at 2 DPH (median 6; O2 significantly higher, P = 0.0020), O2 was significantly richer than Mix at 10 DPH, and Mix exceeded NC and O2 only at 30 DPH (221 vs 110 and 52.5, P = 0.0392).
- **Why the second pass did not confirm it**: The second pass saw the opposite result at 2 DPH. But the sentence "consistently outperformed ... on 2 DPH" can be read in two ways, so the second pass could not decide.

Passage (quotation; source: PMC13292676, CC BY-NC-ND 4.0):

> "consistently outperformed the negative control group and the group given oral probiotics on 2 DPH at both species and genus levels in terms of richness"

#### N5 · PMC13359537 · Animals (Basel) (2026) - not confirmed: unresolved (the unit of analysis is not stated)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13359537](https://pmc.ncbi.nlm.nih.gov/articles/PMC13359537/) · DOI [10.3390/ani16132060](https://doi.org/10.3390/ani16132060) · *Animals (Basel)* (2026) · field: agri_food_vet · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q756465d8-2`
- **Where in the paper**: 3.16 Partial correlation / Conclusions
- **What the first pass flagged** (model summary): With n = 97 cows, which reproduces the paper's protein, urea and SCC correlation p-values (0.031, 0.021, 0.719), hindlimb pathology–teat temperature partial r = 0.23–0.26 with 5 covariates gives p ≈ 0.012–0.027. That contradicts 'p ≤ 0.001' in 3.16, 4.4 and the Conclusions. The bivariate r = 0.21–0.24 gives p ≈ 0.018–0.039, which contradicts 'p < 0.01' in 3.15.
- **Why the second pass did not confirm it**: With n = 97 cows the p-values are about 0.012-0.027. With n = 194 hindlimbs they are about 0.0003-0.0015. The paper does not state the unit for these correlations, so the reported p ≤ 0.001 is possible.

Passage (quotation; source: PMC13359537, CC BY 4.0):

> "significant positive partial correlations were identified between hindlimb pathology and teat surface temperatures across all udder quarters (r = 0.23–0.26, p ≤ 0.001)"

#### N6 · PMC13052302 · Ecol Evol (2026) - not confirmed: unresolved (SD or SE is not stated)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13052302](https://pmc.ncbi.nlm.nih.gov/articles/PMC13052302/) · DOI [10.1002/ece3.73247](https://doi.org/10.1002/ece3.73247) · *Ecol Evol* (2026) · field: ecology_environment · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q76e7b809-1`
- **Where in the paper**: Results, Pollination Efficiency / Table 2
- **What the first pass flagged** (model summary): Table 2 reports pollination efficiency of 12.21 ± 0.13% vs 9.88 ± 1.16% (mean ± SE, 10 repeats) as significantly different (p<0.05). From these values, t = 2.00 with df 18 gives p ≈ 0.061, so the difference is not significant.
- **Why the second pass did not confirm it**: t = 2.00 and p = 0.061 follow only if the ± values are standard errors with n = 10. If they are standard deviations, p < 0.001 and the reported result holds. The second pass could not tell which one the paper uses.

Passage (quotation; source: PMC13052302, CC BY 4.0):

> "with a significant difference between the two (p < 0.05) (Table 2)"

#### N7 · PMC13189902 · Front Sports Act Living (2026) - not confirmed: unresolved (two claims in one flag; only the second one reproduced)

**Status: not confirmed by our own second pass. Not verified by a human. In the process of verification. Not a claim that the paper is wrong.**

- **Paper**: [PMC13189902](https://pmc.ncbi.nlm.nih.gov/articles/PMC13189902/) · DOI [10.3389/fspor.2026.1748973](https://doi.org/10.3389/fspor.2026.1748973) · *Front Sports Act Living* (2026) · field: sports_exercise · licence: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Run id**: `R1-q18d8b5c4-1`
- **Where in the paper**: Abstract / Results (carry distance variability)
- **What the first pass flagged** (model summary): The Methods set the Bonferroni alpha at 0.05/12 = 0.004. The Visual effect on carry distance variability (B = 2.4, SE = 1.0, p = 0.013) fails this threshold, yet the paper reports it as a significant difference and builds Discussion and policy conclusions on it. The Abstract also gives this coefficient to Sitting and B = 2.6 (p = 0.002) to Visual, the reverse of the Results and Discussion.
- **Why the second pass did not confirm it**: The second pass reproduced only the second half of the flag (the Abstract gives the Sitting and Visual coefficients the other way round from the Results). It did not test the first half (Bonferroni alpha 0.004 against p = 0.013). The paper applies the 0.004 "at the GLM level" (Methods), so a test of each coefficient at 0.05 is a defensible reading.

Passage (quotation; source: PMC13189902, CC BY 4.0):

> "higher carry distance variability [B = 2.4, SE = 1.0, p = 0.013, 95% CI (0.5 4.3), partial f2 = 0.01]"

