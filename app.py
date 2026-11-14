
import streamlit as st

st.set_page_config(
    page_title="FieldShift",
    page_icon="🌱",
    layout="wide"
)

st.title("FieldShift")
st.subheader("NASA 데이터를 활용한 농업 의사결정 지원 플랫폼")

st.write(
    "대한민국 지역별 환경 데이터를 분석하고 "
    "작물 윤작 전략을 비교하는 서비스입니다."
)

st.divider()

st.header("지역 선택")

region = st.selectbox(
    "분석할 지역을 선택하세요",
    [
        "전북특별자치도 김제시",
        "전라남도 해남군",
        "강원특별자치도 평창군",
        "경상북도 안동시",
        "충청남도 논산시"
    ]
)

st.write(f"선택한 지역: **{region}**")

st.info(
    "다음 단계에서 NASA 환경 데이터를 연결할 예정입니다."
)

st.header("분석할 환경 요소")

col1, col2, col3 = st.columns(3)

col1.metric("기온", "데이터 연결 예정")
col2.metric("강수량", "데이터 연결 예정")
col3.metric("토양 수분", "데이터 연결 예정")

st.divider()

st.header("윤작 전략 비교")

st.write("현재 재배 방식과 대안 전략 2가지를 비교할 예정입니다.")

st.caption(
    "FieldShift | NASA Earth observation 기반 농업 의사결정 지원"
)
