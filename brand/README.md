# TORTÉ — логотип

## Итоговый логотип (`final/`)

Черепаха «Купол» + надпись TORTÉ (Cormorant Garamond, в кривых).

| Файл | Где использовать |
|---|---|
| `torte-logo-stacked.svg` / `-ivory` | Основной: знак над надписью, «HAIR STUDIO · MOSCOW» |
| `torte-logo-horizontal.svg` / `-ivory` | Шапка сайта, бланки, узкие места |
| `torte-logo-compact.svg` / `-ivory` | Черепаха + TORTÉ без подписи — шапка сайта, аватарки |
| `torte-logo-nav-*.svg` | Шапка сайта: знак + TORTÉ + «HAIR STUDIO · MOSCOW» в одну строку (`-gold-light` — на сайте) |
| `torte-mark.svg` / `-ivory` | Только черепаха |
| `torte-wordmark.svg` / `-ivory` | Только надпись |
| `favicon.svg` | Иконка сайта |

`-ivory` — светлые версии для тёмного/оливкового фона, `-gold` — золото #C5A66A, `-gold-light` — светлое золото #E6CF9A для шалфейного фона.

---

# Варианты, которые рассматривали

## Черепаха с кулона (`pendant/`)

Контур обведён вручную по фото кулона и выровнен.

| Файл | Что это |
|---|---|
| `turtle-gold.svg` | Золотая «ювелирная» версия (градиент, блик, тень, глаз-камушек) |
| `turtle-gold-charm.svg` | То же с колечком и бейлом подвески |
| `turtle-olive.svg`, `turtle-ivory.svg` | Однотонные версии для печати/гравировки |
| `lockup-gold-stacked*.svg` | Золотая черепаха + TORTÉ (`-dark` — для тёмного фона, `-marcellus` — другой шрифт) |
| `lockup-gold-horizontal.svg`, `lockup-olive-*.svg` | Горизонтальная и однотонная композиции |
| `png/*.png` | Золотые версии в PNG 2400 px с прозрачным фоном |

## Упрощённые варианты (`logo/`)

`logo/` — готовые SVG, все надписи переведены в кривые (шрифты для печати не нужны).

| Файл | Что это |
|---|---|
| `mark-classic.svg` | Знак: черепаха как кулон, решётка 2×4 |
| `mark-charm.svg` | Знак с колечком-подвеской |
| `mark-minimal.svg` | Упрощённый знак для мелких размеров |
| `mark-globe.svg` | Панцирь-купол с меридианами |
| `mark-solid.svg` | Залитый силуэт для штампа/тиснения |
| `wordmark-*.svg` | Надпись TORTÉ пятью шрифтами |
| `lockup-horizontal-*.svg` | Знак слева + надпись |
| `lockup-stacked-*.svg` | Знак сверху + надпись (`-ivory` — для тёмного фона) |
| `seal.svg` | Круглая печать |
| `favicon.svg` | Иконка сайта |

Цвета: оливковый #4F5D45, золото #C5A66A, сливочный #F6F1E8.

## Пересобрать

`src/build.py` генерирует все файлы. Нужны `pip install fonttools` и шрифты
в `src/fonts/` (Google Fonts, лицензия OFL): CormorantGaramond, Marcellus,
Italiana, BodoniModa, Jost (.ttf). Запуск: `python3 src/build.py logo`.
Контур кулона — `src/paths.py`, отрисовка — `src/pendant.py`, композиции — `src/lockups.py`.
