import nbformat as nbf
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "notebooks" / "core"
OUT.mkdir(parents=True, exist_ok=True)


def md(text):
    return nbf.v4.new_markdown_cell(text.strip())


def code(text):
    return nbf.v4.new_code_cell(text.strip())


def write(name, cells):
    notebook = nbf.v4.new_notebook(
        cells=cells,
        metadata={
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3"},
        },
    )
    nbf.write(notebook, OUT / name)


COMMON_SETUP = r'''
from pathlib import Path
import warnings

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

RANDOM_SEED = 42
ALPHA = 0.05
ROOT = Path("../..")
DATA_RAW = ROOT / "data" / "raw"
DATA_OUT = ROOT / "data" / "processed"
FIGURES = ROOT / "report" / "figures"
DATA_OUT.mkdir(parents=True, exist_ok=True)
FIGURES.mkdir(parents=True, exist_ok=True)
'''


write(
    "01_data_preparation_and_eda.ipynb",
    [
        md(r'''
# 1. Thu thập, chuẩn bị và mô tả dữ liệu

Notebook cốt lõi cho Chương 1 và Chương 6 của học phần.

**Mục tiêu:** giới thiệu dữ liệu, kiểm tra chất lượng, phân loại biến và mô tả `G3`.
Các phân tích khám phá chi tiết hơn nằm trong `notebooks/01_EDA.ipynb`.
'''),
        code(COMMON_SETUP),
        md("## 1.1. Nguồn dữ liệu và đơn vị quan sát"),
        code(r'''
df = pd.read_csv(DATA_RAW / "student-mat.csv", sep=";")
print(f"Kích thước dữ liệu: {df.shape[0]} học sinh, {df.shape[1]} biến")
print(f"Giá trị thiếu: {int(df.isna().sum().sum())}")
print(f"Dòng trùng lặp: {int(df.duplicated().sum())}")
print("Khoảng G3:", (df["G3"].min(), df["G3"].max()))
df.head()
'''),
        md(r'''
Mỗi dòng là một học sinh môn Toán tại một trong hai trường. Đây là dữ liệu quan sát,
không phải dữ liệu từ thí nghiệm ngẫu nhiên. Vì vậy kết quả mô tả mối liên hệ, không tự
động chứng minh quan hệ nhân quả.
'''),
        md("## 1.2. Phân loại biến"),
        code(r'''
nominal = ["school", "sex", "address", "famsize", "Pstatus", "Mjob", "Fjob",
           "reason", "guardian", "schoolsup", "famsup", "paid", "activities",
           "nursery", "higher", "internet", "romantic"]
ordinal = ["Medu", "Fedu", "traveltime", "studytime", "failures", "famrel",
           "freetime", "goout", "Dalc", "Walc", "health"]
count = ["age", "absences"]
score = ["G1", "G2", "G3"]

variable_types = pd.DataFrame({
    "loai_bien": ["Định danh", "Thứ bậc", "Đếm", "Điểm số"],
    "so_bien": [len(nominal), len(ordinal), len(count), len(score)],
    "vi_du": [", ".join(nominal[:4]), ", ".join(ordinal[:4]), ", ".join(count), ", ".join(score)],
})
variable_types
'''),
        md("## 1.3. Thống kê mô tả và biểu diễn"),
        code(r'''
summary = df[["age", "absences", "G1", "G2", "G3"]].describe().T
summary

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
sns.histplot(df["G3"], bins=range(0, 22), discrete=True, ax=axes[0], color="#4C78A8")
axes[0].axvline(df["G3"].mean(), color="black", linestyle="--", label=f"Mean={df['G3'].mean():.2f}")
axes[0].set_title("Phân phối điểm cuối kỳ G3")
axes[0].legend()
sns.boxplot(data=df, x="school", y="G3", ax=axes[1], color="#72B7B2")
axes[1].set_title("G3 theo trường")
fig.tight_layout()
fig.savefig(FIGURES / "eda_course_overview.png", dpi=150, bbox_inches="tight")
plt.show()
'''),
        md("## 1.4. Chuẩn bị dữ liệu phân tích"),
        code(r'''
# Không sửa dữ liệu raw. G3=0 và các giá trị absences lớn vẫn được giữ.
df.to_csv(DATA_OUT / "student_mat_clean.csv", index=False)
print("Đã xuất dữ liệu phân tích:", DATA_OUT / "student_mat_clean.csv")
'''),
        md(r'''
## Kết luận

- Dữ liệu có 395 học sinh và 33 biến, không có missing hoặc dòng trùng lặp.
- `G3` nằm trên thang 0-20; trung bình khoảng 10,42 và trung vị 11.
- Các biến gồm định danh, thứ bậc, biến đếm và điểm số; loại thang đo cần được xét khi
  chọn phương pháp phân tích.
- Mẫu chỉ đến từ hai trường, nên khả năng khái quát hóa còn hạn chế.
'''),
    ],
)


