# OHARI — Brand

> 오하리상점 비주얼 아이덴티티 시스템.
> 확정본 (2026-11-01). 로고=손글씨 영문 워드마크 2종(심볼 없음) · 컬러=종이·잉크 2색 · 폰트=Pretendard Light/Regular, 제목은 손글씨 · 일러스트=모티프 28종 + 실루엣 7종 + 거북이.

**목차**: Logo · Color · Typography · Illustration · Imagery · Assets

---

## 01. Logo

**심볼 없음 — 손글씨 워드마크가 로고다.** 재은의 손글씨를 벡터화한 영문 워드마크 2종만 쓴다. 폰트 의존 0, 단일 패스 SVG.
한글 `오하리상점`은 **로고로 쓰지 않는다** — 스마트스토어 상호·본문 텍스트(Pretendard)로만 쓴다. 거북이는 캐릭터이지 로고가 아니다(→ 04. Illustration).

로고를 클릭하면 해당 SVG가 바로 내려받아진다.

```tl-logos zip=ohari-logos.zip also=assets/logo/logo-ohari.svg,assets/logo/logo-oharistore.svg
assets/logo/logo-ohari-ink.svg | light | Primary · OHARI | 잉크 SVG ↓
assets/logo/logo-ohari-white.svg | dark | Reversed · OHARI | 화이트 SVG ↓
```

```tl-logos quiet zip=ohari-logos.zip
assets/logo/logo-oharistore-ink.svg | light | Extended · OHARI STORE | 잉크 SVG ↓
assets/logo/logo-oharistore-white.svg | dark | Extended · White | 화이트 SVG ↓
```

### 두 워드마크의 자리

| 워드마크 | viewBox | 쓰는 자리 |
|---|---|---|
| **OHARI** | 350×135 (약 2.6:1) | **패키지** — 박스 윗면·옆면, 원형 봉인 스티커, 명함, 엽서, 네임택. 면이 조용해야 그릇 사진이 산다 |
| **OHARI STORE** | 684×138 (약 5:1) | **채널·대문** — 스마트스토어 대문·헤더, 인스타 프로필, 쇼핑백 사각 스티커, 띠지·테이프. 가로로 긴 자리 |

둘 다 같은 손글씨에서 나왔다. 한 화면에 둘을 같이 두지 않는다.

### Color 사용

| 배경 | 워드마크 색 |
|---|---|
| 종이 / 밝은 사진 | 잉크 `#262320` |
| 잉크 / 어두운 바탕 | 화이트 `#FFFFFF` |

잉크/화이트는 **형태·비율 100% 동일, 채움색만 반전**. 그 외 컬러 없음. 웹에서는 `currentColor` 판(`logo-ohari.svg`·`logo-oharistore.svg`)을 쓰고 CSS `color`로 제어한다.

### Clearspace · Minimum Size
- **클리어스페이스**: `O`의 높이(캡 높이)의 **1/2**을 사방 여백으로.
- **최소 크기**: OHARI 가로 ≥ 64px(디지털) / ≥ 15mm(인쇄) — 64px까지 읽히는 것을 확인했다. OHARI STORE는 가로 ≥ 120px / ≥ 28mm.
- 그보다 작은 자리(파비콘·택)는 로고를 넣지 않는다. 거북이 단독도 24px 아래에서는 선이 사라지므로 쓰지 않는다.

### Don'ts
비율 변형·기울임·회전 / 획 굵기 변경·외곽선 추가 / 잉크·화이트 외 색 / 그라디언트·그림자 / 사진 위에 직접 얹기(단색 면 위에만) / 폰트로 다시 치기 / 한글 워드마크 병기 / 거북이를 로고 옆에 붙여 락업 만들기.

---

## 02. Color

**2색. 종이와 잉크가 전부다.** 포인트 컬러를 쓰지 않는다. 따뜻함은 색이 아니라 **손그림이 담당**하고, 채도는 **그릇 사진이 담당**한다. 그래서 전 인쇄물이 **1도**로 끝난다.

```tl-swatches
종이 | #FFFFFF | --paper | 기본 배경 · 박스 원지 · 인쇄물 바탕(인쇄하지 않고 내추럴 화이트 용지로)
잉크 | #262320 | --ink | 선 · 글자 · 로고 · 일러스트 · 끈(검정 마끈·공단). 순수 블랙보다 따뜻해 손그림과 붙는다
```

위계는 색이 아니라 **잉크의 농도**로 만든다.

