# PHÂN TÍCH THỐNG KÊ CÁC YẾU TỐ LIÊN QUAN ĐẾN KẾT QUẢ HỌC TẬP VÀ ĐỀ XUẤT QUY HOẠCH THỰC NGHIỆM HỖ TRỢ HỌC SINH

**Học phần:** IT2022E - Thống kê ứng dụng và Quy hoạch thực nghiệm  
**Giảng viên:** [Điền tên giảng viên]  
**Nhóm thực hiện:** [Điền tên nhóm]  
**Thành viên:** [Điền họ tên và mã số sinh viên]  
**Thời gian:** Tháng 6 năm 2026

---

## Tóm tắt

Nghiên cứu sử dụng bộ dữ liệu Student Performance của UCI để phân tích các yếu tố liên
quan đến điểm cuối kỳ môn Toán (`G3`) của 395 học sinh tại hai trường trung học ở Bồ Đào
Nha. Quy trình phân tích gồm chuẩn bị và mô tả dữ liệu, ước lượng khoảng tin cậy, kiểm định
giả thuyết, phân tích tương quan, hồi quy tuyến tính và đề xuất một quy hoạch thực nghiệm.

Điểm `G3` trung bình của mẫu là 10,415 trên thang 0-20, với khoảng tin cậy 95% từ 9,962
đến 10,868. Sau khi hiệu chỉnh Holm cho 10 giả thuyết chính, định hướng học đại học
(`higher`), số lần trượt môn trước đó (`failures`) và trình độ học vấn của cha mẹ (`Medu`,
`Fedu`) còn có ý nghĩa thống kê. Tuy nhiên, đây là dữ liệu quan sát nên các kết quả chỉ thể
hiện mối liên hệ, không chứng minh tác động nhân quả.

Hồi quy không sử dụng điểm quá trình `G1`, `G2` có khả năng giải thích và dự báo hạn chế.
Khi bổ sung `G1`, `G2`, hiệu năng dự báo tăng mạnh; trong đánh giá ngoài mẫu, hệ số xác
định tăng từ 0,087 lên 0,806. Kết quả này cho thấy điểm quá trình chứa nhiều thông tin về
điểm cuối kỳ, nhưng không thay thế được nhu cầu nhận diện sớm học sinh cần hỗ trợ.

Từ độ lệch chuẩn quan sát của `G3` là 4,581, nghiên cứu đề xuất thí nghiệm ngẫu nhiên đánh
giá chương trình ôn tập có hướng dẫn. Để phát hiện mức tăng 1,5 điểm với power 80% và mức
ý nghĩa 5%, cần xấp xỉ 296 học sinh. Mô phỏng Monte Carlo xác nhận power đạt khoảng 0,805
khi có 150 học sinh mỗi nhóm. Nghiên cứu kết thúc bằng thảo luận về sai số lấy mẫu, sai số
đo lường, selection bias, confounding và giới hạn khái quát hóa.

**Từ khóa:** thống kê ứng dụng, kiểm định giả thuyết, hồi quy tuyến tính, quy hoạch thực
nghiệm, Student Performance, kết quả học tập.

---

## 1. Giới thiệu

### 1.1. Bối cảnh

Kết quả học tập chịu ảnh hưởng đồng thời của đặc điểm cá nhân, hoàn cảnh gia đình, hành vi
học tập, môi trường nhà trường và nhiều yếu tố khó quan sát khác. Việc phân tích dữ liệu học
tập có thể giúp mô tả các nhóm học sinh, nhận diện những biến liên quan đến kết quả cuối kỳ
và xây dựng giả thuyết cho các chương trình hỗ trợ trong tương lai.

Tuy nhiên, phần lớn dữ liệu giáo dục có tính quan sát. Ví dụ, học sinh có định hướng học đại
học có thể đạt điểm cao hơn, nhưng chênh lệch đó có thể đồng thời liên quan đến năng lực ban
đầu, động lực, điều kiện gia đình hoặc các yếu tố chưa được đo. Vì vậy, phân tích thống kê
cần phân biệt rõ ba khái niệm: mối liên hệ trong dữ liệu, khả năng dự báo và tác động nhân
quả.

Project này áp dụng các nội dung chính của học phần IT2022E: thu thập và chuẩn bị dữ liệu,
thống kê mô tả, ước lượng, khoảng tin cậy, kiểm định giả thuyết, tương quan, hồi quy và quy
hoạch thực nghiệm. Python được sử dụng để bảo đảm quy trình có thể tái lập.

### 1.2. Mục tiêu nghiên cứu

Nghiên cứu có bốn mục tiêu:

1. Mô tả bộ dữ liệu và phân phối điểm cuối kỳ `G3`.
2. Đánh giá mối liên hệ giữa `G3` với một số đặc điểm cá nhân, gia đình và hành vi học tập.
3. So sánh khả năng giải thích và dự báo `G3` của mô hình không có và có điểm quá trình.
4. Đề xuất một quy hoạch thực nghiệm để đánh giá chương trình hỗ trợ học tập trong tương
   lai.