write(
    "02_statistical_inference.ipynb",
    [
        md(r'''
# 2. Ước lượng và kiểm định giả thuyết

Notebook cốt lõi cho Chương 4.1-4.5. Nội dung tập trung vào khoảng tin cậy và một số
kiểm định đại diện. Multiple-testing correction, bootstrap BCa và post-hoc đầy đủ được
giữ trong các notebook phân tích mở rộng 02-03.
'''),
        code(COMMON_SETUP + '\ndf = pd.read_csv(DATA_OUT / "student_mat_clean.csv")'),
        md("## 2.1. Khoảng tin cậy cho trung bình G3"),
        code(r'''
n = len(df)
mean_g3 = df["G3"].mean()
se = stats.sem(df["G3"])
ci_mean = stats.t.interval(1 - ALPHA, df=n - 1, loc=mean_g3, scale=se)
print(f"Mean G3 = {mean_g3:.3f}")
print(f"95% CI = [{ci_mean[0]:.3f}, {ci_mean[1]:.3f}]")
'''),
        md("## 2.2. Hai nhóm: định hướng học đại học và G3"),
        code(r'''
yes = df.loc[df["higher"] == "yes", "G3"]
no = df.loc[df["higher"] == "no", "G3"]
t_stat, p_value = stats.ttest_ind(yes, no, equal_var=False)
diff = yes.mean() - no.mean()
se_diff = np.sqrt(yes.var(ddof=1)/len(yes) + no.var(ddof=1)/len(no))
df_welch = (yes.var(ddof=1)/len(yes) + no.var(ddof=1)/len(no))**2 / (
    (yes.var(ddof=1)/len(yes))**2/(len(yes)-1) + (no.var(ddof=1)/len(no))**2/(len(no)-1)
)
ci_diff = stats.t.interval(1 - ALPHA, df=df_welch, loc=diff, scale=se_diff)
print(f"Chênh lệch mean (yes - no) = {diff:.3f}")
print(f"Welch t={t_stat:.3f}, p={p_value:.4g}, 95% CI={ci_diff}")
print(f"Cỡ nhóm: yes={len(yes)}, no={len(no)}")
'''),
        md(r'''
Nhóm `higher=no` chỉ có 20 học sinh. Chênh lệch quan sát được không phải tác động nhân
quả của việc có ý định học đại học, vì các nhóm không được phân bổ ngẫu nhiên.
'''),
        md("## 2.3. Nhiều nhóm: số lần trượt môn trước đó"),
        code(r'''
failure_groups = [group["G3"].to_numpy() for _, group in df.groupby("failures")]
h_stat, p_failure = stats.kruskal(*failure_groups)
failure_summary = df.groupby("failures")["G3"].agg(["count", "mean", "median", "std"])
print(f"Kruskal-Wallis H={h_stat:.3f}, p={p_failure:.4g}")
failure_summary
'''),
        md("## 2.4. Tương quan thứ hạng: Walc và G3"),
        code(r'''
rho, p_walc = stats.spearmanr(df["Walc"], df["G3"])
print(f"Spearman rho={rho:.3f}, p={p_walc:.4g}")
'''),
        md("## 2.5. Bảng kết quả chính"),
        code(r'''
results = pd.DataFrame([
    {"phan_tich": "Mean G3", "uoc_luong": mean_g3, "ci_lower": ci_mean[0], "ci_upper": ci_mean[1], "p_value": np.nan},
    {"phan_tich": "higher: yes - no", "uoc_luong": diff, "ci_lower": ci_diff[0], "ci_upper": ci_diff[1], "p_value": p_value},
    {"phan_tich": "failures: Kruskal-Wallis", "uoc_luong": h_stat, "ci_lower": np.nan, "ci_upper": np.nan, "p_value": p_failure},
    {"phan_tich": "Walc vs G3: Spearman", "uoc_luong": rho, "ci_lower": np.nan, "ci_upper": np.nan, "p_value": p_walc},
])
results.to_csv(DATA_OUT / "course_inference_summary.csv", index=False)

fig, ax = plt.subplots(figsize=(7, 4))
sns.boxplot(data=df, x="failures", y="G3", ax=ax, color="#A0CBE8")
ax.set_title("G3 theo số lần trượt môn trước đó")
fig.tight_layout()
fig.savefig(FIGURES / "hyp_course_failures.png", dpi=150, bbox_inches="tight")
plt.show()
results
'''),
        md(r'''
## Kết luận

- Khoảng tin cậy lượng hóa độ bất định thay vì chỉ báo cáo một giá trị trung bình.
- `higher` và `failures` có khác biệt đáng chú ý trong dữ liệu quan sát.
- Tương quan `Walc` với `G3` nhỏ và không còn thuyết phục khi xét toàn bộ họ giả thuyết
  trong phân tích mở rộng.
- Ý nghĩa thống kê không đồng nghĩa với ý nghĩa thực tiễn hoặc quan hệ nhân quả.
'''),
    ],
)


