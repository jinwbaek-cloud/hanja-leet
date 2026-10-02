# 한알국쉬(리트버전)

## 기본 정보
- **프로젝트명**: 한알국쉬(리트버전)
- **운영 주소**: [https://leet.easyhanja.org](https://leet.easyhanja.org)
- **작업 프로젝트**: `leet_hanja_02`
- **목적**: LEET 언어이해·추리논증 기출 한자어 학습 웹서비스

---

## 주요 파일 구조
- `index.html`: 메인 웹 애플리케이션 (React UMD + Tailwind 기반 SPA)
- `about.html`: 플랫폼 소개 및 개발 취지
- `guide.html`: 4대 핵심 학습 엔진 활용 가이드
- `js/leet_data.js`: 메인 LEET 373개 어휘 데이터셋 (`window.MOCK_WORDS`)
- `legal_words.json`: 현재 서비스 미사용 연구/수집 중간 데이터 (기존 수집본 중 48건이 `leet_data.js`에 이식 완료됨)
- `fetch_legal_words.py`: 공공데이터포털 법률용어 수집 보조 스크립트 (환경변수 `DATA_GO_KR_SERVICE_KEY` 사용)
- `pdf/`: LEET 기출문제 원본 PDF 20개 (Git 배포 대상 제외)
- `qr_code.png`: 플랫폼 소개 페이지 내 후원 QR 코드 이미지
- `naver59e8a66e935f98c16a5e4376d3dfb872.html`: 네이버 서치어드바이저 사이트 소유확인용 파일

---

## 배포 아키텍처

### 향후 운영 방식
```text
로컬 수정
→ Git commit
→ GitHub main branch push
→ Netlify 자동배포
→ https://leet.easyhanja.org 반영
```

### Netlify 배포 설정
- **Build command**: (없음 / 비워둠)
- **Publish directory**: `.` (루트 디렉토리)

---

## 관리자 데이터 수정 및 영구 반영 절차

현재 관리자 패널(푸터 숨김 점 `•` 클릭)에서 수정한 어휘 데이터는 Netlify 서버나 GitHub에 직접 저장되지 않습니다.

### 영구 반영 워크플로우
```text
로컬 leet_data.js 수정/저장 (File System Access API 또는 다운로드 덮어쓰기)
→ git commit
→ git push
→ Netlify 자동배포
```

---

## Git 제외 대상 (.gitignore)
- `pdf/` (대용량 기출문제 원본 PDF, 약 91MB)
- `.DS_Store` (macOS 메타데이터)
- `.env`, `.env.*` (환경변수 설정 파일)
- `__pycache__/`, `*.pyc` (파이썬 캐시)
- `.vscode/`, `.idea/` (에디터 설정)

---

## TODO (향후 고도화 과제)
- [ ] favicon 제작 및 등록
- [ ] 모바일 UI/UX 고도화 (헤더 2단 액션 버튼 배치 최적화 및 퀴즈 모달 스크롤 개선)
- [ ] Babel Standalone 및 Tailwind Play CDN 기반 구조의 향후 현대화 검토 (Vite + React 번들러 전환 검토)
- [ ] 법률기초 어휘 중 한자/자구분해 결측 데이터(41건) 검증 및 보완
- [ ] 수능버전 「한알국쉬」와의 패밀리룩 디자인 및 컴포넌트 일원화
