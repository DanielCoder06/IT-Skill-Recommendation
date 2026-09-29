# Experimental NER Skill Extraction

# 1. Mục đích

Thư mục này chứa **thử nghiệm NER (Named Entity Recognition)** nhằm đánh giá khả năng sử dụng mô hình NER để hỗ trợ trích xuất kỹ năng từ CV.

NER được xây dựng như một **thành phần bổ sung** cho SkillMatcher hiện tại, không thay thế phương pháp dictionary-based.

Nguyên tắc thiết kế:

```text
SkillMatcher / Dictionary
        ↓
   Kỹ năng xác nhận
        ↓
      NER
        ↓
 Kỹ năng gợi ý thêm
        ↓
 Người dùng xác nhận
```

## Nguyên tắc ưu tiên

Project ưu tiên:

> **Thà không nhận diện được một skill còn hơn nhận diện sai skill.**

Do đó, precision và tính đáng tin cậy được ưu tiên hơn việc cố gắng tăng recall bằng cách suy diễn thêm kỹ năng.

---

# 2. Kiến trúc thử nghiệm

Pipeline thử nghiệm:

```text
CV PDF / TXT / DOCX
        │
        ▼
   Text Extraction
        │
        ▼
   SkillMatcher
   Dictionary-based
        │
        ├──────────────► Confirmed Skills
        │
        ▼
      NER Model
        │
        ▼
 Suggested Skills
        │
        ▼
 Normalization
        │
        ▼
 User Confirmation
```

Trong đó:

- **SkillMatcher** là nguồn xác nhận kỹ năng chính.
- **NER** chỉ đóng vai trò phát hiện các skill có khả năng bị bỏ sót.
- NER không tự động thay đổi kết quả `Match Rate`.
- Skill được NER phát hiện phải được chuẩn hóa và xác nhận trước khi có thể đưa vào hồ sơ kỹ năng.

---

# 3. Dataset

Nguồn dữ liệu CV được sử dụng trong experiment gồm **5.029 CV**.

Dữ liệu được xử lý bằng `auto_label.py`.

## Kết quả tiền xử lý

```text
Found 5029 CV files.

CV có skill:       4430
CV invalid/skipped: 81
CV không có skill:  518
```

Sau khi loại bỏ các CV trùng hoàn toàn về nội dung:

```text
Before deduplication: 4430
After deduplication:  2886
Duplicates removed:   1544
```

Tỷ lệ chia dữ liệu:

```text
Train: 2453 CV
Dev:    216 CV
Test:   217 CV

Total unique CV: 2886
Total SKILL entities: 10292
```

Random seed được cố định ở `42` để đảm bảo khả năng tái lập kết quả.

---

# 4. Tạo nhãn tự động

File:

```text
experiments/ner/auto_label.py
```

Nhãn `SKILL` được tạo tự động bằng `SkillMatcher`.

Điều này có nghĩa là dữ liệu huấn luyện NER được tạo từ dictionary/skill matching hiện tại thay vì sử dụng trực tiếp toàn bộ nhãn gốc của dataset CV.

Lý do là quá trình kiểm tra dữ liệu gốc cho thấy nhãn SKILL có nhiều trường hợp không phù hợp với mục tiêu của project.

Ví dụ một số span bị gán nhãn SKILL nhưng không thực sự thể hiện kỹ năng kỹ thuật rõ ràng.

Do đó experiment sử dụng:

```text
CV Text
   ↓
Skill Dictionary
   ↓
SkillMatcher
   ↓
Pseudo Labels
   ↓
NER Training Data
```

---

# 5. Loại bỏ dữ liệu trùng lặp

Các CV có nội dung hoàn toàn giống nhau được loại bỏ trước khi chia train/dev/test.

Mục đích:

- tránh cùng một CV xuất hiện ở nhiều tập;
- hạn chế data leakage;
- giúp kết quả đánh giá có ý nghĩa hơn.

Kiểm tra overlap được thực hiện bằng:

```text
experiments/ner/check_split_overlap.py
```

