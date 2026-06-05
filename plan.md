# Plan — Phase 3: Confidence Intervals notebook

## Context

The project (`student-performance-project`) analyzes UCI Student Performance data
with a multi-phase statistics pipeline described in `README.md`. Phase 1 (EDA) is
done and produced `data/processed/student_mat_clean.csv` (n=357 — G3=0 dropouts
removed, `absences` winsorized at p95). Phase 3 — **Confidence intervals** — is
assigned to Phong and its notebook `notebooks/03_confidence_intervals.ipynb` does
**not exist yet**. This plan creates that notebook, completing the README Phase 3
checklist (parametric CI, bootstrap CI, group-difference CIs, power analysis) and
emitting `data/processed/bootstrap_ci_results.csv`.

Phase 3's only real input dependency is `student_mat_clean.csv` (per README §4
table), so it can be built standalone — no need to wait on the not-yet-created
`02_hypothesis_testing.ipynb` or a `helpers.py` (neither exists).

User decisions: **comprehensive** depth, CSV → `data/processed/`, power analysis
driven by **n=357** with a note that 395 was the raw pre-cleaning size.

## Conventions to match (from `01_EDA.ipynb`)

- Title markdown cell: `# Phase 3 — Confidence Intervals & Power Analysis`, Vietnamese,
  with `**Dataset:**`, `**Mục tiêu:**`, and a `> **Output của notebook này:**` blockquote.
- `## 0. Setup` cell: imports (`pandas, numpy, matplotlib.pyplot, matplotlib.gridspec,
  seaborn, scipy.stats, warnings, os`), constants
  `RANDOM_SEED = 42`, `ALPHA = 0.05`, **`N_BOOTSTRAP = 5000`**,
  `FIGURES_DIR = "../report/figures"`, `DATA_OUT = "../data/processed"`,
  `os.makedirs(..., exist_ok=True)`, `sns.set_theme(style="whitegrid", palette="muted",
  font_scale=1.1)`, `plt.rcParams.update({"figure.dpi":150,"savefig.bbox":"tight"})`,
  `np.random.seed(RANDOM_SEED)`.
- Sectioned `## N.` / `### N.M` markdown headers; `> **Nhận xét:**` interpretation
  callouts after each result.
- Figures: `fig.savefig(f"{FIGURES_DIR}/ci_*.png")` — **`ci_` prefix** (eda_→01, hyp_→02, ci_→03).
- Load clean data: `df_clean = pd.read_csv(f"{DATA_OUT}/student_mat_clean.csv")`.
- New dependency: add `statsmodels` power tools (`statsmodels.stats.power.TTestIndPower`,
  `tt_ind_solve_power`) — `statsmodels` already in `requirements.txt`. `pingouin` available
  too (optional, for `compute_effsize` / `power_ttest` cross-check).

## Notebook structure — `notebooks/03_confidence_intervals.ipynb`

**Title** (markdown) — Phase 3 overview + output list.

**0. Setup** — constants + imports + style (as above).

**1. Load & recap data** — read `student_mat_clean.csv`; print shape; reusable bootstrap
helper defined here:
- `bootstrap_ci(data, stat_fn=np.mean, n_boot=N_BOOTSTRAP, ci=95, method="percentile"|"bca")`
  returning `(point, lo, hi, boot_dist)`. Implement percentile and BCa (bias-correction
  + acceleration via jackknife) so §3 can reuse both.
- `t_ci_mean(data, conf=0.95)` → parametric t-interval using `stats.t.interval` /
  `stats.sem`.

**2. Parametric CI for mean G3 (95%)** — t-interval on `df_clean["G3"]`; report mean,
SE, df, margin of error, [lo, hi]. `Nhận xét` callout.

**3. Bootstrap CI for mean G3 (n_bootstrap=5000)** — percentile + BCa via helper;
compare against the parametric interval in a small table.
- Figure `ci_bootstrap_mean_g3.png`: histogram of 5000 bootstrap means with
  parametric vs percentile vs BCa bounds drawn as vlines.
- Extension: bootstrap CI for the **median** G3 (shows bootstrap's value for a
  statistic with no clean parametric formula).

**4. CIs for group differences** — difference in mean G3 for:
- `sex`: M − F
- `address`: U − R
For each: (a) parametric Welch CI for difference of means (`stats.t.interval` with
Welch–Satterthwaite df, or `pingouin.ttest` CI), and (b) bootstrap CI of the difference
(resample each group independently). Also bootstrap CI for **Cohen's d** per comparison.
- Figure `ci_group_differences.png`: forest plot — point estimate + CI whiskers for
  each difference, reference line at 0 (CI crossing 0 ⇒ not significant at α).
- `Nhận xét` callout linking back to whether 0 is inside each interval.

**5. Power analysis** — `TTestIndPower`:
- Post-hoc achieved power at **n=357** (per-group n from actual sex / address splits)
  for the *observed* effect sizes (from §4 Cohen's d) and for a *medium* effect (d=0.5).
- Required total n for power=0.80 at d=0.5 (`tt_ind_solve_power`).
- Figure `ci_power_curve.png`: power vs sample-size-per-group curves for d=0.2/0.5/0.8,
  with markers at the project's actual n and the 0.80 threshold line.
- Markdown note: analysis uses n=357 (clean sample); 395 was the raw pre-cleaning size
  (README §1 note).

**6. Export results** — assemble a tidy DataFrame `ci_results` with columns
`[quantity, group, method, point_estimate, ci_lower, ci_upper, conf_level, n]`
covering every CI computed (mean G3 parametric/percentile/BCa, median, sex diff,
address diff, Cohen's d's). Save:
`ci_results.to_csv(f"{DATA_OUT}/bootstrap_ci_results.csv", index=False)`.
Print confirmation + a `## Tóm tắt` summary cell.

## Files

- **Create:** `notebooks/03_confidence_intervals.ipynb`
- **Generates on run:** `data/processed/bootstrap_ci_results.csv`,
  `report/figures/ci_bootstrap_mean_g3.png`, `report/figures/ci_group_differences.png`,
  `report/figures/ci_power_curve.png`
- **No edits** to `data/raw/`, `student_mat_clean.csv`, or `01_EDA.ipynb`.
- Optional: tick the 4 Phase 3 boxes in `README.md` §8 (only if desired).

## Verification

1. `jupyter nbconvert --to notebook --execute --inplace notebooks/03_confidence_intervals.ipynb`
   (or "Restart & Run All" in Jupyter) — must run top-to-bottom with no errors,
   honoring the README pre-push checklist.
2. Confirm `data/processed/bootstrap_ci_results.csv` exists and parses
   (`pd.read_csv` → expected columns, one row per CI).
3. Confirm the 3 `report/figures/ci_*.png` files were written.
4. Sanity checks: parametric and bootstrap mean-G3 CIs should nearly coincide
   (≈ ±0.1); each group-difference forest-plot whisker matches its CSV row;
   power numbers within [0,1] and required-n increases as effect size shrinks.
5. No absolute paths (`C:/Users/...`) anywhere — all paths relative via the
   `FIGURES_DIR` / `DATA_OUT` constants.