| 파생 | 값 | 용도 |
|---|---|---|
| `--line` | `rgba(38,35,32,.14)` | 경계선 · 카드 테두리 |
| `--muted` | `rgba(38,35,32,.55)` | 캡션 · 보조 텍스트 |
| `--faint` | `rgba(38,35,32,.06)` | 면 구분 |

### 강조는 이렇게
| 상태 | 표현 |
|---|---|
| 기본 버튼 · 선택된 라벨 | 잉크 채움 + 종이 글씨 (**면 반전이 강조 수단**) |
| 보조 버튼 · 미선택 라벨 | `--line` 테두리 + 잉크 글씨 |
| 비활성 · 품절 | `--muted` + 테두리 |
| 강조 텍스트 | 색이 아니라 **크기·여백**으로. 굵은 볼드(700)는 쓰지 않는다 |
| 경고 · 마감 | 텍스트로 명시 ("오늘 발송 마감") |

### 보류색 — 감 `#D2502A` [미사용]
기본 사용량 0. 시즌 한정 패키지·세일 고지에 되살릴 수 있고, 조건은 **면적 2% 이하, 한 화면에 한 번**. 토큰에 넣지 않는다.

### 접근성 · 인쇄
| 조합 | 대비 | 판정 |
|---|---|---|
| 잉크 / 종이 | 약 14:1 | ✅ AAA |
| 종이 / 잉크 (반전) | 약 14:1 | ✅ AAA |
| `--muted` / 종이 | 약 6:1 | ✅ AA (캡션 한정) |

> 인쇄는 전부 **검정 1도(K100)**. 별색·CMYK 매칭 없음. 종이는 인쇄하지 않고 **내추럴 화이트 용지** 자체로 대체한다. 그라디언트 금지, 색은 면으로만, 상품 사진 위에는 어떤 브랜드 컬러도 얹지 않는다.

---

## 03. Typography

**본문 = Pretendard Light(300) · Regular(400). 제목 = 손글씨.** 글씨체로 제목을 만들지 않는다 — 제목·헤드라인 자리는 손글씨 SVG(로고, `text-*.svg`)가 맡고, 나머지 모든 글은 Pretendard 두 웨이트로 끝낸다. **700 볼드는 쓰지 않는다.**

| 역할 | 무엇 | 웨이트 | 쓰임새 |
|---|---|---|---|
| 로고 · 헤드라인 | **손글씨 SVG** | — | 워드마크, `A Little Care` · `Use & Care` · `Slowly is wonderful.` 같은 문구 |
| 본문 (Body) | Pretendard | **300** | 상세페이지 본문 · 엽서 뒷면 · 안내문 |
| 강조 · 소제목 · UI | Pretendard | **400** | 상품명 · 가격 · 버튼 · 라벨 · 법정 표기 |
| 캡션 | Pretendard | 300 (`--muted`) | 사이즈 · 주의 · 출처 |

### 타입 스케일

```tl-spec
display · 손글씨가 맡는 자리 (Pretendard로 치지 않는다) | 300 | 36 | display · 손글씨 SVG
title · 둘이 쓰는 첫 상 | 400 | 22 | title/md · 400 · 1.35
sub · 밥공기 둘, 접시 둘, 수저 한 벌 | 400 | 16 | sub/md · 400 · 1.5
body · 매일 쓰는 그릇이라 손에 쥐었을 때 무겁지 않은 것만 골랐습니다. | 300 | 15 | body/md · 300 · 1.7
caption · 지름 21cm · 전자레인지 ○ · 식기세척기 ○ · 오븐 ✕ | 300 | 13 | caption · 300 · 1.5
LABEL · 집들이 · 이사 | 400 | 12 | label · 400 · 1.4
```

| 토큰 | 웨이트 | 크기 / 행간 | 용도 |
|---|---|---|---|
| `display` | 손글씨 | — | 히어로 · 배너 문구 (SVG) |
| `title/md` | 400 | 22px / 1.35 | 세트명 · 섹션 제목 |
| `sub/md` | 400 | 16px / 1.5 | 구성품 · 소제목 |
| `body/md` | **300** | 15px / 1.7 | 본문 |
| `caption` | 300 | 13px / 1.5 | 사이즈 · 주의 · 출처 |
| `label` | 400 | 12px / 1.4 | 상황 라벨 · 필터 |

