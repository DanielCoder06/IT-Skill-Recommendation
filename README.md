# Project Development History

## Phase 1 — Database & Data

- Xác định bài toán IT Skill Recommendation.
- Thiết kế database gồm:
  - `companies`
  - `locations`
  - `jobs`
  - `skills`
  - `job_skills`
- Xây dựng `skills_dictionary.json`.
- Đồng bộ skills vào SQLite.
- Tạo `raw_jobs.json` gồm 10 JD IT.
- Xây dựng Job Loader.
- Fix lỗi `return` nằm trong vòng `for`.
- Mở rộng dữ liệu Job phục vụ phân tích và recommendation.

## Phase 2 — Regex Extraction

- Xây dựng Regex Skill Extractor.
- Sử dụng aliases + word boundary để nhận diện skill.
- Test các edge cases.
- Nhận ra Regex không xử lý tốt synonym và semantic description.

## Phase 3 — Gemini Extraction

- Tích hợp Gemini API.
- Sử dụng `.env` + `python-dotenv`.
- Xây dựng prompt với allowed skill list.
- Xây dựng Pydantic output schema.
- Fix lỗi Gemini schema liên quan đến `additionalProperties`.
- Viết validation tests.
- Gặp HTTP 429 quota khi integration test.

## Phase 4 — Extraction Pipeline

- Kết hợp Regex + Gemini.
- Gemini failure → fallback về Regex.
- Xây dựng skill merger bằng set union.
- Xác định source:
  - `regex`
  - `gemini`
  - `both`
- Fix lỗi `INSERT OR IGNORE` không cập nhật source bằng
  `ON CONFLICT DO UPDATE`.
- Viết integration test cho extraction pipeline.

## Phase 5 — Evaluation

- Xây dựng evaluation dataset.
- So sánh Regex và Gemini bằng Precision / Recall / F1.
- Kết quả trên evaluation dataset hiện tại:
  - Regex: P=0.80, R=0.60, F1=0.67
  - Gemini: P=1.00, R=0.90, F1=0.93
- Lưu ý: evaluation dataset hiện còn nhỏ.

## Phase 6 — Analytics

- Xây dựng skill frequency.
- Xây dựng skill percentage.
- Xây dựng skill distribution by location.
- Xây dựng skill count per job.
- Viết automated tests.
- Mở rộng dữ liệu Job để phục vụ phân tích skill demand.

## Phase 7 — Skill Gap Analysis

- Xây dựng chức năng so sánh skill của sinh viên với yêu cầu của một job.
- Xác định matched skills.
- Xác định missing skills.
- Xác định extra skills.
- Tính match rate.
- Xử lý trường hợp job không tồn tại.
- Xử lý trường hợp sinh viên chưa có skill.
- Xử lý trường hợp sinh viên có đầy đủ skill.
- Viết automated tests.

## Phase 8 — Skill Prerequisite & Learning Roadmap

- Bổ sung quan hệ prerequisite giữa các skills.
- Xây dựng bảng `skill_prerequisites`.
- Xây dựng learning roadmap dựa trên các skill còn thiếu.
- Xử lý dependency giữa các skill.
- Đảm bảo prerequisite được đưa vào trước skill phụ thuộc.
- Làm thứ tự roadmap deterministic để kết quả ổn định giữa các lần chạy.

Ví dụ:

`Python → NumPy → Pandas → Machine Learning → Deep Learning → PyTorch`

## Phase 9 — Resume Dataset & CV Skill Analysis

- Tích hợp dataset `Annotated_NER_PDF_Resumes`.
- Phân tích 5,029 CV.
- Phân tích 538,482 annotations.
- Làm sạch và mapping các skill annotation.
- Kiểm tra độ chính xác của annotation offsets.
- Xây dựng CV skill profiles.
- Phân tích skill phổ biến trong CV.
- Đối chiếu skill trong CV dataset với skill dictionary/database.
- Sử dụng dataset như nguồn hỗ trợ cho skill discovery và evaluation.

## Phase 10 — CV → Job Matching

- Xây dựng chức năng matching giữa CV skill profile và Job skill profile.
- Tính matched skills.
- Tính missing skills.
- Tính match rate.
- Xây dựng CV profile matching.
- Xây dựng job ranking dựa trên mức độ phù hợp.
- Giải thích kết quả ranking thông qua:
  - Match rate
  - Matched skills
  - Missing skills

## Phase 11 — Job Recommendation

- Xây dựng Skill Demand Analysis.
- Phân tích tần suất xuất hiện của các skill còn thiếu trong các Job.
- Xây dựng Skill Recommendation.
- Xếp hạng skill recommendation dựa trên nhu cầu từ Job dataset.
- Kết hợp Skill Gap + Skill Demand để đưa ra skill recommendation.

## Phase 12 — Recommendation Pipeline

