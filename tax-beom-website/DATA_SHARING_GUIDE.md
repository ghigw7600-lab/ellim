# 📊 상담 신청 데이터 공유 & 관리 가이드

## 🎯 요구사항
- 수집된 데이터를 관리자끼리 **실시간 온라인 공유**
- **서버 없이** 사용 가능한 방법
- 전화 상담 후 **업무 내용 기재 및 관리** 기능

---

## ✅ 추천 솔루션: Google Sheets + Google Apps Script

### 왜 Google Sheets인가?

| 특징 | Google Sheets | 기타 방법 |
|------|---------------|----------|
| 실시간 공유 | ✅ 자동 동기화 | ❌ 수동 작업 필요 |
| 서버 비용 | ✅ 무료 | ❌ 월 $5~$50 |
| 관리자 권한 | ✅ 쉬운 설정 | ⚠️ 복잡함 |
| 모바일 접근 | ✅ 앱 지원 | ⚠️ 제한적 |
| 데이터 백업 | ✅ 자동 | ❌ 수동 |
| 업무 메모 추가 | ✅ 쉬움 | ⚠️ 별도 작업 필요 |

---

## 📋 구현 방법 (단계별 가이드)

### Step 1: Google Sheets 준비

1. **스프레드시트 생성**
   - https://sheets.google.com 접속
   - "새 스프레드시트" 생성
   - 이름: "세무회계 범 - 상담 신청 관리"

2. **컬럼 설정**
   ```
   A열: 신청일시
   B열: 상담 유형
   C열: 사업자 유형
   D열: 사업자등록번호
   E열: 연락처
   F열: 이메일
   G열: 상담 내용
   H열: 마케팅 수신동의
   I열: 상담 상태 (대기/진행중/완료)
   J열: 담당자
   K열: 통화일시
   L열: 통화 내용
   M열: 계약여부
   N열: 계약금액
   O열: 비고
   ```

3. **공유 설정**
   - 우측 상단 "공유" 버튼
   - 관리자 이메일 추가 (편집 권한)
   - "링크가 있는 모든 사용자" → "보기 전용" 설정

### Step 2: Google Apps Script 코드 작성

1. **Apps Script 편집기 열기**
   - Google Sheets → 확장 프로그램 → Apps Script

2. **코드 복사 붙여넣기**

```javascript
// Google Sheets URL - 본인의 스프레드시트 URL로 변경하세요
const SHEET_ID = 'YOUR_SHEET_ID_HERE';
const SHEET_NAME = 'Sheet1';

// 웹앱으로 배포 - POST 요청 처리
function doPost(e) {
  try {
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName(SHEET_NAME);
    const data = JSON.parse(e.postData.contents);

    // 새 행 추가
    sheet.appendRow([
      new Date(data.timestamp),     // A: 신청일시
      data.consultType || '',        // B: 상담 유형
      data.businessType || '',       // C: 사업자 유형
      data.businessNumber || '',     // D: 사업자등록번호
      data.phone || '',              // E: 연락처
      data.email || '',              // F: 이메일
      data.content || '',            // G: 상담 내용
      data.agreeMarketing || '',     // H: 마케팅 동의
      '대기',                        // I: 상담 상태
      '',                           // J: 담당자
      '',                           // K: 통화일시
      '',                           // L: 통화 내용
      '',                           // M: 계약여부
      '',                           // N: 계약금액
      ''                            // O: 비고
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

// GET 요청 처리 (데이터 조회)
function doGet(e) {
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

  return ContentService.createTextOutput(JSON.stringify(rows))
    .setMimeType(ContentService.MimeType.JSON);
}
```

3. **배포하기**
   - 배포 → 새 배포
   - 유형: 웹 앱
   - 실행 계정: 나
   - 액세스 권한: 모든 사용자
   - "배포" 클릭
   - **웹 앱 URL 복사** (예: `https://script.google.com/macros/s/AKfycby.../exec`)

### Step 3: index.html 수정

`submitForm` 함수를 다음과 같이 수정:

```javascript
// Form Submit
function submitForm(e) {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  data.timestamp = new Date().toISOString();
  data.id = Date.now();

  // Google Sheets로 전송
  const GOOGLE_SCRIPT_URL = 'YOUR_WEB_APP_URL_HERE'; // 위에서 복사한 URL

  fetch(GOOGLE_SCRIPT_URL, {
    method: 'POST',
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    if (result.success) {
      alert('상담 신청이 완료되었습니다.\\n빠른 시일 내에 연락드리겠습니다.');
      form.reset();
      closeModal();
    } else {
      throw new Error(result.error);
    }
  })
  .catch(error => {
    console.error('Error:', error);
    // 백업: LocalStorage에 저장
    const submissions = JSON.parse(localStorage.getItem('taxBeomDB') || '[]');
    submissions.push(data);
    localStorage.setItem('taxBeomDB', JSON.stringify(submissions));

    alert('상담 신청이 접수되었습니다.\\n빠른 시일 내에 연락드리겠습니다.');
    form.reset();
    closeModal();
  });
}
```