### 운용
- **자간 0.** 손글씨와 나란히 놓이므로 글씨체는 조용히. 영문 대문자 라벨도 자간을 벌리지 않는다.
- 강조는 **굵기(400)** 또는 **면 반전**으로. 밑줄·그림자·이탤릭 금지.
- 본문 최소 15px(모바일 14px). 숫자(사이즈·가격)는 항상 400.
- 손글씨 문구는 **SVG 정본만** 쓴다. 폰트로 흉내 내지 않고, 새 문구가 필요하면 같은 손으로 써서 벡터화한다(→ 04. 재현).

---

## 04. Illustration

**이 그림이 브랜드의 차별점이다.** 상품은 도매라 남과 겹치지만, 이 그림은 겹치지 않는다. 정본은 **그린 것**이지 생성한 것이 아니다 — 재은이 그린 시트를 potrace 베지어 곡선으로 따서 SVG로 만든다. 코드로 형태를 만들지 않는다.

### 선의 성격 (새 그림이 지켜야 할 것)
| # | 특징 |
|---|---|
| 1 | **얇고 고른 선.** 붓펜이 아니라 가는 펜. 두께 변화가 거의 없다 (`--stroke 2.6`, viewBox 100 기준 · 보이는 두께 `TARGET 5.2`) |
| 2 | **모서리가 둥글다.** 각진 곳이 없고 전체가 부풀어 있다 |
| 3 | **삐뚤삐뚤하다.** 원이 정확한 원이 아니고, 좌우가 다르다 |
| 4 | **작은 얼굴을 넣기도 한다.** 점 눈 + 작은 입. 얼굴은 한 종류만 쓴다 |
| 5 | **디테일은 무늬로.** 물결·점·빗금 |
| 6 | **면을 칠하지 않는다.** 하트만 예외 |

### 모티프 — 시트 v1 선물·테이블웨어 16종

아이콘을 누르면 SVG가 내려받아진다. 전부 `viewBox 0 0 100 100` · `fill="currentColor"` · 단일 패스.

```tl-pictos zip=ohari-motifs.zip
assets/motif/motif-plate.svg | 접시
assets/motif/motif-bowl.svg | 볼
assets/motif/motif-cup.svg | 잔
assets/motif/motif-spoon.svg | 수저
assets/motif/motif-fork.svg | 포크
assets/motif/motif-knife.svg | 나이프
assets/motif/motif-flower.svg | 꽃
assets/motif/motif-vase.svg | 화병과 꽃
assets/motif/motif-candle.svg | 초
assets/motif/motif-ribbon.svg | 리본
assets/motif/motif-book.svg | 책
assets/motif/motif-heart.svg | 하트
assets/motif/motif-clover.svg | 클로버
assets/motif/motif-star.svg | 별
assets/motif/motif-fish.svg | 물고기
assets/motif/motif-pear.svg | 배
```

### 모티프 — 시트 v2 바다 12종
여름 시즌·해산물 품목·아동 선물 쪽으로 넓힐 때 쓰는 세트. 기본 세트는 v1이고, v1과 한 화면에 섞을 때는 같은 굵기 규칙을 따른다.

```tl-pictos quiet zip=ohari-motifs.zip
assets/motif/motif-urchin.svg | 성게
assets/motif/motif-anemone.svg | 말미잘
assets/motif/motif-starfish.svg | 불가사리
assets/motif/motif-clam.svg | 진주조개
assets/motif/motif-coral.svg | 산호
assets/motif/motif-seahorse.svg | 해마
assets/motif/motif-wave.svg | 파도
assets/motif/motif-seaweed.svg | 해초
assets/motif/motif-sea-clover.svg | 바다클로버
assets/motif/motif-conch.svg | 소라
assets/motif/motif-sparkle-star.svg | 반짝별
assets/motif/motif-crab.svg | 게
```

### 캐릭터 — 거북이
**행운을 등에 지고 간다.** 한국·동아시아에서 설명 없이 읽히는 상징이라 카피가 필요 없다. 이름은 없고, 지칭은 "거북이" 하나. 표정은 점 눈 + 작은 입 하나, 포즈 변형은 최대 5종. **로고 자리에 세우지 않는다** — 화면의 주인공은 언제나 그릇이다.

```tl-pictos quiet zip=ohari-motifs.zip
assets/motif/char-turtle.svg | 거북이 (정본)
```

