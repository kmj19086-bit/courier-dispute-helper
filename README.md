# 📦 택배 분쟁 전문 도우미 (Courier Dispute Expert Assistant)

이 애플리케이션은 사용자가 택배 분실, 파손, 배송 지연, 오배송 등의 상황을 입력하거나 선택했을 때, 한국 법률(상법, 전자상거래법, 공정위 택배표준약관 등)을 기반으로 **책임 소재(과실 비율) 분석**, **맞춤형 클레임 텍스트 생성**, 그리고 **단계별 구제 및 환불/보상 전략**을 제공하는 Streamlit 기반의 인터랙티브 웹 어플리케이션입니다.

---

## 주요 기능

1. **상황 분석 (누구 책임인가?)**
   - 대표적인 택배 사고 4대 유형(분실, 파손, 지연, 오배송)의 문항 기반 분석
   - 택배사 / 판매자 / 구매자의 과실 책임 비중(%) 산정 및 근거 법률 정보 제시
2. **맞춤형 클레임 텍스트**
   - 쇼핑몰 대면 상황, 일반 택배사 대면 상황 등 조건에 부합하는 정중하고 단호한 클레임 양식 자동 작성
   - 복사 버튼(Copy to Clipboard) 제공으로 즉각적인 활용 가능
3. **단계별 환불/보상 전략**
   - 분쟁 해소 시까지 해야 하는 체크리스트 형태의 3단계 맞춤 대응 가이드
   - 한국소비자원, 국민신문고 등 민원 제기 기관 다이렉트 링크 제공
4. **AI 심층 분석 모드 (Gemini AI)**
   - Gemini API Key를 입력할 경우, 자유 서술형 피해 상황을 깊이 있게 검토하여 더욱 정교하고 상세한 솔루션 제공
5. **보고서 다운로드**
   - 분석 결과, 클레임 양식, 전략 가이드가 합쳐진 통합 솔루션 보고서를 즉시 `.txt` 파일로 다운로드 가능

---

## 로컬 실행 방법

### 1. 사전 요구사항
컴퓨터에 **Python 3.8 이상**이 설치되어 있어야 합니다.

### 2. 프로젝트 폴더로 이동 및 종속성 패키지 설치
터미널(또는 PowerShell, Command Prompt)을 열고 아래 명령어를 순서대로 실행해 주세요.

```bash
# 종속성 패키지 설치
pip install -r requirements.txt
```

### 3. 애플리케이션 실행
설치가 완료되면 다음 명령어로 Streamlit 앱을 실행합니다.

```bash
streamlit run app.py
```

명령어를 실행하면 자동으로 웹 브라우저(`http://localhost:8501`)가 열리며 애플리케이션이 표시됩니다.

---

## Streamlit Community Cloud 무료 배포 방법

Streamlit은 자신의 코드를 웹에 완전히 무료로 배포하고 공유할 수 있는 **Streamlit Community Cloud**를 지원합니다. 아래 단계를 따라 전 세계 어디서든 접속 가능한 URL로 배포해 보세요.

### Step 1. GitHub 리포지토리 생성 및 코드 업로드
1. [GitHub](https://github.com/)에 로그인하고 새로운 리포지토리(예: `courier-dispute-helper`)를 생성합니다.
2. 로컬에 있는 아래의 파일들을 해당 GitHub 리포지토리에 푸시(Push)합니다.
   - `app.py`
   - `requirements.txt`
   - `README.md`
   *(주의: API Key 등 개인 보안 정보가 코드 내에 직접 포함되어 저장되지 않도록 유의하세요)*

### Step 2. Streamlit Community Cloud 로그인
1. [Streamlit Share](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 가입 및 로그인합니다.

### Step 3. 앱 배포하기 (Deploy)
1. 로그인 후 오른쪽 상단의 **[New app]** 버튼을 클릭합니다.
2. 설정 창에서 다음 사항을 입력합니다:
   - **Repository**: 방금 생성한 GitHub 리포지토리 선택 (`GitHub계정명/courier-dispute-helper`)
   - **Branch**: 주로 `main` 혹은 `master`
   - **Main file path**: `app.py`로 입력
3. **[Deploy!]** 버튼을 클릭하면, 약 1~2분 정도 패키지 설치 단계를 거쳐 나만의 고유 도메인(예: `https://xxx.streamlit.app`)으로 전 세계 사용자가 접속 가능한 상태로 배포가 완료됩니다!
