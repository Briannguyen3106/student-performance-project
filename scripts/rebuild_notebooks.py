import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NB_DIR = ROOT / "notebooks"


def md(source):
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


def write_notebook(name, cells):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    with (NB_DIR / name).open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(notebook, ensure_ascii=False, indent=1))


COMMON_SETUP = '''import os
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
RANDOM_SEED = 42
ALPHA = 0.05
ROOT = Path("..").resolve()
DATA_RAW = ROOT / "data" / "raw"
DATA_OUT = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "report" / "figures"
DATA_OUT.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
np.random.seed(RANDOM_SEED)
sns.set_theme(style="whitegrid", palette="muted", font_scale=1.05)
plt.rcParams.update({"figure.dpi": 120, "savefig.bbox": "tight"})
pd.set_option("display.max_columns", 50)

def display_table(data, caption=None, precision=3):
    """Hiển thị DataFrame với đường viền rõ, dùng được trực tiếp trong Jupyter."""
    if isinstance(data, pd.Series):
        data = data.rename("value").to_frame()
    styler = (
        data.style
        .format(precision=precision, na_rep="-")
        .set_caption(caption or "")
        .set_table_styles([
            {"selector": "table", "props": [("border-collapse", "collapse"), ("width", "100%")]},
            {"selector": "th", "props": [("border", "1px solid #777"), ("padding", "6px"),
                                           ("background-color", "#e9eef5"), ("text-align", "center")]},
            {"selector": "td", "props": [("border", "1px solid #999"), ("padding", "6px")]},
            {"selector": "caption", "props": [("caption-side", "top"), ("font-weight", "bold"),
                                                ("font-size", "1.05em"), ("padding", "6px")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#f7f9fc")]},
        ])
    )
    display(styler)

print(f"Project root: {ROOT}")'''


