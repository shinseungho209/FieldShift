import streamlit as st
import pandas as pd

from korean_romanizer.romanizer import Romanizer

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

from translations import t, translate_columns


st.set_page_config(
    page_title="FieldShift",
    page_icon="🌱",
    layout="wide"
)


# --------------------------------------------------
# Language
# --------------------------------------------------

if "language" not in st.session_state:
    st.session_state["language"] = "en"

top_left, top_right = st.columns([6, 2])

with top_right:
    selected_language = st.radio(
        "Language",
        options=["한국어", "English"],
        index=(
            0 if st.session_state["language"] == "ko" else 1
        ),
        horizontal=True,
        label_visibility="collapsed"
    )

    st.session_state["language"] = (
        "ko" if selected_language == "한국어" else "en"
    )

language = st.session_state["language"]


# --------------------------------------------------
# Administrative name translations
# --------------------------------------------------

PROVINCE_EN = {
    "서울특별시": "Seoul",
    "부산광역시": "Busan",
    "대구광역시": "Daegu",
    "인천광역시": "Incheon",
    "광주광역시": "Gwangju",
    "대전광역시": "Daejeon",
    "울산광역시": "Ulsan",
    "세종특별자치시": "Sejong Special Self-Governing City",
    "세중특별자치시": "Sejong Special Self-Governing City",
    "경기도": "Gyeonggi-do",
    "강원도": "Gangwon-do",
    "충청북도": "Chungcheongbuk-do",
    "충청남도": "Chungcheongnam-do",
    "전라북도": "Jeonbuk State",
    "전라남도": "Jeollanam-do",
    "경상북도": "Gyeongsangbuk-do",
    "경상남도": "Gyeongsangnam-do",
    "제주도": "Jeju-do"
}

SPECIAL_DISTRICTS_EN = {
    "세종특별자치시": "Sejong Special Self-Governing City"
}

AGRICULTURE_EN = {
    "농업미미지역": "Limited agricultural activity",
    "복합농업": "Mixed farming",
    "논농업": "Paddy farming",
    "밭농업": "Dry-field farming",
    "시설농업": "Protected agriculture",
    "과수농업": "Fruit farming",
    "고랭지농업": "Highland agriculture"
}


def romanize_region_name(value, field):
    """
    Convert Korean administrative names into English display names.
    Original Korean values remain unchanged in the dataframe.
    """

    value = str(value).strip()

    if field == "sido":
        if value in PROVINCE_EN:
            return PROVINCE_EN[value]

        return Romanizer(value).romanize().title()

    if value in SPECIAL_DISTRICTS_EN:
        return SPECIAL_DISTRICTS_EN[value]

    suffixes = [
        ("특별자치시", "Special Self-Governing City"),
        ("특별자치도", "Special Self-Governing Province"),
        ("광역시", "Metropolitan City"),
        ("특별시", "Special City"),
        ("자치시", "Autonomous City"),
        ("자치구", "Autonomous District"),
        ("시", "si"),
        ("군", "gun"),
        ("구", "gu")
    ]

    for korean_suffix, english_suffix in suffixes:
        if value.endswith(korean_suffix):
            base = value[:-len(korean_suffix)]

            if not base:
                break

            romanized_base = (
                Romanizer(base).romanize().title()
            )

            if english_suffix in [
                "Special Self-Governing City",
                "Special Self-Governing Province",
                "Metropolitan City",
                "Special City",
                "Autonomous City",
                "Autonomous District"
            ]:
                return f"{romanized_base} {english_suffix}"

            return f"{romanized_base}-{english_suffix}"

    return Romanizer(value).romanize().title()


def translate_agriculture_type(value, language):
    value = str(value).strip()

    if language == "ko":
        return value

    return AGRICULTURE_EN.get(value, value)


# --------------------------------------------------
# Data loading
# --------------------------------------------------

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
            f"Missing required columns in regional CSV: {missing}"
        )

    regions["sido"] = (
        regions["sido"]
        .astype(str)
        .str.strip()
        .replace({
            "세중특별자치시": "세종특별자치시"
        })
    )

    regions["sigungu"] = (
        regions["sigungu"]
        .astype(str)
        .str.strip()
    )

    regions["agriculture_type"] = (
        regions["agriculture_type"]
        .astype(str)
        .str.strip()
    )

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


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("🌱 FieldShift")

st.subheader(t(language, "subtitle"))
st.write(t(language, "description"))
st.caption(t(language, "prototype"))


