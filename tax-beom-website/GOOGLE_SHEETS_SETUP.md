# 🚀 Google Sheets 연동 - 빠른 설정 가이드

## ⏰ 소요 시간: 30분

---

## 📋 Step 1: Google Sheets 생성 (5분)

### 1-1. 스프레드시트 만들기

1. https://sheets.google.com 접속
2. **빈 스프레드시트** 클릭
3. 제목: **세무회계 범 - 상담 신청 DB**

### 1-2. 컬럼 헤더 입력

**첫 번째 행에 다음 입력** (A1부터 O1까지):

```
신청일시 | 상담유형 | 사업자유형 | 사업자등록번호 | 연락처 | 이메일 | 상담내용 | 마케팅동의 | 상담상태 | 담당자 | 통화일시 | 통화내용 | 계약여부 | 계약금액 | 비고
```

**복사해서 붙여넣기용**:
```
신청일시	상담유형	사업자유형	사업자등록번호	연락처	이메일	상담내용	마케팅동의	상담상태	담당자	통화일시	통화내용	계약여부	계약금액	비고
```

### 1-3. 스프레드시트 ID 확인

URL에서 `/d/` 다음 부분이 ID입니다:
```
https://docs.google.com/spreadsheets/d/1abc123xyz/edit
                                      ↑ 이 부분
```

**ID 복사해두기**: `____________________________`

---

## 📝 Step 2: Apps Script 코드 작성 (10분)

### 2-1. Apps Script 편집기 열기

1. Google Sheets에서 **확장 프로그램** → **Apps Script** 클릭
2. 새 프로젝트 이름: **세무회계범 데이터 수집**

### 2-2. 코드 복사 붙여넣기

기존 코드 **전체 삭제** 후 아래 코드 붙여넣기:

```javascript
// ⚙️ 설정: 아래 SHEET_ID를 본인의 스프레드시트 ID로 변경하세요
const SHEET_ID = 'YOUR_SHEET_ID_HERE'; // Step 1-3에서 복사한 ID
const SHEET_NAME = 'Sheet1'; // 시트 이름 (보통 Sheet1)

// 📨 웹훅 - POST 요청 처리 (상담 신청 저장)
function doPost(e) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    const data = JSON.parse(e.postData.contents);

    // 새 행 추가
    sheet.appendRow([
      new Date(data.timestamp),     // A: 신청일시
      getLabel(data.consultType, consultTypes),  // B: 상담 유형
      getLabel(data.businessType, businessTypes), // C: 사업자 유형
      data.businessNumber || '',     // D: 사업자등록번호
      data.phone || '',              // E: 연락처
      data.email || '',              // F: 이메일
      data.content || '',            // G: 상담 내용
      data.agreeMarketing === 'on' ? 'Y' : 'N',  // H: 마케팅 동의
      '대기',                        // I: 상담 상태
      '',                            // J: 담당자
      '',                            // K: 통화일시
      '',                            // L: 통화 내용
      '',                            // M: 계약여부
      '',                            // N: 계약금액
      ''                             // O: 비고
    ]);

    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      message: '데이터가 저장되었습니다.'
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 🔍 GET 요청 처리 (데이터 조회 - 관리자 페이지용)
function doGet(e) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    const data = sheet.getDataRange().getValues();

    // 헤더 제외하고 데이터 반환
    const rows = data.slice(1).map(row => ({
      timestamp: row[0],
      consultType: row[1],
      businessType: row[2],
      businessNumber: row[3],
      phone: row[4],
      email: row[5],
      content: row[6],
      agreeMarketing: row[7],
      status: row[8],
      manager: row[9],
      callDate: row[10],
      callNote: row[11],
      contract: row[12],
      contractAmount: row[13],
      note: row[14]
    }));

    return ContentService.createTextOutput(JSON.stringify({
      success: true,
      data: rows
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 📋 라벨 변환 함수
function getLabel(value, mapping) {
  return mapping[value] || value;
}

const consultTypes = {
  'bookkeeping': '세무기장',
  'tax': '법인세/종소세 신고',
  'consulting': '절세 컨설팅',
  'refund': '경정청구',
  'property': '양도/상속/증여',
  'other': '기타'
};

const businessTypes = {
  'corporate': '법인사업자',
  'individual': '개인사업자',
  'startup': '예비창업자',
  'freelancer': '프리랜서'
};
```

