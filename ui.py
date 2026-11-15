import streamlit as st
import pandas as pd

SCORE = "온도 조건 일치율"


def _format_percent(value):
    return f"{value:.1f}%" if pd.notna(value) else "계산 불가"


def render_rotation_ui(region, rotation_results):
    """
    윤작 전략 비교 화면.
    첫 번째 행을 '현재 방식(기준)'으로 보고, 나머지 전략과 비교한다.
    제목(st.header)은 app.py 에서 이미 표시하므로 여기서는 만들지 않는다.
    """

    if rotation_results.empty:
        st.warning("비교할 윤작 전략이 없습니다.")
        return

    df = pd.DataFrame({
        "전략": (
            rotation_results["strategy"]
            + ": "
            + rotation_results["crop_sequence"]
        ),
        "작물 순서": rotation_results["crop_sequence"],
        SCORE: pd.to_numeric(
            rotation_results["temperature_score"],
            errors="coerce"
        ),
    }).reset_index(drop=True)

    baseline_score = df.loc[0, SCORE]

    st.write(
        "현재 재배 방식과 대안 전략을 비교합니다. "
        "(작은 숫자 = 현재 방식 대비 변화)"
    )

    # 전략 카드: 한 줄에 3개씩, 전략이 3개보다 많아도 모두 표시
    for start in range(0, len(df), 3):

        cols = st.columns(3)

        for col, (i, row) in zip(
            cols, df.iloc[start:start + 3].iterrows()
        ):
            with col:
                with st.container(border=True):

                    st.subheader(row["전략"])

                    st.caption(
                        "기준 (현재 방식)" if i == 0 else "대안 전략"
                    )

                    st.write(f"작물 순서: {row['작물 순서']}")

                    delta = None

                    if (
                        i != 0
                        and pd.notna(row[SCORE])
                        and pd.notna(baseline_score)
                    ):
                        delta = f"{row[SCORE] - baseline_score:+.1f}%p"

                    st.metric(
                        SCORE,
                        _format_percent(row[SCORE]),
                        delta=delta
                    )

    st.subheader("한눈에 비교")

    # 전략 이름이 길어서 가로 막대로 표시
    st.bar_chart(
        df.set_index("전략")[[SCORE]],
        horizontal=True
    )

    valid_df = df.dropna(subset=[SCORE])

    if not valid_df.empty:

        best_index = valid_df[SCORE].idxmax()
        best = valid_df.loc[best_index]

        if best_index == 0:
            st.info(
                f"{region}: 온도 지표상 현재 방식이 가장 높습니다 "
                f"({_format_percent(best[SCORE])})."
            )
        else:
            st.info(
                f"{region}: 온도 지표상 가장 높은 전략은 "
                f"{best['전략']} 입니다."
            )

            if pd.notna(baseline_score):
                st.write(
                    f"현재 방식 대비 {SCORE} "
                    f"{best[SCORE] - baseline_score:+.1f}%p"
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
