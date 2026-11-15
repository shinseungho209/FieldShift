import streamlit as st
import pandas as pd

from translations import t, translate_columns


@st.cache_data
def load_crop_translation():
    try:
        crop_data = pd.read_csv(
            "data/crop_requirements.csv",
            encoding="utf-8-sig"
        )

        if "crop" not in crop_data.columns:
            return {}

        translation = {}

        for _, row in crop_data.iterrows():
            korean = str(row.get("crop", "")).strip()
            english = str(row.get("crop_en", "")).strip()

            if not korean or korean == "nan":
                continue

            translation[korean] = {
                "crop": (
                    english
                    if english and english != "nan"
                    else korean
                )
            }

        return translation

    except (
        FileNotFoundError,
        pd.errors.ParserError,
        UnicodeDecodeError
    ):
        return {}


def safe_text(value, language="ko"):
    fallback = "No data" if language == "en" else "자료 없음"

    if value is None:
        return fallback

    try:
        if pd.isna(value):
            return fallback
    except (TypeError, ValueError):
        pass

    text = str(value).strip()

    if not text or text.lower() in {"nan", "none", "null"}:
        return fallback

    text = text.replace("~~", "～")
    text = text.replace("~", "～")

    return text


def translate_crop_names(value, crop_translation):
    text = str(value)

    for korean, data in crop_translation.items():
        text = text.replace(
            korean,
            data["crop"]
        )

    return text


def get_display_value(
    row,
    korean_column,
    english_column,
    language
):
    if language == "en" and english_column in row.index:
        value = row[english_column]

        if pd.notna(value) and str(value).strip():
            return safe_text(value, language)

    if korean_column in row.index:
        return safe_text(
            row[korean_column],
            language
        )

    return "No data" if language == "en" else "자료 없음"


def get_language_value(
    row,
    korean_column,
    english_column,
    language,
    crop_translation=None
):
    value = get_display_value(
        row,
        korean_column,
        english_column,
        language
    )

    if (
        language == "en"
        and crop_translation is not None
        and value not in {"No data", "자료 없음"}
    ):
        value = translate_crop_names(
            value,
            crop_translation
        )

    return value


def get_strategy_label(row, language, crop_translation):
    if language == "en":
        value = get_display_value(
            row,
            "strategy",
            "strategy_en",
            language
        )

        return translate_crop_names(
            value,
            crop_translation
        )

    return safe_text(
        row.get("strategy"),
        language
    )


def get_crop_sequence(row, language, crop_translation):
    value = get_language_value(
        row,
        "crop_sequence",
        "crop_sequence_en",
        language,
        crop_translation
    )

    return value


def get_calendar_status(row, language):
    return get_language_value(
        row,
        "calendar_status",
        "calendar_status_en",
        language
    )


def get_analysis_status(row, language):
    return get_language_value(
        row,
        "analysis_status",
        "analysis_status_en",
        language
    )


def get_confidence(row, korean_column, english_column, language):
    value = get_language_value(
        row,
        korean_column,
        english_column,
        language
    )

    if language == "en":
        replacements = {
            "잠정": "Preliminary",
            "부분검증": "Partially verified",
            "부분 검증": "Partially verified",
            "검증됨": "Verified",
            "자료 확인 필요": "Data verification required",
            "미검증": "Unverified",
            "높음": "High",
            "중간": "Medium",
            "낮음": "Low"
        }

        for korean, english in replacements.items():
            value = value.replace(korean, english)

    return value


def get_chart_label(row, language, crop_translation):
    sequence = get_crop_sequence(
        row,
        language,
        crop_translation
    )

    if language == "en":
        return sequence

    return sequence