write(
    "03_correlation_and_regression.ipynb",
    [
        md(r'''
# 3. Tương quan và hồi quy tuyến tính

Notebook cốt lõi cho Chương 4.6. Mục tiêu là minh họa mô hình tuyến tính, diễn giải hệ số,
độ phù hợp và kiểm tra giả định cơ bản. Cross-validation, HC3 joint tests và sensitivity
analysis chi tiết nằm trong `notebooks/04_regression.ipynb`.
'''),
        code(COMMON_SETUP + r'''
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error

df = pd.read_csv(DATA_OUT / "student_mat_clean.csv")
'''),
        md("## 3.1. Tương quan giữa các điểm số"),
        code(r'''
corr = df[["G1", "G2", "G3", "failures", "studytime", "absences"]].corr(method="spearman")
fig, ax = plt.subplots(figsize=(7, 5))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="vlag", center=0, ax=ax)
ax.set_title("Tương quan Spearman giữa các biến chính")
fig.tight_layout()
fig.savefig(FIGURES / "reg_course_correlation.png", dpi=150, bbox_inches="tight")
plt.show()
corr
'''),
        md("## 3.2. Hai mô hình hồi quy"),
        code(r'''
formula_a = "G3 ~ failures + studytime + absences + C(school) + C(sex)"
formula_b = formula_a + " + G1 + G2"
model_a = smf.ols(formula_a, data=df).fit()
model_b = smf.ols(formula_b, data=df).fit()

comparison = pd.DataFrame([
    {"model": "A: không G1/G2", "r_squared": model_a.rsquared, "adjusted_r_squared": model_a.rsquared_adj,
     "rmse_in_sample": mean_squared_error(df["G3"], model_a.fittedvalues) ** 0.5},
    {"model": "B: có G1/G2", "r_squared": model_b.rsquared, "adjusted_r_squared": model_b.rsquared_adj,
     "rmse_in_sample": mean_squared_error(df["G3"], model_b.fittedvalues) ** 0.5},
])
comparison
'''),
        md(r'''
Model A mô tả mối liên hệ với các thông tin nền và hành vi. Model B thêm `G1`, `G2`, là
điểm số rất gần thời điểm `G3`; do đó Model B phù hợp hơn cho dự báo muộn nhưng không trả
lời tốt câu hỏi can thiệp sớm.
'''),
        md("## 3.3. Hệ số và khoảng tin cậy"),
        code(r'''
def coefficient_table(model, name):
    ci = model.conf_int()
    return pd.DataFrame({
        "model": name,
        "term": model.params.index,
        "coefficient": model.params.values,
        "ci_lower": ci[0].values,
        "ci_upper": ci[1].values,
        "p_value": model.pvalues.values,
    })

coefficients = pd.concat([
    coefficient_table(model_a, "A"),
    coefficient_table(model_b, "B"),
], ignore_index=True)
coefficients.to_csv(DATA_OUT / "course_regression_summary.csv", index=False)
coefficients
'''),
        md("## 3.4. Kiểm tra residual cơ bản"),
        code(r'''
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for row, (name, model) in enumerate([("Model A", model_a), ("Model B", model_b)]):
    axes[row, 0].scatter(model.fittedvalues, model.resid, alpha=0.45, s=20)
    axes[row, 0].axhline(0, color="black", linestyle="--")
    axes[row, 0].set(title=f"{name}: residual vs fitted", xlabel="Fitted G3", ylabel="Residual")
    stats.probplot(model.resid, dist="norm", plot=axes[row, 1])
    axes[row, 1].set_title(f"{name}: Q-Q plot")
fig.tight_layout()
fig.savefig(FIGURES / "reg_course_diagnostics.png", dpi=150, bbox_inches="tight")
plt.show()
'''),
        md(r'''
## Kết luận

- `G1` và đặc biệt `G2` giải thích phần lớn biến thiên của `G3` trong mô hình tuyến tính.
- Model không có điểm quá trình có khả năng giải thích hạn chế hơn.
- Residual không hoàn toàn chuẩn và nhóm `G3=0` tạo cấu trúc khó mô tả bằng OLS.
- Hệ số là association có điều kiện trên các biến đã đưa vào mô hình, không phải tác động
  nhân quả.
'''),
    ],
)