### 1.3. Câu hỏi nghiên cứu

Nghiên cứu trả lời các câu hỏi sau:

- Phân phối `G3` và đặc điểm của mẫu học sinh như thế nào?
- `G3` có khác biệt hoặc liên hệ với `higher`, `failures`, `studytime`, `Walc`, trình độ
  học vấn của cha mẹ và các biến nền khác hay không?
- Các biến nền và hành vi có đủ để dự báo sớm `G3` không? Việc bổ sung `G1`, `G2` thay đổi
  hiệu năng mô hình như thế nào?
- Một thí nghiệm đánh giá chương trình hỗ trợ học tập nên được tổ chức với treatment,
  randomization, replication, blocking và cỡ mẫu ra sao?

### 1.4. Phạm vi

Phân tích chỉ sử dụng dữ liệu môn Toán với 395 học sinh. Dataset môn Tiếng Bồ Đào Nha
không được ghép vào do có học sinh xuất hiện trong cả hai tập và cần một thiết kế liên kết
dữ liệu riêng. Kết quả không đại diện cho toàn bộ học sinh Bồ Đào Nha hoặc các hệ thống
giáo dục khác.

---

## 2. Dữ liệu và lý thuyết đo lường

### 2.1. Nguồn dữ liệu

Dữ liệu được lấy từ bộ Student Performance trên UCI Machine Learning Repository. Tệp sử
dụng là `student-mat.csv`, gồm 395 học sinh, 33 biến và không có giá trị thiếu. Mỗi dòng
biểu diễn một học sinh học môn Toán tại trường Gabriel Pereira (`GP`) hoặc Mousinho da
Silveira (`MS`).

| Thuộc tính | Giá trị |
|---|---:|
| Số quan sát | 395 |
| Số biến | 33 |
| Trường GP | 349 |
| Trường MS | 46 |
| Học sinh nữ | 208 |
| Học sinh nam | 187 |
| Biến kết quả | `G3` |
| Thang điểm `G3` | 0-20 |

### 2.2. Phân loại biến

Các biến được phân loại theo bản chất đo lường:

| Loại biến | Ví dụ | Cách diễn giải |
|---|---|---|
| Định danh | `school`, `sex`, `address`, `Mjob` | Các nhóm không có thứ tự |
| Nhị phân | `higher`, `famsup`, `internet` | Hai trạng thái yes/no hoặc hai nhóm |
| Thứ bậc | `studytime`, `Walc`, `health`, `famrel` | Các mức có thứ tự nhưng khoảng cách chưa chắc bằng nhau |
| Biến đếm | `absences`, `failures` | Số lần hoặc số ngày |
| Điểm số | `G1`, `G2`, `G3` | Điểm trên thang 0-20 |

Việc phân loại này ảnh hưởng đến lựa chọn phương pháp. Chẳng hạn, `studytime=4` không có
nghĩa là thời gian học gấp đôi `studytime=2`; đây là các khoảng thời gian đã được mã hóa.
Do đó, mô hình coi biến thứ bậc là số liên tục cần được diễn giải thận trọng.

### 2.3. Độ tin cậy và độ giá trị của phép đo

`G3` là điểm cuối kỳ và có giá trị trực tiếp đối với kết quả môn học. Tuy nhiên, một bài
thi đơn lẻ không phản ánh đầy đủ mọi khía cạnh của năng lực học tập. Điểm số còn chịu ảnh
hưởng của độ khó đề, điều kiện thi, cách chấm và trạng thái của học sinh tại thời điểm thi.

Các biến `studytime`, `Walc`, `Dalc`, `famrel` và `health` chủ yếu dựa trên tự báo cáo.
Chúng có thể chịu recall bias hoặc social desirability bias. Ví dụ, học sinh có thể báo cáo
mức uống rượu thấp hơn thực tế hoặc ước lượng không chính xác thời gian tự học.

Một số khái niệm phức tạp chỉ được đo bằng một biến ngắn. `famsup` chỉ cho biết có hay
không có hỗ trợ gia đình, không phản ánh tần suất, chất lượng hoặc hình thức hỗ trợ.
`famrel` dùng một thang 1-5 duy nhất, nên chưa đủ để đánh giá độ tin cậy nội tại bằng các
chỉ số như Cronbach's alpha. Vì dataset không có nhiều item cùng đo một cấu trúc tiềm ẩn,
nghiên cứu không thực hiện phân tích thang đo đa mục.

### 2.4. Quyết định chuẩn bị dữ liệu

- Không thay đổi dữ liệu trong `data/raw/`.
- Giữ 38 quan sát `G3=0`, tương ứng 9,62% mẫu, vì 0 thuộc thang điểm hợp lệ.
- Không loại hoặc winsorize `absences` trong phân tích chính.
- Các phân tích chỉ giữ `G3>0` hoặc biến đổi `absences` được xem là sensitivity analysis.
- Dùng `RANDOM_SEED=42` và mức ý nghĩa `ALPHA=0.05`.

