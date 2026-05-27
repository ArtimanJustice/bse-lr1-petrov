import pytest
from compressor import (
    FileInfo,
    CompressionSettings,
    CompressionResult,
    Compressor,
    ImageCompressor,
    VideoCompressor,
    AudioCompressor,
)

# ===========================================================
# FileInfo
# ===========================================================

def test_file_info_detects_image():
    # EP: розширення з класу "image" -> тип "image" (позитивний)
    # Arrange
    path = "photo.jpg"
    # Act
    info = FileInfo(path)
    # Assert
    assert info.type == "image"


def test_file_info_detects_video():
    # EP: розширення з класу "video" -> тип "video" (позитивний)
    # Arrange
    path = "movie.mp4"
    # Act
    info = FileInfo(path)
    # Assert
    assert info.type == "video"


def test_file_info_detects_audio():
    # EP: розширення з класу "audio" -> тип "audio" (позитивний)
    # Arrange
    path = "song.mp3"
    # Act
    info = FileInfo(path)
    # Assert
    assert info.type == "audio"


def test_file_info_unknown_extension_raises():
    # EP: розширення не з жодного класу -> ValueError (негативний)
    # Arrange
    path = "archive.xyz"
    # Act / Assert
    with pytest.raises(ValueError, match="Unsupported file type"):
        FileInfo(path)


def test_file_info_empty_path_raises():
    # EP: порожній шлях -> ValueError (негативний)
    # Arrange
    path = ""
    # Act / Assert
    with pytest.raises(ValueError, match="Path cannot be empty"):
        FileInfo(path)


def test_file_info_no_extension_raises():
    # EP: файл без крапки -> ValueError (негативний)
    # Arrange
    path = "noextension"
    # Act / Assert
    with pytest.raises(ValueError, match="File has no extension"):
        FileInfo(path)


def test_file_info_extracts_name():
    # EP: шлях з директорією -> ім'я файлу без шляху (позитивний)
    # Arrange
    path = "C:/users/danylo/photo.png"
    # Act
    info = FileInfo(path)
    # Assert
    assert info.name == "photo.png"


# ===========================================================
# CompressionSettings
# ===========================================================

def test_settings_default_values():
    # EP: виклик без аргументів -> значення за замовчуванням (позитивний)
    # Arrange / Act
    settings = CompressionSettings.get_default_settings()
    # Assert
    assert settings.image_quality == 70
    assert settings.video_crf == 28
    assert settings.audio_bitrate == 128


def test_settings_quality_min_boundary():
    # BVA: image_quality = 1 (мінімальна межа) -> без винятку (позитивний)
    # Arrange / Act
    settings = CompressionSettings(image_quality=1)
    # Assert
    assert settings.image_quality == 1


def test_settings_quality_max_boundary():
    # BVA: image_quality = 100 (максимальна межа) -> без винятку (позитивний)
    # Arrange / Act
    settings = CompressionSettings(image_quality=100)
    # Assert
    assert settings.image_quality == 100


def test_settings_quality_below_min_raises():
    # BVA: image_quality = 0 (нижче мінімуму) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="image_quality must be 1-100"):
        CompressionSettings(image_quality=0)


def test_settings_quality_above_max_raises():
    # BVA: image_quality = 101 (вище максимуму) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="image_quality must be 1-100"):
        CompressionSettings(image_quality=101)


def test_settings_crf_below_min_raises():
    # BVA: video_crf = 17 (нижче мінімуму 18) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="video_crf must be 18-51"):
        CompressionSettings(video_crf=17)


def test_settings_bitrate_above_max_raises():
    # BVA: audio_bitrate = 321 (вище максимуму 320) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="audio_bitrate must be 32-320"):
        CompressionSettings(audio_bitrate=321)


# ===========================================================
# Compressor.calculate_compression_percent
# ===========================================================

def test_calc_percent_normal():
    # EP: звичайне стиснення вдвічі -> 50% (позитивний)
    # Arrange
    original, compressed = 10.0, 5.0
    # Act
    result = Compressor.calculate_compression_percent(original, compressed)
    # Assert
    assert result == 50.0


def test_calc_percent_full_compression():
    # BVA: compressed = 0 (повне стиснення, мінімальна межа) -> 100.0% (позитивний)
    # Arrange
    original, compressed = 10.0, 0.0
    # Act
    result = Compressor.calculate_compression_percent(original, compressed)
    # Assert
    assert result == 100.0


def test_calc_percent_no_compression():
    # BVA: compressed = original (без стиснення, максимальна межа) -> 0.0% (позитивний)
    # Arrange
    original, compressed = 10.0, 10.0
    # Act
    result = Compressor.calculate_compression_percent(original, compressed)
    # Assert
    assert result == 0.0


def test_calc_percent_zero_original_raises():
    # EP: original_size = 0 -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="original_size must be positive"):
        Compressor.calculate_compression_percent(0, 5.0)


def test_calc_percent_negative_compressed_raises():
    # EP: compressed_size < 0 -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="compressed_size cannot be negative"):
        Compressor.calculate_compression_percent(10.0, -1.0)


def test_calc_percent_compressed_exceeds_original_raises():
    # EP: compressed > original -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="compressed_size cannot exceed original_size"):
        Compressor.calculate_compression_percent(5.0, 10.0)