# --------------------------------------------------
# Region selection
# --------------------------------------------------

try:
    regions = load_regions()

except Exception as error:
    st.error(
        f"{t(language, 'region_load_failed')}: {error}"
    )
    st.stop()


st.header(t(language, "region_section"))

col1, col2 = st.columns(2)

sido_list = sorted(
    regions["sido"].dropna().unique().tolist(),
    key=lambda value: (
        romanize_region_name(value, "sido")
        if language == "en"
        else value
    )
)

with col1:
    selected_sido = st.selectbox(
        t(language, "province"),
        sido_list,
        format_func=lambda value: (
            romanize_region_name(value, "sido")
            if language == "en"
            else value
        )
    )

filtered_regions = regions[
    regions["sido"] == selected_sido
]

sigungu_list = sorted(
    filtered_regions["sigungu"].dropna().unique().tolist(),
    key=lambda value: (
        romanize_region_name(value, "sigungu")
        if language == "en"
        else value
    )
)

with col2:
    selected_sigungu = st.selectbox(
        t(language, "district"),
        sigungu_list,
        format_func=lambda value: (
            romanize_region_name(value, "sigungu")
            if language == "en"
            else value
        )
    )


selected_region = filtered_regions[
    filtered_regions["sigungu"] == selected_sigungu
].iloc[0]


latitude = float(selected_region["latitude"])
longitude = float(selected_region["longitude"])

if language == "en":
    display_sido = romanize_region_name(
        selected_sido,
        "sido"
    )

    display_sigungu = romanize_region_name(
        selected_sigungu,
        "sigungu"
    )
else:
    display_sido = selected_sido
    display_sigungu = selected_sigungu


display_region_name = (
    f"{display_sido} {display_sigungu}"
)

agriculture_type = translate_agriculture_type(
    selected_region["agriculture_type"],
    language
)


st.info(
    f"{t(language, 'selected_region')}: "
    f"{display_region_name}\n\n"
    f"{t(language, 'agriculture_type')}: "
    f"{agriculture_type}\n\n"
    f"{t(language, 'coordinates')}: "
    f"{latitude:.4f}, {longitude:.4f}\n\n"
    f"{t(language, 'registered_regions')}: "
    f"{len(regions)}"
)


# --------------------------------------------------
# NASA environmental data
# --------------------------------------------------

st.header(t(language, "environment_section"))

date_col1, date_col2 = st.columns(2)

with date_col1:
    start_date = st.date_input(
        t(language, "start_date"),
        value=pd.Timestamp("2025-01-01").date()
    )

with date_col2:
    end_date = st.date_input(
        t(language, "end_date"),
        value=pd.Timestamp("2025-12-31").date()
    )


if start_date > end_date:
    st.error(t(language, "invalid_dates"))
    st.stop()


start_text = start_date.strftime("%Y%m%d")
end_text = end_date.strftime("%Y%m%d")


with st.spinner(t(language, "fetching")):
    try:
        daily_data = load_nasa_data(
            latitude,
            longitude,
            start_text,
            end_text
        )

    except Exception as error:
        st.error(
            f"{t(language, 'fetch_failed')}: {error}"
        )
        st.stop()


if daily_data.empty:
    st.error(t(language, "no_data"))
    st.stop()


st.success(t(language, "fetch_success"))

st.caption(
    f"{t(language, 'period')}: "
    f"{start_date} ~ {end_date}"
)


# --------------------------------------------------
# Environmental metrics
# --------------------------------------------------

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
        t(language, "annual_temperature"),
        (
            f"{valid_temperature.mean():.1f} °C"
            if not valid_temperature.empty
            else t(language, "no_value")
        )
    )

with metric_cols[1]:
    display_metric(
        t(language, "rainfall"),
        (
            f"{valid_rainfall.sum():.1f} mm"
            if not valid_rainfall.empty
            else t(language, "no_value")
        )
    )

with metric_cols[2]:
    display_metric(
        t(language, "solar"),
        (
            f"{valid_solar.mean():.2f} kWh/m²/day"
            if not valid_solar.empty
            else t(language, "no_value")
        )
    )


# --------------------------------------------------
# Monthly environmental charts
# --------------------------------------------------

st.subheader(t(language, "monthly_environment"))

monthly_environment = summarize_monthly_environment(
    daily_data
)

