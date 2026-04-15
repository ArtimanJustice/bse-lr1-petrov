# Функція, що приймає шлях до файлу та повертає його розмір у МБ
# Якщо файл не існує - повертає None
def get_file_size_mb(file_path):
    import os
    if not os.path.isfile(file_path):
        print(f"Файл не знайдено: {file_path}")
        return None
    size_bytes = os.path.getsize(file_path)
    size_mb = size_bytes / (1024 * 1024)
    return round(size_mb, 2)