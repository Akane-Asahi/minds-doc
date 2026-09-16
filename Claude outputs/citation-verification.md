# Citation Verification: User Persona Document

*Checked each citation used in the persona against the actual published paper (abstract
or full text where accessible), because Orland's comments raised specific doubts about
several of them and one number turned out to be fabricated. Results below.*

## Confirmed accurate

- **Rello & Baeza-Yates (2016)** — "The Effect of Font Type on Screen Readability by
  People with Dyslexia," ACM TACCESS. Real, correctly attributed, matches the
  font/spacing claim it was cited for.
- **Crescenzi et al. (2021)** — "Supporting Metacognition during Exploratory Search
  with the OrgBox," SIGIR 2021. Real. However, confirmed Orland's point: this is about
  metacognitive scaffolding for a general search population, not specifically people
  with dyslexia. It should be cited for the metacognitive-scaffolding claim only, not
  implied to be dyslexia-specific research.
- **Li et al. (2020)** — actual title is "Everyday Cross-session Search: How and Why Do
  People Search Across Multiple Sessions" (CHIIR 2020). Real, year correct. Confirmed
  Orland's point: it studies general cross-session stopping reasons (found what they
  needed, need to process information, distraction, fatigue), not dyslexia or
  interruption effects specifically. The "task-related vs. non-task-related" stopping
  categories are real and usable, the "loses thread after ~30 min or interruption"
  claim as stated is not directly supported by this paper.

## Wrong as cited, needs correction

- **"Hoeber, Islam et al., 2024"** — the actual paper is Hoeber, Islam, Boon, Storie &
  Ramshaw, "Search Timelines: Visualizing Search History to Enable Cross-Session
  Exploratory Search," *International Journal on Digital Libraries*, **2026**, not
  2024. More importantly: the abstract reports higher engagement, usability, and
  perceived knowledge gain for the Search Timelines condition (n=32 controlled study),
  and participants using it spent *more* time on task, not less. It does **not** report
  a reacquaintance-time percentage for any condition. The "~20% of session time lost to
  reacquaintance" figure in the persona does not come from this paper. This is the
  specific number Orland flagged, and he's right, it isn't in the source.
- **Choi & Arguello (2025)** — real paper, "The Effects of Working Memory during a
  Search and Sensemaking Task," CHIIR 2025. It studies working memory capacity and
  search/sensemaking behavior in a general population. It is not a dyslexia study, so
  citing it for a dyslexia-specific claim (as the persona did) is a misattribution, even
  though the paper itself is real and about working memory.

## Could not verify, recommend dropping or replacing

- **"Duranovic (2018)"** for "reads at ~60% of typical speed, but with high accuracy."
  I could not find a matching paper after multiple searches. There are real Duranovic
  publications on dyslexia (e.g., a 2025 paper on handwriting characteristics in
  children with dyslexia), but nothing matching this reading-speed claim or year. This
  citation and the specific 60% figure should be treated as unverified, most likely
  invented by the earlier AI draft, and removed rather than reused.

## A better-grounded replacement for the "competent, motivated" framing

- **Beveridge, Makri & MacFarlane** — "'I'm just not sure.' The persistence of
  uncertainty in the information seeking of undergraduate students with dyslexia"
  (this is almost certainly the "Beveridge et al." Orland referenced in his comment
  about self-efficacy). Real, and directly relevant: it found that undergraduate
  students with dyslexia showed *low* self-efficacy specifically around "selecting and
  spelling keywords and reading, interpreting and evaluating information online," and
  that this uncertainty often did **not** resolve as searching progressed, contrary to
  what standard information-seeking models predict. Participants coped by avoiding
  challenging texts and over-relying on familiar sources. This directly contradicts the
  "competent, motivated searcher" framing in the original persona, and is a much
  stronger, correctly-scoped source for describing this population's actual relationship
  to search self-efficacy.

## Bottom line for the rewrite

Drop the Duranovic figure entirely. Re-scope Choi & Arguello, Li et al., and Crescenzi
et al. to the claims they actually support (working memory generally; cross-session
stopping behavior generally; metacognitive scaffolding generally), not dyslexia-specific
claims. Fix the Hoeber/Islam citation to 2026 and drop the invented 20% figure, there
is no reacquaintance-time percentage to cite. Replace the self-efficacy framing using
Beveridge, Makri & MacFarlane, which is both real and correctly scoped to this exact
population and exact behavior (query formulation and evaluating results).
