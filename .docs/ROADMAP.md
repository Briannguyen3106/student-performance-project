# Dinh huong tiep theo

## P0: Xac minh luong trinh bay chinh

- [x] Anh xa project voi Chuong 1, 4, 6, 7 va CLO1-CLO4.
- [x] Tao bon notebook trong `notebooks/core/`.
- [x] Tach luong trinh bay chinh va phu luc ky thuat.
- [x] Chay lai toan bo notebook core trong moi truong project.
- [x] Xac nhan artifact tai lap duoc va khong co duong dan tuyet doi.

Hoan thanh khi mot thanh vien moi co the clone, cai dependencies, chay 01-03 va thu duoc
cung schema/kich thuoc output ma khong sua code.

## P1: Phase 4 - Regression

- [x] Tao `notebooks/04_regression.ipynb`.
- [x] Model A khong dung `G1`, `G2`, nham danh gia cac bien hanh vi/xa hoi co san.
- [x] Model B co `G1`, `G2`, gan voi thoi diem du bao muon hon va target-proximal predictors.
- [x] Xac dinh preprocessing trong cross-validation, khong fit encoder tren toan bo data.
- [x] Bao cao VIF, residual diagnostics, heteroscedasticity va influential observations.
- [x] Dung 5-fold cross-validation; bao cao RMSE/MAE/R-squared ngoai mau.
- [x] Xuat coefficient/joint-test/CV tables va figure voi prefix `reg_`.

Hoan thanh 2026-06-09: notebook chay het, co artifact, so sanh Model A/B va dien giai khong
nhan qua. Model A co OOF R-squared 0.087; Model B co OOF R-squared 0.806.

## P2: Experimental design

- [x] Dinh nghia experimental unit, treatment, outcome va primary hypothesis.
- [x] Tinh sample size dua tren effect co y nghia thuc tien.
- [x] Mo phong A/B design va empirical power.
- [x] Mo rong factorial 2x2 voi hai can thiep co the randomize.
- [x] Xac minh notebook va artifact `doe_*` sau khi execute.

## P3: Measurement theory va bao cao

- [x] Phan loai bien nominal, ordinal, count va score; tranh coi moi ma so ordinal la lien tuc.
- [x] Thao luan reliability/validity cua `famrel`, `health`, `Dalc`, `Walc`, `studytime`.
- [x] Tong hop sampling error, measurement error, selection bias va confounding.
- [x] Tao source report Markdown co version control.
- [ ] Review va sinh `report/report.pdf` tu source.
- [ ] Review cheo ket qua, caption, bang va claim voi artifact.

## No luc ky thuat nen lam sau

- [ ] Quyet dinh `scripts/rebuild_notebooks.py` la source of truth hay chi la cong cu tao mau.
- [ ] Sua/loai thu muc `utlis/` sau khi kiem tra khong ai dang phu thuoc vao ten nay.
- [ ] Them kiem tra nhe cho schema CSV, so dong va notebook error outputs.
- [ ] Ghim dependency bang lockfile hoac snapshot moi truong neu can tai lap dai han.