def notebook_01():
    cells = [
        md('''# Phase 1 - Exploratory Data Analysis

**Mục tiêu:** mô tả bộ dữ liệu Student Performance, kiểm tra chất lượng dữ liệu và tạo tập dữ liệu dùng cho các phase sau.

**Nguyên tắc xử lý:**
- `G3=0` là giá trị hợp lệ theo `student.txt`; phân tích chính giữ đủ 395 quan sát.
- Không ghi đè `absences`. Winsorization chỉ được đánh giá trong sensitivity analysis.
- Đây là dữ liệu quan sát từ hai trường; các kết quả mô tả mối liên hệ, không chứng minh quan hệ nhân quả.'''),
        md("## 0. Setup"),
        code(COMMON_SETUP),
        md("## 1. Load dữ liệu và kiểm tra chất lượng"),
        code('''df_raw = pd.read_csv(DATA_RAW / "student-mat.csv", sep=";")
print(f"Shape: {df_raw.shape[0]} học sinh x {df_raw.shape[1]} biến")
print(f"Missing values: {int(df_raw.isna().sum().sum())}")
print(f"Duplicate rows: {int(df_raw.duplicated().sum())}")
print(f"G3=0: {(df_raw['G3'] == 0).sum()} ({(df_raw['G3'] == 0).mean():.1%})")
print()
print("Phân bố failures:", df_raw["failures"].value_counts().sort_index().to_dict())
print("Lưu ý: CSV dùng failures=0..3, trong khi student.txt mô tả không hoàn toàn nhất quán ở mức gộp cuối.")
display_table(df_raw.head(), "5 quan sát đầu tiên")'''),
        md("## 2. Phân loại biến và thống kê mô tả"),
        code('''binary_cols = ["school", "sex", "address", "famsize", "Pstatus", "schoolsup", "famsup",
               "paid", "activities", "nursery", "higher", "internet", "romantic"]
nominal_cols = ["Mjob", "Fjob", "reason", "guardian"]
ordinal_cols = ["Medu", "Fedu", "traveltime", "studytime", "failures", "famrel", "freetime",
                "goout", "Dalc", "Walc", "health"]
numeric_cols = df_raw.select_dtypes(include=np.number).columns.tolist()
desc = df_raw[numeric_cols].describe().T
desc["skewness"] = df_raw[numeric_cols].skew()
display_table(desc, "Thống kê mô tả các biến numeric")'''),
        md("## 3. Phân phối G3 và sensitivity theo G3=0"),
        code('''g3 = df_raw["G3"]
fig, axes = plt.subplots(1, 3, figsize=(14, 4))
sns.histplot(g3, bins=21, kde=False, ax=axes[0], color="#4C72B0")
axes[0].axvline(g3.mean(), color="red", ls="--", label=f"Mean={g3.mean():.2f}")
axes[0].axvline(g3.median(), color="purple", ls=":", label=f"Median={g3.median():.1f}")
axes[0].legend(); axes[0].set_title("Phân phối G3 - toàn bộ mẫu")
sns.boxplot(y=g3, ax=axes[1], color="#55A868"); axes[1].set_title("Boxplot G3")
stats.probplot(g3, dist="norm", plot=axes[2]); axes[2].set_title("Q-Q plot G3")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_g3_distribution.png"); plt.show()

sensitivity_g3 = pd.DataFrame([
    {"sample": "All valid grades", "n": len(df_raw), "mean": g3.mean(), "median": g3.median(), "sd": g3.std()},
    {"sample": "Conditional G3>0", "n": int((g3 > 0).sum()), "mean": g3[g3 > 0].mean(),
     "median": g3[g3 > 0].median(), "sd": g3[g3 > 0].std()},
])
display_table(sensitivity_g3, "Sensitivity khi giữ hoặc loại G3=0")
print("Tập G3>0 chỉ là sensitivity analysis, không thay thế mẫu phân tích chính.")'''),
        md("## 4. Outlier và sensitivity cho absences"),
        code('''continuous_cols = ["age", "absences", "G1", "G2", "G3"]
rows = []
for col in continuous_cols:
    q1, q3 = df_raw[col].quantile([0.25, 0.75]); iqr = q3 - q1
    lo, hi = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    rows.append({"variable": col, "lower": lo, "upper": hi,
                 "n_outliers": int(((df_raw[col] < lo) | (df_raw[col] > hi)).sum())})
display_table(pd.DataFrame(rows), "Tóm tắt outlier theo quy tắc IQR")

cap95 = df_raw["absences"].quantile(0.95)
abs_winsor = df_raw["absences"].clip(upper=cap95)
rho_raw, p_raw = stats.spearmanr(df_raw["absences"], df_raw["G3"])
rho_win, p_win = stats.spearmanr(abs_winsor, df_raw["G3"])
print(f"Spearman absences-G3 raw: rho={rho_raw:.3f}, p={p_raw:.4g}")
print(f"Spearman absences-G3 winsorized@95%: rho={rho_win:.3f}, p={p_win:.4g}")
print("Dữ liệu xuất ra giữ absences gốc; winsorization không được ghi đè.")

fig, axes = plt.subplots(1, len(continuous_cols), figsize=(14, 4))
for ax, col in zip(axes, continuous_cols):
    sns.boxplot(y=df_raw[col], ax=ax, color="#8172B3"); ax.set_title(col)
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_outliers_boxplot.png"); plt.show()'''),
        md("## 5. Mối liên hệ mô tả với G3"),
        code('''corr = df_raw[numeric_cols].corr(method="spearman")
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, cmap="vlag", center=0, vmin=-1, vmax=1, annot=True, fmt=".2f",
            annot_kws={"size": 8}, ax=ax)
ax.set_title("Spearman correlation - mô tả khám phá")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_correlation_heatmap_spearman.png"); plt.show()

g3_corr = corr["G3"].drop(["G1", "G2", "G3"]).sort_values(key=abs, ascending=False)
print("Tương quan Spearman với G3 (exploratory, chưa hiệu chỉnh multiple testing):")
display_table(g3_corr, "Spearman correlation với G3")'''),
        md("### 5.1 Bias-corrected Cramér's V"),
        code('''from scipy.stats import chi2_contingency

def cramers_v_corrected(x, y):
    table = pd.crosstab(x, y)
    chi2 = chi2_contingency(table, correction=False)[0]
    n = table.to_numpy().sum(); r, k = table.shape
    phi2 = chi2 / n
    phi2_corr = max(0, phi2 - ((k - 1) * (r - 1)) / (n - 1))
    r_corr = r - ((r - 1) ** 2) / (n - 1)
    k_corr = k - ((k - 1) ** 2) / (n - 1)
    denom = min(k_corr - 1, r_corr - 1)
    return np.sqrt(phi2_corr / denom) if denom > 0 else 0.0

all_cat = binary_cols + nominal_cols
cv = pd.DataFrame(index=all_cat, columns=all_cat, dtype=float)
for a in all_cat:
    for b in all_cat:
        cv.loc[a, b] = cramers_v_corrected(df_raw[a], df_raw[b])
fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(cv, mask=np.triu(np.ones_like(cv, dtype=bool)), cmap="YlOrRd", vmin=0, vmax=1,
            annot=True, fmt=".2f", annot_kws={"size": 8}, ax=ax)
ax.set_title("Bias-corrected Cramér's V")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_cramers_v_heatmap.png"); plt.show()'''),
        md("## 6. Biểu đồ nhóm và scatter"),
        code('''group_vars = ["sex", "address", "famsup", "higher", "school", "Pstatus", "internet", "romantic"]
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, col in zip(axes.flat, group_vars):
    sns.pointplot(data=df_raw, x=col, y="G3", errorbar=("ci", 95), capsize=.12, ax=ax)
    ax.set_title(f"Mean G3 theo {col}"); ax.set_ylim(0, 20)
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_g3_by_group.png"); plt.show()

fig, axes = plt.subplots(1, 4, figsize=(18, 5))
for ax, col in zip(axes, nominal_cols):
    order = df_raw.groupby(col)["G3"].median().sort_values(ascending=False).index
    sns.boxplot(data=df_raw, x=col, y="G3", order=order, ax=ax, color="#a1d99b")
    ax.tick_params(axis="x", rotation=25)
    ax.set_title(f"G3 theo {col} (exploratory)")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_g3_by_nominal.png"); plt.show()

scatter_vars = ["studytime", "failures", "absences", "Walc", "Medu", "Fedu", "goout", "freetime"]
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for ax, var in zip(axes.flat, scatter_vars):
    sns.regplot(data=df_raw, x=var, y="G3", lowess=True, scatter_kws={"alpha": .3, "s": 18}, ax=ax)
    rho, _ = stats.spearmanr(df_raw[var], df_raw["G3"])
    ax.set_title(f"{var}: rho={rho:.2f}")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "eda_scatter_g3.png"); plt.show()'''),
        md("## 7. Xuất dữ liệu phân tích"),
        code('''df_clean = df_raw.copy()
output_path = DATA_OUT / "student_mat_clean.csv"
with output_path.open("w", encoding="utf-8", newline="") as handle:
    df_clean.to_csv(handle, index=False, lineterminator=chr(10))
print(f"Đã xuất {output_path}: {df_clean.shape[0]} rows x {df_clean.shape[1]} columns")
print("Không loại G3=0; không thay đổi absences.")'''),
        md('''## Kết luận Phase 1

- Bộ dữ liệu không có missing hoặc duplicate và gồm 395 học sinh từ hai trường.
- `G3=0` được giữ vì data dictionary xác định thang điểm hợp lệ là 0-20.
- `absences` có đuôi phải dài nhưng dữ liệu gốc được bảo toàn; kết quả winsorized chỉ dùng để kiểm tra độ nhạy.
- Các tương quan và khác biệt nhóm ở đây mang tính khám phá. Không diễn giải là quan hệ nhân quả và không dùng p-value EDA như bằng chứng xác nhận.'''),
    ]
    write_notebook("01_EDA.ipynb", cells)