write(
    "05_experimental_design.ipynb",
    [
        md(r'''
# 4. Quy hoạch thực nghiệm

Notebook cốt lõi cho Chương 7 và CLO3-CLO4. Dữ liệu UCI được dùng để hiệu chỉnh mức trung
bình và độ phân tán; treatment effect được xác định trước theo ý nghĩa thực tiễn, không lấy
từ chênh lệch quan sát giữa các nhóm.
'''),
        code(COMMON_SETUP + r'''
import statsmodels.formula.api as smf
from statsmodels.stats.power import TTestIndPower

df = pd.read_csv(DATA_OUT / "student_mat_clean.csv")
rng = np.random.default_rng(RANDOM_SEED)
'''),
        md(r'''
## 4.1. Kế hoạch thực nghiệm

- **Experimental unit:** một học sinh.
- **Treatment:** chương trình ôn tập có hướng dẫn trước kỳ thi cuối kỳ.
- **Control:** học theo chương trình thông thường.
- **Response:** điểm `G3`, thang 0-20.
- **Thiết kế:** phân bổ ngẫu nhiên 1:1, block theo trường.
- **Replication:** nhiều học sinh trong mỗi treatment arm.
- **Giả thuyết:** `H0: mean_treatment - mean_control = 0`.
- **Effect mục tiêu chính:** tăng 1,5 điểm G3, được chọn trước vì có ý nghĩa thực tiễn.
'''),
        md("## 4.2. Cỡ mẫu theo effect mục tiêu"),
        code(r'''
sd_g3 = df["G3"].std(ddof=1)
power_solver = TTestIndPower()
effects = [0.5, 1.0, 1.5, 2.0]
design_rows = []
for delta in effects:
    standardized = delta / sd_g3
    n_per_arm = power_solver.solve_power(
        effect_size=standardized, alpha=ALPHA, power=0.80, ratio=1, alternative="two-sided"
    )
    design_rows.append({
        "target_effect_points": delta,
        "standardized_effect_d": standardized,
        "n_per_arm": int(np.ceil(n_per_arm)),
        "total_sample_size": int(2 * np.ceil(n_per_arm)),
    })
design_table = pd.DataFrame(design_rows)
design_table.to_csv(DATA_OUT / "doe_design_scenarios.csv", index=False)
design_table
'''),
        md("## 4.3. Mô phỏng một thí nghiệm hoàn toàn ngẫu nhiên"),
        code(r'''
PRIMARY_EFFECT = 1.5
N_PER_ARM = int(design_table.loc[design_table["target_effect_points"] == PRIMARY_EFFECT, "n_per_arm"].iloc[0])
n_total = 2 * N_PER_ARM

assignment = np.repeat([0, 1], N_PER_ARM)
rng.shuffle(assignment)
baseline = rng.normal(df["G3"].mean(), sd_g3, n_total)
outcome = np.clip(baseline + PRIMARY_EFFECT * assignment, 0, 20)
trial = pd.DataFrame({"treatment": assignment, "G3": outcome})

trial_model = smf.ols("G3 ~ treatment", data=trial).fit()
estimate = trial_model.params["treatment"]
ci = trial_model.conf_int().loc["treatment"]
print(f"Ước lượng treatment effect: {estimate:.3f}")
print(f"95% CI: [{ci.iloc[0]:.3f}, {ci.iloc[1]:.3f}]")
print(f"p-value: {trial_model.pvalues['treatment']:.4g}")
'''),
        md("## 4.4. Monte Carlo: power và Type I error"),
        code(r'''
N_SIMULATIONS = 2000
sample_sizes = [50, 100, 150, 200, 300, 400]
effect_grid = [0.0, 1.0, 1.5, 2.0]
simulation_rows = []

for effect in effect_grid:
    for n_arm in sample_sizes:
        control = rng.normal(df["G3"].mean(), sd_g3, size=(N_SIMULATIONS, n_arm))
        treated = rng.normal(df["G3"].mean() + effect, sd_g3, size=(N_SIMULATIONS, n_arm))
        control = np.clip(control, 0, 20)
        treated = np.clip(treated, 0, 20)
        _, p_values = stats.ttest_ind(treated, control, axis=1, equal_var=False)
        estimates = treated.mean(axis=1) - control.mean(axis=1)
        simulation_rows.append({
            "effect_points": effect,
            "n_per_arm": n_arm,
            "rejection_rate": np.mean(p_values < ALPHA),
            "mean_estimated_effect": np.mean(estimates),
        })

simulation_results = pd.DataFrame(simulation_rows)
simulation_results.to_csv(DATA_OUT / "doe_simulation_results.csv", index=False)

fig, ax = plt.subplots(figsize=(8, 5))
for effect, group in simulation_results.groupby("effect_points"):
    ax.plot(group["n_per_arm"], group["rejection_rate"], marker="o", label=f"Effect={effect:g}")
ax.axhline(0.80, color="black", linestyle="--", label="Power 80%")
ax.axhline(0.05, color="gray", linestyle=":", label="Alpha 5%")
ax.set(xlabel="Số học sinh mỗi nhóm", ylabel="Tỷ lệ bác bỏ H0", ylim=(0, 1.02),
       title="Power mô phỏng theo cỡ mẫu và treatment effect")
ax.legend()
fig.tight_layout()
fig.savefig(FIGURES / "doe_power_curve.png", dpi=150, bbox_inches="tight")
plt.show()
simulation_results
'''),
        md(r'''
Khi effect bằng 0, rejection rate xấp xỉ Type I error. Khi effect lớn hơn 0, rejection
rate là empirical power. Sai khác nhỏ so với công thức lý thuyết xuất hiện do mô phỏng và
việc giới hạn điểm trong khoảng 0-20.
'''),
        md("## 4.5. Mở rộng factorial 2x2"),
        code(r'''
# Hai factor đều là can thiệp có thể phân bổ ngẫu nhiên.
n_cell = 80
factorial = pd.DataFrame({
    "guided_review": np.repeat([0, 0, 1, 1], n_cell),
    "study_reminders": np.repeat([0, 1, 0, 1], n_cell),
})
noise = rng.normal(0, sd_g3, len(factorial))
factorial["G3"] = np.clip(
    df["G3"].mean()
    + 1.2 * factorial["guided_review"]
    + 0.6 * factorial["study_reminders"]
    + 0.4 * factorial["guided_review"] * factorial["study_reminders"]
    + noise,
    0, 20,
)
factorial_model = smf.ols("G3 ~ guided_review * study_reminders", data=factorial).fit()
factorial_results = pd.DataFrame({
    "term": factorial_model.params.index,
    "coefficient": factorial_model.params.values,
    "p_value": factorial_model.pvalues.values,
})
factorial_results.to_csv(DATA_OUT / "doe_factorial_results.csv", index=False)
factorial.groupby(["guided_review", "study_reminders"])["G3"].agg(["count", "mean", "std"]), factorial_results
'''),
        md(r'''
## Kết luận

- Randomization giúp cân bằng các yếu tố gây nhiễu trung bình giữa treatment và control.
- Replication làm giảm sai số ước lượng; blocking theo trường có thể tăng độ chính xác.
- Với độ lệch chuẩn quan sát khoảng 4,58, effect nhỏ đòi hỏi mẫu lớn.
- Factorial 2x2 cho phép ước lượng hai main effects và interaction trong cùng một thiết kế.
- Kết quả mô phỏng minh họa cách thiết kế; nó không chứng minh chương trình giả định thực
  sự làm tăng `G3`.
'''),
    ],
)


print(f"Built core notebooks in {OUT}")
