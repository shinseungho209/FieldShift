import streamlit as st

from nasa_data import get_nasa_power_data

from analysis import (
    summarize_monthly_environment,
    load_crop_requirements,
    compare_crop_temperature,
    load_rotation_strategies,
    compare_rotation_temperature,
    analyze_monthly_rainfall,
    compare_crop_rainfall
)

from ui import render_rotation_ui


st.set_page_config(
    page_title="FieldShift",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 FieldShift")

st.subheader(
    "NASA 데이터를 활용한 농업 의사결정 지원 플랫폼"
)

st.write(
    "대한민국 지역별 환경 데이터를 분석하고 "
    "작물 윤작 전략을 비교하는 서비스입니다."
)

st.divider()


REGIONS = {
    "전북특별자치도 김제시": (35.8036, 126.8808),
    "전라남도 해남군": (34.5736, 126.5990),
    "강원특별자치도 평창군": (37.3700, 128.3900),
    "경상북도 안동시": (36.5684, 128.7294),
    "충청남도 논산시": (36.1872, 127.0987)
}


st.header("지역 선택")

region = st.selectbox(
    "분석할 지역을 선택하세요",
    list(REGIONS.keys())
)

latitude, longitude = REGIONS[region]

st.write(
    f"선택한 지역: {region}"
)

st.caption(
    f"분석 좌표: 위도 {latitude}, 경도 {longitude}"
)

st.divider()


st.header("NASA 환경 데이터 분석")

st.caption(
    "분석 기간: 2025년 1월 1일 ~ 2025년 12월 31일"
)


@st.cache_data(ttl=21600)
def load_environment_data(lat, lon):

    return get_nasa_power_data(
        lat,
        lon
    )


try:

    with st.spinner(
        "NASA POWER 데이터를 수집하고 있습니다..."
    ):

        daily_data = load_environment_data(
            latitude,
            longitude
        )

    st.success(
        "NASA POWER 데이터 수집 완료"
    )

    monthly_data = summarize_monthly_environment(
        daily_data
    )

    monthly_rainfall = analyze_monthly_rainfall(
        daily_data
    )

    average_temperature = (
        daily_data["temperature_C"].mean()
    )

    total_precipitation = (
        daily_data["precipitation_mm_day"].sum()
    )

    average_solar = (
        daily_data["solar_kwh_m2_day"].mean()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "연평균 기온",
        f"{average_temperature:.1f} °C"
    )

    col2.metric(
        "연 누적 강수량",
        f"{total_precipitation:.1f} mm"
    )

    col3.metric(
        "일평균 일사량",
        f"{average_solar:.1f} kWh/m²/day"
    )

    st.divider()

    st.subheader("월별 환경 데이터")

    st.dataframe(
        monthly_data,
        use_container_width=True
    )

    st.subheader("월별 평균 기온")

    st.line_chart(
        monthly_data["average_temperature_C"]
    )

    st.subheader("월별 누적 강수량")

    st.bar_chart(
        monthly_data["total_precipitation_mm"]
    )

    st.subheader("월별 평균 일사량")

    st.line_chart(
        monthly_data["average_solar_kwh_m2_day"]
    )

    st.divider()

    st.subheader("월별 강수량 상세 분석")

    st.dataframe(
        monthly_rainfall,
        use_container_width=True
    )

    st.subheader("월별 일평균 강수량")

    st.bar_chart(
        monthly_rainfall["average_daily_rainfall_mm"]
    )

    st.caption(
        "월 누적 강수량과 일평균 강수량을 구분합니다. "
        "강수량은 실제 작물의 수분 공급량이나 "
        "토양 수분량과 같지 않습니다."
    )

    st.caption(
        "자료 출처: NASA POWER. "
        "선택한 대표 좌표의 환경 데이터이며 "
        "실제 농경지의 측정값과 차이가 있을 수 있습니다."
    )

except Exception as error:

    st.error(
        "NASA 환경 데이터를 불러오지 못했습니다."
    )

    st.error(
        f"오류 내용: {error}"
    )

    st.stop()


st.divider()

st.header("작물별 환경 적합성 비교")


try:

    crop_data = load_crop_requirements()

    st.subheader("작물별 온도 적합성 비교")

    temperature_results = compare_crop_temperature(
        daily_data,
        crop_data
    )

    st.write(
        "선택한 지역의 NASA POWER 일별 기온과 "
        "작물별 적정 온도 범위를 비교한 결과입니다."
    )

    st.dataframe(
        temperature_results,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "작물별 적정 온도 범위 일치 비율"
    )

    temperature_chart = (
        temperature_results.set_index("crop")[
            "matching_days_percent"
        ]
    )

    st.bar_chart(
        temperature_chart
    )

    st.caption(
        "온도만을 비교한 기초 지표이며 "
        "실제 작물 수확량이나 종합 재배 적합도를 "
        "의미하지 않습니다."
    )

    st.divider()

    st.subheader("작물별 연간 강수량 비교")

    rainfall_scores = compare_crop_rainfall(
        daily_data,
        crop_data
    )

    st.dataframe(
        rainfall_scores,
        use_container_width=True,
        hide_index=True
    )

    st.subheader(
        "작물별 참고 기준 대비 강수량 차이"
    )

    rainfall_chart = (
        rainfall_scores.set_index("crop")[
            "rainfall_difference_percent"
        ]
    )

    st.bar_chart(
        rainfall_chart
    )

    st.caption(
        "양수는 임시 참고 기준보다 연간 강수량이 많은 경우, "
        "음수는 적은 경우를 의미합니다. "
        "실제 작물의 수분 적합성이나 관개 필요량을 "
        "나타내는 지표는 아닙니다."
    )

    st.warning(
        "작물별 강수량 기준은 시제품용 임시값입니다. "
        "농업적으로 검증된 적정 강수량이 아니므로 "
        "실제 재배 판단에 사용해서는 안 됩니다."
    )

except Exception as error:

    st.error(
        f"작물 환경 분석 중 오류가 발생했습니다: {error}"
    )


st.divider()

st.header("윤작 전략 비교")


try:

    all_strategies = load_rotation_strategies()

    region_strategies = all_strategies[
        all_strategies["region"] == region
    ]

    if region_strategies.empty:

        st.warning(
            f"{region}에 등록된 윤작 전략이 아직 없습니다."
        )

    else:

        st.write(
            f"선택한 지역: {region}"
        )

        st.subheader("전략 설명")

        for _, strategy in region_strategies.iterrows():

            with st.expander(
                strategy["strategy"]
            ):

                st.write(
                    f"작물 순서: "
                    f"{strategy['crop_sequence']}"
                )

                st.write(
                    strategy["description"]
                )

        rotation_results = compare_rotation_temperature(
            daily_data,
            crop_data,
            region_strategies
        )

        render_rotation_ui(
            region,
            rotation_results
        )

        st.caption(
            "윤작 전략은 시제품용 후보입니다. "
            "실제 적용 전 지역별 재배 달력, 논 배수 조건, "
            "토양 특성 및 작물 재배 가능성을 검증해야 합니다."
        )

except Exception as error:

    st.error(
        f"윤작 전략을 불러오지 못했습니다: {error}"
    )


st.divider()

st.caption(
    "FieldShift | NASA Earth observation 기반 농업 의사결정 지원"
)
