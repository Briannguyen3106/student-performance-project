# Phan tich thong ke ket qua hoc tap cua hoc sinh

> Hoc phan IT2022E: Thong ke ung dung va Quy hoach thuc nghiem
> Dataset: UCI Student Performance, mon Toan, `n=395`

## Muc tieu

Project minh hoa mot quy trinh thong ke ung dung hoan chinh:

1. Thu thap, chuan bi va mo ta du lieu.
2. Uoc luong tham so, khoang tin cay va kiem dinh gia thuyet.
3. Phan tich tuong quan va hoi quy tuyen tinh.
4. De xuat va mo phong mot quy hoach thuc nghiem.
5. Thao luan sai so, gioi han do luong va kha nang khai quat hoa.

Du lieu UCI la du lieu quan sat. Vi vay cac ket qua tu notebook 01-03 mo ta **moi lien
he**, khong duoc trinh bay nhu tac dong nhan qua. Notebook 04 de xuat mot thuc nghiem
ngau nhien de minh hoa cach kiem tra cau hoi nhan qua.

## Cau truc phu hop de cuong

### Luong trinh bay chinh

| Notebook | Noi dung hoc phan |
|---|---|
| `notebooks/core/01_data_preparation_and_eda.ipynb` | Chuong 1, 6: thu thap, chuan bi, mo ta du lieu |
| `notebooks/core/02_statistical_inference.ipynb` | Chuong 4: uoc luong, CI, kiem dinh |
| `notebooks/core/03_correlation_and_regression.ipynb` | Chuong 4.6: tuong quan va hoi quy |
| `notebooks/core/05_experimental_design.ipynb` | Chuong 7: randomization, replication, blocking, factorial design |

### Phu luc phan tich mo rong

Các notebook `notebooks/01_EDA.ipynb` đến `notebooks/04_regression.ipynb` chứa phiên bản
đầy đủ hơn: Holm correction, Dunn post-hoc, bootstrap, cross-validation, robust inference
và sensitivity analysis. Chúng được giữ để kiểm tra độ tin cậy, nhưng không phải toàn bộ
nội dung bắt buộc khi trình bày.

## Cau hoi nghien cuu

1. Phan phoi diem cuoi ky `G3` va dac diem mau nhu the nao?
2. `G3` co lien he voi dinh huong hoc dai hoc, so lan truot mon va mot so hanh vi hoc tap
   hay khong?
3. Cac bien nen va diem qua trinh giai thich `G3` den muc nao trong mo hinh tuyen tinh?
4. Can thiet ke thuc nghiem ra sao de danh gia mot chuong trinh ho tro hoc tap?

## Du lieu

- Nguon: UCI Student Performance.
- File goc: `data/raw/student-mat.csv`.
- Don vi quan sat: mot hoc sinh mon Toan.
- Bien ket qua: `G3`, thang diem 0-20.
- `data/raw/` la read-only; output duoc ghi vao `data/processed/`.

## Cai dat

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Chay notebook

Tu root repo:

```powershell
python scripts/run_notebook_cells.py notebooks/core/01_data_preparation_and_eda.ipynb
python scripts/run_notebook_cells.py notebooks/core/02_statistical_inference.ipynb
python scripts/run_notebook_cells.py notebooks/core/03_correlation_and_regression.ipynb
python scripts/run_notebook_cells.py notebooks/core/05_experimental_design.ipynb
```

Notebook ky vong working directory la thu muc chua notebook. Script runner tu dong dap ung
dieu nay.

## Nguyen tac phan tich

- `RANDOM_SEED = 42`, `ALPHA = 0.05`.
- Giu `G3=0` trong phan tich chinh.
- Khong xoa hoac winsorize `absences` trong dataset chinh.
- Bao cao effect size va confidence interval khi phu hop.
- Phan biet y nghia thong ke, y nghia thuc tien va quan he nhan qua.
- Effect trong mo phong DoE duoc dat truoc theo y nghia thuc tien, khong sao chep tu
  chenh lech quan sat.

## Ket qua tong quan

- Mean `G3`: 10,415; 95% t-CI: [9,962; 10,868].
- `failures` va `higher` co lien he dang chu y voi `G3`, nhung khong chung minh nhan qua.
- Hoi quy khong dung `G1/G2` co kha nang du bao han che; them `G1/G2` cai thien manh.
- Voi SD `G3` khoang 4,58, thuc nghiem nham phat hien effect nho can co mau lon.

Chi tiet ket qua hien tai nam trong `.docs/ANALYSIS_RESULTS.md`.