### 2-3. SHEET_ID 수정

**중요!** 2번째 줄의 `YOUR_SHEET_ID_HERE`를 Step 1-3에서 복사한 ID로 변경:

```javascript
const SHEET_ID = '1abc123xyz'; // ← 여기에 본인 ID 입력
```

### 2-4. 저장

- **Ctrl + S** 또는 **디스크 아이콘** 클릭
- 프로젝트 이름 확인

---

## 🚀 Step 3: 웹 앱으로 배포 (5분)

### 3-1. 배포하기

1. 우측 상단 **배포** → **새 배포** 클릭
2. 유형 선택: **웹 앱**
3. 설정:
   - **실행 계정**: 나
   - **액세스 권한**: **모든 사용자**
4. **배포** 클릭

### 3-2. 권한 승인

1. "권한 검토" 클릭
2. 본인 Google 계정 선택
3. "고급" → "세무회계범 데이터 수집(안전하지 않음)으로 이동" 클릭
4. "허용" 클릭

### 3-3. 웹 앱 URL 복사

**중요!** 다음 형식의 URL이 나타납니다:
```
https://script.google.com/macros/s/AKfycby.../exec
```

**이 URL 전체를 복사해두세요**: `____________________________`

---

## 🔗 Step 4: 웹사이트 연동 (10분)

### 4-1. index.html 파일 열기

VSCode 또는 메모장으로 `C:\Users\기광우\makepage\tax-beom-website\index.html` 열기

### 4-2. submitForm 함수 찾기

`Ctrl + F`로 `function submitForm` 검색

### 4-3. 기존 함수 교체

**기존 코드** (2140번째 줄 근처):
```javascript
function submitForm(e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  // LocalStorage에 저장 (실제로는 서버로 전송)
  const submissions = JSON.parse(localStorage.getItem('taxBeomDB') || '[]');
  data.timestamp = new Date().toISOString();
  data.id = Date.now();
  submissions.push(data);
  localStorage.setItem('taxBeomDB', JSON.stringify(submissions));

  alert('상담 신청이 완료되었습니다.\\n빠른 시일 내에 연락드리겠습니다.');
  form.reset();
  closeModal();
}
```

**새 코드로 교체**:
```javascript
function submitForm(e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  data.timestamp = new Date().toISOString();
  data.id = Date.now();

  // ⚙️ Google Sheets 웹 앱 URL (Step 3-3에서 복사한 URL)
  const GOOGLE_SCRIPT_URL = 'YOUR_WEB_APP_URL_HERE';

  // Google Sheets로 전송
  fetch(GOOGLE_SCRIPT_URL, {
    method: 'POST',
    mode: 'no-cors', // CORS 회피
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
  })
  .then(() => {
    // 백업: LocalStorage에도 저장
    const submissions = JSON.parse(localStorage.getItem('taxBeomDB') || '[]');
    submissions.push(data);
    localStorage.setItem('taxBeomDB', JSON.stringify(submissions));

    alert('상담 신청이 완료되었습니다.\\n빠른 시일 내에 연락드리겠습니다.');
    form.reset();
    closeModal();
  })
  .catch(error => {
    console.error('Error:', error);
    // 오류 시에도 LocalStorage에 백업
    const submissions = JSON.parse(localStorage.getItem('taxBeomDB') || '[]');
    submissions.push(data);
    localStorage.setItem('taxBeomDB', JSON.stringify(submissions));

    alert('상담 신청이 완료되었습니다.\\n빠른 시일 내에 연락드리겠습니다.');
    form.reset();
    closeModal();
  });
}
```

### 4-4. URL 수정

**중요!** 코드에서 `YOUR_WEB_APP_URL_HERE`를 Step 3-3에서 복사한 URL로 변경:

```javascript
const GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycby.../exec';
```

### 4-5. 저장 후 Git 푸시