def notebook_02():
    cells = [
        md('''# Phase 2 - Hypothesis Testing

Phân tích xác nhận trên toàn bộ 395 quan sát. Các kiểm định đều hai phía. So sánh hai nhóm dùng Welch t-test để ước lượng khác biệt trung bình; Shapiro-Wilk và Levene chỉ là diagnostics, không dùng làm pre-test để tự động đổi phương pháp. P-value của 10 kiểm định chính được hiệu chỉnh Holm.

H9 (`absences`) là giả thuyết exploratory/post-hoc vì được hình thành sau EDA.'''),
        md("## 0. Setup và dữ liệu"),
        code(COMMON_SETUP + '''
from itertools import combinations
from statsmodels.stats.multitest import multipletests

df = pd.read_csv(DATA_OUT / "student_mat_clean.csv")
assert len(df) == 395, "Phase 2 phải dùng đủ 395 quan sát"
print(f"Shape: {df.shape}")'''),
        md("## 1. Hàm hỗ trợ"),
        code('''def hedges_g(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    nx, ny = len(x), len(y)
    pooled = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    d = (x.mean() - y.mean()) / pooled
    correction = 1 - 3 / (4 * (nx + ny) - 9)
    return d * correction

def epsilon_squared(h, k, n):
    return max(0.0, (h - k + 1) / (n - k))

def two_group_test(label, variable, level_a, level_b, note=""):
    x = df.loc[df[variable] == level_a, "G3"].to_numpy()
    y = df.loc[df[variable] == level_b, "G3"].to_numpy()
    t, p = stats.ttest_ind(x, y, equal_var=False)
    lev, p_lev = stats.levene(x, y, center="median")
    return {
        "hypothesis": label, "contrast": f"{level_a} - {level_b}", "test": "Welch t-test",
        "statistic": t, "p_raw": p, "effect": "Hedges g", "effect_value": hedges_g(x, y),
        "estimate": x.mean() - y.mean(), "n": len(x) + len(y), "diagnostic": f"Levene p={p_lev:.3g}",
        "note": note,
    }

def kruskal_test(label, variable, note=""):
    groups = [g["G3"].to_numpy() for _, g in df.groupby(variable, sort=True)]
    h, p = stats.kruskal(*groups)
    return {
        "hypothesis": label, "contrast": "omnibus", "test": "Kruskal-Wallis", "statistic": h,
        "p_raw": p, "effect": "epsilon^2", "effect_value": epsilon_squared(h, len(groups), len(df)),
        "estimate": np.nan, "n": len(df), "diagnostic": "ordinal groups", "note": note,
    }

def spearman_test(label, variable, note=""):
    rho, p = stats.spearmanr(df[variable], df["G3"])
    return {
        "hypothesis": label, "contrast": f"{variable} vs G3", "test": "Spearman", "statistic": rho,
        "p_raw": p, "effect": "rho", "effect_value": rho, "estimate": rho, "n": len(df),
        "diagnostic": "ordinal/rank association", "note": note,
    }

def dunn_posthoc(data, group_col, value_col="G3"):
    work = data[[group_col, value_col]].dropna().copy()
    work["rank"] = stats.rankdata(work[value_col])
    n = len(work)
    tie_counts = work[value_col].value_counts().to_numpy()
    tie_correction = 1 - np.sum(tie_counts**3 - tie_counts) / (n**3 - n)
    rank_means = work.groupby(group_col)["rank"].mean()
    sizes = work.groupby(group_col).size()
    variance = n * (n + 1) / 12 * tie_correction
    rows = []
    for a, b in combinations(rank_means.index, 2):
        se = np.sqrt(variance * (1 / sizes[a] + 1 / sizes[b]))
        z = (rank_means[a] - rank_means[b]) / se
        rows.append({"variable": group_col, "group_a": a, "group_b": b, "z": z,
                     "p_raw": 2 * stats.norm.sf(abs(z))})
    result = pd.DataFrame(rows)
    result["p_holm"] = multipletests(result["p_raw"], method="holm")[1]
    return result

def annotate(ax, text):
    ax.text(.02, .98, text, transform=ax.transAxes, ha="left", va="top", fontsize=9,
            bbox={"boxstyle": "round", "facecolor": "white", "alpha": .85})'''),
        md("## 2. Chạy 10 kiểm định chính"),
        code('''results = [
    two_group_test("H1: sex", "sex", "M", "F"),
    two_group_test("H2: address", "address", "U", "R"),
    two_group_test("H3: famsup", "famsup", "yes", "no", note="observational; confounding possible"),
    kruskal_test("H4: studytime", "studytime"),
    spearman_test("H5: Walc", "Walc"),
    two_group_test("H6: higher", "higher", "yes", "no"),
    kruskal_test("H7: failures", "failures"),
    kruskal_test("H8a: Medu", "Medu"),
    kruskal_test("H8b: Fedu", "Fedu"),
    spearman_test("H9: absences", "absences", note="post-hoc/exploratory"),
]
summary = pd.DataFrame(results)
summary["p_holm"] = multipletests(summary["p_raw"], method="holm")[1]
summary["significant_holm"] = summary["p_holm"] < ALPHA
summary = summary[["hypothesis", "contrast", "test", "statistic", "p_raw", "p_holm",
                   "effect", "effect_value", "estimate", "n", "diagnostic", "note", "significant_holm"]]
display_table(summary, "Kết quả kiểm định chính và Holm correction", precision=4)
with (DATA_OUT / "hypothesis_test_results.csv").open("w", encoding="utf-8", newline="") as handle:
    summary.to_csv(handle, index=False, lineterminator=chr(10))'''),
        md("## 3. Dunn post-hoc sau Kruskal-Wallis"),
        code('''posthoc = pd.concat([dunn_posthoc(df, var) for var in ["studytime", "failures", "Medu", "Fedu"]],
                    ignore_index=True)
posthoc["significant_holm"] = posthoc["p_holm"] < ALPHA
with (DATA_OUT / "hypothesis_posthoc_results.csv").open("w", encoding="utf-8", newline="") as handle:
    posthoc.to_csv(handle, index=False, lineterminator=chr(10))
display_table(posthoc, "Dunn post-hoc với Holm correction", precision=4)'''),
        md("## 4. Biểu đồ có annotation"),
        code('''plot_specs = [
    ("sex", "hyp_h1_sex_g3.png", "H1: sex"), ("address", "hyp_h2_address_g3.png", "H2: address"),
    ("famsup", "hyp_h3_famsup_g3.png", "H3: famsup"), ("studytime", "hyp_h4_studytime_g3.png", "H4: studytime"),
    ("higher", "hyp_h6_higher_g3.png", "H6: higher"), ("failures", "hyp_h7_failures_g3.png", "H7: failures"),
    ("Medu", "hyp_h8a_medu_g3.png", "H8a: Medu"), ("Fedu", "hyp_h8b_fedu_g3.png", "H8b: Fedu"),
]
for var, filename, key in plot_specs:
    row = summary.loc[summary["hypothesis"] == key].iloc[0]
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.boxplot(data=df, x=var, y="G3", ax=ax, color="#9ecae1")
    sns.stripplot(data=df, x=var, y="G3", ax=ax, color="black", alpha=.2, size=2)
    counts = df[var].value_counts().sort_index()
    ax.set_xticklabels([tick.get_text() + chr(10) + f"n={counts.get(type(counts.index[0])(tick.get_text()), counts.get(tick.get_text(), ''))}"
                        for tick in ax.get_xticklabels()])
    annotate(ax, f"{row['test']}" + chr(10) + f"Holm p={row['p_holm']:.3g}" + chr(10) +
             f"{row['effect']}={row['effect_value']:.3f}")
    ax.set_title(key); fig.tight_layout(); fig.savefig(FIGURES_DIR / filename); plt.show()

for var, filename, key in [("Walc", "hyp_h5_walc_g3.png", "H5: Walc"),
                           ("absences", "hyp_h9_absences_g3.png", "H9: absences")]:
    row = summary.loc[summary["hypothesis"] == key].iloc[0]
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.regplot(data=df, x=var, y="G3", lowess=True, scatter_kws={"alpha": .35}, ax=ax)
    annotate(ax, f"Spearman rho={row['effect_value']:.3f}" + chr(10) + f"Holm p={row['p_holm']:.3g}")
    ax.set_title(key + (" (post-hoc)" if var == "absences" else ""))
    fig.tight_layout(); fig.savefig(FIGURES_DIR / filename); plt.show()
print("Đã xuất 10 figures hyp_*.png")'''),
        md('''## Kết luận Phase 2

- Kết luận chính dựa trên p-value đã hiệu chỉnh Holm, không dựa trên p-value thô.
- Welch t-test ước lượng khác biệt trung bình và không giả định phương sai bằng nhau; Levene được báo cáo như diagnostic.
- Với biến nhiều mức, Kruskal-Wallis chỉ là omnibus test; bảng Dunn-Holm xác định cặp nhóm khác nhau.
- Dấu effect size luôn theo contrast ghi trong bảng, ví dụ `yes - no` hoặc `U - R`.
- Kết quả chỉ mô tả association trong dữ liệu quan sát. H9 vẫn được ghi rõ là exploratory.'''),
    ]
    write_notebook("02_hypothesis_testing.ipynb", cells)


