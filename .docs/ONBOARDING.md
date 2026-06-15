# Onboarding

## Doc trong 20 phut dau

1. Doc `README.md` de nam muc tieu nghien cuu va data dictionary.
2. Doc `AGENTS.md` de nam quy tac thao tac trong repo.
3. Doc `PROJECT_STATUS.md` va `ANALYSIS_RESULTS.md` de biet phan nao da lam xong.
4. Doc `DECISIONS.md` truoc khi thay doi cach lam sach du lieu hay phuong phap thong ke.
5. Chon mot dau viec chua hoan thanh trong `ROADMAP.md`.

## Setup

Yeu cau Python 3.10+ va pip.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
jupyter notebook
```

Mo notebook tu root repo, nhung luu y code trong notebook ky vong working directory la
`notebooks/`. Jupyter mo notebook theo cach thong thuong dap ung dieu nay.

## Cau truc dang tin cay

```text
data/raw/                       du lieu nguon, read-only
data/processed/                 dataset sach va bang ket qua
notebooks/01_EDA.ipynb          Phase 1
notebooks/02_hypothesis_testing.ipynb
notebooks/03_confidence_intervals.ipynb
notebooks/04_regression.ipynb       Phase 4
notebooks/core/                     luong trinh bay chinh theo de cuong
notebooks/appendix/README.md         huong dan dung phu luc ky thuat
report/figures/                 figure da export
scripts/run_notebook_cells.py   runner khong giao dien
scripts/rebuild_notebooks.py    generator co kha nang ghi de notebook 01-03
scripts/build_notebook_04.py    generator rieng cho notebook 04
```

Bon notebook trong `notebooks/core/` la luong dung de trinh bay va bao cao. Cac notebook
01-04 o thu muc `notebooks/` la phan tich day du, dung nhu phu luc ky thuat. Thu muc hien co
ten `utlis/` va dang rong; khong nen xay dung phu thuoc vao no truoc khi thong nhat viec doi
thanh `utils/`.

## Kiem tra truoc khi sua

```powershell
git status --short
git diff --stat
```

Repo hien co thay doi chua commit, bao gom notebook 01-03, CSV ket qua va figure. Khong
duoc dung lenh lam mat thay doi. Neu sua notebook, xem ca source cell, output va artifact
duoc tao lai.

## Kiem tra truoc khi ban giao

1. Chay notebook lien quan tu dau den cuoi.
2. Xac nhan khong co cell loi va output khong chua duong dan may ca nhan.
3. Doi chieu CSV trong `data/processed/` voi ket luan trong notebook.
4. Kiem tra figure moi da duoc export dung prefix.
5. Cap nhat tai lieu tien do/quyet dinh neu pham vi thay doi.
