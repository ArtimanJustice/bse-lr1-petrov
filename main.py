def get_file_size(file_path):
    """Повертає розмір файлу в байтах"""
    import os
    return os.path.getsize(file_path)

def calculate_compression_ratio(original_size, compressed_size):
    """Розраховує відсоток стиснення"""
    ratio = (1 - compressed_size / original_size) * 100
    return round(ratio, 2)

print("LocalSquash initialized")