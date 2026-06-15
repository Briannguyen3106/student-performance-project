# Ke hoach xu ly Notebook 04 - Regression

Tai lieu nay quy dinh muc tieu, co so ly thuyet, quyet dinh phan tich va artifact cho
`notebooks/04_regression.ipynb`. Notebook 01-03 duoc xem la dau vao da hoan thanh; Phase 4
su dung `data/processed/student_mat_clean.csv` va khong chay lai hay thay doi cac phase truoc.

## 1. Cau hoi cua Phase 4

Phase 4 tach hai cau hoi khac nhau:

1. **Mo hinh association co dieu kien:** cac bien nen, gia dinh, hanh vi va xa hoi lien quan
   den `G3` nhu the nao trong mot dac ta da dinh truoc, sau khi giu cac bien con lai co dinh?
2. **Mo hinh du bao:** viec them diem qua trinh `G1`, `G2` cai thien sai so du bao ngoai mau
   bao nhieu so voi mo hinh chi dung thong tin nen/hanh vi/xa hoi?

Hoi quy tren du lieu quan sat chi uoc luong association conditional on included covariates.
Khong goi day la association "da kiem soat confounding" vi project chua co causal DAG va
khong xac dinh day du mediator/collider. He so khong duoc dien giai la tac dong nhan qua.

## 2. Dinh nghia cac mo hinh

### Baseline

Dung `DummyRegressor(strategy="mean")` lam moc so sanh. Neu mo hinh tuyen tinh khong cai
thien ro so voi du doan trung binh tren du lieu chua thay, do phuc tap them vao khong tao ra
gia tri du bao thuc te.

### Model A - khong dung diem qua trinh

- Outcome: `G3`.
- Predictors: tat ca bien trong clean dataset tru `G1`, `G2`, `G3`.
- Giu ca bien nen nhu `school`, `sex`, `age`, `Medu`, `Fedu` de uoc luong association co
  dieu kien theo cung mot dac ta, khong khang dinh da loai het confounding.
- Khong chon bien dua tren p-value cua Notebook 02. Lam nhu vay se tai su dung cung du lieu
  de vua chon vua kiem dinh, lam tang selection bias va co the loai nham bien confounder.

Giu tat ca bien khong co nghia la bo qua multicollinearity. Day la dac ta full model duoc
chon truoc de tranh data-driven variable selection; VIF va sensitivity analysis ben duoi
quyet dinh muc do co the dien giai tung he so. Cac cap nhu `Walc`/`Dalc` va `Medu`/`Fedu`
do cac khai niem khac nhau (ngay thuong/cuoi tuan; me/cha), nen khong gop hay xoa chi vi
chung tuong quan trong EDA.

Model A tra loi cau hoi du bao som hon, khi chua biet ket qua hoc tap o ky 1 va ky 2. Day la
mo hinh phu hop hon neu muc tieu la nhan dien hoc sinh can ho tro tu thong tin nen va hanh vi.

### Model B - them `G1` va `G2`

- Outcome: `G3`.
- Predictors: toan bo predictors cua Model A, cong `G1` va `G2`.
- Model B dung de dinh luong gia tri du bao bo sung cua lich su diem gan `G3`.

`G1` va `G2` khong tu dong la data leakage neu chung da ton tai tai thoi diem dua ra du bao.
Tuy nhien, chung la target-proximal predictors va co the lam lu mo dong gop cua bien xa
hoi/hanh vi. Vi vay phai bao cao Model A va Model B rieng, gan voi hai thoi diem du bao ro
rang, khong dung Model B de thay the cau hoi cua Model A.

## 3. Tai sao chon multiple linear regression

Multiple linear regression uoc luong ky vong co dieu kien:

```text
E(G3 | X) = beta_0 + beta_1 X_1 + ... + beta_p X_p
```

OLS duoc chon lam mo hinh chinh vi:

- `G3` la score 0-20 va muc tieu la du doan gia tri trung binh, nen linear regression la
  baseline de hieu va de dien giai.
- He so co don vi truc tiep la diem `G3`, phu hop voi bao cao thong ke ung dung.
- OLS cung cap residual, influence diagnostics va interval de kiem tra cac gia dinh.
- So sanh Model A/B minh bach hon khi ca hai dung cung mot lop mo hinh.

