TEXT = {
    "ko": {
        "title": "FieldShift",
        "subtitle": "NASA 데이터를 활용한 기후 적응형 작부체계 추천",
        "description": (
            "지역의 기후 데이터와 작물별 재배 조건을 비교해 "
            "재배 전략 후보를 자동으로 생성합니다."
        ),
        "prototype": "프로토타입",
        "language": "언어",

        "region_section": "1. 지역 선택",
        "province": "시·도 선택",
        "district": "시·군·구 선택",
        "selected_region": "선택한 지역",
        "agriculture_type": "농업 유형",
        "coordinates": "좌표",
        "registered_regions": "등록된 지역 수",

        "start_date": "분석 시작일",
        "end_date": "분석 종료일",
        "invalid_dates": "종료일은 시작일보다 늦어야 합니다.",

        "environment_section": "2. NASA 환경 데이터",
        "fetching": "NASA POWER 데이터를 가져오는 중입니다...",
        "fetch_failed": "NASA 데이터를 가져오지 못했습니다.",
        "fetch_success": "NASA 데이터 수집 완료",
        "no_data": "선택한 기간의 데이터가 없습니다.",
        "period": "분석 기간",
        "temperature": "기온",
        "annual_temperature": "분석 기간 평균 기온",
        "rainfall": "누적 강수량",
        "solar": "평균 일사량",
        "no_value": "데이터 없음",

        "monthly_environment": "월별 환경 데이터",
        "monthly_temperature": "월별 평균 기온",
        "monthly_rainfall": "월별 강수량",
        "monthly_solar": "월별 평균 일사량",

        "rainfall_detail": "강수량 분석",
        "rainfall_table": "월별 강수량 표",
        "no_rainfall": "강수량 데이터가 없습니다.",
        "rainfall_warning": (
            "강수량은 강수 공급량의 참고 지표입니다. "
            "실제 관개 필요량이나 토양 수분을 직접 나타내지는 않습니다."
        ),
        "nasa_source": "데이터 출처: NASA POWER",

        "crop_section": "3. 작물별 기후 적합성 분석",
        "crop_failed": "작물 조건 데이터를 불러오지 못했습니다.",
        "temperature_comparison": "작물별 온도 조건 비교",
        "temperature_match": "온도 적합도",
        "no_temperature": "온도 분석 결과가 없습니다.",
        "temperature_explanation": (
            "작물별 설정 온도 범위와 분석 기간의 기온을 비교한 결과입니다."
        ),
        "temperature_warning": (
            "이 점수는 설정된 온도 범위와의 비교 결과이며, "
            "실제 수확량이나 생산성을 예측하지 않습니다."
        ),
        "temperature_table": "작물별 온도 분석 결과",
        "crop_rainfall_table": "작물별 수분 요구 조건",

        "rotation_section": "4. 자동 재배 전략 후보",
        "additional_section": "5. 데이터 한계 및 분석 범위",

        "footer": "FieldShift | NASA Space Apps Challenge 2026",
        "final_note": (
            "본 서비스는 기후 데이터 기반의 의사결정 보조 도구이며, "
            "실제 재배 전에는 지역 농업 전문가의 검토가 필요합니다."
        ),
        "region_load_failed": "지역 데이터를 불러오지 못했습니다.",

        "rotation_ui": {
            "title": "자동 생성된 재배 전략 후보",
            "description": "의 NASA 기후 데이터와 작물 조건을 활용한 후보입니다.",
            "empty": "생성된 재배 전략 후보가 없습니다.",
            "score_info": (
                "현재 순위 점수는 기온 적합도와 재배 일정 정보를 "
                "기반으로 계산됩니다."
            ),
            "candidate": "후보",
            "temperature_score": "기온 기반 순위 점수",
            "crop_count": "작물 수",
            "crop_sequence": "작물 구성",
            "calendar": "재배 일정 상태",
            "temperature_confidence": "온도 데이터 신뢰 수준",
            "calendar_confidence": "재배 일정 신뢰 수준",
            "water": "수분 요구 조건",
            "soil": "토양 조건",
            "evaluation": "분석 상태",
            "notes": "분석 참고 사항",
            "chart": "재배 전략 후보별 점수",
            "table": "전체 재배 전략 후보",
            "warning": (
                "현재 순위는 기온 적합도와 월별 재배 일정 정보를 "
                "중심으로 계산합니다. 강수량은 참고 정보로 제공되며, "
                "토양 수분, 토양 건강, 병해충, 경제성 및 실제 수확량은 "
                "점수에 반영되지 않습니다."
            ),
        },

        "limitations": {
            "title": "데이터 항목별 활용 범위",
            "item": "항목",
            "status": "활용 상태",
            "description": "설명",
            "temperature": "기온",
            "rainfall": "강수량",
            "solar": "일사량",
            "elevation": "고도",
            "slope": "경사도",
            "soil_moisture": "토양 수분",
            "soil_health": "토양 건강",
            "calendar": "작물 재배 일정",
            "preferences": "농민 우선순위",
            "yield": "수확량",

            "temperature_status": "분석에 사용",
            "rainfall_status": "참고 정보",
            "solar_status": "분석에 사용",
            "elevation_status": "향후 반영",
            "slope_status": "현재 데이터 없음",
            "soil_moisture_status": "현재 데이터 없음",
            "soil_health_status": "현재 데이터 없음",
            "calendar_status": "일부 활용",
            "preferences_status": "향후 반영",
            "yield_status": "현재 데이터 없음",

            "available": "분석에 사용",
            "reference": "참고 정보",
            "partial": "일부 활용",
            "planned": "향후 반영",
            "not_available": "현재 데이터 없음",

            "temperature_desc": "NASA POWER 일별 기온 데이터",
            "precipitation_desc": "NASA POWER 강수량 데이터",
            "solar_desc": "NASA POWER 일사량 데이터",
            "elevation_desc": "외부 고도 데이터가 있는 경우 활용",
            "slope_desc": "고도 자료만으로는 직접 계산할 수 없음",
            "soil_moisture_desc": "현재 분석 점수에 반영되지 않음",
            "soil_health_desc": "토양 건강을 직접 측정한 자료 없음",
            "crop_calendar_desc": "CSV에 입력된 월별 파종·수확 일정",
            "farmer_preferences_desc": "선호도 입력 기능과 점수 연동 필요",
            "yield_desc": "수확량 예측 모델 미구현",
        },

        "columns": {
            "crop": "작물",
            "optimal_temp_min_C": "최저 적정 온도 (°C)",
            "optimal_temp_max_C": "최고 적정 온도 (°C)",
            "water_requirement": "수분 요구 조건",
            "soil_condition": "토양 조건",
            "growing_days_min": "최소 생육 기간 (일)",
            "growing_days_max": "최대 생육 기간 (일)",
            "sowing_start_month": "파종 시작 월",
            "sowing_end_month": "파종 종료 월",
            "harvest_start_month": "수확 시작 월",
            "harvest_end_month": "수확 종료 월",
            "season": "재배 계절",
            "temperature_confidence": "온도 신뢰 수준",
            "calendar_confidence": "일정 신뢰 수준",
            "verification_status": "검증 상태",
            "notes": "참고 사항",
            "matching_days_percent": "온도 적합 일수 (%)",
            "temperature_score": "기온 적합도",
            "rainfall_score": "강수량 참고 점수",
            "ranking_score": "순위 점수",
            "rank": "순위",
            "strategy": "재배 전략",
            "crop_sequence": "작물 구성",
            "crop_count": "작물 수",
            "calendar_status": "재배 일정 상태",
            "analysis_status": "분석 상태",
        },
    },

    "en": {
        "title": "FieldShift",
        "subtitle": "Climate-Adaptive Crop Rotation Using NASA Data",
        "description": (
            "Automatically generates crop strategy candidates "
            "by comparing regional climate data with crop requirements."
        ),
        "prototype": "Prototype",
        "language": "Language",

        "region_section": "1. Select a Region",
        "province": "Province",
        "district": "District",
        "selected_region": "Selected Region",
        "agriculture_type": "Agricultural Type",
        "coordinates": "Coordinates",
        "registered_regions": "Registered Regions",

        "start_date": "Start Date",
        "end_date": "End Date",
        "invalid_dates": "The end date must be later than the start date.",

        "environment_section": "2. NASA Environmental Data",
        "fetching": "Fetching NASA POWER data...",
        "fetch_failed": "Failed to retrieve NASA data.",
        "fetch_success": "NASA data successfully retrieved.",
        "no_data": "No data available for the selected period.",
        "period": "Analysis Period",
        "temperature": "Temperature",
        "annual_temperature": "Average Temperature During Analysis Period",
        "rainfall": "Total Precipitation",
        "solar": "Average Daily Solar Radiation",
        "no_value": "No Data",

        "monthly_environment": "Monthly Environmental Data",
        "monthly_temperature": "Monthly Average Temperature",
        "monthly_rainfall": "Monthly Precipitation",
        "monthly_solar": "Monthly Average Solar Radiation",

        "rainfall_detail": "Precipitation Analysis",
        "rainfall_table": "Monthly Precipitation Table",
        "no_rainfall": "No precipitation data available.",
        "rainfall_warning": (
            "Precipitation is provided as a reference for water input. "
            "It does not directly represent irrigation demand or soil moisture."
        ),
        "nasa_source": "Data Source: NASA POWER",

        "crop_section": "3. Crop Climate Suitability Analysis",
        "crop_failed": "Failed to load crop requirement data.",
        "temperature_comparison": "Temperature Suitability by Crop",
        "temperature_match": "Temperature Suitability",
        "no_temperature": "No temperature analysis results available.",
        "temperature_explanation": (
            "Compares the configured temperature range for each crop "
            "with temperatures during the selected analysis period."
        ),
        "temperature_warning": (
            "This score measures temperature-range compatibility. "
            "It does not predict actual yield or productivity."
        ),
        "temperature_table": "Crop Temperature Analysis Results",
        "crop_rainfall_table": "Crop Water Requirements",

        "rotation_section": "4. Automatically Generated Crop Strategy Candidates",
        "additional_section": "5. Data Limitations and Analysis Scope",

        "footer": "FieldShift | NASA Space Apps Challenge 2026",
        "final_note": (
            "This tool supports climate-informed decision-making. "
            "Consult local agricultural experts before implementation."
        ),
        "region_load_failed": "Failed to load regional data.",

        "rotation_ui": {
            "title": "Automatically Generated Crop Strategy Candidates",
            "description": "Candidates based on NASA climate data and crop requirements.",
            "empty": "No crop strategy candidates were generated.",
            "score_info": (
                "Current ranking scores are based on temperature suitability "
                "and crop calendar information."
            ),
            "candidate": "Candidate",
            "temperature_score": "Temperature-Based Ranking Score",
            "crop_count": "Number of Crops",
            "crop_sequence": "Crop Sequence",
            "calendar": "Calendar Status",
            "temperature_confidence": "Temperature Data Confidence",
            "calendar_confidence": "Crop Calendar Confidence",
            "water": "Water Requirement",
            "soil": "Soil Condition",
            "evaluation": "Analysis Status",
            "notes": "Analysis Notes",
            "chart": "Scores by Crop Strategy Candidate",
            "table": "All Crop Strategy Candidates",
            "warning": (
                "Current rankings are primarily based on temperature "
                "suitability and monthly crop calendar information. "
                "Precipitation is provided as reference information. "
                "Soil moisture, soil health, pests, economics, and actual "
                "crop yields are not included in the ranking."
            ),
        },

        "limitations": {
            "title": "Data Availability and Usage",
            "item": "Item",
            "status": "Status",
            "description": "Description",
            "temperature": "Temperature",
            "rainfall": "Precipitation",
            "solar": "Solar Radiation",
            "elevation": "Elevation",
            "slope": "Slope",
            "soil_moisture": "Soil Moisture",
            "soil_health": "Soil Health",
            "calendar": "Crop Calendar",
            "preferences": "Farmer Preferences",
            "yield": "Crop Yield",

            "temperature_status": "Used in Analysis",
            "rainfall_status": "Reference Only",
            "solar_status": "Used in Analysis",
            "elevation_status": "Planned",
            "slope_status": "Not Currently Available",
            "soil_moisture_status": "Not Currently Available",
            "soil_health_status": "Not Currently Available",
            "calendar_status": "Partially Used",
            "preferences_status": "Planned",
            "yield_status": "Not Currently Available",

            "available": "Used in Analysis",
            "reference": "Reference Only",
            "partial": "Partially Used",
            "planned": "Planned",
            "not_available": "Not Currently Available",

            "temperature_desc": "NASA POWER daily temperature data",
            "precipitation_desc": "NASA POWER precipitation data",
            "solar_desc": "NASA POWER solar radiation data",
            "elevation_desc": "Can be used when external elevation data is available",
            "slope_desc": "Cannot be directly calculated from a single elevation point",
            "soil_moisture_desc": "Not included in current ranking scores",
            "soil_health_desc": "No direct soil health measurements available",
            "crop_calendar_desc": "Monthly sowing and harvesting dates in the CSV file",
            "farmer_preferences_desc": "Preference input and score integration required",
            "yield_desc": "Crop yield prediction model not implemented",
        },

        "columns": {
            "crop": "Crop",
            "optimal_temp_min_C": "Minimum Optimal Temperature (°C)",
            "optimal_temp_max_C": "Maximum Optimal Temperature (°C)",
            "water_requirement": "Water Requirement",
            "soil_condition": "Soil Condition",
            "growing_days_min": "Minimum Growing Period (Days)",
            "growing_days_max": "Maximum Growing Period (Days)",
            "sowing_start_month": "Sowing Start Month",
            "sowing_end_month": "Sowing End Month",
            "harvest_start_month": "Harvest Start Month",
            "harvest_end_month": "Harvest End Month",
            "season": "Growing Season",
            "temperature_confidence": "Temperature Confidence",
            "calendar_confidence": "Calendar Confidence",
            "verification_status": "Verification Status",
            "notes": "Notes",
            "matching_days_percent": "Temperature-Matched Days (%)",
            "temperature_score": "Temperature Suitability",
            "rainfall_score": "Precipitation Reference Score",
            "ranking_score": "Ranking Score",
            "rank": "Rank",
            "strategy": "Crop Strategy",
            "crop_sequence": "Crop Sequence",
            "crop_count": "Number of Crops",
            "calendar_status": "Calendar Status",
            "analysis_status": "Analysis Status",
        },
    },
}


def t(language, key):
    """
    Return translated text or dictionary.
    Falls back to Korean when a key is unavailable.
    """
    language_text = TEXT.get(language, TEXT["ko"])

    return language_text.get(
        key,
        TEXT["ko"].get(key, key)
    )


def translate_columns(dataframe, language):
    """
    Translate DataFrame column names while preserving original data.
    """
    column_translations = TEXT.get(
        language,
        TEXT["ko"]
    ).get("columns", {})

    return dataframe.rename(columns=column_translations)