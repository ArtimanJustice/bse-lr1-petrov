from compressor import ImageCompressor, VideoCompressor, AudioCompressor

# import os  # TODO: maybe add file size check later


def proc(lst, t, q):
    res = []
    total = 0
    saved = 0
    for f in lst:
        if t == 1:
            c = ImageCompressor(q)
            r = c.compress_image(f, f + ".out")
        elif t == 2:
            c = VideoCompressor(q)
            r = c.compress_video(f, f + ".out")
        elif t == 3:
            c = AudioCompressor(q)
            r = c.compress_audio(f, f + ".out")
        else:
            r = None
        if r != None:
            res.append(r)
            total = total + r.original_size_mb
            saved = saved + (r.original_size_mb - r.compressed_size_mb)
            # old = r.original_size_mb * 0.5
    if total > 0:
        pct = saved / total * 100
    else:
        pct = 0
    s = "Оброблено: " + str(len(res)) + " файлів, заощаджено " + str(round(pct, 1)) + "%"
    return s
