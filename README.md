# Project Development History

## Phase 1 — Database & Data

- Xác định bài toán IT Skill Recommendation.
- Thiết kế database gồm companies, locations, jobs, skills, job_skills.
- Xây dựng skills_dictionary.json.
- Đồng bộ skills vào SQLite.
- Tạo raw_jobs.json gồm 10 JD IT.
- Xây dựng Job Loader.
- Fix lỗi `return` nằm trong vòng `for`.

## Phase 2 — Regex Extraction

- Xây dựng Regex Skill Extractor.
- Sử dụng aliases + word boundary.
- Test các edge cases.
- Nhận ra Regex không xử lý tốt synonym/semantic description.

## Phase 3 — Gemini Extraction

- Tích hợp Gemini API.
- Sử dụng `.env` + python-dotenv.
- Xây dựng prompt với allowed skill list.
- Xây dựng Pydantic output schema.
- Fix lỗi Gemini schema liên quan đến `additionalProperties`.
- Viết validation tests.
- Gặp HTTP 429 quota khi integration test.

## Phase 4 — Extraction Pipeline

- Kết hợp Regex + Gemini.
- Gemini failure → fallback về Regex.
- Xây dựng skill merger bằng set union.
- Xác định source: regex / gemini / both.
- Fix lỗi `INSERT OR IGNORE` không cập nhật source bằng `ON CONFLICT DO UPDATE`.
- Viết integration test cho pipeline.

## Phase 5 — Evaluation

- Xây dựng evaluation dataset.
- So sánh Regex và Gemini bằng Precision / Recall / F1.
- Kết quả:
  - Regex: P=0.80, R=0.60, F1=0.67
  - Gemini: P=1.00, R=0.90, F1=0.93
- Lưu ý: evaluation dataset hiện còn nhỏ.

## Phase 6 — Analytics

- Xây dựng skill frequency.
- Xây dựng skill percentage.
- Xây dựng skill distribution by location.
- Xây dựng skill count per job.
- Viết automated tests.
- Full test suite: 43 passed.

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
- Full test suite: 47 passed.

## Current Status

Extraction + Database + Evaluation + Analytics + Skill Gap Analysis đã hoạt động.

## Next

Recommendation → Learning Roadmap
→ FastAPI → Streamlit → Final testing/report.