Kết quả:

```text
Train documents: 2453
Dev documents:    216
Test documents:   217

Train ∩ Dev:  0
Train ∩ Test: 0
Dev ∩ Test:   0
```

Không phát hiện document trùng giữa ba tập.

---

# 6. Chuyển dữ liệu sang spaCy

File:

```text
experiments/ner/to_spacy.py
```

Dữ liệu JSONL được chuyển sang định dạng `.spacy` để sử dụng trong quá trình training.

Pipeline xử lý:

```text
JSONL
  ↓
spaCy Doc
  ↓
Character Span
  ↓
Token Alignment
  ↓
Whitespace Validation
  ↓
.spacy
```

Kết quả kiểm tra:

```text
Train:
Source entities:       8770
Whitespace adjusted:      0
Invalid after alignment:  8
Alignment skipped:      254

Dev:
Source entities:         729
Whitespace adjusted:       0
Invalid after alignment:  0
Alignment skipped:       21

Test:
Source entities:         793
Whitespace adjusted:       0
Invalid after alignment:  0
Alignment skipped:       25
```

Các span không thể align với token của spaCy được bỏ qua.

---

# 7. Kiểm tra dữ liệu bằng spaCy

Lệnh kiểm tra:

```powershell
python -m spacy debug data experiments\ner\config.cfg `
  --paths.train experiments\ner\data\train.spacy `
  --paths.dev experiments\ner\data\dev.spacy
```

Kết quả:

```text
Pipeline can be initialized with data
Corpus is loadable

Language: en
Training pipeline: tok2vec, ner

2367 training docs
211 evaluation docs

No overlap between training and evaluation data

1776332 total words
105732 unique

No word vectors present

1 label
0 missing value(s)

Good amount of examples for all labels
Examples without occurrences available for all labels

No entities consisting of or starting/ending with whitespace
No entities crossing sentence boundaries

7 checks passed
```

Kết quả cho thấy dữ liệu có thể được sử dụng để huấn luyện pipeline NER.

---

# 8. Cấu hình NER

File cấu hình:

```text
experiments/ner/config.cfg
```

Pipeline sử dụng:

```text
tok2vec
ner
```

Mô hình được huấn luyện bằng spaCy.

Training được thực hiện với:

```text
max_steps = 2000
eval_frequency = 200
```

Lệnh:

```powershell
python -m spacy train experiments\ner\config.cfg `
  --output experiments\ner\models\skill_ner_v1 `
  --paths.train experiments\ner\data\train.spacy `
  --paths.dev experiments\ner\data\dev.spacy `
  --training.max_steps 2000 `
  --training.eval_frequency 200
```

---

# 9. Kết quả training

Kết quả training:

```text
Step    Precision    Recall    F1
------------------------------------
200      91.05%      78.00%   84.02%
400      88.38%      85.82%   87.08%
600      95.03%      88.57%   91.69%
800      97.32%      89.29%   93.13%
1000     97.26%      92.47%   94.81%
1200     93.52%      93.92%   93.72%
1400     96.57%      93.78%   95.15%
1600     96.04%      94.79%   95.41%
1800     96.08%      92.19%   94.09%
2000     97.86%      92.62%   95.17%
```

F1 cao nhất được ghi nhận trong quá trình training:

```text
F1 = 95.41%
Step = 1600
```

Model tốt nhất được lưu tại:

```text
experiments/ner/models/skill_ner_v1/model-best/
```

Model cuối cùng:

```text
experiments/ner/models/skill_ner_v1/model-last/
```

Trong các bước đánh giá tiếp theo, experiment sử dụng:

```text
model-best
```

---

# 10. Kiểm tra trên các câu chưa xuất hiện trong training

File:

```text
experiments/ner/test_ner_v1.py
```

Một số trường hợp kiểm tra:

### English

```text
I have experience with Python and SQL.
→ Python, SQL
```

```text
Developed REST APIs using Python and FastAPI.
→ REST, Python
```

```text
Worked on machine learning models using Pandas and Scikit-learn.
→ machine learning, Pandas
```

```text
Built deep learning models with PyTorch.
→ deep learning, PyTorch
```

### Không chứa skill

```text
I worked closely with the development team to complete projects.
→ []
```

```text
I analyzed business requirements and prepared technical documents.
→ []
```

### Vietnamese

```text
Có kinh nghiệm lập trình Python và làm việc với cơ sở dữ liệu SQL.
→ Python, SQL
```

```text
Đã thực hiện các dự án học máy và xử lý dữ liệu bằng Pandas.
→ Pandas
```

```text
Interested in data analysis and artificial intelligence.
→ artificial intelligence
```

Kết quả cho thấy mô hình có khả năng nhận diện một số skill kỹ thuật và không nhận diện các câu không chứa skill trong các trường hợp kiểm tra thủ công.

Tuy nhiên, vẫn tồn tại các trường hợp bỏ sót:

```text
FastAPI
Scikit-learn
học máy
```

Ngoài ra, có trường hợp NER nhận diện span một phần:

```text
REST
```

thay vì:

```text
REST API
```

---

# 11. Kiểm tra mô hình Hybrid

File:

```text
experiments/ner/test_hybrid_v1.py
```

Mục tiêu của thử nghiệm:

```text
SkillMatcher
      +
     NER
      ↓
