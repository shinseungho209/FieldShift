import itertools
import re
import pandas as pd


ENV_COLUMNS = [
    "temperature_C",
    "precipitation_mm_day",
    "solar_kwh_m2_day"
]

SEASON_MONTHS = {
    "봄": [3, 4, 5],
    "여름": [6, 7, 8],
    "가을": [9, 10, 11],
    "겨울": [12, 1, 2]
}


def to_number(value):
    result = pd.to_numeric(
        pd.Series([value]),
        errors="coerce"
    ).iloc[0]

    return result


def prepare_daily_data(daily_df):
    data = daily_df.copy()

    if "date" not in data.columns:
        raise ValueError("일별 데이터에 date 열이 없습니다.")

    data["date"] = pd.to_datetime(
        data["date"],
        errors="coerce"
    )

    for column in ENV_COLUMNS:
        if column not in data.columns:
            data[column] = float("nan")

        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

        data.loc[
            data[column] <= -900,
            column
        ] = float("nan")

    data = data.dropna(subset=["date"])

    return data.sort_values("date").reset_index(drop=True)


def parse_growing_days(value):
    if pd.isna(value):
        return None, None

    numbers = re.findall(r"\d+", str(value))

    if len(numbers) >= 2:
        return int(numbers[0]), int(numbers[1])

    if len(numbers) == 1:
        number = int(numbers[0])
        return number, number

    return None, None


def load_crop_requirements(
    path="data/crop_requirements.csv"
):
    crops = pd.read_csv(
        path,
        encoding="utf-8-sig"
    )

    if "crop" not in crops.columns:
        raise ValueError("작물 데이터에 crop 열이 없습니다.")

    crops["crop"] = (
        crops["crop"]
        .fillna("")
        .astype(str)
        .str.strip()
    )

    numeric_columns = [
        "optimal_temp_min_C",
        "optimal_temp_max_C",
        "growing_days_min",
        "growing_days_max",
        "sowing_start_month",
        "sowing_end_month",
        "harvest_start_month",
        "harvest_end_month"
    ]

    for column in numeric_columns:
        if column not in crops.columns:
            crops[column] = float("nan")

        crops[column] = pd.to_numeric(
            crops[column],
            errors="coerce"
        )

    if "growing_days" in crops.columns:
        for index, value in crops["growing_days"].items():
            minimum, maximum = parse_growing_days(value)

            if pd.isna(crops.at[index, "growing_days_min"]):
                crops.at[index, "growing_days_min"] = minimum

            if pd.isna(crops.at[index, "growing_days_max"]):
                crops.at[index, "growing_days_max"] = maximum

    text_defaults = {
        "season": "",
        "water_requirement": "자료 확인 필요",
        "soil_condition": "자료 확인 필요",
        "temperature_confidence": "잠정",
        "calendar_confidence": "잠정",
        "verification_status": "잠정",
        "notes": ""
    }

    for column, default in text_defaults.items():
        if column not in crops.columns:
            crops[column] = default

        crops[column] = (
            crops[column]
            .fillna(default)
            .astype(str)
            .str.strip()
        )

    crops = crops[
        crops["crop"].ne("")
    ].drop_duplicates(
        subset=["crop"]
    )

    return crops.reset_index(drop=True)


def get_crop_calendar(crop):
    columns = [
        "sowing_start_month",
        "sowing_end_month",
        "harvest_start_month",
        "harvest_end_month"
    ]

    values = [
        to_number(crop.get(column))
        for column in columns
    ]

    if any(pd.isna(value) for value in values):
        return None

    values = [int(value) for value in values]

    if any(value < 1 or value > 12 for value in values):
        return None

    return {
        "sowing_start": values[0],
        "sowing_end": values[1],
        "harvest_start": values[2],
        "harvest_end": values[3]
    }


def months_between(start, end):
    if start <= end:
        return list(range(start, end + 1))

    return (
        list(range(start, 13))
        + list(range(1, end + 1))
    )


def get_active_months(calendar):
    if calendar is None:
        return None

    return set(
        months_between(
            calendar["sowing_start"],
            calendar["harvest_end"]
        )
    )


