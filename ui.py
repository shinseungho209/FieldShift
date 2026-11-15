import streamlit as st
import pandas as pd


def safe_text(value):
    if pd.isna(value):
        return "자료 없음"

    text = str(value)

    text = text.replace("~~", "～")
    text = text.replace("~", "～")

    return text


def render_rotation_ui(region, rotation_results):
    st.subheader("자동 생성된 재배 전략 후보")

    if rotation_results.empty:
        st.warning(
            "현재 데이터 조건에서 생성된 후보가 없습니다."
        )
        return

    st.caption(
        f"{region}의 NASA 기후 데이터와 작물 조건을 활용한 후보입니다."
    )

    st.info(
        "기온 기반 순위 점수는 재배 기간의 일평균 기온이 "
        "입력된 온도 범위에 들어온 날의 비율입니다. "
        "수확량이나 실제 재배 성공 확률을 뜻하지 않습니다."
    )

    for _, row in rotation_results.iterrows():

        with st.container(border=True):

            st.subheader(
                f"{int(row['rank'])}위 · {row['strategy']}"
            )

            col1, col2 = st.columns(2)

            col1.metric(
                "온도 조건 일치율",
                f"{row['temperature_score']:.1f}%"
            )

            col2.metric(
                "포함 작물 수",
                f"{int(row['crop_count'])}개"
            )

            st.write(
                f"작물 조합: {safe_text(row['crop_sequence'])}"
            )

            st.caption(
                f"재배 일정: {safe_text(row['calendar_status'])}"
            )

            st.caption(
                f"온도 기준 신뢰도: "
                f"{safe_text(row['temperature_confidence'])}"
            )

            st.caption(
                f"재배 달력 신뢰도: "
                f"{safe_text(row['calendar_confidence'])}"
            )

            st.write("물 요구 특성")

            st.write(
                safe_text(row["water_requirement"])
            )

            st.write("토양 조건")

            st.write(
                safe_text(row["soil_condition"])
            )

            st.caption(
                f"평가 방식: {safe_text(row['analysis_status'])}"
            )

            notes = safe_text(row.get("notes", ""))

            if notes and notes != "자료 없음":
                with st.expander("작물별 참고 사항"):
                    st.write(notes)

    st.subheader("전략별 기온 기반 점수 비교")

    chart_data = rotation_results[
        ["strategy", "ranking_score"]
    ].copy()

    chart_data = chart_data.set_index("strategy")

    st.bar_chart(
        chart_data,
        horizontal=True
    )

    with st.expander("전체 후보 데이터 보기"):

        display_data = rotation_results.copy()

        text_columns = [
            "strategy",
            "crop_sequence",
            "calendar_status",
            "temperature_confidence",
            "calendar_confidence",
            "water_requirement",
            "soil_condition",
            "analysis_status",
            "notes"
        ]

        for column in text_columns:
            if column in display_data.columns:
                display_data[column] = (
                    display_data[column].apply(safe_text)
                )

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True
        )

    st.warning(
        "현재 순위는 기온 조건과 월별 재배 일정에 기반합니다. "
        "강수량은 참고 정보이며 토양 수분, 토양 건강, 병해충, "
        "경제성, 실제 수확량은 점수에 포함하지 않습니다."
    )


def render_data_limitations():
    st.subheader("데이터 연결 및 분석 한계")

    rows = [
        {
            "평가 항목": "기온",
            "현재 상태": "NASA POWER 일별 기온으로 비교"
        },
        {
            "평가 항목": "강수량",
            "현재 상태": "NASA POWER 일별 및 재배 기간 누적값"
        },
        {
            "평가 항목": "일사량",
            "현재 상태": "NASA POWER 일별 일사량"
        },
        {
            "평가 항목": "고도",
            "현재 상태": "별도 고도 데이터의 출처와 정확도 확인 필요"
        },
        {
            "평가 항목": "경사도",
            "현재 상태": "여러 지점의 고도 자료로 계산 필요"
        },
        {
            "평가 항목": "토양 수분",
            "현재 상태": "토양 수분 관측 또는 위성 자료 연결 필요"
        },
        {
            "평가 항목": "토양 건강",
            "현재 상태": "토양 유기물, pH, 배수성 자료 필요"
        },
        {
            "평가 항목": "재배 달력",
            "현재 상태": "대표 작형 기준이며 지역별 검증 필요"
        },
        {
            "평가 항목": "농민 우선순위",
            "현재 상태": "수익성, 물 절약, 안정성 등 선택 기준 추가 필요"
        },
        {
            "평가 항목": "수확량",
            "현재 상태": "수확량 예측 모델 미구현"
        }
    ]

    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True,
        hide_index=True
    )