---

## 🎨 Google Sheets 활용 팁

### 1. 조건부 서식 설정

**상담 상태별 색상**:
- "대기" → 🟡 노란색
- "진행중" → 🔵 파란색
- "완료" → 🟢 초록색

**설정 방법**:
1. I열 선택
2. 서식 → 조건부 서식
3. 셀 값이 "대기"이면 노란색 배경
4. 반복해서 "진행중", "완료" 설정

### 2. 필터 보기 생성

- 데이터 → 필터 만들기
- 상담 상태, 담당자별로 빠르게 필터링

### 3. 알림 설정

- 도구 → 알림 규칙
- "스프레드시트가 변경되면" → 이메일/모바일 알림
- 새 상담 신청 즉시 알림 받기

### 4. 데이터 검증

**연락처 형식 검증**:
```
E열 선택 → 데이터 → 데이터 확인
텍스트 → 맞춤 수식: =REGEXMATCH(E2, "^010-\\d{4}-\\d{4}$")
```

### 5. 자동 계산

**월별 신청 건수**:
```
=COUNTIF(A:A, ">=2024-12-01")
```

**계약 전환율**:
```
=COUNTIF(M:M, "Y") / COUNTA(A:A) * 100
```

---

## 📊 대안 솔루션 비교

### 방법 1: Airtable (무료 ~ $20/월)

**장점**:
- ✅ 더 강력한 데이터베이스 기능
- ✅ 아름다운 UI
- ✅ 자동화 기능 (Zapier 유사)

**단점**:
- ❌ 무료 플랜 제한 (1,200개 레코드)
- ⚠️ 한국어 지원 부족

**추천**: 월 100건 이상 상담 시

### 방법 2: Notion Database (무료)

**장점**:
- ✅ 완전 무료
- ✅ 강력한 협업 기능
- ✅ 메모, 파일 첨부 자유로움

**단점**:
- ❌ API 연동이 Google Sheets보다 복잡
- ⚠️ 실시간 알림 부족

**추천**: 소규모 팀, 수동 입력 가능 시

### 방법 3: Netlify Forms ($19/월)

**장점**:
- ✅ Netlify와 완벽 통합
- ✅ 스팸 필터링
- ✅ 이메일 알림

**단점**:
- ❌ 유료 (월 100건 무료, 이후 $19/월)
- ❌ 데이터 관리 기능 부족

**추천**: 월 100건 미만 상담 시

---

## 🔐 보안 고려사항

### 1. 민감 정보 보호

- ✅ Google Sheets 공유 권한 "특정 사용자만"으로 제한
- ✅ 2단계 인증 활성화
- ✅ 주기적으로 공유 권한 검토

### 2. GDPR/개인정보보호법 준수

- ✅ 개인정보 수집 동의 받기 (현재 체크박스 있음)
- ✅ 30일 이상 미응대 시 삭제 or 별도 보관
- ✅ 고객 요청 시 데이터 삭제 가능하도록

### 3. 백업

- ✅ Google Sheets 자동 백업 (버전 기록)
- ✅ 주 1회 수동 Excel 다운로드 권장

---

## 📞 다음 단계: 카카오톡 상담 연결

별도 문서 `KAKAO_INTEGRATION_GUIDE.md` 참조

**핵심 방법**:
1. **카카오톡 채널 (무료)** - 추천!
2. **카카오 싱크 API** - 개발 필요
3. **카카오톡 상담톡** - 유료

---

## 🎯 최종 추천

**💚 1순위: Google Sheets + Apps Script**
- 무료
- 실시간 공유
- 관리 편리
- 구현 난이도: ⭐⭐⭐ (중)

**구현 시간**: 약 1시간
**유지비용**: 무료
**확장성**: ⭐⭐⭐⭐

---

## 📝 체크리스트

작업 전 확인:
- [ ] Google 계정 준비
- [ ] 관리자 이메일 리스트
- [ ] 스프레드시트 생성
- [ ] Apps Script 코드 복사
- [ ] 웹 앱 URL 획득
- [ ] index.html 수정
- [ ] 테스트 신청 (5회 이상)
- [ ] 관리자 권한 확인
- [ ] 모바일에서 테스트

완료 후:
- [ ] 실제 고객 신청 테스트
- [ ] 알림 설정
- [ ] 백업 계획 수립
- [ ] 팀원 교육

---

**작성일**: 2024-12-19
**작성자**: Claude AI
**업데이트**: 필요시 언제든지 문의
