# 🚀 Gemini Tutor CLI - 5분 빠른 시작 가이드

> Windows 11 PowerShell 5.1 환경에서 즉시 시작하세요!

---

## 📥 Step 1: 라이브러리 설치 (1분)

PowerShell을 열고 다음 명령을 실행하세요:

```powershell
pip install google-generativeai rich textual
```

**출력 예시:**
```
Successfully installed google-generativeai-0.x.x rich-13.x.x textual-0.x.x
```

---

## 🔑 Step 2: Gemini API 키 발급 (2분)

1. 브라우저에서 열기: **https://aistudio.google.com**
2. Google 계정으로 로그인
3. 화면 좌측 **"🔑 Get API key"** 클릭
4. **"Create API key in new project"** 선택
5. 생성된 키를 **복사** (매우 중요!)

**결과:**
```
API key created successfully
AIzaSyD_xxxxxxxxxxxxxxxxxxxxxxxxx  ← 이것을 복사!
```

---

## 💾 Step 3: 파일 저장 및 테스트 (1분)

### 3-1. 파일 다운로드

아래 두 파일을 **같은 폴더**에 저장하세요:

- `gemini_tutor_app.py` (메인 프로그램)
- `test_setup.py` (테스트 도구)

**추천 위치:**
- `C:\Users\USERNAME\gemini-tutor\` (새 폴더 생성)

### 3-2. 테스트 실행

PowerShell에서:

```powershell
cd C:\Users\USERNAME\gemini-tutor
python test_setup.py
```

**예상 출력:**
```
🎯 Gemini Tutor CLI - 환경 감지
============================================================
✅ OS: Windows (windows)
✅ 아키텍처: AMD64
✅ Python 버전: 3.11.5
============================================================

📦 필수 라이브러리 확인 중...

✅ google.generativeai
✅ rich
✅ textual

✅ 모든 라이브러리가 설치되어 있습니다!

⚙️  초기 설정이 필요합니다.

🔑 Gemini API 키 발급 안내
...
API 키를 입력하세요 (또는 Enter 건너뛰기) > 
```

여기서 **앞서 복사한 API 키를 붙여넣으세요**:

```
API 키를 입력하세요 > AIzaSyD_xxxxxxxxxxxxxxxxxxxxxxxxx
✅ 설정이 저장되었습니다: C:\Users\USERNAME\.g-tutor\config.json
```

그 다음 **Gemini API 테스트**:

```
🧪 Gemini API 테스트

⏳ Gemini API 호출 중...
✅ API 응답 성공!
📝 응답: 안녕하세요! 반갑습니다. 테스트가 성공했습니다...
```

---

## ▶️ Step 4: 메인 프로그램 실행 (1분)

이제 메인 프로그램을 실행하세요:

```powershell
python gemini_tutor_app.py
```

**예상 화면:**
```
┌─────────────┬──────────────────────────────┬──────────────────┐
│   세션      │                              │  설명 패널       │
│   목록      │   메인 터미널                │  (우측 상)       │
│             │   (준비 완료...)            │                  │
│             │                              ├──────────────────┤
│   [1] def.. │                              │  에이전트 가이드 │
│   [+ 새 ]   │                              │  (우측 하)       │
└─────────────┴──────────────────────────────┴──────────────────┘
```

---

## 🎯 기본 사용법

### 시나리오 생성

우측 하단 패널에 명령을 입력하세요:

```
> 하고 싶은 일: Python 개발 환경 세팅
```

**결과:**
```
[목표]
Python 개발 환경 세팅

[추천 시나리오]
1. Python 버전 확인
   - 명령: python --version
   - 설명: 현재 설치된 Python 버전을 확인합니다.

2. pip 업그레이드
   - 명령: pip install --upgrade pip
   - 설명: Python 패키지 관리자를 최신 버전으로 업그레이드합니다.

3. 가상환경 생성
   - 명령: python -m venv myenv
   - 설명: 프로젝트용 독립 Python 환경을 생성합니다.
