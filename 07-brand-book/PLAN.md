# 오하리상점 브랜드북 — 구축 계획 (2026-11-01)

> 타입라운지 브랜드북(`space-brand-system/07-brand-book`, typelounge.vercel.app/brand 형식)을 그대로 빌려 오되,
> 공간 브랜드의 "Signage·Product" 자리를 쇼핑몰 브랜드의 "Packaging·Commerce"로 바꾼다.
> **md가 단일 소스**, `build_book.py`로 4탭 단일 HTML을 빌드, 각 탭에서 SVG·이미지·md·zip을 바로 내려받는다.

---

## 0. 전제 (2026-11-01 재은 확정)

| 항목 | 확정 |
|---|---|
| 로고 | **영문만**. `OHARI`(350×135) · `OHARISTORE`(684×138) — `Downloads/OHARI.svg`·`OHARISTORE.svg`로 교체. 한글 워드마크·거북이 시그니처 락업은 브랜드북 로고 섹션에서 제외 |
| 패키지 | 10-25 발주처 시트의 시안 7종·사이즈 **그대로** (상자 큰 360×270×110 / 작은 270×220×110, 원형 스티커 50×50, 엽서 100×148, 네임택 80×140, 명함 90×50, 쇼핑백 스티커 70×160) |
| 끈 | 마끈 블랙 + 공단 블랙 6mm 기본, 버건디·녹색은 크리스마스 에디션 |
| 쇼핑백 | 무지 + 사각 스티커, 아트/이담 코팅·럭셔리 후보, 색·라인 미정 |
| 바탕 문서 | 기존 `03-identity/logo-guide.html`·`deck-logo-package.html`의 내용 + 01-strategy·03-identity·04-packaging md |

---

## 1. 탭 구성 (타입라운지 ↔ 오하리)

| 타입라운지 | 오하리상점 | 파일 | 내용 |
|---|---|---|---|
| Brand | **Brand** | `brand.md` | Logo · Color · Typography · Illustration(모티프·캐릭터·케어 아이콘) · Imagery · Assets |
| BX | **BX** | `bx.md` | Brand Platform · Persona · Tone of Voice · Brand Language · Sample Copy(엽서·상세) · Target · Positioning · Brand Story(거북이 세계관) |
| Signage | **Packaging** | `packaging.md` | 패키지 시스템(2겹·박스 안 포장 순서) · 인쇄물 7종 시안+사이즈 · 끈·쇼핑백 · 라벨 법정 표기 · 발주처(링크) |
| Product | **Commerce** | `commerce.md` | 웹 토큰(Pretendard·2색) · 컴포넌트 최소(버튼·라벨·카드·가격) · 진열 규칙(상황 1차·무게 2차) · 상세페이지·썸네일·〈복 지고 간 상〉 포맷 · 채널별 보이스 |

---

## 2. 탭별 목차 초안

### Brand (`brand.md`)
1. **Logo** — 워드마크 2종 `OHARI` / `OHARISTORE`. 손글씨 벡터, 폰트 의존 0.
   - 쓰임 분리: `OHARI` = 패키지(박스 윗면·원형 스티커·명함) / `OHARISTORE` = 웹 헤더·띠지·테이프·쇼핑백 스티커 (기존 규칙 "한글=웹, 영문=패키지"는 **영문 단일로 개정**)
   - 색: 잉크 `#262320` / 화이트 반전. 클리어스페이스·최소 크기·Don'ts
   - 다운로드: `logo-ohari-{ink,white,current}.svg` · `logo-oharistore-{ink,white,current}.svg` + zip
2. **Color** — 2색(종이 `#FFFFFF`·잉크 `#262320`) + 파생 투명도 3단. 포인트 컬러 없음, 보류색 감 `#D2502A` 미사용 기록. 인쇄 1도
3. **Typography** — Pretendard 400/700 (제목 자리는 손글씨 SVG가 맡는다). 타입 스케일·자간
4. **Illustration** — 모티프 28종(v1 16 + v2 바다 12) · 캐릭터 거북이·강아지 · v3(케어 아이콘 7·손글씨 3·패턴 4·실루엣 3·선그림 시트 A/B/C). 선 규칙(`--stroke 2.6`)·조합 규칙·금지. 전부 클릭 다운로드 + zip
5. **Imagery** — 손의 흔적·담백한 밝음·넉넉한 여백 / 회피(파스텔·AI티·핸드메이드 클리셰·갤러리 무채색). 촬영 Do/Don't
6. **Assets** — 브랜드 킷 전체 zip(로고·모티프·캐릭터·케어·패턴·md 4종) + 카테고리별 zip

### BX (`bx.md`)
1. Brand Platform — Concept "주는 마음을 고르는 선물가게" · 첫 문장 "골라서 모으고, 싸서 보냅니다"
2. Persona — 다정한, not 호들갑 / 구체적인, not 두루뭉술 / 솔직한, not 자기폄하 (`brand-voice.md`)
3. Tone of Voice — We are / We are not + ✓✗ 예문
4. Brand Language — Use/Avoid 어휘(택갈이 금지·'복'은 접점당 1회·직접 축원 금지·'깃들다' 회피)
5. Sample Copy — 엽서 A안·B안 확정 문안, 상품 상세 한 단락, 품절·배송 안내
6. Target — 여성 중심, 캐주얼 선물 3~5만(상단 7만)
7. Positioning — 매대/직접경쟁/대체재 3층, 빈자리 = 손그림 + 상황진열 + 세트
8. Brand Story — 거북이(이름 없음, 복을 지고 간다), 〈복 지고 간 상〉 세계관 지리