![Tổng quan phân phối G3 và khác biệt theo trường](../figures/eda_course_overview.png)

**Hình 1.** Phân phối điểm cuối kỳ và boxplot `G3` theo trường.

---

## 3. Phương pháp nghiên cứu

### 3.1. Thống kê mô tả

Các biến số được mô tả bằng số quan sát, trung bình, độ lệch chuẩn, trung vị, tứ phân vị,
giá trị nhỏ nhất và lớn nhất. Các biến phân loại được mô tả bằng tần số và tỷ lệ. Histogram,
boxplot, scatterplot và heatmap được dùng để biểu diễn phân phối và mối liên hệ.

### 3.2. Khoảng tin cậy

Khoảng tin cậy 95% cho trung bình `G3` được tính theo phân bố t:

> **CI 95% = x̄ ± t(0,975; n − 1) × s/√n**

Trong đó, `x̄` là trung bình mẫu, `s` là độ lệch chuẩn mẫu và `n` là cỡ mẫu.

Đối với chênh lệch trung bình của hai nhóm có phương sai và cỡ mẫu khác nhau, nghiên cứu
dùng khoảng tin cậy Welch. Phân tích mở rộng còn sử dụng bootstrap percentile và BCa với
5.000 lần lặp để kiểm tra độ bền vững.

### 3.3. Kiểm định giả thuyết

Các phương pháp chính gồm:

- Welch t-test cho biến phân nhóm hai mức.
- Kruskal-Wallis cho biến thứ bậc có nhiều nhóm.
- Spearman correlation cho mối liên hệ thứ hạng.
- Dunn post-hoc sau Kruskal-Wallis trong phân tích mở rộng.

Mười giả thuyết chính được điều chỉnh bằng phương pháp Holm. Kết luận xác nhận dựa trên
`p_holm < 0.05`, không dựa riêng vào p-value thô. Effect size gồm Hedges' g,
epsilon-squared và Spearman rho tùy loại kiểm định.

Giả thuyết H9 về `absences` được hình thành sau EDA, vì vậy luôn được ghi nhận là giả
thuyết post-hoc/exploratory.

### 3.4. Tương quan và hồi quy

Hai mô hình hồi quy được xem xét:

**Model A - thông tin nền và hành vi:**

> **G3 = β₀ + β₁·failures + β₂·studytime + β₃·absences + β₄·school + β₅·sex + ε**

Mô hình này minh họa khả năng nhận diện sớm trước khi sử dụng điểm quá trình.

**Model B - bổ sung điểm quá trình:**

> **G3 = các thành phần của Model A + β₆·G1 + β₇·G2 + ε**

Mô hình được đánh giá bằng hệ số xác định, RMSE, residual plots và Q-Q plots. Phân tích
mở rộng sử dụng 5-fold cross-validation, out-of-fold predictions, HC3 standard errors,
Breusch-Pagan test, VIF và sensitivity analyses.

### 3.5. Quy hoạch thực nghiệm

Một thí nghiệm ngẫu nhiên được đề xuất để đánh giá chương trình ôn tập có hướng dẫn:

- Experimental unit: một học sinh.
- Treatment: tham gia chương trình ôn tập có hướng dẫn.
- Control: học theo chương trình thông thường.
- Response: `G3` trên thang 0-20.
- Randomization: phân bổ 1:1.
- Blocking: theo trường trước khi phân bổ.
- Primary hypothesis: chênh lệch trung bình giữa treatment và control bằng 0.
- Primary target effect: tăng 1,5 điểm `G3`.

Cỡ mẫu được tính cho kiểm định hai phía với alpha 5%, power 80% và độ lệch chuẩn hiệu
chỉnh từ dữ liệu quan sát. Monte Carlo simulation gồm 2.000 lần lặp cho từng tổ hợp cỡ mẫu
và effect.

### 3.6. Phần mềm

Phân tích được thực hiện bằng Python với pandas, NumPy, SciPy, statsmodels,
scikit-learn, matplotlib và seaborn. Notebook được chạy tuần tự và artifact được xuất vào
`data/processed/` và `report/figures/`.

---

## 4. Kết quả

### 4.1. Thống kê mô tả

`G3` có trung bình 10,415, trung vị 11 và độ lệch chuẩn 4,581. Điểm thấp nhất là 0 và cao
nhất là 20. Phân phối có một nhóm riêng tại 0, làm cho phân phối không hoàn toàn gần chuẩn.

| Thống kê | `G3` |
|---|---:|
| Số quan sát | 395 |
| Trung bình | 10,415 |
| Độ lệch chuẩn | 4,581 |
| Trung vị | 11 |
| Tứ phân vị thứ nhất | 8 |
| Tứ phân vị thứ ba | 14 |
| Nhỏ nhất | 0 |
| Lớn nhất | 20 |

