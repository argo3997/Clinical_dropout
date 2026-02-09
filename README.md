# 🏥 Clinical Trial Dropout Prediction

> 임상시험 환자 중도 탈락 예측 모델 — CDISC Pilot SDTM 데이터 기반

## 📌 프로젝트 개요

임상시험에서 환자의 중도 탈락(dropout)은 시험 기간 연장과 비용 증가의 주요 원인입니다.
본 프로젝트는 **환자의 인구통계, 이상반응, 방문 기록 등을 기반으로 중도 탈락 가능성이 높은 환자를 사전에 예측**하는 분류 모델을 구축합니다.

### 비즈니스 목표

- 탈락 고위험 환자를 조기 식별하여 사전 관리(리마인드 콜, 방문 일정 조정 등) 시행
- 임상시험 탈락률 감소를 통한 시험 기간 단축 및 비용 절감

### 분석 질문

- 환자의 인구통계, 이상반응, 활력징후, 방문 기록 데이터를 기반으로 탈락 여부를 예측할 수 있는가?
- 탈락에 가장 큰 영향을 미치는 요인은 무엇인가?

---

## 📂 데이터

### 데이터 출처

**CDISC Pilot 01 (CDISCPILOT01)** — 알츠하이머 치료제 임상시험 SDTM 데이터

