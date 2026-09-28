import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="IT Internship Recommendation",
    page_icon="🎯",
    layout="wide",
)


st.title("🎯 IT Internship Recommendation")

st.write(
    "Phân tích CV và gợi ý cơ hội thực tập IT "
    "dựa trên kỹ năng của ứng viên."
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.header("📄 CV Analysis")

uploaded_file = st.sidebar.file_uploader(
    "Upload CV",
    type=["pdf", "txt"],
    help="Chấp nhận CV định dạng PDF hoặc TXT.",
)

top_n = st.sidebar.slider(
    "Số lượng job",
    min_value=1,
    max_value=10,
    value=5,
)

analyze_button = st.sidebar.button(
    "🔍 Phân tích CV",
    type="primary",
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_file is None:
        st.warning(
            "Vui lòng upload CV trước khi phân tích."
        )

    else:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type,
            )
        }

        endpoint = f"{API_URL}/recommendations/upload"

        try:

            with st.spinner(
                "Đang đọc CV và phân tích kỹ năng..."
            ):

                response = requests.post(
                    endpoint,
                    files=files,
                    params={"top_n": top_n},
                    timeout=120,
                )

            if response.status_code == 400:

                detail = response.json().get(
                    "detail",
                    "CV không hợp lệ.",
                )

                st.error(detail)

            elif response.status_code == 413:

                st.error(
                    "CV vượt quá giới hạn dung lượng 10 MB."
                )

            elif response.status_code != 200:

                detail = response.json().get(
                    "detail",
                    "Không thể phân tích CV.",
                )

                st.error(
                    f"API trả về lỗi "
                    f"HTTP {response.status_code}: "
                    f"{detail}"
                )

            else:

                data = response.json()

                # ====================================================
                # CV INFORMATION
                # ====================================================

                st.success(
                    f"Đã phân tích CV: "
                    f"**{data['filename']}**"
                )

                st.subheader("👤 CV Skill Profile")

                st.metric(
                    "Tổng số kỹ năng",
                    data["cv_skill_count"],
                )

                cv_skills = data["cv_skills"]

                if cv_skills:

                    skill_columns = st.columns(4)

                    for index, skill in enumerate(cv_skills):

                        column = skill_columns[
                            index % len(skill_columns)
                        ]

                        with column:
                            st.write(f"✓ {skill}")

                else:

                    st.warning(
                        "Không phát hiện được kỹ năng "
                        "trong CV."
                    )

                # ====================================================
                # JOB RECOMMENDATIONS
                # ====================================================

                st.divider()

                st.subheader(
                    "🎯 Job Recommendations"
                )

                recommendations = data[
                    "recommendations"
                ]

                if not recommendations:

                    st.info(
                        "Không tìm thấy job phù hợp "
                        "với CV hiện tại."
                    )

                else:

                    for index, recommendation in enumerate(
                        recommendations,
                        start=1,
                    ):

                        match_rate = (
                            recommendation["match_rate"]
                        )

                        with st.expander(
                            f"{index}. "
                            f"{recommendation['job_title']} "
                            f"— {match_rate:.2f}%"
                        ):

                            # ========================================
                            # MATCH RATE
                            # ========================================

                            st.markdown(
                                "### 📊 Match Rate"
                            )

                            st.progress(
                                min(
                                    max(
                                        int(match_rate),
                                        0,
                                    ),
                                    100,
                                )
                            )

                            st.write(
                                f"**{match_rate:.2f}%**"
                            )

                            # ========================================
                            # SKILL GAP
                            # ========================================

                            col1, col2 = st.columns(2)

                            with col1:

                                st.markdown(
                                    "### 🟢 Matched Skills"
                                )

                                matched_skills = (
                                    recommendation[
                                        "matched_skills"
                                    ]
                                )

                                if matched_skills:

                                    for skill in matched_skills:
                                        st.write(
                                            f"✓ {skill}"
                                        )

                                else:

                                    st.write(
                                        "Không có skill "
                                        "phù hợp."
                                    )

                            with col2:

                                st.markdown(
                                    "### 🔴 Missing Skills"
                                )

                                missing_skills = (
                                    recommendation[
                                        "missing_skills"
                                    ]
                                )

                                if missing_skills:

                                    for skill in missing_skills:
                                        st.write(
                                            f"✗ {skill}"
                                        )

                                else:

                                    st.write(
                                        "Không thiếu skill."
                                    )

                            # ========================================
                            # SKILL RECOMMENDATION
                            # ========================================

                            st.divider()

                            st.markdown(
                                "### 📚 Skill Recommendations"
                            )

                            skill_recommendations = (
                                recommendation[
                                    "skill_recommendations"
                                ]
                            )

                            if skill_recommendations:

                                for skill_rec in (
                                    skill_recommendations
                                ):

                                    skill = skill_rec[
                                        "skill"
                                    ]

                                    job_count = (
                                        skill_rec[
                                            "job_count"
                                        ]
                                    )

                                    percentage = (
                                        skill_rec[
                                            "job_percentage"
                                        ]
                                    )

                                    st.markdown(
                                        f"**{skill}** — "
                                        f"{percentage:.0f}%"
                                    )

                                    st.progress(
                                        min(
                                            max(
                                                int(
                                                    percentage
                                                ),
                                                0,
                                            ),
                                            100,
                                        )
                                    )

                                    st.caption(
                                        f"Xuất hiện trong "
                                        f"{job_count} job "
                                        f"đã được phân tích."
                                    )

                            else:

                                st.info(
                                    "Không có dữ liệu "
                                    "skill recommendation."
                                )

                            # ========================================
                            # EVALUATION
                            # ========================================

                            st.divider()

                            st.markdown(
                                "### 📈 Evaluation"
                            )

                            evaluation = (
                                recommendation[
                                    "evaluation"
                                ]
                            )

                            evaluation_col1, evaluation_col2 = (
                                st.columns(2)
                            )

                            with evaluation_col1:

                                st.metric(
                                    "Matched Skills",
                                    evaluation[
                                        "matched_skill_count"
                                    ],
                                )

                            with evaluation_col2:

                                st.metric(
                                    "Missing Skills",
                                    evaluation[
                                        "missing_skill_count"
                                    ],
                                )

        except requests.exceptions.ConnectionError:

            st.error(
                "Không thể kết nối FastAPI. "
                "Hãy kiểm tra API server "
                "đang chạy ở port 8000."
            )

        except requests.exceptions.Timeout:

            st.error(
                "API phản hồi quá lâu. "
                "Hãy thử lại với CV khác."
            )

        except requests.exceptions.RequestException as error:

            st.error(
                f"Lỗi khi gọi API: {error}"
            )