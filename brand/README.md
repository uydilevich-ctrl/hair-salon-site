# TORTÉ — логотип (варианты)

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