```

---

## 🔑 키보드 단축키

| 키 | 기능 |
|----|------|
| `q` | 프로그램 종료 |
| `c` | 화면 지우기 |

---

## ⚠️ 자주 묻는 질문 (FAQ)

### Q1: "ModuleNotFoundError" 에러가 나요.

**A:** 라이브러리를 설치하지 않았거나, 설치된 Python 버전이 다를 수 있습니다.

```powershell
# 현재 Python 확인
python --version

# 다시 설치
pip install --upgrade google-generativeai rich textual
```

### Q2: API 키가 작동하지 않습니다.

**A:** 다음을 확인하세요:

1. **Google AI Studio에서 정말 키를 생성했는가?**
   - https://aistudio.google.com 재방문

2. **키를 정확하게 복사했는가?**
   - 공백이나 줄바꿈이 없는지 확인

3. **키가 `config.json`에 저장되었는가?**
   - `C:\Users\USERNAME\.g-tutor\config.json` 확인

```json
{
  "llm_provider": "gemini",
  "llm_model": "gemini-2.0-flash",
  "gemini_api_key": "AIzaSyD_..."  ← 여기 있는지 확인
}
```

### Q3: 프로그램이 응답하지 않습니다.

**A:** 보통 Gemini API가 응답 중입니다 (3~10초 소요).

- 기다려보세요
- 안 되면 `Ctrl+C`로 중단 후 재실행

### Q4: 한글이 깨집니다.

**A:** PowerShell의 인코딩을 UTF-8로 변경하세요:

```powershell
chcp 65001
```

그 다음 프로그램 재실행.

### Q5: 파일은 어디에 저장하나요?

**A:** 편한 곳에 저장하면 됩니다:

```powershell
# 방법 1: 홈 디렉터리
C:\Users\USERNAME\

# 방법 2: Documents
C:\Users\USERNAME\Documents\

# 방법 3: 전용 폴더 (추천)
C:\Users\USERNAME\gemini-tutor\
mkdir C:\Users\USERNAME\gemini-tutor
cd C:\Users\USERNAME\gemini-tutor
```

### Q6: 여러 세션을 동시에 사용할 수 있나요?

**A:** 네! PowerShell 여러 개를 열고 각각 실행하면 됩니다.

```powershell
# PowerShell 창 1
python gemini_tutor_app.py

# PowerShell 창 2 (새로 열기)
python gemini_tutor_app.py
```

---

## 📊 무료 티어 한계

Google Gemini API 무료 티어:

| 항목 | 제한 |
|------|------|
| 일일 요청 | 약 250 요청 |
| 분당 요청 | 약 10 요청 |
| 사용 가능 모델 | `gemini-2.0-flash` (또는 최신) |

충분히 테스트하고 학습하기에는 적당합니다! 🎉

---

## 🚨 보안 주의사항

⚠️ **다음 사항을 지키세요:**

1. **API 키는 절대 공개하지 마세요**
   - 깃허브/커뮤니티/공개 채팅에 붙여넣지 말 것

2. **`config.json` 파일을 백업하세요**
   - 다른 컴퓨터에서 복원할 때 필요

3. **API 키가 유출되면**
   - Google AI Studio에서 키를 삭제하고 새로 발급받으세요

---

## 💡 다음 단계

기본 사용법을 익히셨다면:

1. **여러 명령어 시도**
   - "Node.js 환경 세팅"
   - "Docker 컨테이너 실행"
   - "Python 가상환경 생성"
   등등

2. **세션 기록 확인**
   - `C:\Users\USERNAME\.g-tutor\sessions\` 폴더 확인

3. **고급 기능 활용**
   - 다음 문서 참조: `README_KR.md`

---

## 📞 문제 해결 체크리스트

- [ ] Python 3.8+ 설치 확인? (`python --version`)
- [ ] 라이브러리 설치 완료? (`pip list | grep generativeai`)
- [ ] Gemini API 키 생성 완료?
- [ ] API 키를 정확하게 입력?
- [ ] 인터넷 연결 확인?
- [ ] PowerShell을 관리자로 실행?

모든 항목에 체크하면 완벽합니다! ✅

---

**축하합니다! 🎉**

이제 Gemini Tutor CLI를 사용할 준비가 되었습니다.

**Happy Learning!** 🚀
