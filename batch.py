from compressor import AudioCompressor, ImageCompressor, VideoCompressor

# Коди типів медіа (замість магічних чисел)
IMAGE = 1
VIDEO = 2
AUDIO = 3


def _compress_one(path, media_type, setting):
    """Стискає один файл за типом медіа. Повертає CompressionResult або None."""
    if media_type == IMAGE:
        return ImageCompressor(setting).compress_image(path, path + ".out")
    if media_type == VIDEO:
        return VideoCompressor(setting).compress_video(path, path + ".out")
    if media_type == AUDIO:
        return AudioCompressor(setting).compress_audio(path, path + ".out")
    return None


def compress_files(paths, media_type, setting):
    """Стискає список файлів і повертає підсумковий рядок зі статистикою."""
    results = []
    total = 0
    saved = 0
    for path in paths:
        result = _compress_one(path, media_type, setting)
        if result is not None:
            results.append(result)
            total += result.original_size_mb
            saved += result.original_size_mb - result.compressed_size_mb
    percent = saved / total * 100 if total > 0 else 0
    return f"Оброблено: {len(results)} файлів, заощаджено {round(percent, 1)}%"
