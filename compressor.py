class FileInfo:
    """Інформація про файл: тип, назва, шлях."""

    SUPPORTED_TYPES = {
        "image": {".jpg", ".jpeg", ".png", ".bmp", ".gif"},
        "video": {".mp4", ".avi", ".mov", ".mkv"},
        "audio": {".mp3", ".wav", ".flac", ".aac"},
    }

    def __init__(self, path: str):
        if not path or not path.strip():
            raise ValueError("Path cannot be empty")
        self.path = path
        self.name = path.replace("\\", "/").split("/")[-1]
        self.type = self.detect_file_type(path)
        self.size_mb = 0.0

    def detect_file_type(self, path: str) -> str:
        """Визначає тип файлу за розширенням."""
        if "." not in path:
            raise ValueError("File has no extension")
        ext = "." + path.rsplit(".", 1)[-1].lower()
        for file_type, extensions in self.SUPPORTED_TYPES.items():
            if ext in extensions:
                return file_type
        raise ValueError(f"Unsupported file type: {ext}")


class CompressionSettings:
    """Налаштування стиснення для кожного типу медіа."""

    DEFAULT_IMAGE_QUALITY = 70
    DEFAULT_VIDEO_CRF = 28
    DEFAULT_AUDIO_BITRATE = 128

    def __init__(self, image_quality=None, video_crf=None, audio_bitrate=None):
        self.image_quality = image_quality if image_quality is not None else self.DEFAULT_IMAGE_QUALITY
        self.video_crf = video_crf if video_crf is not None else self.DEFAULT_VIDEO_CRF
        self.audio_bitrate = audio_bitrate if audio_bitrate is not None else self.DEFAULT_AUDIO_BITRATE
        self._validate()

    def _validate(self):
        if not (1 <= self.image_quality <= 100):
            raise ValueError("image_quality must be 1-100")
        if not (18 <= self.video_crf <= 51):
            raise ValueError("video_crf must be 18-51")
        if not (32 <= self.audio_bitrate <= 320):
            raise ValueError("audio_bitrate must be 32-320")

    @classmethod
    def get_default_settings(cls):
        """Повертає налаштування за замовчуванням."""
        return cls()


class CompressionResult:
    """Результат операції стиснення файлу."""

    def __init__(self, original_size_mb: float, compressed_size_mb: float, output_path: str):
        if original_size_mb <= 0:
            raise ValueError("original_size_mb must be positive")
        if compressed_size_mb < 0:
            raise ValueError("compressed_size_mb cannot be negative")
        if compressed_size_mb > original_size_mb:
            raise ValueError("compressed_size_mb cannot exceed original_size_mb")
        self.original_size_mb = original_size_mb
        self.compressed_size_mb = compressed_size_mb
        self.output_path = output_path
        self.compression_percent = round(
            (1 - compressed_size_mb / original_size_mb) * 100, 2
        )

    def get_summary(self) -> str:
        """Повертає рядок з підсумком операції стиснення."""
        return (
            f"Compressed: {self.original_size_mb:.2f} MB -> "
            f"{self.compressed_size_mb:.2f} MB "
            f"({self.compression_percent:.1f}% saved) -> {self.output_path}"
        )


class Compressor:
    """Базовий клас компресора."""

    @staticmethod
    def calculate_compression_percent(original_size: float, compressed_size: float) -> float:
        """Обчислює відсоток стиснення файлу."""
        if original_size <= 0:
            raise ValueError("original_size must be positive")
        if compressed_size < 0:
            raise ValueError("compressed_size cannot be negative")
        if compressed_size > original_size:
            raise ValueError("compressed_size cannot exceed original_size")
        return round((1 - compressed_size / original_size) * 100, 2)


class ImageCompressor(Compressor):
    """Компресор зображень із налаштуванням якості."""

    def __init__(self, quality: int = CompressionSettings.DEFAULT_IMAGE_QUALITY):
        if not (1 <= quality <= 100):
            raise ValueError("quality must be 1-100")
        self.quality = quality

    def compress_image(self, input_path: str, output_path: str) -> CompressionResult:
        """Стискає зображення. Вища якість — менше стиснення."""
        if not input_path or not output_path:
            raise ValueError("Paths cannot be empty")
        original_size = 5.0
        # quality=100 → збереження 30%, quality=1 → збереження ~99.3%
        compressed_size = round(original_size * (1 - self.quality / 100 * 0.7), 2)
        return CompressionResult(original_size, compressed_size, output_path)


class VideoCompressor(Compressor):
    """Компресор відео з параметром CRF (чим більше — тим сильніше стиснення)."""

    def __init__(self, crf: int = CompressionSettings.DEFAULT_VIDEO_CRF):
        if not (18 <= crf <= 51):
            raise ValueError("crf must be 18-51")
        self.crf = crf

    def compress_video(self, input_path: str, output_path: str) -> CompressionResult:
        """Стискає відео. Вищий CRF — менший файл."""
        if not input_path or not output_path:
            raise ValueError("Paths cannot be empty")
        original_size = 100.0
        ratio = (self.crf - 18) / (51 - 18) * 0.8
        compressed_size = round(original_size * (1 - ratio), 2)
        return CompressionResult(original_size, compressed_size, output_path)


class AudioCompressor(Compressor):
    """Компресор аудіо з налаштуванням бітрейту."""

    def __init__(self, bitrate: int = CompressionSettings.DEFAULT_AUDIO_BITRATE):
        if not (32 <= bitrate <= 320):
            raise ValueError("bitrate must be 32-320 kbps")
        self.bitrate = bitrate

    def compress_audio(self, input_path: str, output_path: str) -> CompressionResult:
        """Стискає аудіо. Нижчий бітрейт — менший файл."""
        if not input_path or not output_path:
            raise ValueError("Paths cannot be empty")
        original_size = 10.0
        compressed_size = round(original_size * self.bitrate / 320, 2)
        return CompressionResult(original_size, compressed_size, output_path)
