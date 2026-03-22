# 🎱 로또 분석기 (Lotto Analyzer)

> 로또 번호를 예측할 수 있을까? 데이터로 직접 확인해보는 통계 분석 + 몬테카를로 시뮬레이터

🔗 **배포 URL**: https://lotto-analyzer-jael.streamlit.app/

---

## 📌 프로젝트 개요

로또 번호 예측은 불가능합니다. 이 프로젝트는 예측이 아닌 **데이터 분석**과 **확률 시뮬레이션**을 통해 그 사실을 직접 확인하는 것을 목적으로 합니다.

---

## ⚙️ 기술 스택

| 분류 | 기술 |
|------|------|
| Language | Python 3.11.9 |
| UI | Streamlit |
| 데이터 처리 | Pandas, NumPy |
| 시각화 | Plotly |
| 인프라 (실습) | AWS S3, AWS Athena |
| 배포 | GitHub + Streamlit Cloud |

---

## 🗂️ 프로젝트 구조
```
lotto-analyzer/
├── analyzer/
│   ├── crawler.py       # 데이터 수집 및 S3 업로드
│   └── stats.py         # 통계 분석 모듈
├── simulator/
│   └── monte_carlo.py   # 몬테카를로 시뮬레이터
├── data/
│   └── lotto_numbers.csv  # 1~1216회차 당첨번호
├── app.py               # Streamlit 메인 앱
└── requirements.txt
```

---

## 📊 주요 기능

### 옵션 A — 통계 분석
- 번호별 출현 빈도 (1~45번)
- 홀짝 비율 분석
- 구간별 분포 (1~9, 10~19, 20~29, 30~39, 40~45)
- 회차별 당첨번호 합계 분포
- 최근 50회차 핫/콜드 번호

### 옵션 B — 몬테카를로 시뮬레이터
- 4가지 전략 비교 (랜덤 / 핫번호 / 콜드번호 / 고정번호)
- 전략별 누적 손익 추이 차트
- 회차별 당첨 현황 (1~5등, 꽝)

---

## 💡 핵심 결론

> **어떤 전략을 써도 로또의 기댓값은 동일하게 마이너스입니다.**

한국 로또 6/45는 완전한 독립 시행입니다. 매 회차 결과는 이전 회차와 수학적으로 아무 관계가 없으며, 당첨 확률은 항상 **1/8,145,060**입니다.

---

## 🚀 로컬 실행 방법
```bash
# 1. 레포 클론
git clone https://github.com/dvlp-jael/lotto-analyzer.git
cd lotto-analyzer

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\Activate.ps1

# 3. 패키지 설치
pip install -r requirements.txt

# 4. 실행
streamlit run app.py
```

---

## 📝 데이터 출처

- 동행복권 로또 6/45 당첨번호 (1회차 ~ 1216회차)