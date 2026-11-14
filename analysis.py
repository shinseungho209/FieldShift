import pandas as pd


def compare_crop_rainfall(daily_df, crop_df):
    """
    작물별 연간 강수량 참고 지표를 계산한다.
    주의: 실제 작물의 물 필요량이나 관개량을 직접 나타내지는 않는다.
    """
    total_rainfall = daily_df["precipitation_mm_day"].sum()

    results = []

    for _, crop in crop_df.iterrows():
        water_requirement = crop["water_requirement"]

        # 시제품용 상대 지표: 강수량 수준을 작물의 물 요구 수준과 비교
        if water_requirement == "high":
            reference = 1500
        elif water_requirement == "medium":
            reference = 1000
        else:
            reference = 700

        difference_percent = (
            total_rainfall - reference
        ) / reference * 100

        results.append({
            "crop": crop["crop"],
            "annual_rainfall_mm": round(total_rainfall, 1),
            "reference_rainfall_mm": reference,
            "rainfall_difference_percent": round(
                difference_percent, 1
            )
        })

    return pd.DataFrame(results)


def analyze_monthly_rainfall(daily_df):
    """
    일별 강수량을 월별로 집계하고
    강수량이 많은 달과 적은 달을 확인한다.
    """
    data = daily_df.copy()

    data["month"] = data["date"].dt.month

    monthly_rainfall = data.groupby("month").agg(
        total_rainfall_mm=(
            "precipitation_mm_day",
            "sum"
        ),
        average_daily_rainfall_mm=(
            "precipitation_mm_day",
            "mean"
        )
    )

    monthly_rainfall = monthly_rainfall.round(2)

    return monthly_rainfall


def compare_rotation_temperature(daily_df, crop_df, strategy_df):
    """
    윤작 전략에 포함된 작물들의 온도 적합성을 비교한다.
    """
    crop_scores = compare_crop_temperature(daily_df, crop_df)

    results = []

    for _, strategy in strategy_df.iterrows():
        crop_names = strategy["crop_sequence"].split("→")

        selected_scores = crop_scores[
            crop_scores["crop"].isin(crop_names)
        ]

        if selected_scores.empty:
            average_score = None
        else:
            average_score = round(
                selected_scores["matching_days_percent"].mean(),
                1
            )

        results.append({
            "strategy": strategy["strategy"],
            "crop_sequence": strategy["crop_sequence"],
            "temperature_score": average_score
        })

    return pd.DataFrame(results)


def load_rotation_strategies():
    """
    지역별 윤작 전략 CSV 파일을 불러온다.
    """
    strategies = pd.read_csv(
        "data/rotation_strategies.csv",
        encoding="utf-8-sig"
    )

    return strategies



def load_crop_requirements():
    """
    작물별 재배 조건 CSV 파일을 불러온다.
    """
    import pandas as pd

    crop_data = pd.read_csv(
        "data/crop_requirements.csv",
        encoding="utf-8-sig"
    )

    return crop_data


def summarize_monthly_environment(df):
    """
    일별 환경 데이터를 월별 통계로 변환한다.
    """
    data = df.copy()

    data["month"] = data["date"].dt.month

    monthly = data.groupby("month").agg(
        average_temperature_C=("temperature_C", "mean"),
        total_precipitation_mm=("precipitation_mm_day", "sum"),
        average_solar_kwh_m2_day=("solar_kwh_m2_day", "mean")
    )

    return monthly.round(2)



def compare_crop_temperature(daily_df, crop_df):
    """
    일별 기온이 각 작물의 적정 온도 범위에
    들어오는 비율을 계산한다.
    """
    results = []

    monthly_temperature = (
        daily_df.groupby(daily_df["date"].dt.month)["temperature_C"]
        .mean()
    )

    for _, crop in crop_df.iterrows():
        min_temp = crop["optimal_temp_min_C"]
        max_temp = crop["optimal_temp_max_C"]

        # 전체 일수 중 적정 온도 범위에 해당하는 날의 비율
        matching_days = daily_df["temperature_C"].between(
            min_temp, max_temp
        )

        matching_percent = matching_days.mean() * 100

        # 월평균 기온이 적정 온도 범위에 들어오는 달
        matching_months = monthly_temperature.between(
            min_temp, max_temp
        ).sum()

        results.append({
            "crop": crop["crop"],
            "optimal_temperature": f"{min_temp}~{max_temp}°C",
            "matching_days_percent": round(matching_percent, 1),
            "matching_months": int(matching_months)
        })

    return pd.DataFrame(results)
