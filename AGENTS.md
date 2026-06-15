# AGENTS.md

## Muc dich

Tai lieu nay la diem bat dau cho thanh vien moi va cac coding agent lam viec trong repo.
Doc theo thu tu:

1. [Onboarding](.docs/ONBOARDING.md)
2. [Trang thai du an](.docs/PROJECT_STATUS.md)
3. [Quyet dinh quan trong](.docs/DECISIONS.md)
4. [Ket qua phan tich hien tai](.docs/ANALYSIS_RESULTS.md)
5. [Dinh huong tiep theo](.docs/ROADMAP.md)

README cung cap boi canh nghien cuu, nhung bang tien do trong README dang cham hon hien
trang repo. Khi co mau thuan, uu tien `.docs/PROJECT_STATUS.md` va kiem tra artifact thuc te.

## Tong quan nhanh

- Muc tieu: phan tich cac yeu to lien quan den diem cuoi ky `G3` trong UCI Student
  Performance, mon Toan, `n=395`.
- Stack: Python, pandas, NumPy, SciPy, statsmodels, scikit-learn, matplotlib,
  seaborn, Jupyter.
- Luong trinh bay chinh: data/EDA -> statistical inference -> correlation/regression -> DoE.
- Notebook phan tich day du 01-04 duoc giu nhu phu luc ky thuat.
- Chua co: measurement theory va bao cao cuoi.
- Working tree hien co nhieu thay doi chua commit. Khong duoc reset, checkout hay ghi de
  cac thay doi khong lien quan.

## Quy tac lam viec

- Khong sua `data/raw/`. File goc la nguon bat bien.
- Chay notebook core theo thu tu `01`, `02`, `03`, `04`; cac phase sau dung
  `data/processed/student_mat_clean.csv`.
- Lam viec tu thu muc chua notebook khi chay, vi code dung duong dan tuong doi.
- Dung `RANDOM_SEED = 42`, `ALPHA = 0.05`; bootstrap hien dung 5.000 lan lap.
- Giu `G3=0` trong phan tich chinh. Neu loai, chi bao cao nhu sensitivity analysis.
- Khong xoa/winsorize `absences` trong dataset chinh; chi dung bien the de kiem tra do nhay.
- Voi nhieu kiem dinh, ket luan dua tren Holm-adjusted p-value, khong dua tren p-value tho.
- Luon bao cao effect size va confidence interval khi co the; khong dong nhat y nghia
  thong ke voi y nghia thuc tien hay quan he nhan qua.
- H9 (`absences` va `G3`) la gia thuyet post-hoc/exploratory va phai luon duoc gan nhan nhu vay.
- Figure moi vao `report/figures/` voi prefix phase: `eda_`, `hyp_`, `ci_`, `reg_`, `doe_`.
- Output dang bang vao `data/processed/`; ten file phai mo ta ro noi dung.
- Truoc khi ban giao: Restart/Run All, khong con cell loi, khong co duong dan tuyet doi,
  cap nhat `.docs/PROJECT_STATUS.md` va `.docs/ROADMAP.md`.

## Lenh thuong dung

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook
```

Chay lai notebook khong can giao dien, tu root repo:

```powershell
python scripts/run_notebook_cells.py notebooks/01_EDA.ipynb
python scripts/run_notebook_cells.py notebooks/02_hypothesis_testing.ipynb
python scripts/run_notebook_cells.py notebooks/03_confidence_intervals.ipynb
python scripts/run_notebook_cells.py notebooks/04_regression.ipynb
```

Luong trinh bay chinh theo de cuong:

```powershell
python scripts/run_notebook_cells.py notebooks/core/01_data_preparation_and_eda.ipynb
python scripts/run_notebook_cells.py notebooks/core/02_statistical_inference.ipynb
python scripts/run_notebook_cells.py notebooks/core/03_correlation_and_regression.ipynb
python scripts/run_notebook_cells.py notebooks/core/05_experimental_design.ipynb
```

`scripts/rebuild_notebooks.py` tai tao notebook 01-03 tu ma nguon trong script va co the
ghi de noi dung notebook. Chi dung khi chu dich dong bo notebook voi generator.

## Definition of done

- Notebook chay het, khong co output `error`.
- Artifact CSV/PNG duoc tao lai va khop voi ket luan viet trong notebook/bao cao.
- Quyet dinh phan tich moi duoc ghi vao `.docs/DECISIONS.md`.
- Trang thai va viec tiep theo duoc cap nhat trong `.docs/PROJECT_STATUS.md` va
  `.docs/ROADMAP.md`.
- `git diff` chi gom thay doi co chu dich; khong commit `venv/` hay cache Jupyter.