def get_crop_analysis_months(crop):
    calendar = get_crop_calendar(crop)

    if calendar is not None:
        return months_between(
            calendar["sowing_start"],
            calendar["harvest_end"]
        )

    season = str(crop.get("season", "")).strip()

    if season in SEASON_MONTHS:
        return SEASON_MONTHS[season]

    return None


def get_temperature_range(crop):
    minimum = to_number(
        crop.get("optimal_temp_min_C")
    )

    maximum = to_number(
        crop.get("optimal_temp_max_C")
    )

    if (
        pd.isna(minimum)
        or pd.isna(maximum)
        or minimum > maximum
    ):
        return None, None

    return float(minimum), float(maximum)


def summarize_monthly_environment(daily_df):
    data = prepare_daily_data(daily_df)

    data["month"] = data["date"].dt.month

    monthly = data.groupby("month").agg(
        average_temperature_C=(
            "temperature_C",
            "mean"
        ),
        total_precipitation_mm=(
            "precipitation_mm_day",
            "sum"
        ),
        average_solar_kwh_m2_day=(
            "solar_kwh_m2_day",
            "mean"
        )
    )

    return monthly.round(2)


def analyze_monthly_rainfall(daily_df):
    data = prepare_daily_data(daily_df)

    data = data.dropna(
        subset=["precipitation_mm_day"]
    )

    if data.empty:
        return pd.DataFrame()

    data["month"] = data["date"].dt.month

    return data.groupby("month").agg(
        total_rainfall_mm=(
            "precipitation_mm_day",
            "sum"
        ),
        average_daily_rainfall_mm=(
            "precipitation_mm_day",
            "mean"
        )
    ).round(2)


def compare_crop_temperature(daily_df, crop_df):
    data = prepare_daily_data(daily_df)

    if data["temperature_C"].notna().sum() == 0:
        raise ValueError("분석 가능한 기온 데이터가 없습니다.")

    results = []

    for _, crop in crop_df.iterrows():
        name = crop["crop"]

        minimum, maximum = get_temperature_range(crop)
        months = get_crop_analysis_months(crop)

        if minimum is None or months is None:
            results.append({
                "crop": name,
                "optimal_temperature": "기준 확인 필요",
                "analysis_period": "계산 제외",
                "matching_days": None,
                "total_days": 0,
                "matching_days_percent": None,
                "analysis_status": "온도 또는 재배 일정 자료 부족"
            })
            continue

        period = data[
            data["date"].dt.month.isin(months)
        ].dropna(
            subset=["temperature_C"]
        )

        if period.empty:
            matching_days = None
            total_days = 0
            percentage = None
            status = "분석 기간 데이터 없음"
        else:
            matched = period["temperature_C"].between(
                minimum,
                maximum
            )

            matching_days = int(matched.sum())
            total_days = len(period)
            percentage = round(
                matched.mean() * 100,
                1
            )
            status = "재배 기간 일평균 기온 범위 일치율"

        results.append({
            "crop": name,
            "optimal_temperature": (
                f"{minimum:g}~{maximum:g}°C"
            ),
            "analysis_period": (
                f"{months[0]}월~{months[-1]}월"
            ),
            "matching_days": matching_days,
            "total_days": total_days,
            "matching_days_percent": percentage,
            "analysis_status": status
        })

    return pd.DataFrame(results)


def compare_crop_rainfall(daily_df, crop_df):
    data = prepare_daily_data(daily_df)

    results = []

    for _, crop in crop_df.iterrows():
        months = get_crop_analysis_months(crop)

        if months is None:
            results.append({
                "crop": crop["crop"],
                "growing_period_rainfall_mm": None,
                "water_requirement": crop["water_requirement"],
                "analysis_status": "재배 일정 확인 필요"
            })
            continue

        period = data[
            data["date"].dt.month.isin(months)
        ]

        rainfall = period[
            "precipitation_mm_day"
        ].sum(min_count=1)

        results.append({
            "crop": crop["crop"],
            "growing_period_rainfall_mm": (
                round(float(rainfall), 1)
                if pd.notna(rainfall)
                else None
            ),
            "water_requirement": crop["water_requirement"],
            "analysis_status": (
                "재배 기간 누적 강수량 참고값이며 "
                "실제 작물 이용 수분량이나 관개 필요량은 아님"
            )
        })

    return pd.DataFrame(results)