Hybrid Skill Extraction
```

Trong đó:

```text
SkillMatcher → skill xác nhận
NER          → skill gợi ý
```

Kết quả trên 10 trường hợp kiểm tra:

```text
CASE 1
Confirmed: Python, SQL
NER: Python, SQL

CASE 2
Confirmed: Python, REST API
NER: REST, Python

CASE 3
Confirmed: Machine Learning, Pandas, Scikit-learn
NER: machine learning, Pandas

CASE 4
Confirmed: Deep Learning, PyTorch
NER: deep learning, PyTorch

CASE 5
Confirmed: []
NER: []

CASE 6
Confirmed: []
NER: []

CASE 7
Confirmed: Git
NER: Git

CASE 8
Confirmed: Python, SQL
NER: Python, SQL

CASE 9
Confirmed: Machine Learning, Pandas
NER: Pandas

CASE 10
Confirmed: Artificial Intelligence
NER: artificial intelligence
```

Kết quả quan trọng:

> Trong 10 trường hợp kiểm tra này, NER không phát hiện thêm skill mới ngoài những skill đã được SkillMatcher nhận diện.

NER chủ yếu lặp lại những skill đã được dictionary phát hiện.

---

# 12. Đánh giá khả năng bổ sung skill

File:

```text
experiments/ner/test_ner_supplement.py
```

Đây là bài kiểm tra gồm **25 trường hợp thủ công** nhằm kiểm tra riêng khả năng NER bổ sung skill mới.

Kết quả:

```text
                 SkillMatcher       NER
--------------------------------------------
TP                     29           24
FP                      0            0
FN                      8           13

Precision            100.00%      100.00%
Recall                78.38%       64.86%
F1                    87.88%       78.69%
```

Đánh giá phần bổ sung:

```text
New NER skills:          0
New correct skills:      0
New false positives:     0
```

Kết luận của experiment:

```text
RESULT:
Chưa chứng minh được NER bổ sung skill mới
so với SkillMatcher.
```

---

# 13. Phân tích kết quả

Kết quả cần được hiểu trong đúng phạm vi của experiment.

## 13.1. NER có khả năng nhận diện skill

Mô hình NER đạt F1 cao trên tập đánh giá sinh từ SkillMatcher:

```text
Best F1: 95.41%
```

Điều này cho thấy mô hình có thể học được pattern của các skill đã được SkillMatcher gán nhãn.

---

## 13.2. Nhưng NER chưa chứng minh được khả năng phát hiện skill ngoài dictionary

Trong bài kiểm tra bổ sung:

```text
New correct skills = 0
```

Do đó chưa có bằng chứng thực nghiệm rằng NER có thể bổ sung các kỹ năng mà dictionary không nhận diện được.

---

## 13.3. Nguyên nhân quan trọng

Dữ liệu training NER được tạo bằng:

```text
SkillMatcher
```

Do đó:

```text
SkillMatcher
     ↓
