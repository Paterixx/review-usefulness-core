# review-usefulness-core

Общая Python-библиотека с бизнес-логикой расчёта полезности отзывов для сортировок.

## Возможности
Сейчас библиотека содержит:
- расчёт полезности отзыва `P` на основе likes/dislikes
- учёт текстового фактора для ранжирования при равных или близких значениях `P`

## Структура
```text
src/review_usefulness/
src/usefulness_kernel/
```

## Установка для локальной разработки
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```
