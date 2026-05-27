## Лабораторна робота №1

У межах лабораторної роботи №1 було виконано налаштування середовища розробки та створено початковий GitHub-репозиторій проєкту.

Було виконано:

- створення репозиторію на GitHub;
- налаштування Git;
- створення файлів `README.md` та `.gitignore`;
- додавання початкового Python-коду;
- створення декількох комітів;
- робота з гілкою `feature/add-main-code`;
- створення та злиття Pull Request;
- використання GitHub Copilot для генерації допоміжної функції.

## Лабораторна робота №2

У межах лабораторної роботи №2 було виконано UML-моделювання програмної системи **LocalSquash**.

Було підготовлено:

- функціональні вимоги до системи;
- діаграму прецедентів;
- діаграму класів;
- діаграму послідовності;
- матрицю трасовності вимог.

## Матеріали лабораторної роботи №2

### Документація

- [Функціональні вимоги](docs/requirements.md)
- [Матриця трасовності вимог](docs/traceability-matrix.md)

### UML-діаграми

- [Діаграма прецедентів — PNG](diagrams/use-case.png)
- [Діаграма прецедентів — Mermaid](diagrams/use-case.mmd)

- [Діаграма класів — PNG](diagrams/class-diagram.png)
- [Діаграма класів — Mermaid](diagrams/class-diagram.mmd)

- [Діаграма послідовності — PNG](diagrams/sequence-diagram.png)
- [Діаграма послідовності — Mermaid](diagrams/sequence-diagram.mmd)

### Онлайн-посилання на Mermaid

- [Use Case Diagram](https://mermaid.ai/d/a5809cbb-a0a9-449e-893f-5a9c066f6218)
- [Class Diagram](https://mermaid.ai/d/40c75808-1f61-48e8-9b14-9f99d25e1283)
- [Sequence Diagram](https://mermaid.ai/d/096c2adf-b683-49ae-961a-b906cd992a31)

## Лабораторна робота №3

У межах лабораторної роботи №3 реалізовано програмний модуль системи **LocalSquash** на основі UML-діаграми класів з ЛР 2 та написано набір модульних тестів.

Було виконано:

- реалізацію модуля `compressor.py` (7 класів: `FileInfo`, `CompressionSettings`, `CompressionResult`, `Compressor`, `ImageCompressor`, `VideoCompressor`, `AudioCompressor`);
- проєктування тест-кейсів із застосуванням технік EP та BVA;
- написання 38 модульних тестів за патерном AAA (фреймворк **pytest**);
- досягнення line coverage **100 %** (94 statements, 0 missing).

### Запуск тестів

```bash
pip install pytest pytest-cov
pytest test_compressor.py --cov=compressor --cov-report=html
```

### Результат

```
38 passed in 0.18s
compressor.py   94   0   100%
```

### Матеріали лабораторної роботи №3

- [Модуль compressor.py](compressor.py)
- [Тести test_compressor.py](test_compressor.py)
- Гілка: `feature/lab3`