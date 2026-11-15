import itertools
import pandas as pd


SEASON_ORDER = {
    "겨울": 0,
    "봄": 1,
    "여름": 2,
    "가을": 3
}


def normalize_season(value):
    text = str(value).strip()

    if "겨울" in text:
        return "겨울"

    if "봄" in text:
        return "봄"

    if "여름" in text:
        return "여름"

    if "가을" in text:
        return "가을"

    return None


def generate_rotation_candidates(
    crop_scores,
    crop_df,
    max_candidates=30
):
    score_map = crop_scores.set_index("crop").to_dict(
        orient="index"
    )

    candidates = []

    crops = []

    for _, crop in crop_df.iterrows():
        name = str(crop["crop"]).strip()
        season = normalize_season(crop.get("season"))

        score_info = score_map.get(name, {})
        score = score_info.get("matching_days_percent")

        if season is None or pd.isna(score):
            continue

        crops.append({
            "crop": name,
            "season": season,
            "season_order": SEASON_ORDER[season],
            "temperature_score": float(score)
        })

    for crop in crops:
        candidates.append({
            "strategy": f"단작 후보: {crop['crop']}",
            "crop_sequence": crop["crop"],
            "temperature_score": crop["temperature_score"],
            "crop_count": 1,
            "legume_present": False,
            "calendar_status": "단작 후보",
            "analysis_status": "온도 조건 기준"
        })

    for first, second in itertools.combinations(crops, 2):
        if first["season"] == second["season"]:
            continue

        ordered = sorted(
            [first, second],
            key=lambda item: item["season_order"]
        )

        sequence = "→".join(
            item["crop"] for item in ordered
        )

        average_score = (
            first["temperature_score"]
            + second["temperature_score"]
        ) / 2

        candidates.append({
            "strategy": f"윤작 탐색 후보: {sequence}",
            "crop_sequence": sequence,
            "temperature_score": round(average_score, 1),
            "crop_count": 2,
            "legume_present": any(
                item["crop"] in ["콩", "강낭콩", "팥", "녹두"]
                for item in ordered
            ),
            "calendar_status": "파종·수확 달력 검증 필요",
            "analysis_status": "작물별 온도 점수의 단순 평균"
        })

    result = pd.DataFrame(candidates)

    if result.empty:
        return result

    result = result.sort_values(
        "temperature_score",
        ascending=False
    ).head(max_candidates)

    result = result.reset_index(drop=True)

    result.insert(
        0,
        "rank",
        range(1, len(result) + 1)
    )

    return result