Có 312 học sinh chưa từng trượt môn, trong khi 83 học sinh có ít nhất một lần trượt. Nhóm
`higher=yes` gồm 375 học sinh, còn `higher=no` chỉ có 20 học sinh. Sự mất cân bằng này làm
khoảng tin cậy của contrast `higher` rộng và hạn chế khả năng khái quát hóa kết quả cho
nhóm không có định hướng học đại học.

### 4.2. Khoảng tin cậy cho trung bình G3

Khoảng tin cậy t 95% cho trung bình `G3` là [9,962; 10,868]. Bootstrap percentile và BCa
cho kết quả rất gần, lần lượt khoảng [9,975; 10,858] và [9,965; 10,848]. Sự tương đồng giữa
các phương pháp cho thấy ước lượng trung bình toàn mẫu tương đối ổn định, dù phân phối có
điểm khối tại 0.

![Phân phối bootstrap của trung bình G3](../figures/ci_bootstrap_mean_g3.png)

**Hình 2.** Phân phối bootstrap của trung bình `G3`.

### 4.3. Kiểm định giả thuyết

Kết quả sau Holm correction được tóm tắt như sau:

| Giả thuyết | Kết quả chính | Effect size | `p_holm` | Kết luận |
|---|---:|---:|---:|---|
| H1: `sex` | M - F = 0,948 | g = 0,207 | 0,220 | Chưa đủ bằng chứng |
| H2: `address` | U - R = 1,163 | g = 0,254 | 0,220 | Chưa đủ bằng chứng |
| H3: `famsup` | yes - no = -0,368 | g = -0,080 | 0,880 | Chưa đủ bằng chứng |
| H4: `studytime` | Khác biệt omnibus | epsilon² = 0,012 | 0,220 | Chưa đủ bằng chứng |
| H5: `Walc` | rho = -0,104 | rho = -0,104 | 0,220 | Chưa đủ bằng chứng |
| H6: `higher` | yes - no = 3,808 | g = 0,843 | 0,0195 | Có ý nghĩa |
| H7: `failures` | Khác biệt omnibus | epsilon² = 0,128 | 1,73e-10 | Có ý nghĩa |
| H8a: `Medu` | Khác biệt omnibus | epsilon² = 0,052 | 0,000685 | Có ý nghĩa |
| H8b: `Fedu` | Khác biệt omnibus | epsilon² = 0,027 | 0,0379 | Có ý nghĩa |
| H9: `absences` | rho = 0,018 | rho = 0,018 | 0,880 | Không có bằng chứng; exploratory |

#### 4.3.1. Định hướng học đại học

Nhóm `higher=yes` có `G3` trung bình cao hơn nhóm `higher=no` 3,808 điểm. Khoảng tin cậy
Welch 95% là [1,509; 6,107] và Hedges' g bằng 0,843, tương ứng effect size lớn. Tuy nhiên,
nhóm `higher=no` chỉ có 20 học sinh. Kết quả có thể phản ánh sự khác biệt về động lực hoặc
năng lực nền, không phải tác động của việc trả lời “có” cho câu hỏi định hướng học đại học.

#### 4.3.2. Số lần trượt môn

Kruskal-Wallis cho `failures` đạt `H=53,115`, với p-value rất nhỏ. Effect size
epsilon-squared bằng 0,128. Dunn post-hoc cho thấy nhóm `failures=0` khác từng nhóm 1, 2
và 3 sau hiệu chỉnh Holm; không nên suy rộng rằng mọi cặp mức `failures` đều khác nhau.

![Điểm G3 theo số lần trượt môn](../figures/hyp_course_failures.png)

**Hình 3.** Phân phối `G3` theo số lần trượt môn trước đó.

#### 4.3.3. Trình độ học vấn của cha mẹ

`Medu` và `Fedu` có khác biệt omnibus sau Holm correction, nhưng effect size lần lượt chỉ
ở mức khoảng 0,052 và 0,027. Điều này cho thấy ý nghĩa thống kê không đồng nghĩa với chênh
lệch lớn về mặt thực tiễn. Trình độ học vấn của cha mẹ cũng có thể đại diện cho nhiều yếu
tố nền khác như điều kiện kinh tế, tài nguyên học tập hoặc kỳ vọng giáo dục.

#### 4.3.4. Walc và absences

Tương quan thô giữa `Walc` và `G3` là -0,104 với p-value 0,038, nhưng không còn ý nghĩa
sau Holm correction. `absences` có rho gần 0 trong mẫu đầy đủ. H9 về `absences` là kết quả
exploratory và không hỗ trợ kết luận rằng số ngày vắng có quan hệ đơn điệu rõ với `G3`.

### 4.4. Tương quan

Tương quan Spearman của `G1` và `G2` với `G3` lần lượt là 0,878 và 0,957. `failures` có
tương quan âm -0,361. `studytime` có tương quan dương nhỏ 0,105, còn `absences` gần 0.

![Heatmap tương quan các biến chính](../figures/reg_course_correlation.png)

**Hình 4.** Tương quan Spearman giữa các điểm số và biến học tập chính.