# ===========================================================
# ImageCompressor
# ===========================================================

def test_image_compressor_quality_zero_raises():
    # BVA: quality = 0 (нижче мінімуму 1) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="quality must be 1-100"):
        ImageCompressor(quality=0)


def test_image_compressor_quality_min_valid():
    # BVA: quality = 1 (мінімальна межа) -> ОК (позитивний)
    # Arrange / Act
    comp = ImageCompressor(quality=1)
    # Assert
    assert comp.quality == 1


def test_image_compressor_compress_returns_result():
    # EP: коректні шляхи, якість за замовчуванням -> CompressionResult (позитивний)
    # Arrange
    comp = ImageCompressor(quality=70)
    # Act
    result = comp.compress_image("input.jpg", "output.jpg")
    # Assert
    assert isinstance(result, CompressionResult)
    assert result.compressed_size_mb < result.original_size_mb


def test_image_compressor_empty_path_raises():
    # EP: порожній шлях -> ValueError (негативний)
    # Arrange
    comp = ImageCompressor()
    # Act / Assert
    with pytest.raises(ValueError, match="Paths cannot be empty"):
        comp.compress_image("", "output.jpg")


# ===========================================================
# VideoCompressor
# ===========================================================

def test_video_compressor_crf_below_min_raises():
    # BVA: crf = 17 (нижче мінімуму 18) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="crf must be 18-51"):
        VideoCompressor(crf=17)


def test_video_compressor_crf_min_valid():
    # BVA: crf = 18 (мінімальна межа) -> ОК (позитивний)
    # Arrange / Act
    comp = VideoCompressor(crf=18)
    # Assert
    assert comp.crf == 18


def test_video_compressor_crf_above_max_raises():
    # BVA: crf = 52 (вище максимуму 51) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="crf must be 18-51"):
        VideoCompressor(crf=52)


def test_video_compressor_compress_returns_result():
    # EP: коректні шляхи, CRF за замовчуванням -> CompressionResult (позитивний)
    # Arrange
    comp = VideoCompressor(crf=28)
    # Act
    result = comp.compress_video("input.mp4", "output.mp4")
    # Assert
    assert isinstance(result, CompressionResult)
    assert 0 < result.compressed_size_mb < result.original_size_mb


# ===========================================================
# AudioCompressor
# ===========================================================

def test_audio_compressor_bitrate_below_min_raises():
    # BVA: bitrate = 31 (нижче мінімуму 32) -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="bitrate must be 32-320"):
        AudioCompressor(bitrate=31)


def test_audio_compressor_bitrate_min_valid():
    # BVA: bitrate = 32 (мінімальна межа) -> ОК (позитивний)
    # Arrange / Act
    comp = AudioCompressor(bitrate=32)
    # Assert
    assert comp.bitrate == 32


def test_audio_compressor_compress_returns_result():
    # EP: коректні шляхи, бітрейт за замовчуванням -> CompressionResult (позитивний)
    # Arrange
    comp = AudioCompressor(bitrate=128)
    # Act
    result = comp.compress_audio("input.mp3", "output.mp3")
    # Assert
    assert isinstance(result, CompressionResult)
    assert result.compressed_size_mb < result.original_size_mb


# ===========================================================
# CompressionResult
# ===========================================================

def test_compression_result_percent_calculation():
    # EP: 10 MB -> 5 MB = 50% (позитивний)
    # Arrange / Act
    result = CompressionResult(10.0, 5.0, "out.mp4")
    # Assert
    assert result.compression_percent == 50.0


def test_compression_result_summary_format():
    # EP: перевірка формату рядка get_summary() (позитивний)
    # Arrange
    result = CompressionResult(10.0, 5.0, "out.mp3")
    # Act
    summary = result.get_summary()
    # Assert
    assert "10.00 MB" in summary
    assert "5.00 MB" in summary
    assert "50.0% saved" in summary
    assert "out.mp3" in summary


def test_compression_result_compressed_exceeds_original_raises():
    # EP: compressed > original -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="cannot exceed original"):
        CompressionResult(5.0, 10.0, "out.mp4")


def test_compression_result_negative_original_raises():
    # EP: original_size_mb <= 0 -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="original_size_mb must be positive"):
        CompressionResult(-1.0, 0.5, "out.jpg")


def test_compression_result_negative_compressed_raises():
    # EP: compressed_size_mb < 0 -> ValueError (негативний)
    # Arrange / Act / Assert
    with pytest.raises(ValueError, match="compressed_size_mb cannot be negative"):
        CompressionResult(10.0, -1.0, "out.jpg")


def test_video_compressor_empty_path_raises():
    # EP: порожній вхідний шлях -> ValueError (негативний)
    # Arrange
    comp = VideoCompressor()
    # Act / Assert
    with pytest.raises(ValueError, match="Paths cannot be empty"):
        comp.compress_video("", "output.mp4")


def test_audio_compressor_empty_path_raises():
    # EP: порожній вхідний шлях -> ValueError (негативний)
    # Arrange
    comp = AudioCompressor()
    # Act / Assert
    with pytest.raises(ValueError, match="Paths cannot be empty"):
        comp.compress_audio("", "output.mp3")