monthly_columns = {
    "average_temperature_C": t(
        language,
        "monthly_temperature"
    ),
    "total_precipitation_mm": t(
        language,
        "monthly_rainfall"
    ),
    "average_solar_kwh_m2_day": t(
        language,
        "monthly_solar"
    )
}

st.write(t(language, "monthly_temperature"))

st.line_chart(
    monthly_environment[
        ["average_temperature_C"]
    ].rename(columns=monthly_columns)
)

st.write(t(language, "monthly_rainfall"))

st.bar_chart(
    monthly_environment[
        ["total_precipitation_mm"]
    ].rename(columns=monthly_columns)
)

st.write(t(language, "monthly_solar"))

st.line_chart(
    monthly_environment[
        ["average_solar_kwh_m2_day"]
    ].rename(columns=monthly_columns)
)


# --------------------------------------------------
# Rainfall analysis
# --------------------------------------------------

st.subheader(t(language, "rainfall_detail"))

rainfall_detail = analyze_monthly_rainfall(
    daily_data
)

if not rainfall_detail.empty:

    st.bar_chart(
        rainfall_detail[
            ["average_daily_rainfall_mm"]
        ].rename(
            columns={
                "average_daily_rainfall_mm":
                t(language, "monthly_rainfall")
            }
        )
    )

    with st.expander(t(language, "rainfall_table")):
        st.dataframe(
            translate_columns(
                rainfall_detail,
                language
            ),
            use_container_width=True
        )

else:
    st.warning(t(language, "no_rainfall"))

st.caption(t(language, "rainfall_warning"))
st.caption(t(language, "nasa_source"))


# --------------------------------------------------
# Crop analysis
# --------------------------------------------------

st.header(t(language, "crop_section"))

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
    st.error(
        f"{t(language, 'crop_failed')}: {error}"
    )
    st.stop()


# --------------------------------------------------
# Crop temperature comparison
# --------------------------------------------------

st.subheader(t(language, "temperature_comparison"))

temperature_chart = temperature_results.dropna(
    subset=["matching_days_percent"]
).copy()

if language == "en" and "crop_en" in crop_data.columns:
    crop_name_map = (
        crop_data[["crop", "crop_en"]]
        .dropna()
        .drop_duplicates("crop")
        .set_index("crop")["crop_en"]
        .to_dict()
    )

    temperature_chart["crop_display"] = (
        temperature_chart["crop"]
        .map(crop_name_map)
        .fillna(temperature_chart["crop"])
    )
else:
    temperature_chart["crop_display"] = (
        temperature_chart["crop"]
    )


temperature_chart = temperature_chart.set_index(
    "crop_display"
)[
    ["matching_days_percent"]
].sort_values(
    "matching_days_percent",
    ascending=True
)


if not temperature_chart.empty:

    st.bar_chart(
        temperature_chart.rename(
            columns={
                "matching_days_percent":
                t(language, "temperature_match")
            }
        ),
        horizontal=True
    )

else:
    st.warning(t(language, "no_temperature"))


st.caption(t(language, "temperature_explanation"))
st.warning(t(language, "temperature_warning"))


with st.expander(t(language, "temperature_table")):
    st.dataframe(
        translate_columns(
            temperature_results,
            language
        ),
        use_container_width=True,
        hide_index=True
    )


with st.expander(t(language, "crop_rainfall_table")):
    st.dataframe(
        translate_columns(
            rainfall_results,
            language
        ),
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Rotation candidates
# --------------------------------------------------

st.header(t(language, "rotation_section"))

rotation_results = generate_rotation_candidates(
    temperature_results,
    crop_data,
    max_candidates=30,
    language=language
)


if language == "en" and not rotation_results.empty:

    required_english_columns = [
        "strategy_en",
        "crop_sequence_en",
        "water_requirement_en",
        "soil_condition_en",
        "analysis_status_en"
    ]

    missing_columns = [
        column
        for column in required_english_columns
        if column not in rotation_results.columns
    ]

    if missing_columns:
        st.warning(
            "Some English candidate fields are missing: "
            + ", ".join(missing_columns)
        )


render_rotation_ui(
    display_region_name,
    rotation_results,
    language
)


# --------------------------------------------------
# Data limitations
# --------------------------------------------------

st.header(t(language, "additional_section"))

render_data_limitations(language)


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(t(language, "footer"))

st.caption(
    f"{t(language, 'period')}: "
    f"{start_date} ~ {end_date}"
)

st.caption(t(language, "final_note"))