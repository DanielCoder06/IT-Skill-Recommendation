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
    "Phân tích kỹ năng và gợi ý cơ hội thực tập IT dựa trên hồ sơ kỹ năng."
)


st.sidebar.header("CV Profile")

cv_id = st.sidebar.number_input(
    "CV ID",
    min_value=1,
    value=1,
    step=1,
)

top_n = st.sidebar.slider(
    "Số lượng job",
    min_value=1,
    max_value=10,
    value=5,
)


if st.button("🔍 Phân tích CV"):
    endpoint = f"{API_URL}/recommendations/{cv_id}"

    try:
        response = requests.get(
            endpoint,
            params={"top_n": top_n},
            timeout=10,
        )

        if response.status_code == 404:
            st.error("Không tìm thấy CV.")

        elif response.status_code != 200:
            st.error(
                f"API trả về lỗi HTTP {response.status_code}."
            )

        else:
            data = response.json()

            st.success(
                f"Đã tìm thấy {data['count']} job phù hợp."
            )

            st.subheader("📋 Job Recommendations")

            for index, recommendation in enumerate(
                data["recommendations"],
                start=1,
            ):
                with st.expander(
                    f"{index}. {recommendation['job_title']} "
                    f"— {recommendation['match_rate']:.2f}%"
                ):
                    # ==========================================
                    # 1. SKILL GAP
                    # ==========================================

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("### 🟢 Matched Skills")

                        if recommendation["matched_skills"]:
                            for skill in recommendation["matched_skills"]:
                                st.write(f"✓ {skill}")
                        else:
                            st.write("Không có skill phù hợp.")

                    with col2:
                        st.markdown("### 🔴 Missing Skills")

                        if recommendation["missing_skills"]:
                            for skill in recommendation["missing_skills"]:
                                st.write(f"✗ {skill}")
                        else:
                            st.write("Không thiếu skill.")

                    # ==========================================
                    # 2. SKILL RECOMMENDATION
                    # ==========================================

                    st.markdown("---")
                    st.markdown("### 📊 Skill Recommendations")

                    skill_recommendations = recommendation[
                        "skill_recommendations"
                    ]

                    if skill_recommendations:
                        for skill_rec in skill_recommendations:
                            skill = skill_rec["skill"]
                            job_count = skill_rec["job_count"]
                            percentage = skill_rec["job_percentage"]

                            st.markdown(
                                f"**{skill}** — "
                                f"{percentage:.0f}%"
                            )

                            st.progress(
                                min(
                                    max(
                                        int(percentage),
                                        0,
                                    ),
                                    100,
                                )
                            )

                            st.caption(
                                f"Xuất hiện trong "
                                f"{job_count} job đã được phân tích."
                            )
                    else:
                        st.info(
                            "Không có dữ liệu skill recommendation."
                        )

                    # ==========================================
                    # 3. LEARNING ROADMAP
                    # ==========================================

                    st.markdown("---")
                    st.markdown("### 🗺️ Learning Roadmap")

                    roadmap = recommendation["learning_roadmap"]

                    if roadmap:
                        st.markdown(
                            "Thứ tự được sắp xếp từ skill nền tảng "
                            "đến skill mục tiêu."
                        )

                        for index, step in enumerate(roadmap, start=1):
                            st.markdown(
                                f"**Bước {index}** — {step['skill']}"
                            )

                    else:
                        st.info(
                            "Không có dữ liệu learning roadmap."
                        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Không thể kết nối FastAPI. "
            "Hãy kiểm tra API server đang chạy ở port 8000."
        )

    except requests.exceptions.Timeout:
        st.error("API phản hồi quá lâu.")

    except requests.exceptions.RequestException as error:
        st.error(f"Lỗi khi gọi API: {error}")