`G3` bi chan va roi rac, nen OLS khong phai mo hinh hoan hao cua toan bo phan phoi. Phase 4
se danh gia tinh phu hop bang residual diagnostics va hieu nang ngoai mau; khong dua vao
R-squared trong mau de tu khang dinh mo hinh.

## 4. Ma hoa va preprocessing

### Phan loai bien

- Nominal/binary: one-hot encoding.
- Ordinal/count/numeric: giu dang so theo data dictionary trong mo hinh chinh. Day la gia
  dinh xu huong tuyen tinh va khoang cach cac muc du de xem nhu bang nhau.
- `absences`: giu nguyen gia tri goc, khong xoa va khong winsorize.

One-hot encoding dung `drop="first"` de tao nhom tham chieu va tranh perfect
multicollinearity trong OLS. Dung `handle_unknown="ignore"` trong cross-validation de fold
validation van transform duoc neu mot category chi xuat hien trong training fold khac.

Preprocessing phai nam trong `sklearn.pipeline.Pipeline` va duoc fit rieng trong tung
training fold. Khong fit encoder/scaler tren toan bo dataset truoc cross-validation, vi nhu
vay validation fold da tham gia vao qua trinh hoc preprocessing.

Standardization khong can cho nghiem OLS, nhung co the dung cho cac bien numeric trong
pipeline de he thong nhat va de san cho sensitivity model co regularization. Bang he so OLS
chinh nen giu thang do goc de dien giai theo diem `G3`.

Chay ordinal-encoding sensitivity cho `Medu`, `Fedu`, `traveltime`, `studytime`,
`failures`, `famrel`, `freetime`, `goout`, `Dalc`, `Walc`, `health` bang cach xem chung la
categorical. So sanh aggregate OOF metrics va joint tests. Neu ket qua thay doi dang ke,
khong dien giai linear trend cua ma ordinal la ben vung.

## 5. Danh gia ngoai mau

Dung 5-fold cross-validation voi `shuffle=True`, `random_state=42`. Mau phan tich chinh la
du 395 quan sat; con so 357 chi la mau `G3 > 0` cua sensitivity analysis.

Khong stratify theo `G3` hoac cac bin tao tu `G3`, vi outcome la bien lien tuc va viec tao
bin la mot quyet dinh tuy y. Tuy nhien, `failures=0` chiem 312/395 (79.0%) va la predictor
manh da thay o Phase 2. Vi vay dung `StratifiedKFold` voi nhan chia fold duoc tao truoc la
`failures == 0` va `failures > 0`. Day la stratification theo mot predictor co san, khong
dung outcome, va giup moi fold co ty le hoc sinh tung truot mon gan nhau. Khong stratify
theo bon muc `failures` vi muc 2 va 3 chi co 17 va 16 quan sat, tao ra strata qua nho.

Ca baseline, Model A va Model B phai dung chinh xac cung mot bo fold de chenh lech metric
khong bi nhieu do chia mau khac nhau. Luu fold id trong output de ket qua co the tai lap va
kiem tra phan phoi `G3`, `failures` sau khi chia.

Bao cao:

- **RMSE:** phat nang sai so lon; la metric chinh cho so sanh mo hinh.
- **MAE:** de dien giai la sai lech tuyet doi trung binh theo diem `G3`, it nhay voi sai so
  lon hon RMSE.
- **R-squared ngoai mau:** ty le cai thien so voi du doan trung binh trong tung fold; co the
  am neu mo hinh tong quat hoa kem.
- Mean, standard deviation va ket qua tung fold, khong chi mot con so trung binh.

Aggregate metric tinh tren toan bo out-of-fold predictions la ket qua chinh. Fold-wise
metrics dung de xem do bien dong va tinh paired difference Model B tru Model A. Khong xem
SD cua 5 fold la confidence interval va khong lay trung binh fold-wise R-squared lam chi so
R-squared chinh.

Khong dung adjusted R-squared hay AIC lam bang chung chinh cho kha nang du bao, vi day la
chi so in-sample. Chung co the duoc bao cao bo sung cho OLS fit tren toan bo du lieu.

Neu can danh gia do on dinh cao hon, co the them sensitivity analysis bang repeated 5-fold
CV. Ket qua chinh van la 5-fold theo roadmap de tranh thay doi dac ta sau khi xem ket qua.

## 6. Uoc luong he so va do bat dinh