Tương quan rất cao giữa `G2` và `G3` là hợp lý vì hai điểm số được đo gần nhau trong cùng
môn học. Tuy nhiên, nó cũng có nghĩa rằng mô hình dùng `G2` chỉ khả dụng ở thời điểm muộn,
không phù hợp với mọi mục tiêu can thiệp sớm.

### 4.5. Hồi quy tuyến tính

#### 4.5.1. Kết quả in-sample của mô hình cốt lõi

| Mô hình | R² | Adjusted R² | RMSE in-sample |
|---|---:|---:|---:|
| Model A: không `G1/G2` | 0,155 | 0,144 | 4,206 |
| Model B: có `G1/G2` | 0,829 | 0,826 | 1,892 |

Trong Model A, mỗi mức tăng của `failures` liên quan đến giảm khoảng 2,195 điểm `G3`, khi
giữ các biến còn lại cố định. Khoảng tin cậy 95% là [-2,770; -1,620]. `studytime` có hệ số
dương 0,468 nhưng khoảng tin cậy chứa 0. Hệ số `absences` nhỏ và cũng chưa có bằng chứng
rõ trong mô hình cốt lõi này.

Trong Model B, hệ số của `G2` là 0,977 với khoảng tin cậy [0,880; 1,073]. Khi giữ các biến
khác cố định, tăng một điểm `G2` liên quan đến gần một điểm `G3` cao hơn. Hệ số `G1` là
0,146 với khoảng tin cậy [0,036; 0,257]. Sau khi thêm `G1/G2`, hệ số riêng của `failures`
giảm mạnh, cho thấy một phần mối liên hệ của `failures` với `G3` được chia sẻ với kết quả
học tập trước đó.

#### 4.5.2. Đánh giá ngoài mẫu

Kết quả 5-fold cross-validation trên toàn bộ out-of-fold predictions:

| Mô hình | RMSE | MAE | OOF R² |
|---|---:|---:|---:|
| Baseline mean | 4,585 | 3,435 | -0,004 |
| Model A | 4,373 | 3,405 | 0,087 |
| Model B | 2,017 | 1,353 | 0,806 |

Model A chỉ cải thiện nhẹ so với baseline, cho thấy các biến nền, hành vi và xã hội trong
đặc tả tuyến tính hiện tại chưa đủ để dự báo sớm chính xác. Model B cải thiện mạnh nhờ
`G1/G2`, nhưng đây là các predictors gần outcome.

![So sánh hiệu năng cross-validation](../figures/reg_cv_model_comparison.png)

**Hình 5.** So sánh hiệu năng dự báo ngoài mẫu của baseline, Model A và Model B.

#### 4.5.3. Diagnostics

Max VIF khoảng 6 cho cả hai mô hình, thể hiện mức cảnh báo nhưng chưa vượt ngưỡng nghiêm
trọng 10. Breusch-Pagan không có ý nghĩa ở Model A nhưng có ý nghĩa ở Model B; vì vậy phân
tích đầy đủ dùng HC3 standard errors.

Residual plots cho thấy một dải chéo liên quan đến nhóm `G3=0` và sai lệch ở hai đuôi.
OLS không mô tả hoàn hảo outcome bị giới hạn trong [0;20] và có point mass tại 0. Do đó,
diễn giải hệ số cần thận trọng; kết luận về dự báo ưu tiên OOF metrics.

![Residual diagnostics của hai mô hình](../figures/reg_course_diagnostics.png)

**Hình 6.** Residual-vs-fitted và Q-Q plots của Model A, Model B.

---

## 5. Quy hoạch thực nghiệm

### 5.1. Lý do cần thực nghiệm

Các phân tích trước chỉ sử dụng dữ liệu quan sát. Ngay cả khi `higher`, `failures` hoặc
trình độ học vấn của cha mẹ liên quan đến `G3`, không thể trực tiếp biến các chênh lệch đó
thành tác động can thiệp. Một thí nghiệm ngẫu nhiên cần treatment có thể triển khai và kiểm
soát được.

Nghiên cứu đề xuất chương trình ôn tập có hướng dẫn trước kỳ thi cuối kỳ. Chương trình có
thể gồm lịch ôn tập cố định, bài tập theo chủ đề và phản hồi từ người hướng dẫn. Mục tiêu là
đánh giá liệu việc được phân bổ vào chương trình có làm tăng `G3` trung bình hay không.

### 5.2. Thiết kế chính

| Thành phần | Định nghĩa |
|---|---|
| Experimental unit | Một học sinh |
| Factor | Chương trình ôn tập có hướng dẫn |
| Treatment levels | Có chương trình / học thông thường |
| Response | `G3` |
| Randomization | 1:1 trong từng trường |
| Blocking | `school` |
| Replication | Nhiều học sinh ở mỗi treatment arm |
| Primary estimand | Chênh lệch trung bình `G3` theo phân bổ treatment |
| Mức ý nghĩa | 0,05, hai phía |
| Power mục tiêu | 0,80 |

