# Phân tích các yếu tố ảnh hưởng đến kết quả học tập của học sinh

> Môn: Thống kê ứng dụng &nbsp;|&nbsp; Dataset: Student Performance (UCI) &nbsp;|&nbsp; Tháng 6/2026

---

## 1. Tổng quan project

### Mục tiêu

Project áp dụng toàn diện các phương pháp thống kê để phân tích bộ dữ liệu **Student Performance** (UCI), tập trung vào môn Toán (`student-mat.csv`, n=395). Mục tiêu là xác định các yếu tố hành vi, gia đình và xã hội có ảnh hưởng có ý nghĩa thống kê đến điểm cuối kỳ G3.

### Research questions

1. Các yếu tố nhân khẩu học cá nhân (giới tính, khu vực) và bối cảnh gia đình (trình độ học vấn bố/mẹ, cấu trúc gia đình) có tạo ra sự khác biệt điểm số có ý nghĩa thống kê không?
2. Hành vi học tập (thời gian học, số lần trượt môn trước đó) và hành vi xã hội (tiêu thụ rượu) tương quan thế nào với G3?
3. Mô hình hồi quy tuyến tính bội có thể dự đoán G3 với độ chính xác chấp nhận được từ các biến hành vi/xã hội (không bao gồm G1, G2) không?

### Dataset