def render_rotation_ui(
    region,
    rotation_results,
    language="ko"
):
    labels = t(language, "rotation_ui")
    crop_translation = load_crop_translation()

    st.subheader(labels["title"])

    if rotation_results.empty:
        st.warning(labels["empty"])
        return

    if language == "en":
        st.caption(
            f"Candidates for {region} based on NASA climate data "
            "and crop requirements."
        )
    else:
        st.caption(
            f"{region}{labels['description']}"
        )

    st.info(labels["score_info"])

    for _, row in rotation_results.iterrows():

        with st.container(border=True):

            strategy = get_strategy_label(
                row,
                language,
                crop_translation
            )

            st.subheader(
                f"{int(row['rank'])}. {strategy}"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                labels["temperature_score"],
                f"{float(row['temperature_score']):.1f}%"
            )

            col2.metric(
                labels["crop_count"],
                (
                    str(int(row["crop_count"]))
                    if language == "en"
                    else f"{int(row['crop_count'])}개"
                )
            )

            crop_sequence = get_crop_sequence(
                row,
                language,
                crop_translation
            )

            st.write(
                f"{labels['crop_sequence']}: {crop_sequence}"
            )

            calendar_status = get_calendar_status(
                row,
                language
            )

            st.caption(
                f"{labels['calendar']}: {calendar_status}"
            )

            temperature_confidence = get_confidence(
                row,
                "temperature_confidence",
                "temperature_confidence_en",
                language
            )

            st.caption(
                f"{labels['temperature_confidence']}: "
                f"{temperature_confidence}"
            )

            calendar_confidence = get_confidence(
                row,
                "calendar_confidence",
                "calendar_confidence_en",
                language
            )

            st.caption(
                f"{labels['calendar_confidence']}: "
                f"{calendar_confidence}"
            )

            st.write(labels["water"])

            water_value = get_language_value(
                row,
                "water_requirement",
                "water_requirement_en",
                language,
                crop_translation
            )

            st.write(water_value)

            st.write(labels["soil"])

            soil_value = get_language_value(
                row,
                "soil_condition",
                "soil_condition_en",
                language,
                crop_translation
            )

            st.write(soil_value)

            analysis_status = get_analysis_status(
                row,
                language
            )

            st.caption(
                f"{labels['evaluation']}: {analysis_status}"
            )

            notes_value = get_language_value(
                row,
                "notes",
                "notes_en",
                language,
                crop_translation
            )

            if notes_value not in {
                "자료 없음",
                "No data"
            }:
                with st.expander(labels["notes"]):
                    st.write(notes_value)

    st.subheader(labels["chart"])

    chart_rows = []

    for _, row in rotation_results.iterrows():
        chart_rows.append({
            "strategy": get_chart_label(
                row,
                language,
                crop_translation
            ),
            "score": float(row["ranking_score"])
        })

    chart_data = pd.DataFrame(chart_rows)

    chart_data = chart_data.set_index(
        "strategy"
    )

    chart_data = chart_data.rename(
        columns={
            "score": labels["temperature_score"]
        }
    )

    st.bar_chart(
        chart_data,
        horizontal=True
    )

    with st.expander(labels["table"]):

        display_data = rotation_results.copy()

        if language == "en":

            display_data["strategy"] = display_data.apply(
                lambda row: get_strategy_label(
                    row,
                    language,
                    crop_translation
                ),
                axis=1
            )

            display_data["crop_sequence"] = display_data.apply(
                lambda row: get_crop_sequence(
                    row,
                    language,
                    crop_translation
                ),
                axis=1
            )

            column_pairs = [
                ("calendar_status", "calendar_status_en"),
                (
                    "temperature_confidence",
                    "temperature_confidence_en"
                ),
                (
                    "calendar_confidence",
                    "calendar_confidence_en"
                ),
                ("water_requirement", "water_requirement_en"),
                ("soil_condition", "soil_condition_en"),
                ("analysis_status", "analysis_status_en"),
                ("notes", "notes_en")
            ]

            for korean_column, english_column in column_pairs:
                if english_column in display_data.columns:
                    display_data[korean_column] = display_data[
                        english_column
                    ].where(
                        display_data[english_column].notna()
                        & display_data[english_column].astype(str).str.strip().ne(""),
                        display_data[korean_column]
                    )

        else:
            display_data["strategy"] = display_data[
                "strategy"
            ].apply(
                lambda value: safe_text(value, language)
            )

            display_data["crop_sequence"] = display_data[
                "crop_sequence"
            ].apply(
                lambda value: safe_text(value, language)
            )

        hidden_english_columns = [
            "strategy_en",
            "crop_sequence_en",
            "calendar_status_en",
            "temperature_confidence_en",
            "calendar_confidence_en",
            "water_requirement_en",
            "soil_condition_en",
            "analysis_status_en",
            "notes_en"
        ]

        display_data = display_data.drop(
            columns=[
                column
                for column in hidden_english_columns
                if column in display_data.columns
            ],
            errors="ignore"
        )

        display_data = translate_columns(
            display_data,
            language
        )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

    st.warning(labels["warning"])


def render_data_limitations(language="ko"):

    labels = t(language, "limitations")

    st.subheader(labels["title"])

    rows = [
        {
            labels["item"]: labels["temperature"],
            labels["status"]: labels["temperature_status"]
        },
        {
            labels["item"]: labels["rainfall"],
            labels["status"]: labels["rainfall_status"]
        },
        {
            labels["item"]: labels["solar"],
            labels["status"]: labels["solar_status"]
        },
        {
            labels["item"]: labels["elevation"],
            labels["status"]: labels["elevation_status"]
        },
        {
            labels["item"]: labels["slope"],
            labels["status"]: labels["slope_status"]
        },
        {
            labels["item"]: labels["soil_moisture"],
            labels["status"]: labels["soil_moisture_status"]
        },
        {
            labels["item"]: labels["soil_health"],
            labels["status"]: labels["soil_health_status"]
        },
        {
            labels["item"]: labels["calendar"],
            labels["status"]: labels["calendar_status"]
        },
        {
            labels["item"]: labels["preferences"],
            labels["status"]: labels["preferences_status"]
        },
        {
            labels["item"]: labels["yield"],
            labels["status"]: labels["yield_status"]
        }
    ]

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )