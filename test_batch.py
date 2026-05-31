from batch import proc


def test_proc_single_image():
    result = proc(["a.jpg"], 1, 70)
    assert "1 файлів" in result


def test_proc_multiple_images():
    result = proc(["a.jpg", "b.jpg", "c.jpg"], 1, 70)
    assert "3 файлів" in result


def test_proc_video():
    result = proc(["v.mp4"], 2, 28)
    assert "1 файлів" in result


def test_proc_audio():
    result = proc(["s.mp3"], 3, 128)
    assert "1 файлів" in result


def test_proc_empty_list():
    result = proc([], 1, 70)
    assert "0 файлів" in result


def test_proc_unknown_type():
    result = proc(["x.jpg"], 99, 70)
    assert "0 файлів" in result