| Thuộc tính | Chi tiết |
|---|---|
| File làm việc | `student-mat.csv` |
| Số quan sát | 395 học sinh |
| Số biến | 33 biến |
| Biến mục tiêu | `G3` — điểm cuối kỳ, thang 0–20 |
| Nguồn | [UCI ML Repository](https://archive.ics.uci.edu/dataset/320/student+performance) |

> **Lưu ý về sample size:** n=395 là tương đối nhỏ. Project này chủ động xử lý hạn chế này bằng bootstrap CI (Phase 3), báo cáo effect size song song p-value (Phase 2), và k-fold cross-validation (Phase 4).

---

## 2. Setup & cài đặt

### Yêu cầu

- Python 3.10+
- pip

### Cài đặt

```bash
# 1. Clone repo
git clone <repo-url>
cd student-performance-project

# 2. Cài dependencies
pip install -r requirements.txt

# 3. Kiểm tra dataset có đúng chỗ chưa
ls data/raw/
# → student-mat.csv
```

### Dependencies chính

```
pandas>=2.0
numpy>=1.24
scipy>=1.11
statsmodels>=0.14
scikit-learn>=1.3
matplotlib>=3.7
seaborn>=0.12
jupyter>=1.0
pingouin>=0.5        # effect size, power analysis
```

---

## 3. Cấu trúc project

```
student-performance-project/
│
├── data/
│   ├── raw/
│   │   └── student-mat.csv        # ← KHÔNG chỉnh sửa file này
│   └── processed/
│       └── student_mat_clean.csv  # output của 01_EDA.ipynb
│
├── notebooks/
│   ├── 01_EDA.ipynb               # Phase 1: khám phá dữ liệu
│   ├── 02_hypothesis_testing.ipynb # Phase 2: kiểm định giả thuyết
│   ├── 03_confidence_intervals.ipynb # Phase 3: CI + bootstrap + power
│   ├── 04_regression.ipynb        # Phase 4: mô hình hồi quy
│   └── 05_doe_simulation.ipynb    # Phase 5: A/B test simulation
│
├── report/
│   ├── figures/                   # tất cả chart export từ notebooks
│   └── report.pdf                 # báo cáo cuối (nộp)
│
├── utils/
│   └── helpers.py                 # hàm dùng chung giữa các notebooks
│
├── requirements.txt
└── README.md
```

**Quy tắc quan trọng:** `data/raw/` là read-only. Mọi thay đổi dữ liệu đều thực hiện trong notebook và lưu vào `data/processed/`.

---

## 4. Analysis pipeline

Chạy các notebook **theo đúng thứ tự**. Mỗi notebook phụ thuộc vào output của notebook trước.

```
01_EDA  ──────────────────►  data/processed/student_mat_clean.csv
                                          │
                              ┌───────────┴───────────┐
                              ▼                       ▼
                      02_hypothesis         03_confidence_intervals
                      03_confidence  ──►   bootstrap_ci_results.csv
                              │
                              ▼
                        04_regression  ──►  model_coefficients.csv
                              │
                              ▼
                        05_doe_simulation
```

### Chi tiết từng notebook

| Notebook | Input | Output chính | Phase |
|---|---|---|---|
| `01_EDA.ipynb` | `data/raw/student-mat.csv` | `data/processed/student_mat_clean.csv`, `report/figures/eda_*.png` | Phase 1 |
| `02_hypothesis_testing.ipynb` | `student_mat_clean.csv` | `report/figures/hyp_*.png`, in-notebook summary table | Phase 2 |
| `03_confidence_intervals.ipynb` | `student_mat_clean.csv` | `bootstrap_ci_results.csv`, power analysis summary | Phase 3 |
| `04_regression.ipynb` | `student_mat_clean.csv` | `model_coefficients.csv`, `report/figures/reg_*.png` | Phase 4 |
| `05_doe_simulation.ipynb` | distribution params từ Phase 1 | `report/figures/doe_*.png`, simulation summary | Phase 5 |

---

## 5. Phân công & deadline

| Thành viên | Phase phụ trách | Notebook | Deadline |
|---|---|---|---|
| **[Nguyễn Danh Bảo]** | Phase 1 — EDA | `01_EDA.ipynb` | 1/6 |
| **[Tên A]** | Phase 6 — Measurement theory | section trong báo cáo | 12/6 |
| **[Tên B]** | Phase 2 — Hypothesis testing | `02_hypothesis_testing.ipynb` | 5/6 |
| **[Tên B]** | Phase 3 — CI + Bootstrap + Power | `03_confidence_intervals.ipynb` | 5/6 |
| **[Tên C]** | Phase 4 — Regression | `04_regression.ipynb` | 5/6 |
| **[Tên C]** | Phase 5 — DoE simulation | `05_doe_simulation.ipynb` | 5/6 |
| **Cả nhóm** | Tổng hợp báo cáo | `report/report.pdf` | 15/6 |
| **Cả nhóm** | Review & nộp | — | 15/6 |

> Cập nhật tên thành viên thực tế vào bảng trên.

---

## 6. Conventions

### Đặt tên file & biến

```python
# Biến hằng số thống kê — luôn khai báo ở đầu notebook
ALPHA = 0.05
N_BOOTSTRAP = 5000
RANDOM_SEED = 42

# Tên DataFrame
df_raw    # dữ liệu gốc, không chỉnh
df_clean  # sau khi xử lý missing/outlier
```

### Export figure

```python
# Mọi figure đều lưu vào report/figures/ với prefix tương ứng
# 01_EDA → eda_*, 02_hyp → hyp_*, ...
fig.savefig("../report/figures/eda_g3_distribution.png", dpi=150, bbox_inches="tight")
```

### Commit message

```
[phase1] add G3 distribution histogram
[phase2] add t-test urban vs rural
[fix]    correct normality test for failures variable
[report] add regression interpretation section
```

### Checklist trước khi push

- [ ] Notebook đã chạy từ đầu đến cuối không có lỗi (`Restart & Run All`)
- [ ] Tất cả figure đã export vào `report/figures/`
- [ ] Không có đường dẫn tuyệt đối (`C:/Users/...`) trong code
- [ ] Đã update Progress tracking bên dưới

---

## 7. Tóm tắt các giả thuyết (Phase 2)

**Nhóm A — Nhân khẩu học cá nhân**

| # | Giả thuyết | Test | Biến |
|---|---|---|---|
| H1 | Nam và nữ có điểm G3 khác nhau | Independent t-test (hoặc Mann-Whitney U) | `sex` × `G3` |
| H2 | Học sinh urban có điểm cao hơn rural | Independent t-test | `address` × `G3` |

**Nhóm B — Bối cảnh gia đình**

| # | Giả thuyết | Test | Biến |
|---|---|---|---|
| H3 | Học sinh có `famsup=yes` điểm cao hơn | Independent t-test | `famsup` × `G3` |
| H8 | Trình độ học vấn bố/mẹ (`Medu`, `Fedu`) ảnh hưởng đến G3 | One-way ANOVA (hoặc Kruskal-Wallis) | `Medu`, `Fedu` × `G3` |

**Nhóm C — Hành vi học tập & xã hội**

| # | Giả thuyết | Test | Biến |
|---|---|---|---|
| H4 | `studytime` ảnh hưởng đến G3 | One-way ANOVA (hoặc Kruskal-Wallis) | `studytime` × `G3` |
| H5 | `Walc` (rượu cuối tuần) tương quan âm với G3 | Spearman correlation | `Walc` ↔ `G3` |
| H6 | Học sinh muốn học đại học (`higher=yes`) điểm cao hơn | Independent t-test | `higher` × `G3` |
| H7 | `failures` ảnh hưởng mạnh đến G3 | ANOVA + regression | `failures` × `G3` |
| H9 ⚠️ | Học sinh vắng mặt nhiều (`absences` cao) có G3 thấp hơn | Spearman correlation | `absences` ↔ `G3` |

> ⚠️ **H9 là post-hoc hypothesis** — phát hiện từ EDA Phase 1 (Spearman r=-0.243, mạnh thứ 2 sau `failures`).
> Không được đặt ra trước khi nhìn data. Cần ghi rõ điều này khi trình bày kết quả trong báo cáo
> để tránh bị xem là p-hacking.

> Với mọi kiểm định: (1) kiểm tra normality bằng Shapiro-Wilk trước, (2) nếu vi phạm thì dùng non-parametric fallback, (3) luôn báo cáo effect size (Cohen's d / η² / r) kèm p-value.

---

## 8. Progress tracking

### Phase 1 — EDA
- [ ] Mô tả dataset (shape, dtypes, value counts)
- [ ] Thống kê mô tả cho biến numeric
- [ ] Phân phối G3 (histogram + boxplot)
- [ ] Missing value & outlier analysis
- [ ] Visualizations: barplot theo nhóm, correlation heatmap (Pearson + Cramér's V)
- [ ] Export `student_mat_clean.csv`

### Phase 2 — Hypothesis testing
- [ ] Kiểm tra normality (Shapiro-Wilk) cho từng nhóm
- [ ] H1: t-test sex × G3
- [ ] H2: t-test address × G3
- [ ] H3: t-test famsup × G3
- [ ] H4: ANOVA studytime × G3
- [ ] H5: Spearman Walc ↔ G3
- [ ] H6: t-test higher × G3
- [ ] H7: ANOVA failures × G3
- [ ] Effect size cho tất cả tests

### Phase 3 — Confidence intervals
- [ ] Parametric CI cho mean G3 (95%)
- [ ] Bootstrap CI (n_bootstrap=5000) cho mean G3
- [ ] CI cho sự khác biệt nam/nữ, urban/rural
- [ ] Power analysis: với n=395, đạt power bao nhiêu ở effect size trung bình?

### Phase 4 — Regression
- [ ] Model A: tất cả biến hành vi/xã hội (không có G1, G2)
- [ ] Model B: bao gồm G1, G2 (so sánh predictive power)
- [ ] VIF check (multicollinearity)
- [ ] Residual diagnostics (normality, homoscedasticity)
- [ ] K-fold cross-validation (k=5)
- [ ] So sánh Adjusted R², AIC

### Phase 5 — DoE simulation
- [ ] Đề xuất thiết kế A/B test (treatment: chương trình hỗ trợ học tập)
- [ ] Simulate dataset dựa trên distribution thực
- [ ] Tính required sample size
- [ ] Chạy full pipeline kiểm định
- [ ] Factorial design 2×2 (studytime × famsup)

### Phase 6 — Measurement theory & sai số
- [ ] Thảo luận độ tin cậy các biến thang đo (famrel, health, Walc...)
- [ ] Phân loại sai số: sampling error, measurement error, selection bias
- [ ] Giới hạn của nghiên cứu

### Báo cáo cuối
- [ ] Tổng hợp tất cả kết quả vào report
- [ ] Review chéo (mỗi người đọc phần của người khác)
- [ ] Nộp