Blocking theo trường bảo đảm cả hai trường có đại diện ở treatment và control. Trong phạm
vi mỗi block, học sinh được phân bổ ngẫu nhiên để giảm confounding trung bình. Replication
giúp giảm standard error và tăng khả năng phát hiện effect thực tế.

### 5.3. Cỡ mẫu

Độ lệch chuẩn của `G3` trong dữ liệu quan sát là 4,581. Cỡ mẫu tham khảo cho các mức effect:

| Effect mục tiêu | Cohen d | Số học sinh mỗi nhóm | Tổng mẫu |
|---:|---:|---:|---:|
| 0,5 điểm | 0,109 | 1.319 | 2.638 |
| 1,0 điểm | 0,218 | 331 | 662 |
| 1,5 điểm | 0,327 | 148 | 296 |
| 2,0 điểm | 0,437 | 84 | 168 |

Effect 1,5 điểm được chọn làm kịch bản chính vì vừa có ý nghĩa thực tiễn, vừa tạo ra quy mô
mẫu có thể thảo luận trong bối cảnh một nghiên cứu nhiều lớp hoặc nhiều trường. Effect 0,5
điểm đòi hỏi mẫu rất lớn, cho thấy thí nghiệm nhỏ có thể bỏ sót những cải thiện nhỏ.

### 5.4. Kết quả mô phỏng power

Khi effect bằng 0, tỷ lệ bác bỏ giả thuyết không dao động khoảng 0,045-0,059, gần mức
alpha 0,05. Điều này cho thấy quy trình mô phỏng kiểm soát Type I error tương đối phù hợp.

Với effect 1,5 điểm:

| Số học sinh mỗi nhóm | Empirical power | Effect ước lượng trung bình |
|---:|---:|---:|
| 50 | 0,363 | 1,453 |
| 100 | 0,638 | 1,456 |
| 150 | 0,805 | 1,439 |
| 200 | 0,888 | 1,437 |
| 300 | 0,983 | 1,444 |
| 400 | 0,998 | 1,442 |

Kết quả tại 150 học sinh mỗi nhóm gần với phép tính lý thuyết 148 mỗi nhóm. Effect ước
lượng thấp hơn 1,5 một chút vì outcome mô phỏng được giới hạn trong thang 0-20, tạo ceiling
effect ở một số quan sát.

![Đường cong power mô phỏng](../figures/doe_power_curve.png)

**Hình 7.** Empirical power theo cỡ mẫu và treatment effect.

### 5.5. Mở rộng factorial 2x2

Thiết kế mở rộng sử dụng hai factor đều có thể randomize:

- Factor A: chương trình ôn tập có hướng dẫn (`guided_review`).
- Factor B: chương trình nhắc lịch và hỗ trợ duy trì kế hoạch học (`study_reminders`).

Bốn treatment combinations gồm: không có chương trình, chỉ guided review, chỉ study
reminders và có cả hai. Mô hình:

> **G3 = β₀ + βA·A + βB·B + βAB·(A×B) + ε**

Trong đó, `A×B` là thành phần tương tác giữa hai can thiệp.

Trong một lần mô phỏng với 80 học sinh mỗi cell, hệ số guided review ước lượng là 2,386 và
có ý nghĩa thống kê. Hệ số study reminders là 1,140, còn interaction là -1,715; hai hệ số
sau không đạt mức ý nghĩa 5% trong lần mô phỏng này. Các con số riêng của một simulation
không phải bằng chứng thực nghiệm. Ý nghĩa của phần này là minh họa cách một factorial
design ước lượng đồng thời main effects và interaction.

### 5.6. Giới hạn của thiết kế đề xuất

- Chương trình treatment mới ở mức khái niệm, cần protocol triển khai cụ thể.
- Độ lệch chuẩn từ dữ liệu UCI có thể không phù hợp hoàn toàn với quần thể triển khai mới.
- Điểm `G3` bị giới hạn và có thể có floor/ceiling effects.
- Blocking chỉ theo trường chưa chắc kiểm soát mọi nguồn biến thiên quan trọng.
- Noncompliance, contamination và attrition chưa được đưa vào mô hình cốt lõi.
- Cần xác định trước tiêu chí loại trừ, cách xử lý missing outcome và kế hoạch phân tích.

---

## 6. Sai số và hạn chế

### 6.1. Sai số lấy mẫu

Mẫu chỉ có 395 học sinh. Các ước lượng thay đổi nếu lấy một mẫu khác từ cùng quần thể.
Khoảng tin cậy biểu diễn một phần độ bất định này. Những nhóm nhỏ như `higher=no` có
standard error lớn và khoảng tin cậy rộng hơn.

### 6.2. Selection bias và khả năng khái quát hóa

Dữ liệu chỉ gồm hai trường. Việc học sinh xuất hiện trong dataset không phải kết quả của
một mẫu ngẫu nhiên toàn quốc. Trường `MS` chỉ có 46 học sinh. Model A có OOF R² âm khi
đánh giá riêng trên nhóm này, cho thấy hiệu năng có thể khác đáng kể giữa các trường.

Do đó, kết quả không nên được khái quát trực tiếp sang trường, quốc gia hoặc thời kỳ khác.
Random cross-validation trong cùng dataset cũng không chứng minh khả năng tổng quát hóa
sang một trường hoàn toàn mới.

### 6.3. Sai số đo lường

Các biến tự báo cáo có thể sai lệch. Sai số ngẫu nhiên thường làm mối liên hệ yếu đi, trong
khi sai số có hệ thống có thể tạo hoặc che giấu association. Việc mã hóa nhiều khái niệm
phức tạp thành thang 1-5 cũng làm mất thông tin.

`G3` có thể chịu ảnh hưởng của sai số chấm điểm hoặc khác biệt đề thi. Nếu treatment trong
thí nghiệm ảnh hưởng đến cách chấm hoặc khả năng tham dự kỳ thi, outcome còn có nguy cơ
measurement bias hoặc missing-not-at-random.

### 6.4. Confounding

Năng lực ban đầu, động lực, thu nhập gia đình, chất lượng giáo viên và môi trường học tập
có thể cùng liên quan đến predictors và `G3`. Hồi quy chỉ điều chỉnh cho các biến đã quan
sát và đưa vào mô hình. Không có causal DAG và không có bảo đảm đã kiểm soát đầy đủ
confounding, mediator hoặc collider.

### 6.5. Sai số mô hình

OLS giả định mối liên hệ tuyến tính và residual có cấu trúc phù hợp. Outcome `G3` bị giới
hạn 0-20 và có nhiều giá trị 0, nên mô hình tuyến tính không mô tả hoàn hảo phân phối.
Heteroscedasticity xuất hiện rõ trong Model B. HC3 giúp standard error bền vững hơn nhưng
không sửa được model misspecification.

### 6.6. Multiple testing và phân tích exploratory

Thực hiện nhiều kiểm định làm tăng xác suất có ít nhất một kết quả dương tính giả. Holm
correction được sử dụng cho 10 giả thuyết chính. H9 được đặt ra sau khi xem EDA nên chỉ có
vai trò exploratory. Các p-value hệ số riêng lẻ trong hồi quy cũng không nên được dùng để
chọn biến hoặc tạo câu chuyện nhân quả sau khi xem dữ liệu.

### 6.7. Sai số thực nghiệm

Trong thí nghiệm đề xuất, biến thiên cá nhân, độ tuân thủ treatment, contamination giữa
các nhóm, attrition và sai số chấm điểm đều có thể làm tăng experimental error. Randomization
giảm confounding trung bình nhưng không bảo đảm hai nhóm cân bằng hoàn hảo trong một mẫu
nhỏ. Replication, blocking và protocol chuẩn hóa cần được dùng để kiểm soát các nguồn sai
số này.

---

## 7. Thảo luận

Kết quả nổi bật nhất của dữ liệu quan sát là mối liên hệ giữa `failures`, định hướng học
đại học và điểm cuối kỳ. Trong đó, `failures` có effect size omnibus lớn nhất trong các
biến được kiểm định. Tuy nhiên, số lần trượt môn vừa có thể phản ánh năng lực học tập trước
đó, vừa có thể chịu ảnh hưởng của động lực, hoàn cảnh và chính sách nhà trường. Vì vậy,
`failures` phù hợp như một dấu hiệu nhận diện rủi ro hơn là một nguyên nhân can thiệp trực
tiếp.

`higher=yes` có chênh lệch lớn nhưng nhóm đối chứng quan sát rất nhỏ. Biến này có thể phản
ánh aspiration hoặc động lực học tập, song cũng có khả năng là kết quả của thành tích trước
đó. Một chương trình thực tế không thể đơn giản “gán” định hướng học đại học và kỳ vọng thu
được effect 3,808 điểm.

Model A cho thấy dữ liệu nền và hành vi hiện có chỉ hỗ trợ dự báo sớm ở mức hạn chế. Điều
này có thể do thiếu các biến quan trọng, sai số đo lường hoặc quan hệ phi tuyến. Model B đạt
hiệu năng cao nhờ `G1/G2`, đặc biệt là `G2`. Đây là kết quả hữu ích cho việc dự báo gần kỳ
thi, nhưng thời điểm nhận diện có thể quá muộn cho một số can thiệp dài hạn.

Sự khác biệt giữa phân tích quan sát và quy hoạch thực nghiệm là trọng tâm của nghiên cứu.
Phân tích quan sát tạo bằng chứng về association và giúp xác định nhóm hoặc vấn đề đáng
quan tâm. Thí nghiệm ngẫu nhiên mới là thiết kế phù hợp để đánh giá tác động của một chương
trình hỗ trợ cụ thể. Effect trong tính cỡ mẫu phải dựa trên mức cải thiện có ý nghĩa thực
tiễn, không sao chép từ chênh lệch giữa các nhóm quan sát.

Việc báo cáo effect size, khoảng tin cậy, kết quả ngoài mẫu và sensitivity analysis giúp
tránh phụ thuộc hoàn toàn vào p-value. Một kết quả có ý nghĩa thống kê nhưng effect nhỏ có
thể không đủ quan trọng trong thực tế. Ngược lại, một effect thực tiễn đáng quan tâm có thể
không đạt ý nghĩa do mẫu quá nhỏ.

---

## 8. Kết luận

Nghiên cứu đã áp dụng một quy trình thống kê từ chuẩn bị dữ liệu đến thiết kế thực nghiệm.
Các câu hỏi nghiên cứu được trả lời như sau:

1. Mẫu gồm 395 học sinh với `G3` trung bình 10,415 và khoảng tin cậy 95%
   [9,962; 10,868]. Phân phối có 9,62% giá trị bằng 0.
2. Sau Holm correction, `higher`, `failures`, `Medu` và `Fedu` còn có ý nghĩa thống kê.
   Các kết quả này là association trong dữ liệu quan sát.
3. Mô hình không có `G1/G2` dự báo sớm còn hạn chế. Bổ sung điểm quá trình làm OOF R²
   tăng từ 0,087 lên 0,806, với `G2` là predictor nổi bật nhất.
4. Một thí nghiệm ngẫu nhiên 1:1, blocking theo trường, cần khoảng 296 học sinh để phát
   hiện effect 1,5 điểm với power 80% theo giả định hiện tại.

Đóng góp chính của project không phải là khẳng định một nguyên nhân duy nhất của thành
tích học tập, mà là minh họa cách kết hợp thống kê mô tả, suy luận, hồi quy, đánh giá sai số
và quy hoạch thực nghiệm trong một quy trình có thể tái lập.

Hướng phát triển tiếp theo gồm thử nghiệm mô hình phù hợp hơn với outcome bị giới hạn,
thu thập dữ liệu từ nhiều trường, cải thiện thang đo hành vi và triển khai pilot study để
ước lượng thực tế hơn về phương sai, compliance và attrition.

---

## 9. Tài liệu tham khảo

1. Cortez, P., & Silva, A. M. G. (2008). *Using Data Mining to Predict Secondary School
   Student Performance*. Proceedings of FUture Business TEChnology Conference.
2. UCI Machine Learning Repository. *Student Performance Dataset*.
   <https://archive.ics.uci.edu/dataset/320/student+performance>
3. Walpole, R. E., Myers, R. H., Myers, S. L., & Ye, K. *Probability and Statistics for
   Engineers and Scientists*, 8th edition. Pearson, 2007.
4. Trosset, M. W. *An Introduction to Statistical Inference and Data Analysis with R*.
   CRC Press, 2009.
5. Mason, R. L., Gunst, R. F., & Hess, J. L. *Statistical Design and Analysis of
   Experiments*.
6. Slide bài giảng học phần IT2022E - Thống kê ứng dụng và Quy hoạch thực nghiệm.

---

## Phụ lục A. Hệ thống notebook và khả năng tái lập

Luồng trình bày chính:

1. `notebooks/core/01_data_preparation_and_eda.ipynb`
2. `notebooks/core/02_statistical_inference.ipynb`
3. `notebooks/core/03_correlation_and_regression.ipynb`
4. `notebooks/core/05_experimental_design.ipynb`

Phân tích kỹ thuật mở rộng:

1. `notebooks/01_EDA.ipynb`
2. `notebooks/02_hypothesis_testing.ipynb`
3. `notebooks/03_confidence_intervals.ipynb`
4. `notebooks/04_regression.ipynb`

Các notebook core đã được chạy đầy đủ, không có output lỗi và không chứa đường dẫn máy cá
nhân. Dữ liệu raw không bị thay đổi. Các bảng được xuất vào `data/processed/`, còn hình
được xuất vào `report/figures/`.

## Phụ lục B. Phân tích độ nhạy chính

- Giữ `G3=0` là phân tích chính; chỉ xét `G3>0` làm sensitivity analysis.
- Giữ `absences` gốc; `log1p(absences)` chỉ dùng để kiểm tra độ nhạy.
- Mã hóa ordinal dạng categorical làm Model A kém ổn định hơn trong mẫu nhỏ.
- Model B có heteroscedasticity; inference mở rộng sử dụng HC3.
- Prediction clipping vào [0;20] chỉ là sensitivity, không thay estimator chính.
- Random cross-validation đánh giá học sinh mới trong cấu trúc hai trường hiện tại, không
  đánh giá trực tiếp khả năng tổng quát hóa sang trường mới.

## Phụ lục C. Việc cần hoàn thiện trước khi nộp

- Điền thông tin giảng viên, nhóm và thành viên ở trang đầu.
- Thống nhất quy định định dạng, font chữ, giãn dòng và cách đánh số hình/bảng.
- Kiểm tra yêu cầu trích dẫn của giảng viên và hoàn thiện thông tin xuất bản tài liệu.
- Chuyển Markdown sang định dạng báo cáo cuối và kiểm tra ngắt trang.
- Review chéo mọi số liệu với CSV và notebook trước khi xuất PDF.