### Packaging (`packaging.md`)
1. Principles — 화이트 박스·먹1도·2겹 구조·기본 포장료 포함
2. 구성품 인벤토리(확정 7종) — 시안 이미지 + 사이즈 + 수량 + 발주처. **사이즈 숫자는 10-25 시트와 1:1**
3. 박스 안 포장 순서 — 에어캡 → 습자지 → 마끈 십자 → 같은 높이 → 네임택 → 트레이싱지 → 뚜껑 안 원형 스티커 (목업 사진 6장)
4. 끈 — 마끈 블랙 2mm / 공단 블랙 6mm 기본, 크리스마스 에디션 버건디·녹색
5. 쇼핑백 — 무지 + 사각 스티커, 조합 4안, 색 미정
6. 라벨 법정 표기 7항목 + '식품용' 아이콘 규칙 (`label-spec.md`)
7. 발주처·단가 — 발주처 비교 시트로 링크(숫자는 그쪽이 정본, 여기 중복 기재 안 함)
8. 다운로드 — 시안 7종 이미지 zip, 엽서·네임택 문안 md

### Commerce (`commerce.md`)
1. Principles — 색 없이 위계(면 반전·굵기), 상품 사진이 색을 담당
2. Tokens — `design-tokens.md` CSS 그대로
3. Components — 버튼 2종·라벨(선택/미선택)·카드(`--line` 테두리)·가격·품절 상태
4. 진열 — 1차 상황 5종(집들이·결혼·감사·생일·나에게) · 2차 무게 · 카테고리는 필터 · 단품 노출 규칙
5. 상세페이지·썸네일 — 구성·촬영 가이드 · 〈복 지고 간 상〉 포맷(`06-commerce/bok-jigogan-sang-01-03.md`)
6. 채널 — Tier 0~3, 채널별 보이스 조절
7. Accessibility — 대비표(2색이라 전부 AAA)

---

## 3. 파일 구조

```
b2c-gift-brand/07-brand-book/
├── PLAN.md                 ← 이 문서
├── brand.md · bx.md · packaging.md · commerce.md   ← 단일 소스
├── build_book.py           ← space-brand-system 것을 복사해 와서 수정
├── shell.html              ← 탭 4개·사이드바·다운로드 핸들러 (복사 후 브랜드 토큰만 교체)
├── assets/
│   ├── logo/        logo-ohari-*.svg · logo-oharistore-*.svg (6종)
│   ├── motif/       motif-*.svg 28 + char-*.svg 2  (03-identity 사본)
│   ├── v3/          care-*.svg 7 · text-*.svg 3 · pattern-*.svg 4 · silhouette-*.svg 3
│   ├── proofs/      시안 7종 jpg/png + mockup 6장 (package-proofs-261025 사본)
│   └── md/          4개 md 사본(다운로드용)
└── site/ · site/standalone/index.html   ← 빌드 산출물, 손대지 않음
```

---

## 4. 작업 순서

| # | 단계 | 산출 | 비고 |
|---|---|---|---|
| 1 | **로고 교체** — Downloads 2종을 `03-identity/`에 정본으로 넣고 ink/white/currentColor 6종 생성 (`fill` 치환 스크립트) | `logo-ohari-*.svg` `logo-oharistore-*.svg` | 기존 `logo-wordmark-en/ohari-*.svg`는 `_legacy/`로 이동, 한글·시그니처는 그대로 보관(브랜드북엔 미노출) |
| 2 | **빌더 이식** — `build_book.py`·`shell.html` 복사, 경로·탭 이름(Brand/BX/Packaging/Commerce)·파일명 스탬프(`ohari_brandbook`)·폰트(Paperlogy→Pretendard CDN 또는 시스템) 교체 | 빈 4탭이 빌드되는 상태 | `tl-logos`의 `orange` 배경 옵션은 안 씀(2색) |
| 3 | **brand.md** 작성 — logo-guide.html·color-palette·design-tokens·illustration-system·visual-principles에서 옮김 | | 모티프 30종 `tl-pictos` 그리드로 클릭 다운로드 |
| 4 | **bx.md** 작성 — brand-voice·positioning·personas·character·character-world·postcard-copy | | |
| 5 | **packaging.md** 작성 — box-system §7·label-spec·10-25 시트의 시안 섹션 | | 시안 이미지는 `tl-shots`/`tl-sheets` 펜스 |
| 6 | **commerce.md** 작성 — design-tokens·curation-criteria §6·channel-strategy·06-commerce | | |
| 7 | **빌드·검증** — 4탭 렌더 스크린샷 + playwright로 다운로드 클릭 테스트(file://·http) | `site/standalone/index.html` | 타입라운지 때 `file://` 다운로드 함정 그대로 적용 |
| 8 | 커밋·푸시(양쪽) + README 갱신 + NMWC 위키 첨부 | | 배포는 GitHub만(별도 호스팅 없음) |

---

## 5. 확인 결과 (2026-11-01 재은 답변 · 승인)

1. 거북이 — 로고 섹션 제외, Illustration(캐릭터)·BX(세계관)에는 유지
2. 한글 `오하리상점` — **로고로는 아예 사용 안 함**. 스마트스토어 상호·본문 텍스트로만. 대문·헤더는 영문 로고
3. 발주용 원본 — Figma: https://www.figma.com/design/gBU5G6YNK0ILgW9v2nsWVF/ (node 171-18). Packaging 탭에서 링크로 연결, 시안 이미지는 jpg/png 다운로드
4. Commerce — **자사몰 없음, 네이버 스마트스토어 우선**. 세트·단품 둘 다 판매. 〈복 지고 간 상〉 회차 포맷은 **쓰지 않음**. 상황별 추천 카테고리는 유지. 탭 내용은 진열·상세 규칙 위주
5. 폰트 — 본문 **Pretendard Light(300) / Regular(400)**, 제목은 **손글씨(SVG)**. 700 볼드 체계는 폐기
