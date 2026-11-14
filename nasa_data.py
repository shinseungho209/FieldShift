
import requests
import pandas as pd


def get_nasa_power_data(
    latitude,
    longitude,
    start_date="20250101",
    end_date="20251231"
):
    """
    NASA POWER에서 일별 기온, 강수량, 일사량을 수집한다.
    """

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": (
            "T2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"
        ),
        "community": "AG",
        "longitude": longitude,
        "latitude": latitude,
        "start": start_date,
        "end": end_date,
        "format": "JSON"
    }

    response = requests.get(
        url,
        params=params,
        timeout=60
    )

    response.raise_for_status()

    result = response.json()

    parameters = result["properties"]["parameter"]

    df = pd.DataFrame({
        "date": pd.to_datetime(
            list(parameters["T2M"].keys()),
            format="%Y%m%d"
        ),
        "temperature_C": list(parameters["T2M"].values()),
        "precipitation_mm_day": list(
            parameters["PRECTOTCORR"].values()
        ),
        "solar_kwh_m2_day": list(
            parameters["ALLSKY_SFC_SW_DWN"].values()
        )
    })

    # NASA POWER 결측값 처리
    columns = [
        "temperature_C",
        "precipitation_mm_day",
        "solar_kwh_m2_day"
    ]

    for column in columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

        df.loc[df[column] <= -900, column] = float("nan")

    df = df.sort_values("date").reset_index(drop=True)

    return df


if __name__ == "__main__":

    # 전북특별자치도 김제시 좌표
    latitude = 35.8036
    longitude = 126.8808

    print("NASA POWER 데이터 수집 시작...")

    try:
        data = get_nasa_power_data(
            latitude,
            longitude
        )

        print("\n데이터 수집 성공!")
        print(data.head())

        print("\n환경 데이터 통계")
        print(data.describe())

        print("\n변수별 결측값")
        print(data.isna().sum())

        print("\n수집 데이터 개수:", len(data))

    except Exception as error:
        print("\n데이터 수집 실패:", error)
