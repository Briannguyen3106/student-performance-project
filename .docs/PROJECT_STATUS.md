# Trang thai du an

Snapshot: 2026-06-14, nhanh `main`.

## Tong quan

| Phase | Trang thai | Bang chung |
|---|---|---|
| 1. EDA | Hoan thanh, dang co thay doi chua commit | `01_EDA.ipynb`, clean CSV, 7 figure `eda_*` |
| 2. Hypothesis testing | Hoan thanh, chua commit | `02_hypothesis_testing.ipynb`, 2 CSV, 10 figure `hyp_*` |
| 3. CI + power sensitivity | Hoan thanh, chua commit | `03_confidence_intervals.ipynb`, 2 CSV, 3 figure `ci_*` |
| 4. Regression | Hoan thanh, chua commit | `04_regression.ipynb`, 7 CSV, 4 figure `reg_*` |
| 5. DoE simulation | Chua bat dau | Chua co notebook/artifact |
| 6. Measurement theory | Chua bat dau | Chua co section bao cao |
| Bao cao cuoi | Da co ban thao Markdown | `report/results/report_draft.md`; chua co PDF |

## Tai cau truc theo de cuong

Da tao luong trinh bay chinh trong `notebooks/core/`:

| Notebook | Trang thai | Pham vi |
|---|---|---|
| `01_data_preparation_and_eda.ipynb` | Da tao | Chuong 1, 6 |
| `02_statistical_inference.ipynb` | Da tao | Chuong 4.1-4.5 |
| `03_correlation_and_regression.ipynb` | Da tao | Chuong 4.6 |
| `05_experimental_design.ipynb` | Da tao va xac minh | Chuong 7, CLO3-CLO4 |

Notebook cu va artifact Phase 1-4 van duoc bao toan nhu phu luc ky thuat.

Ngay 2026-06-14, ca bon notebook core da execute day du, khong co output loi va khong co
duong dan may ca nhan trong output. Notebook DoE da duoc vector hoa de chay trong khoang
vai chuc giay thay vi lap tung phep kiem dinh.

Ban thao bao cao chi tiet da duoc tao tai `report/results/report_draft.md`, gom 9 phan,
phu luc va 7 figure tham chieu. Can dien thong tin nhom, review noi dung va chuyen sang dinh
dang nop cuoi.

Ca ba notebook hien co deu da execute tat ca code cell va khong co output loi:

| Notebook | Code cells | Cell chua chay | Loi |
|---|---:|---:|---:|
| `01_EDA.ipynb` | 9 | 0 | 0 |
| `02_hypothesis_testing.ipynb` | 5 | 0 | 0 |
| `03_confidence_intervals.ipynb` | 7 | 0 | 0 |
| `04_regression.ipynb` | 6 | 0 | 0 |

## Artifact hien co

- `student_mat_clean.csv`: 395 dong, 33 bien.
- `hypothesis_test_results.csv`: 10 kiem dinh chinh.
- `hypothesis_posthoc_results.csv`: 32 so sanh cap.
- `bootstrap_ci_results.csv`: 16 uoc luong/khoang tin cay.
- `power_sensitivity_results.csv`: 4 contrast.
- Regression: CV, paired fold differences, OOF predictions, coefficients, joint tests,
  diagnostics va sensitivity results.
- Core course tables: inference summary, regression summary, DoE design scenarios,
  simulation results va factorial results.
- 24 figure: 7 EDA, 10 hypothesis, 3 CI, 4 regression.
- 5 figure cho luong trinh bay chinh: `eda_course_*`, `hyp_course_*`, `reg_course_*`,
  `doe_*`.

## Viec dang do

- Working tree co nhieu file modified/untracked cua Phase 1-4; can review va commit theo
  don vi logic truoc khi nhieu nguoi cung sua.
- README da duoc viet lai theo luong trinh bay chinh; can tiep tuc doi chieu voi source bao
  cao khi bao cao cuoi duoc tao.
- Chua co test tu dong cho schema/output; viec xac minh hien dua vao chay notebook.
- `scripts/rebuild_notebooks.py` la nguon sinh notebook 01-03 nhung chua co quy trinh ro
  rang de tranh notebook va generator lech nhau.
- `utlis/` co ve la loi chinh ta cua `utils/`; chua co helper module thuc te.

## Rui ro hien tai

- Du lieu quan sat, khong ho tro ket luan nhan qua.
- Mau 395 hoc sinh chi den tu hai truong; kha nang khai quat hoa bi han che.
- Mot so nhom rat mat can bang, dac biet `higher=no` chi co 20 quan sat.
- Random CV cua Phase 4 chi danh gia hoc sinh moi trong cung cau truc hai truong; `MS` chi
  co 46 quan sat, khong du de khang dinh tong quat hoa sang truong moi.
- Model B co heteroscedasticity ro theo Breusch-Pagan; coefficient inference dung HC3.
- Chay generator co the ghi de notebook; can xem diff truoc va sau khi dung.
