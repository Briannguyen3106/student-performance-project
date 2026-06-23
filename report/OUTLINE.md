Giúp tôi tạo ra 1 file .md bằng tiếng việt có nội dung là tổng quan và pipeline tổng thể của project này. File này sẽ là tiền đề để tôi yêu cầu bạn tạo ra những file nội dung chi tiết, phục vụ # DÀN Ý BÁO CÁO — Phân tích thống kê kết quả học tập & Quy hoạch thực nghiệm

> Học phần IT2022E. Dàn ý có tính phân tích, bám sát `report/results/report_draft.md` và 8
> notebook (4 core trình bày + 4 appendix kỹ thuật). Mỗi thí nghiệm/kiểm định được trình bày
> theo khuôn: **Setup → (H0/H1 + giả định + quy tắc) → Phân tích toán học → Phân tích kết quả**.
> Với các *thí nghiệm* (§4.5, §5) bổ sung **Lý do thực hiện** và **Quy trình thực hiện**.

---

## Phần I — Tổng quan project

**Mục tiêu (4):**
1. Mô tả bộ dữ liệu và phân phối điểm cuối kỳ `G3`.
2. Đánh giá mối liên hệ (association) giữa `G3` với đặc điểm cá nhân, gia đình, hành vi.
3. So sánh khả năng giải thích/dự báo `G3` của mô hình **không** và **có** điểm quá trình `G1,G2`.
4. Đề xuất một quy hoạch thực nghiệm để đánh giá chương trình hỗ trợ học tập.

**4 câu hỏi nghiên cứu:** (1) phân phối `G3` và đặc điểm mẫu; (2) `G3` có liên hệ với `higher`,
`failures`, `studytime`, `Walc`, trình độ học vấn cha mẹ…?; (3) biến nền/hành vi có đủ dự báo
sớm `G3` không, thêm `G1/G2` đổi gì?; (4) thiết kế thí nghiệm đánh giá chương trình hỗ trợ ra sao?

**Dataset:** `data/raw/student-mat.csv` (`;`-separated), **n=395**, 33 biến, 2 trường
(GP=349, MS=46), nữ=208/nam=187. Biến kết quả `G3` thang **0–20**. Không missing, không
duplicate. `G3=0` chiếm **9,62%** (38 quan sát).

**3 nguyên tắc xuyên suốt:**
- **Association ≠ Causation** — dữ liệu quan sát, không kết luận nhân quả.
- **Ý nghĩa thống kê ≠ ý nghĩa thực tiễn** — luôn báo cáo effect size + khoảng tin cậy (CI).
- **Đa kiểm định phải hiệu chỉnh** — kết luận theo **Holm** / joint test, p thô chỉ tham khảo.

**Hằng số:** `RANDOM_SEED = 42`, `ALPHA = 0.05`, bootstrap **5.000** lần lặp.

---

## Phần II — Pipeline phân tích

```
data/raw/student-mat.csv  (;-sep, 395×33, READ-ONLY)
      │  NB 01: đọc, kiểm tra chất lượng, xuất NGUYÊN TRẠNG (giữ G3=0, giữ absences)
      ▼
data/processed/student_mat_clean.csv  (395×33)
      │  NB 02/03/05 (core) + NB 01–04 (appendix) cùng nạp file này
      ▼
data/processed/*.csv  (bảng kết quả)   +   report/figures/*.png  (29 hình)
      ▼
report/results/report_draft.md  (báo cáo 9 phần)
```

> **Lưu ý mấu chốt:** hậu tố `_clean` chỉ là **chuẩn hóa định dạng** (đổi separator), KHÔNG
> biến đổi dữ liệu — giữ `G3=0`, không winsorize `absences` (quyết định D-002/D-003/D-004).

**Hai luồng notebook:**

| Luồng | File | Vai trò |
|---|---|---|
| **Core** (trình bày, gọn) | `notebooks/core/01,02,03,05` | Bám đề cương Chương 1/4/6/7 |
| **Appendix** (kỹ thuật, đầy đủ) | `notebooks/01,02,03,04` | Holm, Dunn, BCa, 5-fold CV, HC3, sensitivity |

---

## Phần III — Khuôn phân tích dùng chung

Mỗi mục ở Phần IV–V bám 4 khối:

1. **Setup** — đối tượng so sánh; biến + loại thang đo; nhóm/cỡ mẫu; thiết kế.
2. **Giả thuyết & quy tắc** — H0 / H1 (hai phía); **giả định** của phương pháp + cách kiểm
   tra/xử lý; **quy tắc quyết định** (bác bỏ H0 nếu `p_holm < 0,05`).
3. **Phân tích toán học** — **lý do chọn kiểm định** (gắn giả định + loại dữ liệu); **công
   thức đầy đủ** của thống kê, bậc tự do, effect size; diễn giải ngắn từng thành phần.
4. **Phân tích kết quả** — giá trị thống kê, `p_raw`/`p_holm`, effect size, CI; kết luận +
   cảnh báo association/thực tiễn.

Với các mục là **thí nghiệm** (so sánh mô hình §4.5, mô phỏng DoE §5), thêm 2 khối đứng trước:
- **Lý do thực hiện thí nghiệm** — câu hỏi nó trả lời, vì sao cần làm, vì sao không dừng ở
  phân tích trước.
- **Quy trình thực hiện (các bước)** — liệt kê tuần tự từng bước chạy thí nghiệm.

---

## Phần IV — Dàn ý chi tiết từng mục báo cáo

### Tóm tắt & §1 Giới thiệu
- Kết quả nổi bật: mean `G3`=10,415; sau Holm còn `higher`/`failures`/`Medu`/`Fedu`; OOF R²
  0,087→0,806; DoE cần ~296 học sinh để phát hiện +1,5 điểm.
- §1.1 bối cảnh · §1.2 mục tiêu · §1.3 câu hỏi · §1.4 phạm vi (chỉ môn Toán, không ghép
  Portuguese vì học sinh trùng lặp).
- *Nguồn:* `README.md`, `.docs/ANALYSIS_RESULTS.md`.

### §2 Dữ liệu & lý thuyết đo lường
- §2.1 nguồn dữ liệu (UCI, n=395, 2 trường).
- §2.2 phân loại **4 loại biến**: định danh (`school`, `sex`…), thứ bậc (`studytime`, `Walc`…),
  đếm (`age`, `absences`), điểm số (`G1`, `G2`, `G3`). Lưu ý `studytime=4` ≠ gấp đôi `=2`.
- §2.3 reliability/validity: self-report bias (recall, social desirability); single-item →
  không tính được Cronbach's alpha.
- §2.4 quyết định dữ liệu: giữ `G3=0`; không winsorize `absences`; `G3>0`/winsorize chỉ là
  sensitivity.