- Source: [PhUSE Scripts Repository](https://github.com/phuse-org/phuse-scripts/tree/master/data/sdtm/cdiscpilot01)
- Standard: SDTM Version 2
- 대상 환자 수: 306명 (등록 254명 + Screen Failure 52명)

> Note: CDISC Pilot 01은 업계 표준 교육 데이터셋으로, 현재 SDTM 구조와 동일한 형식을 따릅니다.

### 사용 도메인

| 도메인 | 파일 | 설명 | 활용 |
|--------|------|------|------|
| DM | `dm.xpt` | Demographics (인구통계) | 나이, 성별, 인종, 투약군 등 기본 피처 |
| AE | `ae.xpt` | Adverse Events (이상반응) | 이상반응 횟수, 심각도, 종류 |
| DS | `ds.xpt` | Disposition (완료/탈락) | **타겟 변수 (y)** |
| SV | `sv.xpt` | Subject Visits (방문 기록) | 방문 지연, 누락 여부 |
| VS | `vs.xpt` | Vital Signs (활력징후) | 방문별 활력징후 변화 추이 |
| CM | `cm.xpt` | Concomitant Medications (병용약물) | 병용약물 수, 종류 |
| MH | `mh.xpt` | Medical History (병력) | 기저질환 수, 종류 |

---

## 🏗️ 프로젝트 구조

```
clinical-trial-dropout-prediction/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/                        # 원본 SDTM .xpt 파일
│   │   ├── dm.xpt
│   │   ├── ae.xpt
│   │   ├── ds.xpt
│   │   ├── sv.xpt
│   │   ├── vs.xpt
│   │   ├── cm.xpt
│   │   └── mh.xpt
│   └── model_dataset.csv           # 전처리 완료된 분석 데이터셋
│
├── notebooks/
│   ├── 01_EDA.ipynb                # 탐색적 데이터 분석
│   ├── 02_preprocessing.ipynb      # 전처리 + 피처 엔지니어링
│   └── 03_modeling.ipynb           # 모델링 + 해석
│
├── src/
│   └── utils.py                    # 공통 함수 모듈
│
└── outputs/
    └── figures/                    # 시각화 결과물
```

---

## 🔍 분석 프로세스

### 1. 탐색적 데이터 분석 (EDA)
- 각 도메인별 데이터 구조 및 결측치 확인
- 탈락 vs 완료 환자 분포 분석
- 주요 변수 간 상관관계 탐색

### 2. 전처리 및 피처 엔지니어링
- SDTM 도메인 간 USUBJID 기준 병합
- 도메인 지식 기반 파생 변수 33개 생성:
  - **AE**: 총 건수, SAE 여부, 심각도별 건수, 약물 관련 AE, 미회복 AE, 피부 AE
  - **VS**: Baseline 활력징후(SYSBP, DIABP, PULSE, TEMP, WEIGHT), 혈압/맥박 변동성(STD)
  - **CM**: 병용약물 수, 고유 약물 수, 약물 분류 수
  - **MH**: 기저질환 수, 기존 질환 수, Body System 다양성, 고혈압 병력
- Data Leakage 검토: 방문 관련 피처(탈락의 "결과")를 식별하여 모델링에서 제거
- 결측치 처리(중앙값 대체) 및 범주형 변수 인코딩

### 3. 모델링
- Logistic Regression, Random Forest, Gradient Boosting 3개 모델 비교
- 5-Fold Stratified Cross-Validation
- GridSearchCV를 활용한 하이퍼파라미터 튜닝
- 평가 지표: AUC-ROC, Precision, Recall, F1-Score

### 4. 모델 해석 및 비즈니스 제언
- Feature Importance 기반 주요 탈락 요인 도출
- 실무 적용 가능한 개선 방안 3가지 제시

---

## 🛠️ 기술 스택

| 구분 | 도구 |
|------|------|
| Language | Python 3.x |
| Data | pandas, numpy |
| Visualization | matplotlib, seaborn |
| Modeling | scikit-learn, imbalanced-learn |
| Interpretation | SHAP |
| Environment | Jupyter Notebook |

---

## ⚙️ 설치 및 실행

```bash
# 레포지토리 클론
git clone https://github.com/your-username/clinical-trial-dropout-prediction.git
cd clinical-trial-dropout-prediction

# 패키지 설치
pip install -r requirements.txt

# 노트북 실행
jupyter notebook
```

---

## 📊 주요 결과

### 데이터 요약

- 분석 대상: **254명** (Screen Failure 52명 제외)
- 투약군: Placebo(86), Xanomeline Low Dose(84), Xanomeline High Dose(84)
- **전체 탈락률: 56.7%** (144/254)
- 탈락 사유 1위: Adverse Event — 92건 (63.9%)

### 탈락률 by 투약군

| 투약군 | 탈락률 | 완료 | 탈락 |
|--------|--------|------|------|
| Placebo | 32.6% | 58 | 28 |
| Xanomeline Low Dose | 70.2% | 25 | 59 |
| Xanomeline High Dose | 67.9% | 27 | 57 |

### 피처 엔지니어링

7개 SDTM 도메인에서 **33개 파생 피처**를 생성했으며, Data Leakage 검토를 통해 방문 관련 피처(VISIT_TOTAL, VISIT_SCHEDULED, MAX_WEEK 등)를 제거하여 최종 **28개 피처**로 모델링을 수행했습니다.

### 모델 성능

| 모델 | CV AUC (5-Fold) | Test AUC |
|------|-----------------|----------|
| Logistic Regression | 0.733 | 0.627 |
| Random Forest | 0.728 | 0.630 |
| **Gradient Boosting** | **0.758** | 0.614 |

> Data Leakage 제거 전 방문 피처 포함 시 상관관계 r > 0.85로 모델 성능이 과대 추정됩니다. 이를 인지하고 제거한 후의 결과이며, 254명의 소규모 데이터 한계를 고려하면 합리적인 수준입니다.

### Top Feature Importance

1. **ARM_PLACEBO** — 투약군 여부가 탈락의 가장 강력한 예측 변수
2. **VS_BL_SYSBP** — 기저 수축기혈압
3. **VS_BL_PULSE** — 기저 맥박
4. **VS_BL_DIABP** — 기저 이완기혈압
5. **AE_MILD / AE_MODERATE** — 이상반응 심각도 패턴

### 비즈니스 제언

1. **투약군 환자 대상 강화 모니터링** — 특히 피부 관련 부작용 발생 시 즉각 대응 프로토콜 도입
2. **Baseline 활력징후 기반 위험 계층화** — 혈압/맥박 불안정 환자에게 사전 관리 강화
3. **AE 심각도 기반 조기 경고 시스템** — MODERATE 이상 AE 발생 시 자동 알림 + 추가 방문 스케줄링

### 한계점

- 소규모 데이터(254명)로 인한 일반화 한계
- 시간적 요소 미반영 — 향후 초기 2~4주 데이터만으로 예측하는 시계열 접근 고려 필요

---

## 📝 참고

- [CDISC SDTM Implementation Guide](https://www.cdisc.org/standards/foundational/sdtm)
- [PhUSE Scripts Repository](https://github.com/phuse-org/phuse-scripts)
- CDISC Pilot 01 Study: Alzheimer's Disease Clinical Trial

---

## 👤 Author

- GitHub: https://github.com/argo3997
