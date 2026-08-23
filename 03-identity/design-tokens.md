# 디자인 토큰

> 정본. 웹·상세페이지·인쇄가 모두 여기서 값을 가져간다.

```css
:root{
  /* color */
  --paper:#F6F1E8;  --ink:#262320;
  --persimmon:#D2502A; --celadon:#4A7A6B; --dust:#C9BFAE;
  --paper-card:#FFFFFF;      /* 카드 배경(종이 위에 얹는 면) */
  --line:#E4DCCD;            /* 경계선 */

  /* type */
  --font:"Wanted Sans","Pretendard",-apple-system,system-ui,sans-serif;
  --w-regular:400; --w-bold:700;
  --fs-title:28px; --fs-section:20px; --fs-sub:16px;
  --fs-body:15px;  --fs-caption:13px; --fs-label:12px;
  --lh-body:1.7;   --lh-title:1.35;

  /* space — 4px 배수 */
  --s1:4px; --s2:8px; --s3:12px; --s4:16px; --s5:24px; --s6:32px; --s7:48px; --s8:64px;

  /* shape */
  --r-sm:6px; --r-md:10px; --r-lg:16px;
  --stroke:2.6;              /* 모티프 기본 획(viewBox 100 기준) */
}
```

## 인쇄 대응 `[미정]`

| 토큰 | HEX | CMYK | Pantone |
|---|---|---|---|
| 종이 | #F6F1E8 | 미정 | 용지 자체로 대체 검토(내추럴 화이트) |
| 잉크 | #262320 | 미정 | 검정 별색 또는 K100+ |
| 감 | #D2502A | 미정 | **별색 권장** (CMYK 변환 시 탁해짐) |
| 청자 | #4A7A6B | 미정 | 미정 |

→ Phase 4 패키징에서 인쇄소와 확정한다.

## 사용 규칙
- 하드코딩 금지. 색·크기·간격은 토큰 이름으로만 참조한다.
- 모티프 SVG는 색을 갖지 않는다 — `currentColor`로 상속받는다.
- 간격은 4px 배수 밖으로 나가지 않는다.