- **Hình 1** `report/figures/eda_course_overview.png` (phân phối + boxplot theo trường).
- *Nguồn:* `notebooks/core/01_data_preparation_and_eda.ipynb` + `notebooks/01_EDA.ipynb`
  (Cramér's V bias-corrected, sensitivity `G3=0` vs `>0`, winsorize@95%).

### §3 Phương pháp
- Tóm lược: thống kê mô tả; CI (t/Welch/bootstrap); kiểm định (Welch t / Kruskal–Wallis /
  Spearman + Holm + Dunn); hồi quy Model A vs B; DoE. Chi tiết toán đặt ở §4–§5.
- §3.6 phần mềm: pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib, seaborn.
- *Nguồn:* cả 8 notebook.

### §4.1 Thống kê mô tả `G3`
- mean 10,415 · median 11 · SD 4,581 · Q1=8 / Q3=14 · min 0 / max 20 · skew −0,73.
- Phân phối có **point mass tại 0** → không gần chuẩn. 312 học sinh `failures=0`;
  `higher=yes`=375 / `no`=20 (rất mất cân bằng).
- *Nguồn:* `notebooks/core/01` + `notebooks/01_EDA.ipynb`.

### §4.2 Khoảng tin cậy cho trung bình `G3` — *thí nghiệm so sánh phương pháp CI*
- **Setup:** ước lượng μ(`G3`) trên n=395; so 3 phương pháp: t, bootstrap percentile, BCa.
- **Giả thuyết & quy tắc:** đây là **ước lượng khoảng** (không kiểm định H0); mức tin cậy 95%.
- **Phân tích toán học:**
  - t-CI: `x̄ ± t(0,975; n−1) · s/√n`.
  - Bootstrap percentile: phân vị 2,5% và 97,5% của B=5.000 trung bình mẫu lặp lại.
  - **BCa:** hiệu chỉnh bias `z0 = Φ⁻¹(tỷ lệ boot < điểm ước lượng)` và gia tốc `a` (từ
    jackknife) → điều chỉnh hai đầu phân vị. *Lý do dùng cả 3:* kiểm tra độ bền vững khi
    phân phối lệch và có point-mass tại 0.
- **Phân tích kết quả:** t [9,962; 10,868]; percentile ≈ [9,975; 10,858]; BCa ≈ [9,965;
  10,848] → ba phương pháp **tương đồng** ⇒ ước lượng trung bình ổn định.
- **Hình 2** `report/figures/ci_bootstrap_mean_g3.png`.
- *Nguồn:* `notebooks/core/02_statistical_inference.ipynb` + `notebooks/03_confidence_intervals.ipynb`.

### §4.3 Kiểm định giả thuyết (H1–H9) — *nhóm thí nghiệm so sánh chính*

**Phân tích toán học dùng chung (công thức đầy đủ + diễn giải ngắn):**
- **Welch t-test:** `t = (x̄₁ − x̄₂) / √(s₁²/n₁ + s₂²/n₂)`; bậc tự do Welch–Satterthwaite
  `df = (s₁²/n₁ + s₂²/n₂)² / [ (s₁²/n₁)²/(n₁−1) + (s₂²/n₂)²/(n₂−1) ]`.
- **Kruskal–Wallis:** `H = 12/[N(N+1)] · Σ Rᵢ²/nᵢ − 3(N+1)` (Rᵢ = tổng hạng nhóm i); effect
  size `ε² = (H − k + 1)/(N − k)`.
- **Spearman:** `ρ_s` = hệ số Pearson tính trên hạng; kiểm định qua xấp xỉ phân phối t.
- **Dunn post-hoc:** `z` chuẩn hóa chênh lệch hạng trung bình giữa 2 nhóm, **có hiệu chỉnh ties**.
- **Effect size 2 nhóm — Hedges g:** `g = d · (1 − 3/[4(n₁+n₂) − 9])`, với `d` = chênh lệch
  trung bình / SD gộp (pooled).
- **Holm (step-down):** sắp p tăng dần, so ngưỡng `α/(m − i + 1)`; kiểm soát FWER cho m=10 test.

**Lý do chọn kiểm định:**
- **Welch t** cho 2 nhóm: không giả định đồng phương sai, chịu được n không cân bằng (chọn
  thay **Student t**); chọn t thay **Mann–Whitney** vì cần ước lượng **chênh lệch trung bình**
  và n đủ lớn (CLT).
- **Kruskal–Wallis** cho biến thứ bậc nhiều mức: `G3` lệch, bị chặn [0,20], có point-mass →
  không thỏa giả định **ANOVA** chuẩn; KW là omnibus theo hạng.
- **Spearman** cho liên hệ đơn điệu theo hạng: biến ordinal, bền với phi tuyến/outlier (thay **Pearson**).
- **Holm** thay **Bonferroni**: mạnh hơn (uniformly more powerful) mà vẫn kiểm soát FWER.
- **Hedges g** thay **Cohen d**: hiệu chỉnh chệch mẫu nhỏ — quan trọng vì `higher=no` chỉ n=20.

**H0/H1 + áp khuôn cho từng test:**

| Giả thuyết | Kiểm định | H0 | Ghi chú |
|---|---|---|---|
| H1 `sex`, H2 `address`, H3 `famsup`, H6 `higher` | Welch t | `μ₁ = μ₂` | hai phía |
| H4 `studytime`, H7 `failures`, H8a `Medu`, H8b `Fedu` | Kruskal–Wallis (+Dunn) | phân phối `G3` đồng nhất giữa các mức | omnibus rồi post-hoc |
| H5 `Walc`, H9 `absences` | Spearman | `ρ_s = 0` | **H9 = post-hoc/exploratory** |

- **Giả định & xử lý:** Levene/Shapiro chỉ là **diagnostic**, không dùng làm pre-test tự đổi
  phương pháp. Giả định độc lập quan sát là **giới hạn** (học sinh nằm trong 2 trường).
- **Quy tắc quyết định:** bác bỏ H0 khi `p_holm < 0,05`.

**Phân tích kết quả (sau Holm, m=10):**

| Giả thuyết | Kết quả | Effect | `p_holm` | Kết luận |
|---|---|---|---|---|
| H6 `higher` | yes−no = 3,808 (CI Welch [1,509; 6,107]) | g=0,843 | 0,0195 | **Có ý nghĩa** (cảnh báo n_no=20) |
| H7 `failures` | omnibus | ε²=0,128 | 1,7e-10 | **Có ý nghĩa** (Dunn: 0 khác 1/2/3) |
| H8a `Medu` | omnibus | ε²=0,052 | 0,00069 | **Có ý nghĩa** |
| H8b `Fedu` | omnibus | ε²=0,027 | 0,038 | **Có ý nghĩa** |
| H1–H5, H9 | sex/address/famsup/studytime/Walc/absences | nhỏ | >0,05 | Rớt sau Holm (H9 rho=0,018, exploratory) |

- **Hình 3** `report/figures/hyp_course_failures.png`.
- *Nguồn:* `notebooks/core/02` + `notebooks/02_hypothesis_testing.ipynb`.

### §4.4 Tương quan
- Spearman với `G3`: **G2=0,957**, **G1=0,878**, `failures`=−0,361, `studytime`=0,105,
  `absences`≈0. G2↔G3 rất cao là hợp lý (đo gần nhau) nhưng chỉ dùng được ở thời điểm muộn.
- **Hình 4** `report/figures/reg_course_correlation.png`.
- *Nguồn:* `notebooks/core/03` + `notebooks/01_EDA.ipynb`.

### §4.5 Hồi quy — so sánh Model A vs Model B — *thí nghiệm so sánh mô hình*

- **Lý do thực hiện thí nghiệm:** trả lời câu hỏi #3 — biến nền/hành vi có đủ **dự báo sớm**
  `G3` không, và thêm `G1/G2` đổi hiệu năng ra sao? Cần *thí nghiệm so sánh* vì:
  (i) R² in-sample bị thổi phồng, không nói về dự báo thực → phải đánh giá **ngoài mẫu** (CV);
  (ii) phải tách "dự báo sớm can thiệp được" (A) khỏi "dự báo muộn target-proximal" (B —
  `G1/G2` rất gần `G3`, chỉ có ở thời điểm muộn);
  (iii) một con số R² đơn lẻ không đủ → cần **baseline** + **paired comparison cùng folds**
  để biết cải thiện có nhất quán không.
- **Quy trình thực hiện (các bước):**
  1. Định nghĩa 3 đặc tả: **baseline** (dự đoán trung bình), **Model A**, **Model B**.
  2. Tạo strata `failures==0` vs `>0`; chia **5-fold StratifiedKFold** (shuffle, `seed=42`).
  3. Mỗi fold: fit preprocessing (OneHot drop-first + StandardScaler) **chỉ trên train**
     (tránh leakage) → fit OLS → predict test fold → gom **out-of-fold (OOF) predictions**.
  4. Tính metric: **aggregate OOF** RMSE/MAE/R² (kết quả chính) + fold-wise cho paired (B−A).
  5. Fit OLS toàn mẫu → hệ số + **HC3** + **joint Wald + Holm**; tính VIF, Breusch–Pagan,
     Cook's distance.
  6. Sensitivity đã định trước: ordinal-as-category, `log1p(absences)`, `G3>0`, per-school.
  7. Xuất CSV (`regression_*`) + Hình `reg_*`.
- **Setup:** Model A = `failures + studytime + absences + C(school) + C(sex)`; Model B = A +
  `G1 + G2`; biến kết quả `G3`; n=395.
- **Giả thuyết & quy tắc:** joint Wald cho mỗi term, `H0:` các hệ số của term = 0, bác bỏ nếu
  `p_holm < 0,05`. So dự báo qua paired fold differences (B−A) trên cùng folds.
- **Phân tích toán học:** OLS `β̂ = (XᵀX)⁻¹Xᵀy`; chỉ số `R²`, `adj R²`, `RMSE`, `MAE`, `OOF R²`;
  **VIF** `= 1/(1 − R_j²)`; **Breusch–Pagan** (LM cho dị phương sai); **HC3** sandwich SE
  (*lý do HC3:* hiệu chỉnh dị phương sai mẫu nhỏ tốt hơn HC0/HC1); **joint Wald test**.
- **Phân tích kết quả:** in-sample A R²=0,155 / B R²=0,829; **OOF R²: baseline −0,004 → A
  0,087 → B 0,806**; `failures` p_holm=0,001 (A); `G2` trội (B); VIF max≈6 (<10 ⇒ không kích
  hoạt Ridge); BP Model B p=5,42e-5 ⇒ dùng HC3; residual có dải chéo tại `G3=0`.
- **Hình 5** `report/figures/reg_cv_model_comparison.png`, **Hình 6**
  `report/figures/reg_course_diagnostics.png`.
- *Nguồn:* `notebooks/core/03` + `notebooks/04_regression.ipynb`.
- ⚠️ **Đồng bộ số liệu:** hệ số `G1/G2` ở core/03 (OLS thường) = 0,146 / 0,977; ở appendix/04
  (HC3, full features) = 0,189 / 0,957. Nêu rõ **hai đặc tả khác nhau** để tránh nhầm.

---

## Phần V — Quy hoạch thực nghiệm (§5) — *các thí nghiệm mô phỏng*

**Lý do thực hiện cả §5 (động cơ chung):** §4 chỉ là dữ liệu quan sát ⇒ không thể biến chênh
lệch quan sát thành **tác động can thiệp**. Muốn trả lời nhân quả "chương trình hỗ trợ có làm
tăng `G3` không" thì cần **thí nghiệm ngẫu nhiên**. Chưa triển khai thực địa nên **mô phỏng**
để: (a) tính cỡ mẫu trước khi chạy thật; (b) kiểm chứng power/Type I khi outcome bị chặn [0,20];
(c) minh họa factorial. Effect được **đặt trước theo ý nghĩa thực tiễn**, KHÔNG lấy từ chênh
lệch quan sát (D-016).

### 5.1–5.2 Khung thiết kế
- Unit = một học sinh; treatment = chương trình ôn tập có hướng dẫn vs học thông thường;
  randomization **1:1**; **blocking theo `school`**; replication; estimand = chênh lệch trung
  bình `G3`; α=0,05 hai phía, power 0,80; effect mục tiêu chính **+1,5 điểm**.

### 5.3 Thí nghiệm tính cỡ mẫu
- **Lý do:** trước khi triển khai phải biết cần bao nhiêu học sinh để đủ power, tránh
  under-powered (bỏ sót effect thật).
- **Quy trình:** (1) lấy `SD=4,581` từ dữ liệu; (2) mỗi effect δ tính `d = δ/SD`;
  (3) `TTestIndPower.solve_power(α, power=0,8, ratio=1)` → n/nhóm; (4) lập bảng.
- **Toán:** `d = δ/SD`; cỡ mẫu 2 mẫu (xấp xỉ `n/nhóm ≈ 2(z₁₋α/₂ + z₁₋β)² / d²`).
- **Kết quả:**

  | Effect | Cohen d | n/nhóm | Tổng |
  |---:|---:|---:|---:|
  | 0,5đ | 0,109 | 1.319 | 2.638 |
  | 1,0đ | 0,218 | 331 | 662 |
  | **1,5đ** | 0,327 | 148 | **296** |
  | 2,0đ | 0,437 | 84 | 168 |

### 5.4 Thí nghiệm Monte Carlo power
- **Lý do:** kiểm chứng công thức cỡ mẫu *lý thuyết* có còn đúng khi outcome bị chặn [0,20]
  (floor/ceiling), và xác nhận **Type I error** được kiểm soát ở mức α.
- **Quy trình:** với mỗi cặp (effect, n): lặp **2.000 lần** → sinh control `~N(mean, SD)`,
  treated `~N(mean+effect, SD)` → **clip [0,20]** → Welch t hai phía → đếm `p < α`. Rejection
  rate = **power** (khi effect>0) hoặc **Type I** (khi effect=0). Vẽ power curve.
- **Toán/DGP:** mô hình sinh dữ liệu nêu trên; `power = E[reject | H1]`, `Type I = E[reject | H0]`.
- **Kết quả:** power **0,805** tại 150/nhóm (≈ lý thuyết 148/nhóm); Type I ≈ 0,045–0,059
  (gần α). Effect ước lượng hơi < 1,5 do clip gây ceiling.
- **Hình 7** `report/figures/doe_power_curve.png`.

### 5.5 Thí nghiệm factorial 2×2
- **Lý do:** minh họa ước lượng **đồng thời** 2 main effects + interaction trong một thiết kế
  (hiệu quả hơn 2 thí nghiệm riêng), với 2 can thiệp đều randomize được.
- **Quy trình:** (1) tạo design 2×2 = 4 cell × 80 học sinh; (2) sinh `G3` theo mô hình tuyến
  tính + nhiễu `N(0, SD)`, clip [0,20]; (3) fit OLS có interaction; (4) đọc hệ số/p.
- **Toán:** `G3 = β₀ + β_A·A + β_B·B + β_AB·(A×B) + ε`; hệ số đặt trước **1,2 / 0,6 / 0,4**
  (A=`guided_review`, B=`study_reminders`).
- **Kết quả 1 sim:** guided 2,386 (có ý nghĩa), reminders 1,140, interaction −1,715 (hai cái
  sau không đạt mức 5% trong lần mô phỏng này). Đây là **minh họa thiết kế**, không phải bằng
  chứng thực nghiệm.

### 5.6 Giới hạn thiết kế
- Noncompliance, contamination, attrition chưa đưa vào mô hình cốt lõi; SD từ UCI có thể lệch
  quần thể triển khai; `G3` bị chặn → floor/ceiling; blocking chỉ theo trường.
- *Nguồn:* `notebooks/core/05_experimental_design.ipynb`.

---

## Phần VI — §6 Sai số & hạn chế · §7 Thảo luận · §8 Kết luận · §9 Tham khảo

- **§6 (6.1–6.7):** sai số lấy mẫu; selection bias & khái quát hóa (Model A R² **âm** tại MS,
  n=46); sai số đo lường (self-report); confounding (không có causal DAG); sai số mô hình
  (point-mass tại 0, heteroscedasticity → HC3 không sửa misspecification); multiple testing &
  exploratory (H9); sai số thực nghiệm. *Nguồn:* `notebooks/03`, `notebooks/04`.
- **§7 Thảo luận:** `failures`/`higher` là **dấu hiệu rủi ro**, không phải nguyên nhân can
  thiệp; Model A dự báo sớm hạn chế; quan sát vs thực nghiệm.
- **§8 Kết luận:** trả lời 4 câu hỏi nghiên cứu + hướng phát triển (mô hình cho outcome bị
  chặn, nhiều trường hơn, pilot study).
- **§9 Tài liệu tham khảo:** 6 mục (Cortez & Silva 2008; UCI; Walpole; Trosset; Mason; slide
  IT2022E).

---

## Phần VII — Bản đồ artifact & việc còn lại

**7 hình chính của báo cáo:**

| Hình | File | Notebook sinh ra | Mục |
|---|---|---|---|
| 1 | `eda_course_overview.png` | core/01 | §2 |
| 2 | `ci_bootstrap_mean_g3.png` | appendix/03 | §4.2 |
| 3 | `hyp_course_failures.png` | core/02 | §4.3 |
| 4 | `reg_course_correlation.png` | core/03 | §4.4 |
| 5 | `reg_cv_model_comparison.png` | appendix/04 | §4.5 |
| 6 | `reg_course_diagnostics.png` | core/03 | §4.5 |
| 7 | `doe_power_curve.png` | core/05 | §5.4 |

**CSV chính (`data/processed/`):** `student_mat_clean.csv`; `hypothesis_test_results.csv` /
`hypothesis_posthoc_results.csv`; `bootstrap_ci_results.csv` / `power_sensitivity_results.csv`;
`regression_cv_results.csv` + các bảng `regression_*`; `course_*` và `doe_*` (luồng core).

**Việc còn lại để hoàn thiện báo cáo:**
- Điền placeholder trang đầu (giảng viên, nhóm, thành viên).
- ROADMAP P3: review chéo mọi số liệu với artifact + sinh `report/report.pdf`.
- ⚠️ Discrepancy đã phát hiện (cần xử lý trước khi nộp): output `notebooks/01,02,03` (appendix)
  in **đường dẫn máy cá nhân** (`C:\Users\LENOVO\...`) — mâu thuẫn "Definition of done";
  `matplotlib.use("Agg")` bị comment ở NB 02/03.
