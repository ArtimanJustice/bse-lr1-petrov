# Матриця трасовності вимог LocalSquash

| Вимога | Use Case | Класи | Sequence Diagram |
|---|---|---|---|
| FR-01 | Обрати файл | FileInfo | SD-01 Стиснення файлу |
| FR-02 | Визначити тип файлу | FileInfo, Compressor | SD-01 Стиснення файлу |
| FR-03 | Стиснути зображення | ImageCompressor, CompressionSettings, CompressionResult | SD-01 Стиснення файлу |
| FR-04 | Стиснути відео | VideoCompressor, CompressionSettings, CompressionResult | SD-01 Стиснення файлу |
| FR-05 | Стиснути аудіо | AudioCompressor, CompressionSettings, CompressionResult | SD-01 Стиснення файлу |
| FR-06 | Обчислити розмір файлу | FileInfo, Compressor, CompressionResult | SD-01 Стиснення файлу |
| FR-07 | Показати відсоток стиснення | Compressor, CompressionResult | SD-01 Стиснення файлу |

## Висновок

Кожна функціональна вимога покрита відповідним прецедентом, класами та сценарієм взаємодії. Це забезпечує трасовність між вимогами, UML-моделями та логікою програмної системи LocalSquash.
