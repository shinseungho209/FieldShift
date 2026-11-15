import requests


ELEVATION_API = (
    "https://openzenith.pages.dev/api/elevation"
)


def get_elevation(latitude, longitude):

    params = {
        "lat": latitude,
        "lon": longitude,
        "units": "meters",
        "interpolation": "bilinear"
    }

    try:
        response = requests.get(
            ELEVATION_API,
            params=params,
            timeout=30
        )

        if not response.ok:
            raise RuntimeError(
                f"API 오류: {response.status_code}\n"
                f"{response.text[:2000]}"
            )

        result = response.json()

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"지형 데이터 요청 실패: {error}"
        )

    elevation = result.get("elevation")

    if elevation is None:
        raise RuntimeError(
            f"고도 데이터가 없습니다: {result}"
        )

    return {
        "elevation_m": float(elevation),
        "unit": result.get("unit", "meters"),
        "resolution_m": result.get("resolution"),
        "source": result.get("source"),
        "tile": result.get("srtmTile"),
        "location": result.get("location"),
        "metadata": result.get("metadata", {})
    }


if __name__ == "__main__":

    latitude = 37.751
    longitude = 128.8764

    print("NASA SRTM 지형 데이터 수집 시작...")

    try:
        data = get_elevation(
            latitude,
            longitude
        )

        print("\n데이터 수집 성공!")

        print(
            f"고도: {data['elevation_m']:.2f} m"
        )

        print(
            f"해상도: {data['resolution_m']} m"
        )

        print(
            f"자료 출처: {data['source']}"
        )

        print(
            f"SRTM 타일: {data['tile']}"
        )
        print("상세 메타데이터:", data["metadata"])

    except Exception as error:
        print("\n데이터 수집 실패:")
        print(error)
