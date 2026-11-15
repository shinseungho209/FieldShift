import streamlit as st
import pandas as pd

from nasa_data import get_nasa_power_data

from analysis import (
    load_crop_requirements,
    summarize_monthly_environment,
    analyze_monthly_rainfall,
    compare_crop_temperature,
    compare_crop_rainfall,
    generate_rotation_candidates
)

from ui import (
    render_rotation_ui,
    render_data_limitations
)


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
    "NASA 지구관측 데이터와 지역 농업 정보를 활용해 "
    "기후변화에 대응하는 작물 재배 및 윤작 전략을 탐색합니다."
)

st.caption(
    "현재 버전은 기후와 작물의 온도 조건을 중심으로 분석하는 초기 시제품입니다."
)


@st.cache_data(ttl=21600)
def load_regions():
    regions = pd.read_csv(
        "data/regions_national.csv",
        encoding="utf-8-sig"
    )

    required = [
        "sido",
        "sigungu",
        "latitude",
        "longitude",
        "agriculture_type"
    ]

    missing = [
        column
        for column in required
        if column not in regions.columns
    ]

    if missing:
        raise ValueError(
            f"지역 CSV에 필요한 열이 없습니다: {missing}"
        )

    regions["sido"] = regions["sido"].astype(str).str.strip()
    regions["sigungu"] = regions["sigungu"].astype(str).str.strip()

    regions["latitude"] = pd.to_numeric(
        regions["latitude"],
        errors="coerce"
    )

    regions["longitude"] = pd.to_numeric(
        regions["longitude"],
        errors="coerce"
    )

    regions = regions.dropna(
        subset=["latitude", "longitude"]
    )

    return regions.reset_index(drop=True)


@st.cache_data(ttl=21600)
def load_nasa_data(latitude, longitude, start_date, end_date):
    return get_nasa_power_data(
        latitude,
        longitude,
        start_date,
        end_date
    )


def display_metric(label, value, help_text=None):
    st.metric(
        label,
        value,
        help=help_text
    )


try:
    regions = load_regions()
except Exception as error:
    st.error(f"지역 데이터 로드 실패: {error}")
    st.stop()


st.header("1. 지역 선택")

col1, col2 = st.columns(2)

sido_list = sorted(
    regions["sido"].dropna().unique().tolist()
)

with col1:
    selected_sido = st.selectbox(
        "① 도 또는 광역시",
        sido_list
    )

filtered_regions = regions[
    regions["sido"] == selected_sido
]

sigungu_list = sorted(
    filtered_regions["sigungu"].dropna().unique().tolist()
)

with col2:
    selected_sigungu = st.selectbox(
        "② 시·군·구",
        sigungu_list
    )

selected_region = filtered_regions[
    filtered_regions["sigungu"] == selected_sigungu
].iloc[0]

latitude = float(selected_region["latitude"])
longitude = float(selected_region["longitude"])
agriculture_type = str(selected_region["agriculture_type"])

region_name = f"{selected_sido} {selected_sigungu}"

st.info(
    f"선택한 지역: {region_name}\n\n"
    f"농업 유형: {agriculture_type}\n\n"
    f"분석 좌표: 위도 {latitude:.4f}, 경도 {longitude:.4f}\n\n"
    f"등록된 지역 수: {len(regions)}개"
)


st.header("2. NASA 환경 데이터 분석")

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        "분석 시작일",
        value=pd.Timestamp("2025-01-01").date()
    )

with date_col2:
    end_date = st.date_input(
        "분석 종료일",
        value=pd.Timestamp("2025-12-31").date()
    )

if start_date > end_date:
    st.error("분석 시작일은 종료일보다 늦을 수 없습니다.")
    st.stop()

start_text = start_date.strftime("%Y%m%d")
end_text = end_date.strftime("%Y%m%d")

with st.spinner("NASA POWER 환경 데이터를 수집하고 있습니다..."):
    try:
        daily_data = load_nasa_data(
            latitude,
            longitude,
            start_text,
            end_text
        )
    except Exception as error:
        st.error(
            f"NASA POWER 데이터 수집에 실패했습니다: {error}"
        )
        st.stop()

if daily_data.empty:
    st.error("수집된 환경 데이터가 없습니다.")
    st.stop()

st.success("NASA POWER 데이터 수집 완료")

st.caption(
    f"분석 기간: {start_date} ~ {end_date}"
)

valid_temperature = daily_data[
    "temperature_C"
].dropna()

valid_rainfall = daily_data[
    "precipitation_mm_day"
].dropna()