def notebook_03():
    cells = [
        md('''# Phase 3 - Confidence Intervals and Sensitivity Analysis

Notebook báo cáo CI cho trung bình G3 và bốn contrast được xác định rõ: `M-F`, `U-R`, `higher yes-no`, `failures 0->0`. Power hậu nghiệm dựa trên effect quan sát được thay bằng minimum detectable effect (MDE) ở power 80%.'''),
        md("## 0. Setup và dữ liệu"),
        code(COMMON_SETUP + '''
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower

N_BOOTSTRAP = 5000
df = pd.read_csv(DATA_OUT / "student_mat_clean.csv")
assert len(df) == 395
print(f"Shape: {df.shape}")'''),
        md("## 1. Hàm CI và effect size"),
        code('''def bootstrap_ci(data, stat_fn=np.mean, n_boot=N_BOOTSTRAP, ci=.95, method="percentile", seed=RANDOM_SEED):
    data = np.asarray(data, float); rng = np.random.default_rng(seed); n = len(data)
    point = stat_fn(data)
    boot = np.array([stat_fn(data[rng.integers(0, n, n)]) for _ in range(n_boot)])
    alpha = 1 - ci
    if method == "percentile":
        lo, hi = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    elif method == "bca":
        prop = np.clip(np.mean(boot < point), 1e-9, 1 - 1e-9)
        z0 = stats.norm.ppf(prop)
        jack = np.array([stat_fn(np.delete(data, i)) for i in range(n)])
        delta = jack.mean() - jack
        acceleration = np.sum(delta**3) / (6 * np.sum(delta**2)**1.5) if np.sum(delta**2) else 0
        z = stats.norm.ppf([alpha / 2, 1 - alpha / 2])
        adjusted = stats.norm.cdf(z0 + (z0 + z) / (1 - acceleration * (z0 + z)))
        lo, hi = np.quantile(boot, adjusted)
    else:
        raise ValueError("method must be percentile or bca")
    return point, lo, hi, boot

def t_ci_mean(x, conf=.95):
    x = np.asarray(x, float); mean = x.mean(); se = stats.sem(x)
    lo, hi = stats.t.interval(conf, len(x) - 1, loc=mean, scale=se)
    return mean, lo, hi

def hedges_g(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float); nx, ny = len(x), len(y)
    pooled = np.sqrt(((nx - 1) * x.var(ddof=1) + (ny - 1) * y.var(ddof=1)) / (nx + ny - 2))
    return ((x.mean() - y.mean()) / pooled) * (1 - 3 / (4 * (nx + ny) - 9))

def welch_diff_ci(x, y, conf=.95):
    x, y = np.asarray(x, float), np.asarray(y, float); nx, ny = len(x), len(y)
    vx, vy = x.var(ddof=1), y.var(ddof=1); diff = x.mean() - y.mean()
    se = np.sqrt(vx / nx + vy / ny)
    dof = (vx / nx + vy / ny)**2 / ((vx / nx)**2 / (nx - 1) + (vy / ny)**2 / (ny - 1))
    lo, hi = stats.t.interval(conf, dof, loc=diff, scale=se)
    return diff, lo, hi

def bootstrap_two_group(x, y, stat_fn, n_boot=N_BOOTSTRAP, seed=RANDOM_SEED):
    x, y = np.asarray(x, float), np.asarray(y, float); rng = np.random.default_rng(seed)
    boot = np.empty(n_boot)
    for i in range(n_boot):
        sx = x[rng.integers(0, len(x), len(x))]; sy = y[rng.integers(0, len(y), len(y))]
        boot[i] = stat_fn(sx, sy)
    return stat_fn(x, y), *np.quantile(boot, [.025, .975])'''),
        md("## 2. CI cho trung bình và trung vị G3"),
        code('''records = []
mean_t = t_ci_mean(df["G3"])
mean_pct = bootstrap_ci(df["G3"], np.mean, method="percentile")
mean_bca = bootstrap_ci(df["G3"], np.mean, method="bca")
median_pct = bootstrap_ci(df["G3"], np.median, method="percentile")
for quantity, method, values in [
    ("mean_G3", "t", mean_t), ("mean_G3", "bootstrap_percentile", mean_pct[:3]),
    ("mean_G3", "bootstrap_bca", mean_bca[:3]), ("median_G3", "bootstrap_percentile", median_pct[:3]),
]:
    records.append({"quantity": quantity, "group": "all", "method": method,
                    "point_estimate": values[0], "ci_lower": values[1], "ci_upper": values[2], "n": len(df)})
display_table(pd.DataFrame(records), "CI cho trung bình và trung vị G3", precision=4)

fig, ax = plt.subplots(figsize=(9, 5))
ax.hist(mean_pct[3], bins=50, color="#4C72B0", alpha=.75)
for value, color, label in [(mean_t[0], "black", "mean"), (mean_bca[1], "purple", "BCa 95% CI"),
                            (mean_bca[2], "purple", None)]:
    ax.axvline(value, color=color, ls="--", label=label)
ax.legend(); ax.set_title("Bootstrap distribution of mean G3 - n=395")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "ci_bootstrap_mean_g3.png"); plt.show()'''),
        md("## 3. CI cho các contrast được định nghĩa trước"),
        code('''contrasts = [
    ("sex (M - F)", df.loc[df.sex == "M", "G3"], df.loc[df.sex == "F", "G3"]),
    ("address (U - R)", df.loc[df.address == "U", "G3"], df.loc[df.address == "R", "G3"]),
    ("higher (yes - no)", df.loc[df.higher == "yes", "G3"], df.loc[df.higher == "no", "G3"]),
    ("failures (0 - >0)", df.loc[df.failures == 0, "G3"], df.loc[df.failures > 0, "G3"]),
]
contrast_rows = []
for label, x, y in contrasts:
    w = welch_diff_ci(x, y)
    b = bootstrap_two_group(x, y, lambda a, b: a.mean() - b.mean())
    g = bootstrap_two_group(x, y, hedges_g)
    contrast_rows.append({"comparison": label, "n1": len(x), "n2": len(y), "diff_mean": w[0],
                          "welch_lo": w[1], "welch_hi": w[2], "boot_lo": b[1], "boot_hi": b[2],
                          "hedges_g": g[0], "g_lo": g[1], "g_hi": g[2]})
    records.extend([
        {"quantity": "diff_mean_G3", "group": label, "method": "welch", "point_estimate": w[0],
         "ci_lower": w[1], "ci_upper": w[2], "n": len(x) + len(y)},
        {"quantity": "diff_mean_G3", "group": label, "method": "bootstrap_percentile", "point_estimate": b[0],
         "ci_lower": b[1], "ci_upper": b[2], "n": len(x) + len(y)},
        {"quantity": "hedges_g", "group": label, "method": "bootstrap_percentile", "point_estimate": g[0],
         "ci_lower": g[1], "ci_upper": g[2], "n": len(x) + len(y)},
    ])
contrast_table = pd.DataFrame(contrast_rows)
display_table(contrast_table, "CI cho các contrast định nghĩa trước", precision=4)

fig, ax = plt.subplots(figsize=(10, 6))
ypos = np.arange(len(contrast_table))[::-1]
for y, (_, row) in zip(ypos, contrast_table.iterrows()):
    ax.plot([row.boot_lo, row.boot_hi], [y, y], lw=2, color="#4C72B0")
    ax.plot(row.diff_mean, y, "o", color="#4C72B0")
ax.axvline(0, color="black", ls="--"); ax.set_yticks(ypos); ax.set_yticklabels(contrast_table.comparison)
ax.set_xlabel("Mean difference in G3 (bootstrap 95% CI)"); ax.set_title("Predefined group contrasts")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "ci_group_differences.png"); plt.show()'''),
        md("## 4. Sensitivity analysis cho quyết định dữ liệu"),
        code('''sensitivity = []
for label, sample in [("all G3 values", df), ("conditional G3>0", df[df.G3 > 0])]:
    point, lo, hi, _ = bootstrap_ci(sample["G3"], np.mean, method="bca")
    rho, p = stats.spearmanr(sample["absences"], sample["G3"])
    sensitivity.append({"sample": label, "n": len(sample), "mean_G3": point, "mean_bca_lo": lo,
                        "mean_bca_hi": hi, "rho_absences_G3": rho, "p_absences_G3": p})
display_table(pd.DataFrame(sensitivity), "Sensitivity analysis cho quyết định dữ liệu", precision=4)'''),
        md("## 5. Sensitivity power: minimum detectable effect"),
        code('''tt_power = TTestIndPower()
mde_rows = []
for label, x, y in contrasts:
    ratio = len(y) / len(x)
    mde = tt_power.solve_power(effect_size=None, nobs1=len(x), alpha=ALPHA, power=.80,
                               ratio=ratio, alternative="two-sided")
    mde_rows.append({"comparison": label, "n1": len(x), "n2": len(y), "MDE_d_at_80pct_power": mde})
mde_table = pd.DataFrame(mde_rows)
display_table(mde_table, "Minimum detectable effect tại power 80%", precision=4)

anova_power = FTestAnovaPower()
anova_mde = anova_power.solve_power(effect_size=None, nobs=len(df), alpha=ALPHA, power=.80, k_groups=4)
print(f"ANOVA sensitivity for failures (4 groups, balanced approximation): MDE Cohen f={anova_mde:.3f}")
print("Lưu ý: phép tính ANOVA là xấp xỉ vì nhóm failures mất cân bằng và Phase 2 dùng Kruskal-Wallis.")

n_range = np.arange(10, 401)
fig, ax = plt.subplots(figsize=(9, 5))
for d, color in zip([.2, .3, .5], ["#C44E52", "#8172B3", "#4C72B0"]):
    ax.plot(n_range, tt_power.power(d, n_range, ALPHA, ratio=1), label=f"d={d}", color=color)
ax.axhline(.8, color="black", ls="--", label="power=.80")
ax.set_xlabel("n per group (balanced design)"); ax.set_ylabel("Power"); ax.legend()
ax.set_title("Sensitivity curves for two-sample tests")
fig.tight_layout(); fig.savefig(FIGURES_DIR / "ci_power_curve.png"); plt.show()'''),
        md("## 6. Xuất kết quả"),
        code('''ci_results = pd.DataFrame(records)
ci_results["conf_level"] = .95
ci_results = ci_results[["quantity", "group", "method", "point_estimate", "ci_lower", "ci_upper", "conf_level", "n"]]
with (DATA_OUT / "bootstrap_ci_results.csv").open("w", encoding="utf-8", newline="") as handle:
    ci_results.to_csv(handle, index=False, lineterminator=chr(10))
with (DATA_OUT / "power_sensitivity_results.csv").open("w", encoding="utf-8", newline="") as handle:
    mde_table.to_csv(handle, index=False, lineterminator=chr(10))
print(f"Đã xuất {len(ci_results)} dòng CI và {len(mde_table)} dòng sensitivity power.")'''),
        md('''## Kết luận Phase 3

- CI được báo cáo cho toàn bộ mẫu 395 quan sát và cho bốn contrast định nghĩa trước.
- Các CI 95% của contrast là khoảng riêng lẻ, chưa phải simultaneous CI; kết luận xác nhận nhiều giả thuyết vẫn dựa trên Holm correction ở Phase 2.
- CI diễn tả độ bất định của ước lượng; không loại bỏ confounding hoặc giới hạn khả năng khái quát hóa.
- So sánh `G3>0` chỉ là sensitivity analysis, cho thấy hậu quả của việc loại điểm 0.
- MDE ở power 80% thay cho observed power, tránh diễn giải vòng tròn từ effect size quan sát và p-value.
- CI bootstrap vẫn giả định các quan sát đủ độc lập; cấu trúc học sinh nằm trong hai trường là một giới hạn của dữ liệu.'''),
    ]
    write_notebook("03_confidence_intervals.ipynb", cells)


if __name__ == "__main__":
    notebook_01()
    notebook_02()
    notebook_03()
    print("Rebuilt notebooks 01, 02, and 03.")
