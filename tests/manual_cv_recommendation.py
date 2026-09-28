from pathlib import Path

from src.pipeline.cv_pipeline import extract_cv_skills
from src.recommendation.recommendation_pipeline import (
    recommend_for_cv_skills,
)


BASE_DIR = Path(__file__).resolve().parents[1]
CV_PATH = BASE_DIR / "data" / "sample_cv.pdf"


def main() -> None:
    print("=" * 60)
    print("CV PDF -> RECOMMENDATION")
    print("=" * 60)

    print(f"\nCV: {CV_PATH}")

    # 1. Extract skills from CV
    cv_skills = extract_cv_skills(CV_PATH)

    print("\n===== CV SKILLS =====")

    for skill in sorted(cv_skills):
        print(f"- {skill}")

    print(f"\nTotal skills: {len(cv_skills)}")

    # 2. Generate recommendations
    recommendations = recommend_for_cv_skills(
        cv_skills=cv_skills,
        top_n=5,
    )

    # 3. Display recommendations
    print("\n===== JOB RECOMMENDATIONS =====")

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        print(
            f"\n{index}. {recommendation.job_title}"
        )

        print(
            f"   Match rate: "
            f"{recommendation.match_rate}%"
        )

        print(
            "   Matched skills: "
            f"{sorted(recommendation.matched_skills)}"
        )

        print(
            "   Missing skills: "
            f"{sorted(recommendation.missing_skills)}"
        )

        print("\n   Skill recommendations:")

        for skill in recommendation.recommendations:
            print(
                f"   - {skill.skill}: "
                f"{skill.job_percentage}% "
                f"({skill.job_count} jobs)"
            )

        print("\n   Learning roadmap:")

        for step in recommendation.learning_roadmap:
            print(
                f"   - {step.skill}"
            )


if __name__ == "__main__":
    main()