| ✅ 거북이가 사는 자리 | ❌ 쓰지 않는 자리 |
|---|---|
| 엽서 · 네임택 · 스티커 · 띠지 · 에디토리얼 | **로고 자리**, 상품 사진 위 |
| 안내 문구 옆 작게, 한 화면에 **하나** | **배송·물류 맥락** (송장·발송 지연 공지 — "느리다"로 읽힌다) |
| 패턴(파도 속 거북이) | 옷 입히기 · 소품 들리기 · 표정 늘리기 |

### 케어 아이콘 7종 (v3)
네임택·상세페이지의 세척·가열 안내용. 같은 손으로 그려 같은 굵기로 땄다. 반드시 **텍스트 라벨과 병행**한다(아이콘만으로 전달 금지).

```tl-pictos zip=ohari-care-icons.zip
assets/v3/care-microwave.svg | 전자레인지 가능
assets/v3/care-no-microwave.svg | 전자레인지 불가
assets/v3/care-dishwasher.svg | 식기세척기 가능
assets/v3/care-no-dishwasher.svg | 식기세척기 불가
assets/v3/care-oven.svg | 오븐 가능
assets/v3/care-no-oven.svg | 오븐 불가
assets/v3/care-no-fire-oven.svg | 직화 · 오븐 불가
```

### 실루엣 모티프 7종
선 그림과 짝을 이루는 **면 채움** 버전. 패키지에 쓰인 것만 정본으로 둔다 — 큰 상자 후면(주전자·볼·포크·수저·머그), 작은 상자 윗면(거북이·클로버). 선 그림과 한 면에 섞지 않는다 — 실루엣은 실루엣끼리.

```tl-pictos zip=ohari-motifs.zip
assets/v3/silhouette-pitcher.svg | 실루엣 · 주전자
assets/v3/silhouette-bowl.svg | 실루엣 · 볼
assets/v3/silhouette-fork.svg | 실루엣 · 포크
assets/v3/silhouette-spoon.svg | 실루엣 · 수저
assets/v3/silhouette-mug.svg | 실루엣 · 머그
assets/v3/silhouette-turtle.svg | 실루엣 · 거북이
assets/v3/silhouette-clover.svg | 실루엣 · 클로버
```

### 법정 표시 — '식품용' 마크
식약처가 정한 **식품용 기구 도안**. 브랜드 요소가 아니라 법정 표시라 **손그림으로 다시 그리거나 색·비율을 바꾸지 않는다.** 네임택 뒷면·라벨 스티커의 표시 사항 자리에 원본 그대로 넣는다(→ Packaging 「06」).

```tl-pictos zip=ohari-care-icons.zip
assets/v3/mark-food-contact.svg | 식품용 기구 마크 (식약처 원본)
```

### 손글씨 문구 · 패턴 (v3)

손글씨 문구 3종은 **제목 자리**를 맡는다(→ 03. Typography). 해초 띠 패턴은 박스 윗면·띠지의 면 요소.

```tl-sheets land zip=ohari-handwriting-patterns.zip
assets/v3/text-a-little-care.svg | A Little Care
assets/v3/text-use-and-care.svg | Use & Care
assets/v3/text-slowly.svg | Slowly is wonderful.
assets/v3/pattern-seaweed-band.svg | 패턴 · 해초 띠
```

### 조합 규칙
- 그림과 사진은 자리를 나눈다 — **제품 사진 위에 일러스트를 얹지 않는다.** 그림은 여백·패키지·카드·에디토리얼에 산다.
- 한 면에 모티프는 **3~5개**, 거북이는 하나. 크기는 두 단계(큰 것 하나 + 작은 것들)까지.
- 색은 잉크 단색. 면 채움 금지(하트 예외). 그라디언트·그림자·외곽선 추가 금지.
- 작게 줄여도 살아야 한다 — 24px 아래에서는 모티프를 쓰지 않는다.

### 재현
```
그림(PNG) → 03-identity/vectorize.py (v1) · vectorize_sea.py (v2) · gen_v3.py (v3) → SVG
```
새 시트를 그릴 때는 `assets/reference/motif-sheet-v1.jpg`를 참조 이미지로 옆에 둔다 — 같은 손을 유지하는 방법이다. 트레이싱은 반드시 **potrace 곡선**(2배 업스케일 + σ1.2 블러 후). 직선 근사는 지그재그로 깨져 거부됐다.

---

## 05. Imagery

사진·화면·인쇄물이 지켜야 할 세 가지. 이 셋만 지키면 오하리상점 그림이 된다.