Pseudo Labels
     ↓
NER
```

NER đang học lại các pattern được SkillMatcher cung cấp.

Vì vậy, việc NER đạt F1 cao không đồng nghĩa với việc NER đã chứng minh khả năng phát hiện các skill mới ngoài dictionary.

Đây là một hạn chế quan trọng của experiment.

---

# 14. Một số lỗi còn tồn tại

NER vẫn còn bỏ sót một số kỹ năng:

```text
FastAPI
Scikit-learn
```

và một số cách diễn đạt tiếng Việt:

```text
học máy
```

Ngoài ra có hiện tượng nhận diện một phần của skill:

```text
REST
```

thay vì:

```text
REST API
```

Điều này cho thấy vấn đề không chỉ nằm ở khả năng nhận diện entity mà còn liên quan đến:

- span detection;
- skill normalization;
- synonym mapping;
- multilingual skill representation.

---

# 15. Quyết định đối với hệ thống chính

Sau khi đánh giá, NER **chưa được tích hợp vào pipeline chính**.

Pipeline chính tiếp tục sử dụng:

```text
CV
 ↓
Document Extraction
 ↓
SkillMatcher / Skill Extraction
 ↓
CV Skill Profile
 ↓
Job Ranking
 ↓
Skill Matching
 ↓
Skill Gap
 ↓
Skill Recommendation
```

NER được giữ riêng trong:

```text
experiments/ner/
```

và được xem là:

> **Experimental / Future Work**

---

# 16. Lý do chưa tích hợp

Có ba lý do chính.

### 1. Chưa chứng minh được khả năng bổ sung

Trong 25 trường hợp đánh giá:

```text
New correct skills = 0
```

Do đó chưa có bằng chứng rằng NER tạo thêm giá trị so với SkillMatcher.

### 2. Precision là ưu tiên của project

Project ưu tiên:

```text
Không nhận diện
        >
Nhận diện sai
```

Do đó không nên đưa NER vào pipeline chính chỉ vì mô hình có F1 cao trên pseudo-label.

### 3. Dataset training phụ thuộc SkillMatcher

NER được train từ pseudo-label do SkillMatcher tạo ra.

Điều này khiến việc đánh giá khả năng NER phát hiện skill ngoài dictionary chưa thực sự độc lập.

---

# 17. Future Work

NER vẫn có thể được phát triển trong tương lai.

Một hướng cải thiện là xây dựng một tập dữ liệu NER có annotation độc lập với SkillMatcher:

```text
CV
 ↓
Human Annotation
 ↓
Gold-standard Dataset
 ↓
NER Training
 ↓
Independent Evaluation
```

Khi đó có thể đánh giá rõ hơn:

- NER có phát hiện skill ngoài dictionary hay không;
- khả năng generalization;
- khả năng xử lý tiếng Việt;
- khả năng xử lý synonym;
- khả năng phát hiện skill mới;
- khả năng bổ sung skill cho SkillMatcher.

Một hướng khác là xây dựng hybrid pipeline hoàn chỉnh:

```text
Dictionary
     +
NER
     +
Skill Normalization
     +
Evidence Validation
     ↓
Final Skill Profile
```

Tuy nhiên, các hướng này được xem là mở rộng của project, không thuộc phạm vi triển khai hiện tại.

---

# 18. Cấu trúc thư mục

```text
experiments/
└── ner/
    ├── README.md
    │
    ├── auto_label.py
    ├── config.cfg
    ├── parse_cv.py
    ├── skill_matcher.py
    ├── to_spacy.py
    │
    ├── analyze_duplicates.py
    ├── check_jsonl_spans.py
    ├── check_split_overlap.py
    ├── check_whitespace_spans.py
    ├── debug_char_span.py
    │
    ├── test_hybrid_v1.py
    ├── test_ner_v1.py
    ├── test_ner_supplement.py
    │
    ├── data/
    │   ├── train.jsonl
    │   ├── dev.jsonl
    │   ├── test.jsonl
    │   ├── train.spacy
    │   ├── dev.spacy
    │   └── test.spacy
    │
    └── models/
        └── skill_ner_v1/
            └── model-best/
