from batch import AUDIO, IMAGE, VIDEO, compress_files


def test_single_image():
    result = compress_files(["a.jpg"], IMAGE, 70)
    assert "1 файлів" in result


def test_multiple_images():
    result = compress_files(["a.jpg", "b.jpg", "c.jpg"], IMAGE, 70)
    assert "3 файлів" in result


def test_video():
    result = compress_files(["v.mp4"], VIDEO, 28)
    assert "1 файлів" in result


def test_audio():
    result = compress_files(["s.mp3"], AUDIO, 128)
    assert "1 файлів" in result


def test_empty_list():
    result = compress_files([], IMAGE, 70)
    assert "0 файлів" in result


def test_unknown_type():
    result = compress_files(["x.jpg"], 99, 70)
    assert "0 файлів" in result
