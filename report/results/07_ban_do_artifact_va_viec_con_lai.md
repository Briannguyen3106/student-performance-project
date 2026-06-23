# PHẦN VII — BẢN ĐỒ ARTIFACT VÀ VIỆC CÒN LẠI

> **Học phần:** IT2022E — Thống kê ứng dụng và Quy hoạch thực nghiệm.
> **Kế thừa:** [`01`](01_tong_quan_va_pipeline.md) → [`06`](06_sai_so_han_che_va_ket_luan.md);
> khung [`report/OUTLINE.md`](../OUTLINE.md) Phần VII.
>
> File tra cứu: ánh xạ **notebook ↔ hình ↔ bảng CSV ↔ file báo cáo**, để bất kỳ con số/hình
> nào trong báo cáo cũng truy ngược được về artifact và notebook sinh ra nó. Cuối file là
> **việc còn lại** và các **điểm cần xử lý (discrepancy)** trước khi nộp.

---

## 1. Bản đồ notebook → file báo cáo

| Notebook | Luồng | Vai trò | File báo cáo |
|---|---|---|---|
| `core/01_data_preparation_and_eda.ipynb` | Core | Chuẩn bị + EDA (Chương 1,6) | [01](01_tong_quan_va_pipeline.md), [02](02_du_lieu_va_ly_thuyet_do_luong.md) |
| `core/02_statistical_inference.ipynb` | Core | CI + kiểm định (Chương 4.1–4.5) | [03](03_suy_luan_thong_ke.md) |
| `core/03_correlation_and_regression.ipynb` | Core | Tương quan + hồi quy (Chương 4.6) | [04](04_tuong_quan_va_hoi_quy.md) |
| `core/05_experimental_design.ipynb` | Core | Quy hoạch thực nghiệm (Chương 7) | [05](05_quy_hoach_thuc_nghiem.md) |
| `01_EDA.ipynb` | Appendix | EDA đầy đủ, Cramér's V, sensitivity | [02](02_du_lieu_va_ly_thuyet_do_luong.md) |
| `02_hypothesis_testing.ipynb` | Appendix | 10 kiểm định, Holm, Dunn | [03](03_suy_luan_thong_ke.md) |
| `03_confidence_intervals.ipynb` | Appendix | Bootstrap BCa, MDE/power | [03](03_suy_luan_thong_ke.md) |
| `04_regression.ipynb` | Appendix | 5-fold CV, HC3, sensitivity | [04 — Phụ lục IV-A](04_tuong_quan_va_hoi_quy.md) |

---

## 2. Bản đồ hình (`report/figures/`, 32 hình)

### 2.1. EDA — 8 hình
| Hình | Notebook | Dùng ở |
|---|---|---|
| [eda_course_overview](../figures/eda_course_overview.png) | core/01 | 01 §4.2 · 02 §3 (Hình 1) |
| [eda_g3_distribution](../figures/eda_g3_distribution.png) | appendix/01 | 01 §4.4 · 02 §3 (Hình 2) |
| [eda_outliers_boxplot](../figures/eda_outliers_boxplot.png) | appendix/01 | 01 §4.4 · 02 §4 (Hình 3) |
| [eda_correlation_heatmap_spearman](../figures/eda_correlation_heatmap_spearman.png) | appendix/01 | 02 §5.1 (Hình 4) |
| [eda_cramers_v_heatmap](../figures/eda_cramers_v_heatmap.png) | appendix/01 | 02 §5.2 (Hình 5) |
| [eda_g3_by_group](../figures/eda_g3_by_group.png) | appendix/01 | 02 §5.3 (Hình 6) |
| [eda_g3_by_nominal](../figures/eda_g3_by_nominal.png) | appendix/01 | 02 §5.3 (Hình 7) |
| [eda_scatter_g3](../figures/eda_scatter_g3.png) | appendix/01 | 02 §5.4 (Hình 8) |

