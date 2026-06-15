# Quyet dinh quan trong

## D-001: Chi phan tich mon Toan

- Trang thai: accepted.
- Quyet dinh: dung `data/raw/student-mat.csv`, 395 hoc sinh, 33 bien.
- Ly do: day la pham vi duoc xac dinh trong muc tieu project.
- He qua: khong tron voi dataset mon Tieng Bo Dao Nha neu chua co thiet ke xu ly 382 hoc
  sinh trung lap giua hai tap.

## D-002: Bao toan du lieu raw

- Trang thai: accepted.
- Quyet dinh: `data/raw/` la read-only; moi output vao `data/processed/`.
- Ly do: dam bao truy vet va tai lap.

## D-003: Giu cac gia tri `G3=0`

- Trang thai: accepted.
- Quyet dinh: `G3=0` hop le theo data dictionary 0-20 va nam trong phan tich chinh.
- He qua: phan tich chi tren `G3>0` chi duoc trinh bay nhu sensitivity analysis, khong thay
  the ket qua chinh.

## D-004: Khong loai outlier `absences` trong dataset chinh

- Trang thai: accepted.
- Quyet dinh: giu nguyen duoi phai cua `absences`; winsorization chi de kiem tra do nhay.
- Ly do: gia tri lon co the la quan sat that, va viec xoa tuy y lam thay doi estimand.

## D-005: Phuong phap kiem dinh va multiple testing

- Trang thai: accepted.
- Quyet dinh: dung Welch t-test cho hai nhom; Kruskal-Wallis cho cac nhom ordinal nhieu
  muc; Spearman cho lien he thu hang. Dung Holm correction cho 10 kiem dinh chinh.
- He qua: ket luan xac nhan dua tren `p_holm < 0.05`; p-value tho chi la thong tin bo sung.
  Sau Kruskal-Wallis, dung Dunn post-hoc voi Holm correction cho so sanh cap.

## D-006: Effect size va dau contrast

- Trang thai: accepted.
- Quyet dinh: bao cao Hedges' g, epsilon-squared hoac Spearman rho tuy test. Dau effect
  size phai theo contrast da ghi, vi du `yes - no`, `U - R`.
- Ly do: p-value khong dien ta cuong do hay y nghia thuc tien.

## D-007: H9 la exploratory

- Trang thai: accepted.
- Quyet dinh: gia thuyet `absences` lien quan den `G3` phat sinh sau EDA va phai luon gan
  nhan post-hoc/exploratory.
- Ly do: tranh trinh bay mot phat hien sau khi xem du lieu nhu gia thuyet dinh truoc.

## D-008: Dinh luong do bat dinh

- Trang thai: accepted.
- Quyet dinh: dung CI tham so va bootstrap 5.000 lan; bao cao MDE tai power 80% thay cho
  observed power.
- Ly do: MDE tra loi kha nang phat hien cua thiet ke ma khong dien giai vong tron tu ket
  qua quan sat.

## D-009: Khong dien giai nhan qua

- Trang thai: accepted.
- Quyet dinh: moi ket qua hien tai la association trong du lieu quan sat.
- He qua: regression tuong lai khong duoc tu dong mo ta la tac dong nhan qua; can neu ro
  confounding, selection bias va cau truc hai truong.

## D-010: Multicollinearity trong Phase 4

- Trang thai: accepted.
- Quyet dinh: full OLS Model A/B giu cac predictors da dinh truoc, khong chon bien theo
  p-value. `VIF > 5` la canh bao, `VIF > 10` la nghiem trong va kich hoat kiem tra design
  matrix, han che dien giai he so rieng le, joint test khi phu hop va Ridge sensitivity.
- He qua: khong tu dong xoa bien co VIF cao. Reduced model chi duoc bao cao song song khi
  co ly do noi dung ve trung lap khai niem/thoi diem du bao, khong dua tren viec toi uu
  R-squared trong mau.

## D-011: Chia fold cho regression

- Trang thai: accepted.
- Quyet dinh: dung 5-fold shuffled cross-validation voi `random_state=42`, stratify theo
  `failures == 0` so voi `failures > 0`; khong stratify theo `G3` hay bin cua `G3`.
- Ly do: `failures=0` chiem 312/395 quan sat va la predictor manh; stratification giu ty le
  nay gan nhau giua cac fold ma khong dung outcome de thiet ke split.
- He qua: baseline, Model A va Model B dung cung fold; fold id duoc luu trong artifact de
  tai lap va kiem tra.

## D-012: Pham vi dien giai he so regression

- Trang thai: accepted.
- Quyet dinh: he so OLS la association conditional on included covariates, khong duoc mo ta
  la da kiem soat day du confounding. Project chua co causal DAG de phan loai confounder,
  mediator va collider.
- He qua: Model A dung cho mo ta association co dieu kien va du bao; Model B chu yeu dung
  cho du bao vi `G1`, `G2` rat gan outcome.

## D-013: Ordinal encoding va multiple testing trong Phase 4

- Trang thai: accepted.
- Quyet dinh: mo hinh chinh ma hoa ordinal dang numeric de tiet kiem bac tu do; sensitivity
  xem cac ordinal quan trong la categorical. P-value coefficient la exploratory; ket luan
  theo term/block dua tren joint Wald tests voi Holm correction rieng cho tung model.
- He qua: neu categorical sensitivity thay doi ket qua dang ke, khong dien giai linear trend
  cua ordinal code la ben vung.

## D-014: Estimand cua cross-validation

- Trang thai: accepted.
- Quyet dinh: aggregate metrics tren toan bo out-of-fold predictions la ket qua chinh;
  fold-wise metric dung cho paired comparison va variability, khong tao CI tu SD cua 5 fold.
- He qua: random CV danh gia hoc sinh moi trong cung cau truc hai truong. Metric theo school
  va prediction ngoai [0,20] la sensitivity diagnostics, khong chung minh kha nang tong quat
  sang mot truong moi.

## D-015: Cau truc project bam theo de cuong IT2022E

- Trang thai: accepted.
- Quyet dinh: dung bon notebook trong `notebooks/core/` lam luong trinh bay chinh: data/EDA,
  statistical inference, correlation/regression va experimental design.
- Ly do: cau truc nay anh xa truc tiep Chuong 1, 4, 6, 7 va CLO1-CLO4; quy mo phu hop voi
  bai tap nhom va co the trinh bay day du.
- He qua: notebook 01-04 hien tai va cac artifact nang cao duoc giu lam phu luc ky thuat,
  khong bi xoa hay coi la noi dung bat buoc tren slide.

## D-016: Pham vi DoE cua luong trinh bay chinh

- Trang thai: accepted.
- Quyet dinh: DoE chinh gom treatment/control, randomization 1:1, replication, blocking theo
  school, sample-size benchmark, Monte Carlo power va mo rong factorial 2x2 don gian.
- Ly do: day la cac noi dung cot loi cua Chuong 7. Attrition, noncompliance va causal
  estimators nang cao khong nam trong pham vi trinh bay chinh.
- He qua: treatment effect trong simulation phai duoc dat truoc theo y nghia thuc tien;
  khong dung association quan sat cua `famsup`, `studytime`, `higher` hay `failures` nhu causal
  effect.