```bash
cd C:\Users\기광우\makepage\tax-beom-website
git add index.html
git commit -m "✅ Google Sheets 연동 완료"
git push origin main
```

---

## ✅ Step 5: 테스트 (5분)

### 5-1. 웹사이트에서 테스트 신청

1. https://tax-beom.netlify.app/ 접속
2. "무료 상담 신청" 클릭
3. 양식 작성 후 제출

### 5-2. Google Sheets 확인

1. Google Sheets로 돌아가기
2. 2번째 행에 데이터 자동 추가 확인

**성공 예시**:
```
2024-12-19 15:30 | 세무기장 | 개인사업자 | 123-45-67890 | 010-1234-5678 | ...
```

---

## 🎨 보너스: 조건부 서식 설정

### 상담 상태별 색상

1. **I열** (상담상태) 선택
2. **서식** → **조건부 서식**
3. 규칙 추가:
   - "대기" = 🟡 노란색 배경
   - "진행중" = 🔵 파란색 배경
   - "완료" = 🟢 초록색 배경

### 데이터 검증

**E열 (연락처) 검증**:
1. E열 선택
2. 데이터 → 데이터 확인
3. 조건: 맞춤 수식
4. 수식: `=REGEXMATCH(E2, "^010-[0-9]{4}-[0-9]{4}$")`

---

## 🔔 관리자 알림 설정

### 이메일 알림

1. **도구** → **알림 규칙**
2. "스프레드시트가 변경되면" 선택
3. 알림 빈도: **즉시**
4. 이메일 주소 확인
5. **저장**

→ 새 상담 신청 시 즉시 이메일 알림!

---

## 📱 모바일 앱 설치

### Android/iOS Google Sheets 앱

1. 앱 스토어에서 **Google Sheets** 설치
2. 본인 계정 로그인
3. "세무회계 범 - 상담 신청 DB" 열기
4. 홈 화면에 바로가기 추가

→ 언제 어디서나 실시간 확인!

---

## 🛠️ 트러블슈팅

### Q1: 데이터가 저장 안 돼요

**확인 사항**:
- [ ] SHEET_ID가 정확한가?
- [ ] 웹 앱 URL이 정확한가?
- [ ] Apps Script 배포 시 "모든 사용자" 선택했는가?
- [ ] 권한 승인을 완료했는가?

### Q2: "권한이 없습니다" 오류

**해결**:
1. Apps Script → 배포 → 배포 관리
2. 기존 배포 "보관처리"
3. 새 배포 다시 생성

### Q3: CORS 오류가 나요

**정상입니다!**
- `mode: 'no-cors'` 때문에 응답을 못 받지만 데이터는 저장됨
- Google Sheets 확인하면 데이터 정상 저장됨

---

## 📊 데이터 활용 예시

### 월별 상담 통계

```
=COUNTIF(A:A, ">=2024-12-01")
```

### 계약 전환율

```
=COUNTIF(M:M, "Y") / COUNTA(A:A) * 100
```

### 상담 유형별 분류

```
=COUNTIF(B:B, "세무기장")
```

---

## ✅ 최종 체크리스트

작업 완료 전 확인:
- [ ] Google Sheets 생성 완료
- [ ] 15개 컬럼 헤더 입력 완료
- [ ] SHEET_ID 복사 완료
- [ ] Apps Script 코드 작성 완료
- [ ] SHEET_ID 수정 완료
- [ ] 웹 앱 배포 완료
- [ ] 웹 앱 URL 복사 완료
- [ ] index.html submitForm 함수 교체 완료
- [ ] GOOGLE_SCRIPT_URL 수정 완료
- [ ] Git 푸시 완료
- [ ] 테스트 신청 3회 이상 완료
- [ ] Google Sheets에 데이터 확인 완료
- [ ] 조건부 서식 설정 완료
- [ ] 이메일 알림 설정 완료

---

**소요 시간**: 총 30분
**비용**: 무료
**난이도**: ⭐⭐⭐ (중)

**문제 발생 시**: `KAKAO_INTEGRATION_GUIDE.md` 또는 `DATA_SHARING_GUIDE.md` 참조