Sau danh gia cross-validation, fit OLS tren toan bo dataset de tao bang he so. Bao cao:

- ten bien va nhom tham chieu;
- coefficient theo thang diem `G3`;
- standard error HC3;
- 95% confidence interval;
- p-value chua dieu chinh;
- VIF khi co the tinh on dinh.

Dung heteroscedasticity-consistent standard errors HC3 vi mau chi co 395 quan sat va phuong
sai residual co the khong dong nhat. HC3 khong sua nonlinearity hay omitted-variable bias;
no chi lam suy dien standard error ben vung hon truoc heteroscedasticity.

Bang he so co nhieu predictors mang tinh exploratory. Khong nen tao mot danh sach "bien co
anh huong" chi dua tren `p < 0.05`. Trong phan dien giai, uu tien magnitude, 95% CI, tinh
on dinh, tinh hop ly cua contrast va ket qua cross-validation.

Tat ca p-value tung coefficient la exploratory va phai duoc gan nhan `p_raw`. Suy dien theo
term/block dung joint Wald test; Holm correction ap dung tren tap joint tests cua tung model.
Ket luan co y nghia thong ke chi dua tren `p_holm < 0.05`, phu hop quy tac cua project.

## 7. Diagnostics bat buoc

### Linearity

- Ve residuals versus fitted values.
- Kiem tra mau cong co he thong.
- Partial residual plot chi dung cho mot so bien numeric quan trong neu can.

Neu co phi tuyen ro, sensitivity analysis co the them spline/polynomial da dinh truoc cho
bien lien quan. Khong them hang loat bien doi chi de tang R-squared trong mau.

### Homoscedasticity

- Residuals versus fitted.
- Breusch-Pagan test nhu thong tin diagnostics.
- Suy dien he so chinh dung HC3 du test co y nghia hay khong.

### Residual distribution

- Q-Q plot va histogram residual.
- Khong dung Shapiro-Wilk lam tieu chi nhi phan de chap nhan/bac bo mo hinh. Voi regression,
  normality lien quan den suy dien mau nho, khong phai dieu kien de OLS uoc luong he so.

### Multicollinearity

- Bao cao VIF tren design matrix sau encoding, bo intercept.
- Dung `VIF > 5` lam canh bao va `VIF > 10` lam muc multicollinearity nghiem trong. Day la
  nguong diagnostics, khong phai quy tac chon bien tu dong.
- Dac biet dien giai than trong `G1`, `G2` trong Model B vi hai diem nay co the tuong quan
  cao va chia se phuong sai du bao.

Neu co `VIF > 10`, xu ly theo thu tu:

1. Kiem tra design matrix de loai tru loi ma hoa, dummy trap, cot hang so hoac category qua
   hiem. Loi ky thuat phai duoc sua, nhung khong xoa quan sat de giam VIF.
2. Giu full OLS Model A/B lam dac ta chinh de tranh selection theo ket qua. Gan co cac he so
   VIF cao la khong on dinh, khong dien giai dau/p-value rieng le nhu bang chung doc lap;
   bao cao CI va, voi mot nhom bien lien quan, joint Wald/F-test neu cau hoi can hieu ung
   chung cua ca block.
3. Fit Ridge trong cung cross-validation lam sensitivity analysis ve du bao. Neu can mot
   reduced OLS de dien giai, chi gop/loai bien khi co ly do noi dung duoc ghi truoc (bien
   trung lap ve khai niem hoac khong phu hop thoi diem du bao), sau do bao cao song song voi
   full model. Khong chon bien can xoa dua tren p-value hay chon phuong an cho R-squared dep
   nhat.

Neu Ridge cai thien do on dinh/ngoai mau trong khi he so OLS thay doi manh, ket luan la du
bao tong the co the van huu ich nhung khong the tach dong gop rieng cua cac predictors dong
tuyen mot cach tin cay.

Voi bien categorical nhieu muc, VIF tung dummy phu thuoc reference category. Vi vay cung
bao cao condition number cua design matrix, so quan sat moi category va joint Wald test cua
toan bo dummy thuoc cung term. GVIF chi them neu co implementation duoc xac minh; khong bat
buoc vi statsmodels khong cung cap truc tiep.

### Influential observations

