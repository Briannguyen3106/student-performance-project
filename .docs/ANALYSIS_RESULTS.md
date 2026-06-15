# Ket qua phan tich hien tai

Nguon: cac CSV trong `data/processed/`, duoc tao boi notebook 01-03. Snapshot 2026-06-07.
Phase 4 duoc bo sung tu `04_regression.ipynb` ngay 2026-06-09.

## Du lieu va EDA

- 395 quan sat, 33 bien; khong co missing hay duplicate theo notebook EDA.
- Trung binh `G3`: 10.415; trung vi: 11.
- 95% t-CI cho trung binh `G3`: [9.962, 10.868].
- `G3=0` va outlier `absences` duoc giu trong phan tich chinh.

## Ket qua sau Holm correction

Co y nghia thong ke tai alpha 0.05:

| Gia thuyet | Ket qua | Effect size | `p_holm` |
|---|---|---:|---:|
| H6 `higher` | `yes - no` = 3.808 diem G3 | Hedges g = 0.843 | 0.0195 |
| H7 `failures` | Khac biet omnibus | epsilon-squared = 0.128 | 1.73e-10 |
| H8a `Medu` | Khac biet omnibus | epsilon-squared = 0.052 | 0.000685 |
| H8b `Fedu` | Khac biet omnibus | epsilon-squared = 0.027 | 0.0379 |

Khong con y nghia sau Holm correction: `sex`, `address`, `famsup`, `studytime`, `Walc`
va H9 `absences`. H9 la exploratory; trong pipeline xac nhan, rho = 0.018 va
`p_holm = 0.880`.

## Dien giai can than trong

- `higher=yes` co effect size lon nhung nhom `higher=no` chi co 20 hoc sinh, nen CI rong:
  Welch 95% CI cho chenh lech trung binh la [1.509, 6.107].
- `failures=0` khac co y nghia voi tung muc 1, 2, 3 trong Dunn-Holm; khong nen suy rong
  rang moi cap failures deu khac nhau.
- CI rieng le cua cac contrast khong phai simultaneous CI; ket luan nhieu gia thuyet van
  dua tren Holm correction o Phase 2.
- Cac quan he tren khong chung minh nhan qua.

## Power sensitivity

Minimum detectable Hedges/Cohen d xap xi tai power 80%:

| Contrast | MDE |
|---|---:|
| sex | 0.283 |
| address | 0.340 |
| higher | 0.645 |
| failures (0 so voi >0) | 0.347 |

Thiet ke co the bo sot effect nho, dac biet voi contrast mat can bang `higher`.

## Regression va du bao ngoai mau

Aggregate 5-fold out-of-fold metrics tren du 395 quan sat:

| Model | RMSE | MAE | OOF R-squared |
|---|---:|---:|---:|
| Baseline mean | 4.585 | 3.435 | -0.004 |
| Model A, khong `G1/G2` | 4.373 | 3.405 | 0.087 |
| Model B, co `G1/G2` | 2.017 | 1.353 | 0.806 |

Model A chi cai thien nhe so voi baseline, nen cac bien nen/hanh vi/xa hoi co gia tri du bao
som han che trong dac ta tuyen tinh nay. Model B cai thien RMSE trung binh 2.421 diem va MAE
2.051 diem so voi Model A tren cung folds; `G1/G2` la target-proximal predictors va ket qua
nay khong thay the cau hoi can thiep som cua Model A.

Joint Wald tests voi Holm correction:

- Model A: `failures` co association co dieu kien (`p_holm = 0.0010`).
- Model B: `G1` (`p_holm = 0.0230`) va `G2` (`p_holm < 1e-77`) co y nghia trong dac ta
  ordinal-numeric chinh.
- Khi ma hoa ordinal nhu categorical, `failures` van co y nghia trong Model A
  (`p_holm = 0.0098`), `G2` van rat on dinh trong Model B, nhung `G1` khong con qua Holm.

Diagnostics va sensitivity:

- Max VIF la 6.06 o Model A va 6.15 o Model B: co canh bao nhung khong vuot nguong 10, nen
  Ridge sensitivity khong duoc kich hoat theo protocol.
- Breusch-Pagan khong co y nghia o Model A (`p = 0.165`) nhung co o Model B
  (`p = 5.42e-05`); coefficient inference dung HC3.
- Residual plots co dai cheo ro tai nhom `G3=0` va Q-Q tails lech, dac biet o Model B. OLS
  khong mo ta tot point mass tai 0; HC3 khong sua misspecification nay. Vi vay coefficient
  inference can than trong, con ket luan prediction dua tren OOF metrics.
- Ordinal-as-category lam Model A kem baseline (OOF R-squared = -0.039), cho thay gia tang
  bac tu do khong cai thien du bao trong mau nho.
- `log1p(absences)` cai thien nhe Model A (OOF R-squared = 0.121) va Model B (0.823), chi la
  sensitivity analysis.
- Tren mau `G3>0` (n=357), OOF R-squared tang len 0.160 o Model A va 0.926 o Model B. Day
  cho thay point mass tai 0 anh huong manh den fit, nhung sensitivity nay khong thay ket qua
  chinh vi project da quyet dinh giu `G3=0`.
- Model A co R-squared -0.092 rieng o truong `MS` (n=46); random CV khong chung minh kha
  nang tong quat sang truong moi.
- OOF prediction ngoai [0,20]: 0.5% o Model A va 3.8% o Model B. Clipping chi duoc bao cao
  nhu sensitivity, khong thay estimator chinh.

Tat ca he so regression la association conditional on included covariates, khong phai tac
dong nhan qua va khong khang dinh da kiem soat day du confounding.

## Quy hoach thuc nghiem trong luong trinh bay chinh

Notebook `notebooks/core/05_experimental_design.ipynb` dung SD quan sat cua `G3` la 4.581
de lap ke hoach mot A/B test hai phia, alpha 0.05 va power 80%. Cac benchmark ly thuyet:

| Effect muc tieu | Cohen d xap xi | Tong mau |
|---:|---:|---:|
| 0.5 diem | 0.109 | 2638 |
| 1.0 diem | 0.218 | 662 |
| 1.5 diem | 0.327 | 296 |
| 2.0 diem | 0.437 | 168 |

Monte Carlo simulation minh hoa empirical Type I error va power khi diem bi gioi han trong
khoang 0-20. Factorial 2x2 dung hai can thiep co the randomize: guided review va study
reminders. Day la thiet ke de xuat, khong phai bang chung rang cac can thiep gia dinh co tac
dong that trong quan the.
