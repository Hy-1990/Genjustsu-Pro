from fractions import Fraction
from pathlib import Path
import tempfile
import unittest

import av
import numpy as np

from audio_workflow import finish_preview


def clip(path, count, *, audio=False):
    with av.open(str(path), "w") as output:
        video = output.add_stream("libx264", rate=24)
        video.width = video.height = 64
        video.pix_fmt = "yuv420p"
        soundtrack = None
        if audio:
            soundtrack = output.add_stream("aac", rate=44100)
            soundtrack.layout = "stereo"
        for index in range(count):
            frame = av.VideoFrame.from_ndarray(np.full((64, 64, 3), 80, dtype=np.uint8), format="rgb24")
            frame.pts, frame.time_base = index, Fraction(1, 24)
            for packet in video.encode(frame):
                output.mux(packet)
        for packet in video.encode():
            output.mux(packet)
        if soundtrack:
            samples = round(count / 24 * 44100)
            for index in range(0, samples, 4096):
                frame = av.AudioFrame.from_ndarray(np.zeros((2, min(4096, samples-index)), dtype=np.float32), format="fltp", layout="stereo")
                frame.sample_rate, frame.pts = 44100, index
                for packet in soundtrack.encode(frame):
                    output.mux(packet)
            for packet in soundtrack.encode():
                output.mux(packet)


def audio_packets(path):
    with av.open(str(path)) as media:
        return [bytes(packet) for packet in media.demux(audio=0) if packet.dts is not None]


class DurationAlignmentTests(unittest.TestCase):
    def test_rounding_short_and_long_outputs_keeps_complete_source_audio(self):
        for source_count, generated_count in ((103, 96), (103, 120)):
            with self.subTest(source=source_count, generated=generated_count), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                clip(root / "upload.mp4", source_count, audio=True)
                clip(root / "result.mp4", generated_count)
                result = finish_preview(root / "result.mp4", root)
                self.assertEqual(audio_packets(root / "upload.mp4"), audio_packets(result))
                with av.open(str(result)) as video:
                    self.assertEqual(sum(1 for _ in video.decode(video=0)), source_count)
                self.assertTrue((root / "duration-adjustment.json").exists())

    def test_large_mismatch_does_not_publish_a_partial_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clip(root / "upload.mp4", 96, audio=True)
            clip(root / "result.mp4", 48)
            with self.assertRaises(ValueError):
                finish_preview(root / "result.mp4", root)
            self.assertFalse((root / "final-preview.mp4").exists())


if __name__ == "__main__":
    unittest.main()
