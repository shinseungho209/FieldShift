import streamlit as st


def get_farmer_preferences():
    st.subheader("농민의 재배 우선순위")

    st.caption(
        "현재 데이터로 계산할 수 없는 항목은 "
        "전략 점수에 반영하지 않습니다."
    )

    climate_weight = st.slider(
        "기후 적합성 중요도",
        min_value=0,
        max_value=100,
        value=60
    )

    water_weight = st.slider(
        "물 관리 중요도",
        min_value=0,
        max_value=100,
        value=20
    )

    soil_weight = st.slider(
        "토양 건강 중요도",
        min_value=0,
        max_value=100,
        value=20
    )

    return {
        "climate": climate_weight,
        "water": water_weight,
        "soil": soil_weight
    }