```

---

# 19. Các file quan trọng

| File                        | Vai trò                                  |
| --------------------------- | ---------------------------------------- |
| `auto_label.py`             | Tạo pseudo-label từ CV bằng SkillMatcher |
| `to_spacy.py`               | Chuyển JSONL sang `.spacy`               |
| `config.cfg`                | Cấu hình pipeline NER                    |
| `skill_matcher.py`          | Dictionary-based skill matching          |
| `parse_cv.py`               | Prototype hybrid CV parser               |
| `test_ner_v1.py`            | Kiểm tra NER trên các câu thủ công       |
| `test_hybrid_v1.py`         | Kiểm tra SkillMatcher + NER              |
| `test_ner_supplement.py`    | Đánh giá khả năng NER bổ sung skill      |
| `check_split_overlap.py`    | Kiểm tra data leakage giữa các tập       |
| `check_jsonl_spans.py`      | Kiểm tra entity spans                    |
| `check_whitespace_spans.py` | Kiểm tra span chứa whitespace            |
| `debug_char_span.py`        | Debug character/token alignment          |
| `analyze_duplicates.py`     | Phân tích dữ liệu trùng lặp              |

---

# 20. Các lệnh chính

## Tạo dataset

```powershell
python experiments\ner\auto_label.py
```

## Kiểm tra duplicate

```powershell
python experiments\ner\analyze_duplicates.py
```

## Kiểm tra overlap

```powershell
python experiments\ner\check_split_overlap.py
```

## Chuyển sang spaCy

```powershell
python experiments\ner\to_spacy.py
```

## Kiểm tra dataset

```powershell
python -m spacy debug data experiments\ner\config.cfg `
  --paths.train experiments\ner\data\train.spacy `
  --paths.dev experiments\ner\data\dev.spacy
```

## Training

```powershell
python -m spacy train experiments\ner\config.cfg `
  --output experiments\ner\models\skill_ner_v1 `
  --paths.train experiments\ner\data\train.spacy `
  --paths.dev experiments\ner\data\dev.spacy `
  --training.max_steps 2000 `
  --training.eval_frequency 200
```

## Test NER

```powershell
python experiments\ner\test_ner_v1.py
```

## Test Hybrid

```powershell
python experiments\ner\test_hybrid_v1.py
```

## Đánh giá khả năng bổ sung

```powershell
python experiments\ner\test_ner_supplement.py
```

---

# 21. Kết luận

Experiment NER đã hoàn thành pipeline từ:

```text
CV Dataset
    ↓
Deduplication
    ↓
Train / Dev / Test Split
    ↓
Automatic Labeling
    ↓
spaCy Conversion
    ↓
Data Validation
    ↓
NER Training
    ↓
Manual Testing
    ↓
Hybrid Testing
    ↓
Supplement Evaluation
```

Mô hình `skill_ner_v1` đạt:

```text
Best F1: 95.41%
```

trên quá trình đánh giá của spaCy.

Tuy nhiên, bài kiểm tra bổ sung 25 trường hợp chưa chứng minh được rằng NER có thể bổ sung thêm skill mới so với SkillMatcher:

```text
New correct skills = 0
```

Do đó, trong phiên bản hiện tại:

> **SkillMatcher tiếp tục là phương pháp trích xuất skill chính. NER được giữ lại như một experiment và hướng Future Work, chưa được tích hợp vào hệ thống chính.**

Điều này giúp hệ thống hiện tại duy trì nguyên tắc:

```text
Reliability
     ↓
Precision
     ↓
Controlled Skill Extraction
     ↓
Recommendation
```

thay vì đưa một mô hình chưa chứng minh được giá trị bổ sung vào pipeline chính.

```

```