### 2.2. Kiểm định giả thuyết — 11 hình
| Hình | Notebook | Dùng ở |
|---|---|---|
| [hyp_course_failures](../figures/hyp_course_failures.png) | core/02 | 03 §4.4 (Hình 4) |
| [hyp_h1_sex_g3](../figures/hyp_h1_sex_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h2_address_g3](../figures/hyp_h2_address_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h3_famsup_g3](../figures/hyp_h3_famsup_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h4_studytime_g3](../figures/hyp_h4_studytime_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h5_walc_g3](../figures/hyp_h5_walc_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h6_higher_g3](../figures/hyp_h6_higher_g3.png) | appendix/02 | 03 §4.4 (Hình 3) |
| [hyp_h7_failures_g3](../figures/hyp_h7_failures_g3.png) | appendix/02 | 03 §4.3 (bảng) |
| [hyp_h8a_medu_g3](../figures/hyp_h8a_medu_g3.png) | appendix/02 | 03 §4.4 (Hình 5) |
| [hyp_h8b_fedu_g3](../figures/hyp_h8b_fedu_g3.png) | appendix/02 | 03 §4.4 (Hình 6) |
| [hyp_h9_absences_g3](../figures/hyp_h9_absences_g3.png) | appendix/02 | 03 §4.3 (bảng) |

### 2.3. Khoảng tin cậy — 3 hình
| Hình | Notebook | Dùng ở |
|---|---|---|
| [ci_bootstrap_mean_g3](../figures/ci_bootstrap_mean_g3.png) | appendix/03 | 03 §2 (Hình 1) |
| [ci_group_differences](../figures/ci_group_differences.png) | appendix/03 | 03 §3 (Hình 2) · 06 §1.1 (Hình 1) |
| [ci_power_curve](../figures/ci_power_curve.png) | appendix/03 | 03 §6 (Hình 7) |

### 2.4. Hồi quy — 6 hình
| Hình | Notebook | Dùng ở |
|---|---|---|
| [reg_course_correlation](../figures/reg_course_correlation.png) | core/03 | 04 §1 (Hình 1) |
| [reg_course_diagnostics](../figures/reg_course_diagnostics.png) | core/03 | 04 §5 (Hình 2) |
| [reg_cv_model_comparison](../figures/reg_cv_model_comparison.png) | appendix/04 | 04 Phụ lục (Hình A1) |
| [reg_observed_vs_predicted](../figures/reg_observed_vs_predicted.png) | appendix/04 | 04 (A2) · 06 §1.2 (Hình 2) |
| [reg_residual_diagnostics](../figures/reg_residual_diagnostics.png) | appendix/04 | 04 (A3) · 06 §1.5 (Hình 3) |
| [reg_influence](../figures/reg_influence.png) | appendix/04 | 04 Phụ lục (Hình A4) |

### 2.5. Quy hoạch thực nghiệm — 4 hình
| Hình | Notebook | Dùng ở | Ghi chú |
|---|---|---|---|
| [doe_sample_size_curve](../figures/doe_sample_size_curve.png) | core/05 | 05 §2 (Hình 1) | **Mới sinh** |
| [doe_single_trial](../figures/doe_single_trial.png) | core/05 | 05 §3 (Hình 2) | **Mới sinh** |
| [doe_power_curve](../figures/doe_power_curve.png) | core/05 | 05 §4 (Hình 3) | |
| [doe_factorial_interaction](../figures/doe_factorial_interaction.png) | core/05 | 05 §5 (Hình 4) | **Mới sinh** |

> Tổng: **32 hình** = 8 `eda_` + 11 `hyp_` + 3 `ci_` + 6 `reg_` + 4 `doe_` (3 hình DoE mới
> được bổ sung và sinh trực tiếp từ `core/05`).

---

## 3. Bản đồ bảng CSV (`data/processed/`, 17 file)