- Leverage, studentized residual va Cook's distance.
- Nguong tham khao Cook's distance `4/n` chi dung de gan co quan sat can xem lai.
- Khong xoa quan sat chi vi vuot nguong. Neu ket qua nhay, fit lai khong co cac diem anh
  huong nhu sensitivity analysis va bao cao ca hai ket qua.

## 8. Sensitivity analyses

Chi them sau khi ket qua chinh da duoc tao:

1. `log1p(absences)` thay cho `absences` goc de kiem tra anh huong cua duoi phai.
2. Fit Ridge regression trong cung cross-validation khi co bat ky `VIF > 10` hoac metric
   OLS bien dong manh. Hyperparameter phai duoc chon trong inner CV neu dung de bao cao
   hieu nang, tranh tuning tren validation fold.
3. Fit mo hinh tren `G3 > 0` chi de kiem tra do nhay; ket qua nay khong thay the phan tich
   chinh va phai gan nhan ro.
4. Ma hoa cac bien ordinal quan trong nhu categorical de kiem tra gia dinh linear trend.
5. Bao cao metric theo `school` de mo ta do on dinh noi bo. Random CV chi uoc luong kha
   nang du bao hoc sinh moi trong cung cau truc hai truong, khong chung minh tong quat hoa
   sang truong moi; khong dung leave-one-school-out lam ket qua chinh vi chi co hai cluster.
6. Bao cao ty le OOF prediction nam ngoai [0, 20]. Khong clip trong ket qua chinh; clipping
   vao [0, 20] chi la sensitivity analysis va phai bao cao song song.

Khong winsorize `absences`, khong xoa `G3=0`, va khong loai influential observations trong
dataset chinh.

## 9. Cau truc de xuat cho notebook

1. Muc tieu, estimand va thoi diem du bao cua Model A/B.
2. Import, constants: `RANDOM_SEED = 42`, `ALPHA = 0.05`.
3. Doc clean data va kiem tra schema/shape.
4. Khai bao feature groups va preprocessing pipeline.
5. Baseline va 5-fold cross-validation cho Model A/B.
6. Bang so sanh metric va figure ngoai mau.
7. Fit OLS tren toan bo du lieu, xuat coefficient table voi HC3 CI.
8. VIF va residual/influence diagnostics.
9. Sensitivity analyses da dinh truoc.
10. Ket luan: predictive performance, association co dieu kien, gioi han va khong nhan qua.

## 10. Artifact dau ra

Bat buoc:

- `data/processed/regression_cv_results.csv`: ket qua tung fold va summary cho baseline,
  Model A, Model B.
- `data/processed/regression_coefficients.csv`: he so, HC3 SE, CI, p-value va model.
- `data/processed/regression_diagnostics.csv`: VIF va cac thong tin diagnostics co cau truc.
- `data/processed/regression_oof_predictions.csv`: outcome, prediction, fold, model,
  `school`, `failures` va co du doan ngoai [0, 20].
- `data/processed/regression_joint_tests.csv`: joint Wald tests va Holm-adjusted p-value.
- `report/figures/reg_cv_model_comparison.png`.
- `report/figures/reg_observed_vs_predicted.png`, tao tu out-of-fold predictions.
- `report/figures/reg_residual_diagnostics.png`.
- `report/figures/reg_influence.png`.

Out-of-fold predictions phai duoc dung cho figure danh gia du bao. Khong ve observed versus
fitted tren chinh training data roi mo ta do la hieu nang tong quat hoa.

## 11. Tieu chi hoan thanh

- Notebook chay het khong loi tu working directory `notebooks/`.
- Khong co duong dan tuyet doi va khong thay doi `data/raw/`.
- Preprocessing nam trong CV pipeline; Model A/B dung cung folds.
- Co baseline, RMSE, MAE va out-of-sample R-squared.
- Aggregate OOF metrics la ket qua chinh; co paired fold differences Model B - Model A.
- Co HC3 CI, VIF, residual va influence diagnostics.
- Co joint term tests voi Holm correction; coefficient p-value duoc gan nhan exploratory.
- Cac sensitivity analysis duoc tach khoi ket qua chinh.
- Dien giai phan biet association, prediction va causation.
- Artifact CSV/PNG khop voi ket luan trong notebook.
- Cap nhat `DECISIONS.md`, `PROJECT_STATUS.md`, `ANALYSIS_RESULTS.md` va `ROADMAP.md` sau
  khi Notebook 04 da duoc thuc thi va xac minh.