| 규칙 | 뜻 | 어디서 보이나 |
|---|---|---|
| **손으로 그린 선** | 로고·그림·글씨는 사람이 펜으로 그린 것만 쓴다. 폰트나 벡터 아이콘으로 흉내 내지 않는다 | 로고 · 일러스트 · 손글씨 문구 |
| **흰 바탕, 색은 그릇만** | 배경은 흰색, 선은 잉크 한 색. 화면에서 색이 있는 건 **그릇 사진뿐**이다. 파스텔·필터·색 소품을 쓰지 않는다 | 컬러 · 촬영 · 배경 |
| **비워 둔다** | 꽉 채우지 않는다. 한 면에 그림은 3~5개, 거북이는 하나. 요소를 더 넣고 싶을 때가 멈출 때다 | 레이아웃 · 패키지 · 상세페이지 |

이 셋이 함께 만드는 인상: **누가 손으로 그려서 싸 준 것 같은데, 지저분하지는 않은.**

```tl-cards half
# Do
- 흰 배경 · 자연광 · 그릇의 유약색이 화면의 유일한 채도
- 세트를 **한 상 차린 모습**으로 — 조합이 보여야 안목이 보인다
- 포장 공정(에어캡 → 습자지 → 마끈)을 사진으로 보여 준다
- 손글씨·거북이는 여백에, 작게, 하나
- 여백이 곧 가격대 — 요소를 더 넣고 싶을 때가 위험 신호
# !Don't
- **파스텔톤** (유아용품·문구점으로 읽히고 3~7만 원이 설명되지 않는다)
- 기계적 대칭 · 그라디언트 · 균일한 벡터 선 ("AI가 그린 귀여움")
- 크라프트지 + 스탬프 핸드메이드 클리셰, 캘리그라피 감성 문구
- 갤러리식 무채색 절제 (로파서울·이나피스퀘어의 자리)
- 제품 사진 위 일러스트 · 스티커 남발 · 시즌 컬러 총동원
```

---

## 06. Assets

```tl-kit zip=ohari-brand-kit.zip
브랜드 킷 전체 | 워드마크 6종 · 모티프 28종 + 거북이 + 실루엣 7종 · 케어 아이콘 7종 · 손글씨·패턴 4종 · 패키지 시안 · 문서 md 4종 | Download all ↓
assets/logo/*.svg
assets/motif/*.svg
assets/v3/*.svg
assets/proofs/*.jpg
assets/proofs/*.png
assets/proofs/box-large/*.jpg
assets/proofs/box-small/*.jpg
assets/proofs/mockup/*.jpg
md/*.md
```

### 카테고리별 받기

```tl-dl
묶음 zip ↓ | 워드마크 6종=ohari-logos.zip | 모티프·거북이·실루엣 36종=ohari-motifs.zip | 케어 아이콘 7종 + 식품용 마크=ohari-care-icons.zip | 손글씨·패턴 4종=ohari-handwriting-patterns.zip | 패키지 시안=ohari-package-proofs.zip
```

| 파일 | 용도 | 사양 |
|---|---|---|
| `logo-ohari-{ink,white}.svg` · `logo-ohari.svg` | 워드마크 OHARI (패키지) | 손글씨 벡터 · 350×135 · currentColor 판은 웹용 |
| `logo-oharistore-{ink,white}.svg` · `logo-oharistore.svg` | 워드마크 OHARI STORE (채널·대문) | 손글씨 벡터 · 684×138 |
| `motif-*.svg` 28종 · `char-turtle.svg` | 일러스트 정본 | viewBox 100 · currentColor · 단일 패스 · 색 기본값 `#262320` |
| `care-*.svg` 7종 | 세척·가열 안내 아이콘 | viewBox 100 · currentColor |
| `mark-food-contact.svg` | 식품용 기구 마크 (법정 표시 · 식약처 원본) | 원본 그대로 · 변형 금지 |
| `silhouette-*.svg` 7종 | 실루엣 모티프 (면 채움) | viewBox 100 · currentColor |
| `text-*.svg` 3 · `pattern-seaweed-band.svg` | 손글씨 제목 · 해초 띠 패턴 | currentColor |
| `proofs/` | 패키지 확정 시안 7종 + 목업 | jpg/png · 발주 원본은 Figma (→ Packaging) |

> 원본(소스): `03-identity/`(로고·모티프·v3) · `assets/package-proofs-261025/`(시안). 브랜드북 사본: `07-brand-book/assets/`. 원본을 고치면 사본도 같이 고친다.