def check_rotation_order(first, second):
    first_calendar = first["calendar"]
    second_calendar = second["calendar"]

    if first_calendar is None or second_calendar is None:
        return None

    first_active = get_active_months(first_calendar)
    second_active = get_active_months(second_calendar)

    if first_active & second_active:
        return None

    harvest_month = first_calendar["harvest_end"]
    sowing_month = second_calendar["sowing_start"]

    gap = (sowing_month - harvest_month - 1) % 12

    if gap > 3:
        return None

    return gap


def generate_rotation_candidates(
    crop_scores,
    crop_df,
    max_candidates=30
):
    if crop_scores.empty or crop_df.empty:
        return pd.DataFrame()

    score_lookup = crop_scores.set_index(
        "crop"
    ).to_dict(orient="index")

    candidates = []

    for _, crop in crop_df.iterrows():
        name = crop["crop"]
        score_info = score_lookup.get(name, {})

        score = to_number(
            score_info.get("matching_days_percent")
        )

        if pd.isna(score):
            continue

        candidates.append({
            "crop": name,
            "temperature_score": float(score),
            "calendar": get_crop_calendar(crop),
            "temperature_confidence": crop[
                "temperature_confidence"
            ],
            "calendar_confidence": crop[
                "calendar_confidence"
            ],
            "water_requirement": crop[
                "water_requirement"
            ],
            "soil_condition": crop[
                "soil_condition"
            ],
            "notes": crop["notes"]
        })

    results = []

    for crop in candidates:
        calendar_status = (
            "대표 재배 달력 자료 있음"
            if crop["calendar"] is not None
            else "재배 달력 확인 필요"
        )

        results.append({
            "strategy": f"단작 후보: {crop['crop']}",
            "crop_sequence": crop["crop"],
            "temperature_score": round(
                crop["temperature_score"],
                1
            ),
            "ranking_score": round(
                crop["temperature_score"],
                1
            ),
            "crop_count": 1,
            "calendar_status": calendar_status,
            "temperature_confidence": crop[
                "temperature_confidence"
            ],
            "calendar_confidence": crop[
                "calendar_confidence"
            ],
            "water_requirement": crop[
                "water_requirement"
            ],
            "soil_condition": crop[
                "soil_condition"
            ],
            "analysis_status": (
                "재배 기간의 일평균 기온 범위 일치율"
            ),
            "notes": crop["notes"]
        })

    for first, second in itertools.permutations(
        candidates,
        2
    ):
        gap = check_rotation_order(first, second)

        if gap is None:
            continue

        score = (
            first["temperature_score"]
            + second["temperature_score"]
        ) / 2

        sequence = (
            f"{first['crop']} → {second['crop']}"
        )

        results.append({
            "strategy": f"윤작 후보: {sequence}",
            "crop_sequence": sequence,
            "temperature_score": round(score, 1),
            "ranking_score": round(score, 1),
            "crop_count": 2,
            "calendar_status": (
                f"월별 일정상 후보 · 작물 사이 약 {gap}개월 간격"
            ),
            "temperature_confidence": (
                f"{first['temperature_confidence']} / "
                f"{second['temperature_confidence']}"
            ),
            "calendar_confidence": (
                f"{first['calendar_confidence']} / "
                f"{second['calendar_confidence']}"
            ),
            "water_requirement": (
                f"{first['crop']}: {first['water_requirement']} / "
                f"{second['crop']}: {second['water_requirement']}"
            ),
            "soil_condition": (
                f"{first['crop']}: {first['soil_condition']} / "
                f"{second['crop']}: {second['soil_condition']}"
            ),
            "analysis_status": (
                "두 작물의 기온 일치율 평균. "
                "실제 윤작 효과를 검증한 점수는 아님"
            ),
            "notes": (
                f"{first['notes']} / {second['notes']}"
            )
        })

    result = pd.DataFrame(results)

    if result.empty:
        return result

    result = result.sort_values(
        ["ranking_score", "crop_count"],
        ascending=[False, True]
    ).head(
        max_candidates
    ).reset_index(drop=True)

    result.insert(
        0,
        "rank",
        range(1, len(result) + 1)
    )

    return result