- Xây dựng end-to-end recommendation pipeline.
- Kết hợp:
  - CV skill profile
  - Job skill extraction
  - Skill matching
  - Skill gap
  - Job ranking
  - Skill recommendation
  - Learning roadmap
- Xây dựng Recommendation Evaluation.
- Xây dựng Recommendation Service.

## Phase 13 — Job Data Acquisition

- Xây dựng job scraping/data acquisition pipeline.
- Xây dựng Job Schema.
- Xây dựng Job Filter.
- Xây dựng Job Classifier.
- Phân loại job theo level:
  - Internship
  - Junior
  - Senior
  - Unspecified
- Tích hợp nguồn dữ liệu Arbeitnow.
- Thu thập 250 job records từ API.
- Phân loại được 68 IT jobs.
- Import dữ liệu vào SQLite.
- Đảm bảo import có tính idempotent bằng job URL.
- Áp dụng Regex Skill Extraction cho dữ liệu Job mới.

## Phase 14 — Recommendation API

- Xây dựng FastAPI backend.
- Xây dựng Recommendation API.
- Kết nối API với Recommendation Service.
- Kiểm thử API bằng automated tests.
- Cung cấp endpoint phục vụ:
  - CV → Job matching
  - Job ranking
  - Skill gap
  - Skill recommendation
  - Learning roadmap

## Phase 15 — Streamlit Demo

- Xây dựng giao diện Streamlit.
- Kết nối Streamlit với recommendation pipeline.
- Hiển thị Top-N Job recommendations.
- Hiển thị Match Rate.
- Hiển thị Matched Skills.
- Hiển thị Missing Skills.
- Hiển thị Skill Recommendations.
- Hiển thị Learning Roadmap.
- Hoàn thành demo end-to-end từ CV skill profile → Job Recommendation.

## Phase 16 — Testing & Validation

- Mở rộng automated tests trong quá trình phát triển.
- Kiểm thử Database.
- Kiểm thử Skill Extraction.
- Kiểm thử Recommendation.
- Kiểm thử API.
- Kiểm thử các trường hợp edge case.
- Full test suite hiện tại:

`112 passed, 1 deselected, 1 warning`

- Warning hiện tại liên quan đến deprecation giữa Starlette TestClient và httpx và chưa ảnh hưởng đến chức năng chính.

---

# Current Status

## Đã hoàn thành

- Database
- Job Data Pipeline
- Regex Skill Extraction
- Gemini Skill Extraction
- Hybrid Skill Extraction Pipeline
- Skill Extraction Evaluation
- Skill Analytics
- Skill Gap Analysis
- Skill Prerequisite
- Learning Roadmap
- Resume Dataset Profiling
- CV Skill Profile
- CV → Job Matching
- Job Ranking
- Skill Demand Analysis
- Skill Recommendation
- End-to-End Recommendation Pipeline
- Recommendation Evaluation
- Recommendation Service
- Job Data Acquisition
- Arbeitnow Integration
- FastAPI
- Streamlit Demo
- Automated Testing

## Current System Flow

CV Skill Profile
↓
Job Skill Profile
↓
Skill Matching
↓
Skill Gap Analysis
↓
Job Ranking
↓
Skill Recommendation
↓
Learning Roadmap

---

# Current Data Status

- 340 jobs trong SQLite database.
- 68 IT jobs được import từ Arbeitnow.
- 67/68 Arbeitnow IT jobs có ít nhất một skill.
- 44 skills trong database.
- 477 quan hệ `job_skills`.
- 5,029 CV trong resume dataset.
- 4,293 CV có ít nhất một skill được nhận diện.
- Full test suite: `112 passed`.

---

## Phase 17 — CV PDF/Text Extraction

- Added TXT text extraction.
- Added PDF text extraction using PyMuPDF.
- Added document dispatcher supporting `.pdf` and `.txt`.
- Added unit tests for extraction and error handling.
- Added PyMuPDF to project dependencies.
- Full test suite: 122 passed.

## Phase 18 — CV Upload → Recommendation

Hoàn thiện luồng:

CV PDF
↓
PDF/Text Extraction
↓
CV Text
↓
Skill Extraction
↓
CV Skill Profile
↓
Job Matching
↓
Top-N Job Recommendation
↓
Skill Gap
↓
Skill Recommendation
↓
Learning Roadmap

## Phase 19 — Final Validation

- Kiểm thử end-to-end.
- Kiểm tra chất lượng recommendation.
- Kiểm tra các edge cases.
- Đánh giá kết quả.
- Hoàn thiện Streamlit demo.
- Hoàn thiện documentation.

## Phase 20 — Report

- Hoàn thiện mô tả bài toán.
- Mô tả kiến trúc hệ thống.
- Mô tả database.
- Mô tả skill extraction.
- Mô tả CV/JD matching.
- Mô tả recommendation.
- Mô tả learning roadmap.
- Trình bày kết quả thực nghiệm.
- Phân tích hạn chế.
- Đề xuất hướng phát triển tiếp theo.
