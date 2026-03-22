# analyzer/crawler.py
# 엑셀 파일 로드 → 정제 → 로컬 CSV 저장 → S3 업로드

import pandas as pd
import boto3
import os

# 설정
EXCEL_PATH = "data/로또 회차별 당첨번호_20260322101919.xlsx"
S3_BUCKET = "lotto-analyzer-data"
S3_KEY = "lotto/lotto_numbers.csv"
LOCAL_PATH = "data/lotto_numbers.csv"

def load_and_clean():
    """엑셀 파일 로드 및 컬럼 정제"""
    df = pd.read_excel(EXCEL_PATH)

    # 컬럼 이름 정리
    df = df.rename(columns={
        "당첨번호": "1번",
        "Unnamed: 3": "2번",
        "Unnamed: 4": "3번",
        "Unnamed: 5": "4번",
        "Unnamed: 6": "5번",
        "Unnamed: 7": "6번"
    })

    # 필요한 컬럼만 선택
    df = df[["회차", "1번", "2번", "3번", "4번", "5번", "6번", "보너스"]]

    # 회차 오름차순 정렬
    df = df.sort_values("회차").reset_index(drop=True)

    return df

def save_local(df):
    """로컬 CSV 저장"""
    os.makedirs("data", exist_ok=True)
    df.to_csv(LOCAL_PATH, index=False, encoding="utf-8-sig")
    print(f"로컬 저장 완료: {LOCAL_PATH} (총 {len(df)}회차)")

def upload_to_s3(df):
    """S3 업로드"""
    try:
        s3 = boto3.client("s3", region_name="ap-northeast-2")
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=S3_KEY,
            Body=df.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig"),
            ContentType="text/csv"
        )
        print(f"S3 업로드 완료: s3://{S3_BUCKET}/{S3_KEY}")
    except Exception as e:
        print(f"S3 업로드 실패: {e}")

def run():
    """전체 실행"""
    print("=== 로또 데이터 처리 시작 ===")

    df = load_and_clean()
    print(f"데이터 로드 완료: 총 {len(df)}회차")
    print(df.head(3))
    print(df.tail(3))

    save_local(df)
    upload_to_s3(df)

    print("\n=== 완료 ===")

if __name__ == "__main__":
    run()