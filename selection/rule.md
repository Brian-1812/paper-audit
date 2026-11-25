# Paper selection rule (500 papers, 5 fields)

We drew the list `selection/papers.tsv` by this rule. We saved it before any model saw a paper.
The list holds identifiers only: opaque id, field, PMCID, DOI, journal, year and two test counts. It holds no paper
text.

## Fields and journals

We chose fields where we found no active automated checker for internal errors. We left out fields that other tools
already cover: psychology (statcheck, GRIM), machine learning, astrophysics and mathematics.

| field | journals (Europe PMC `JOURNAL:` names) |
|---|---|
| ecology_environment | Ecol Evol; BMC Ecol Evol; Glob Chang Biol; Insects |
| agri_food_vet | Animals (Basel); Front Vet Sci; Poult Sci; Foods |
| sports_exercise | Front Sports Act Living; Sports (Basel); BMC Sports Sci Med Rehabil; J Funct Morphol Kinesiol |
| nursing_public_health | BMC Nurs; Nurs Open; BMC Public Health; Front Public Health |
| wetlab_biology | Front Pharmacol; Front Microbiol; Microbiol Spectr; Cells |

We chose the journals on 2026-11-22. Each is a large open-access journal of its field that deposits full text in
PubMed Central (PMC).

## Rule (code: `pipeline/select_papers.py`)

1. Candidates. For each journal, run this Europe PMC REST search:
   `JOURNAL:"<j>" AND OPEN_ACCESS:y AND IN_EPMC:y AND (PUB_YEAR:2025 OR PUB_YEAR:2026) AND PUB_TYPE:"research-article"`.
   Keep the first 1,500 results in Europe PMC order (cursor paging, 100 per page).
2. Order: ascending `sha1("t391:" + PMCID)` inside each field. The salt `t391:` is fixed. A different salt gives a
   different list.
3. In that order, fetch the JATS full text (NCBI efetch, `db=pmc`). Keep the paper when the body text has 8,000 or
   more characters AND the counter finds 5 or more reported test statistics with a p-value (t, F, z, W, U, H, r or
   chi-square, an optional df, "= value", then a p-value within 60 characters).
4. Stop each field at 100 kept papers. A network error is not a rejection: the program tries the paper again.
5. Write the list. Model calls see only the opaque id and the paper text.

A new search today gives different candidates, because the databases grow. We searched on 2026-11-22. The frozen
candidate lists are not in this repository. To check a rebuilt list, compare its sha256 with the value below.

## Result

- 500 papers, 100 per field. Papers examined: ecology 983, sports 450, wet-lab 2,408, agri 2,449, nursing 811.
- sha256 of `selection/papers.tsv`:
  `aba315e619cd4edb78c9bf713d62479a4240c21350b9907f860676756d229460`
- Median 10 counted tests per paper. 169 papers also have tests in the APA text format.
- Skew: 63 of the 100 ecology papers are from Insects. 44 of the 100 wet-lab papers are from Front Pharmacol.
  About two thirds of the 500 papers come from two publishers. So the sample is "large open-access journals that deposit in PMC".
  It is not a sample of each field.
- Licences of the 500 papers (from the JATS `<license>` element): CC BY 4.0: 418, CC BY-NC-ND 4.0: 75,
  CC BY-NC 4.0: 7.

## History

A first version of the rule used an APA-format test counter only. It kept 8 of 226 ecology papers and 4 of 262
agriculture papers, because these fields write "F1,23 = 4.5, P = 0.03" or "chi2 = 12.3, df = 2, P < 0.001". We
did not use that version.
