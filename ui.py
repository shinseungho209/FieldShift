import streamlit as st
import pandas as pd


def render_rotation_ui(region, rotation_results):

    RISKS = ["온도 조건 일치율"]

    st.header("윤작 전략 비교")

    st.write(
        "현재 재배 방식과 대안 전략 2가지를 비교합니다. "
        "(아래 작은 숫자 = 현재 방식 대비 변화)"
    )

    if rotation_results.empty:
        st.warning("비교할 윤작 전략이 없습니다.")
        return

    names = {}

    for i, (_, strategy) in enumerate(
        rotation_results.iterrows()
    ):
        names[f"strategy_{i}"] = (
            f"{strategy['strategy']}: "
            f"{strategy['crop_sequence']}"
        )

    rows = []

    for i, (_, strategy) in enumerate(
        rotation_results.iterrows()
    ):

        rows.append({
            "전략": names[f"strategy_{i}"],
            "작물 순서": strategy["crop_sequence"],
            "온도 조건 일치율": strategy["temperature_score"],
        })

    df = pd.DataFrame(rows)

    baseline = rows[0]

    cols = st.columns(min(3, len(rows)))

    for i, (col, row) in enumerate(
        zip(cols, rows)
    ):

        with col:

            with st.container(border=True):

                st.subheader(row["전략"])

                st.write(
                    f"작물 순서: {row['작물 순서']}"
                )

                for k in RISKS:

                    diff = (
                        row[k] - baseline[k]
                        if pd.notna(row[k])
                        and pd.notna(baseline[k])
                        else None
                    )

                    st.metric(
                        k,
                        (
                            f"{row[k]:.1f}%"
                            if pd.notna(row[k])
                            else "계산 불가"
                        ),
                        delta=(
                            f"{diff:+.1f}%p"
                            if diff is not None and i != 0
                            else None
                        ),
                        delta_color="normal",
                    )

    st.subheader("한눈에 비교")

    chart_df = df.set_index("전략")[RISKS]

    st.bar_chart(
        chart_df,
        stack=False
    )

    valid_df = df.dropna(
        subset=["온도 조건 일치율"]
    )

    if not valid_df.empty:

        best = valid_df.sort_values(
            "온도 조건 일치율",
            ascending=False
        ).iloc[0]

        base_score = baseline["온도 조건 일치율"]

        score_change = (
            best["온도 조건 일치율"] - base_score
            if pd.notna(base_score)
            else None
        )

        st.info(
            f"온도 지표상 가장 높은 전략: "
            f"{best['전략']}"
        )

        if score_change is not None:

            st.write(
                f"기준 전략 대비 온도 조건 일치율 "
                f"{score_change:+.1f}%p"
            )

        st.caption(
            "이 결과는 온도 지표만을 비교한 것입니다. "
            "종합적인 윤작 추천이나 실제 수확량 예측이 아닙니다."
        )

    with st.expander("상세 표 보기"):

        st.dataframe(
            df,
            hide_index=True,
            width="stretch"
        )

    st.warning(
        "현재 분석은 온도 조건만 반영합니다. "
        "폭염·가뭄·병해충 위험도와 소득지수는 "
        "검증된 데이터 및 모델 확보 후 추가할 예정입니다."
    )
