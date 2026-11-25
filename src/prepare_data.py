"""Gabungkan semua sheet tahunan dataset kualitas udara jadi satu CSV seragam untuk Spark/MLlib.

Pakai:  python prepare_data.py [input.xlsx] [output.csv]
Butuh:  pip install pandas openpyxl
"""
import sys

import pandas as pd

SRC = sys.argv[1] if len(sys.argv) > 1 else "data/raw/AirQuality_Benowo_xv6vmsv.xlsx"
OUT = sys.argv[2] if len(sys.argv) > 2 else "data/processed/airquality_benowo_clean.csv"

# nama asli -> nama snake_case 
RENAME = {
    "Datetime_start": "timestamp",  # sheet 2022-2025
    "AQI US": "aqi_us",
    "AQI CN": "aqi_cn",
    "PM2.5 (ug/m3)": "pm25",
    "PM10 (ug/m3)": "pm10",
    "PM1 (ug/m3)": "pm1",
    "CO2 (ppm)": "co2",
    "Temperature (Celsius)": "temp_c",
    "Temperature (Fahrenheit)": "temp_f",
    "Humidity (%)": "humidity",
}
COLS = ["timestamp", "aqi_us", "aqi_cn", "pm25", "pm10", "pm1", "co2", "temp_c", "temp_f", "humidity"]

sheets = pd.read_excel(SRC, sheet_name=None)
frames = []
for name, df in sheets.items():
    if not name.isdigit():  # lewati sheet "About"
        continue
    # reindex: kolom yang tidak ada di tahun tsb jadi NaN
    df = df.rename(columns=RENAME).reindex(columns=COLS)
    frames.append(df)
    print(f"{name}: {len(df):>6} baris")

df = pd.concat(frames, ignore_index=True)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")  # string & datetime -> datetime64
df[COLS[1:]] = df[COLS[1:]].apply(pd.to_numeric, errors="coerce").astype("float64")

n = len(df)
df = (df.dropna(subset=["timestamp"])
        .sort_values("timestamp")
        .drop_duplicates(subset="timestamp", keep="first")
        .reset_index(drop=True))
print(f"total: {n} -> {len(df)} baris setelah buang duplikat/timestamp invalid")

# cek sederhana: kalau ini gagal, output tidak layak dipakai
assert list(df.columns) == COLS
assert df["timestamp"].is_unique and df["timestamp"].is_monotonic_increasing
assert df["aqi_us"].notna().all()

df.to_csv(OUT, index=False, date_format="%Y-%m-%d %H:%M:%S")
print(f"tersimpan: {OUT}")
print(df.isna().mean().round(3).rename("rasio_kosong").to_string())