| CSV | Notebook | Nội dung |
|---|---|---|
| `student_mat_clean.csv` | core/01 | Dữ liệu phân tích (395×33, giữ nguyên trạng) |
| `course_inference_summary.csv` | core/02 | Tóm tắt CI + kiểm định mạch chính |
| `course_regression_summary.csv` | core/03 | Hệ số Model A/B (core) |
| `hypothesis_test_results.csv` | appendix/02 | 10 kiểm định chính + Holm |
| `hypothesis_posthoc_results.csv` | appendix/02 | 32 so sánh cặp Dunn |
| `bootstrap_ci_results.csv` | appendix/03 | 16 ước lượng/CI bootstrap |
| `power_sensitivity_results.csv` | appendix/03 | MDE 4 contrast |
| `regression_cv_results.csv` | appendix/04 | Fold + aggregate OOF |
| `regression_coefficients.csv` | appendix/04 | Hệ số + HC3 |
| `regression_joint_tests.csv` | appendix/04 | Joint Wald + Holm |
| `regression_diagnostics.csv` | appendix/04 | VIF, BP, Cook's D |
| `regression_oof_predictions.csv` | appendix/04 | Dự báo out-of-fold |
| `regression_paired_fold_differences.csv` | appendix/04 | Chênh lệch B−A theo fold |
| `regression_sensitivity_results.csv` | appendix/04 | Các sensitivity analysis |
| `doe_design_scenarios.csv` | core/05 | Cỡ mẫu theo effect |
| `doe_simulation_results.csv` | core/05 | Monte Carlo power/Type I |
| `doe_factorial_results.csv` | core/05 | Hệ số factorial 2×2 |

---

## 4. Việc còn lại trước khi nộp

- [ ] **Điền thông tin trang đầu** (`report/results/report_draft.md`): tên giảng viên, nhóm,
  thành viên + MSSV.
- [ ] **Review chéo số liệu** (ROADMAP P3): đối chiếu mọi con số/caption/bảng trong 6 file chi
  tiết với CSV trong `data/processed/` và output notebook.
- [ ] **Sinh `report/report.pdf`** từ source Markdown; kiểm tra ngắt trang, đánh số hình/bảng,
  font, định dạng trích dẫn theo yêu cầu giảng viên.
- [ ] **Thống nhất ghép bộ**: quyết định ghép 6 file `01–06` thành một báo cáo liền mạch hay
  giữ tách; nếu ghép, đánh số hình/mục lại toàn cục.

---

## 5. Điểm cần xử lý đã phát hiện (discrepancy)

| Vấn đề | Vị trí | Ảnh hưởng | Đề xuất |
|---|---|---|---|
| **Đường dẫn máy cá nhân** in trong output (`C:\Users\LENOVO\...`) | output `notebooks/01_EDA`, `02_hypothesis_testing`, `03_confidence_intervals` | Mâu thuẫn "Definition of done" (không đường dẫn tuyệt đối) | Restart/Run All trên máy hiện tại để output sạch, hoặc clear output trước khi nộp |
| `matplotlib.use("Agg")` **bị comment** | NB `02`, `03` (appendix) | Không lỗi, nhưng không nhất quán với các notebook khác | Bật lại `matplotlib.use("Agg")` cho đồng bộ |
| **Hệ số G1/G2 khác nhau** giữa core/03 (0,146/0,977) và appendix/04 (HC3 0,189/0,957) | file 04 | Dễ hiểu nhầm là sai số | Đã ghi chú rõ là **hai đặc tả khác nhau** trong file 04 |

> Hai mục đầu là **nợ kỹ thuật của luồng appendix**; luồng core (01,02,03,05) và 6 file báo
> cáo đã sạch đường dẫn và chạy không lỗi. Mục thứ ba đã được chú thích, không phải lỗi.

---

> **Hình liên quan:** file này liên kết **toàn bộ 32 hình** trong `report/figures/` (mục 2) —
> mỗi tên hình là một đường dẫn click được tới file PNG tương ứng.
>
> **Kết thúc bộ tài liệu chi tiết** (file 01–07). Khung tổng thể: [`report/OUTLINE.md`](../OUTLINE.md);
> bản thảo báo cáo gốc: [`report_draft.md`](report_draft.md).
