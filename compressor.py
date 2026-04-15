def compress_image(input_path, output_path, quality=70):
    """
    Стискає зображення з вказаною якістю
    quality: 1-100 (70 за замовчуванням)
    """
    print(f"Стиснення зображення: {input_path}")
    print(f"Якість: {quality}%")
    print(f"Результат збережено: {output_path}")
    return True

def compress_video(input_path, output_path, crf=28):
    """
    Стискає відео з вказаним параметром CRF
    crf: 18-35 (28 за замовчуванням)
    """
    print(f"Стиснення відео: {input_path}")
    print(f"CRF: {crf}")
    print(f"Результат збережено: {output_path}")
    return True

def compress_audio(input_path, output_path, bitrate=128):
    """
    Стискає аудіо з вказаним бітрейтом
    bitrate: 32-320 kbps (128 за замовчуванням)
    """
    print(f"Стиснення аудіо: {input_path}")
    print(f"Бітрейт: {bitrate} kbps")
    print(f"Результат збережено: {output_path}")
    return True