valid_solar = daily_data[
    "solar_kwh_m2_day"
].dropna()

metric_cols = st.columns(3)

with metric_cols[0]:
    display_metric(
        "연평균 기온",
        (
            f"{valid_temperature.mean():.1f} °C"
            if not valid_temperature.empty
            else "자료 없음"
        )
    )

with metric_cols[1]:
    display_metric(
        "누적 강수량",
        (
            f"{valid_rainfall.sum():.1f} mm"
            if not valid_rainfall.empty
            else "자료 없음"
        )
    )

with metric_cols[2]:
    display_metric(
        "일평균 일사량",
        (
            f"{valid_solar.mean():.2f} kWh/m²/day"
            if not valid_solar.empty
            else "자료 없음"
        )
    )

st.subheader("월별 환경 데이터")

monthly_environment = summarize_monthly_environment(
    daily_data
)

st.write("월별 평균 기온")
st.line_chart(
    monthly_environment[
        ["average_temperature_C"]
    ]
)

st.write("월별 누적 강수량")
st.bar_chart(
    monthly_environment[
        ["total_precipitation_mm"]
    ]
)

st.write("월별 평균 일사량")
st.line_chart(
    monthly_environment[
        ["average_solar_kwh_m2_day"]
    ]
)

st.subheader("월별 강수량 상세 분석")

rainfall_detail = analyze_monthly_rainfall(
    daily_data
)

if not rainfall_detail.empty:
    st.bar_chart(
        rainfall_detail[
            ["average_daily_rainfall_mm"]
        ]
    )

    with st.expander("월별 강수량 표 보기"):
        st.dataframe(
            rainfall_detail,
            use_container_width=True
        )
else:
    st.warning("강수량 데이터가 없습니다.")

st.caption(
    "강수량은 실제 토양 수분이나 작물이 이용할 수 있는 수분량과 같지 않습니다."
)

st.caption(
    "자료 출처: NASA POWER. 선택한 지역의 대표 좌표를 기준으로 한 데이터이며 "
    "실제 농경지 측정값과 차이가 있을 수 있습니다."
)


st.header("3. 작물별 환경 적합성 분석")

try:
    crop_data = load_crop_requirements(
        "data/crop_requirements.csv"
    )

    temperature_results = compare_crop_temperature(
        daily_data,
        crop_data
    )

    rainfall_results = compare_crop_rainfall(
        daily_data,
        crop_data
    )

except Exception as error:
    st.error(f"작물 분석에 실패했습니다: {error}")
    st.stop()


st.subheader("작물별 온도 조건 비교")

temperature_chart = temperature_results.dropna(
    subset=["matching_days_percent"]
).set_index("crop")[
    ["matching_days_percent"]
].sort_values(
    "matching_days_percent",
    ascending=True
)

if not temperature_chart.empty:
    st.bar_chart(
        temperature_chart,
        horizontal=True
    )
else:
    st.warning("온도 조건을 비교할 수 있는 작물이 없습니다.")

st.caption(
    "온도 조건 일치율은 해당 작물의 재배 기간 중 일평균 기온이 "
    "입력된 온도 범위에 들어온 날의 비율입니다."
)

st.warning(
    "작물별 온도 범위는 초기 비교 기준입니다. 생육 단계별 온도 차이, "
    "품종, 실제 재배 환경을 모두 반영하지 않으며 수확량이나 "
    "종합 재배 적합도를 의미하지 않습니다."
)

with st.expander("작물별 온도 분석 데이터"):
    st.dataframe(
        temperature_results,
        use_container_width=True,
        hide_index=True
    )

with st.expander("작물별 재배 기간 강수량"):
    st.dataframe(
        rainfall_results,
        use_container_width=True,
        hide_index=True
    )


st.header("4. 윤작 전략 자동 생성")

rotation_results = generate_rotation_candidates(
    temperature_results,
    crop_data,
    max_candidates=30
)

render_rotation_ui(
    region_name,
    rotation_results
)


st.header("5. 추가 데이터 연결 현황")

render_data_limitations()


st.divider()

st.caption(
    "FieldShift | NASA Earth observation 기반 농업 의사결정 지원"
)

st.caption(
    f"현재 분석은 {start_date}부터 {end_date}까지의 "
    "대표 좌표 환경 데이터를 사용합니다."
)

st.caption(
    "실제 농업 적용 전 지역별 토양 특성, 재배 달력, 작물 생육 조건 "
    "및 농민의 재배 목표를 추가로 검증해야 합니다."
)