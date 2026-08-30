# 디자인 토큰

> 정본. 웹·상세페이지·인쇄가 모두 여기서 값을 가져간다.

```css
:root{
  /* color */
  --paper:#FFFFFF;  --ink:#262320;      /* 2색이 전부 — 포인트 컬러 없음 */
  --paper-card:#FFFFFF;              /* 종이 위에 얹는 면 */
  --line:rgba(38,35,32,.14);         /* 경계선  = 잉크 투명도 */
  --muted:rgba(38,35,32,.55);        /* 보조 텍스트 */
  --faint:rgba(38,35,32,.06);        /* 면 구분 */

  /* type */
  --font:"Pretendard","Apple SD Gothic Neo","Malgun Gothic",system-ui,sans-serif;
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

## 인쇄 대응

| 토큰 | HEX | CMYK | Pantone |
|---|---|---|---|
| 종이 | #FFFFFF | — | 인쇄하지 않고 **내추럴 화이트 용지**로 대체 |
| 잉크 | #262320 | 미정 | **1도 인쇄.** 검정 별색 또는 K100+ |

> 2색이라 **전 인쇄물이 1도로 끝난다.** 별색·CMYK 매칭 불필요, 단가 하락.

→ Phase 4 패키징에서 인쇄소와 확정한다.

## 사용 규칙
- 하드코딩 금지. 색·크기·간격은 토큰 이름으로만 참조한다.
- **색은 2개가 전부다.** 회색이 필요하면 새 색을 만들지 말고 잉크의 투명도를 쓴다.
- 강조는 색이 아니라 **면 반전(잉크 채움)과 굵기(700)**로 한다.
- 모티프 SVG는 색을 갖지 않는다 — `currentColor`로 상속받는다.
- 간격은 4px 배수 밖으로 나가지 않는다.
