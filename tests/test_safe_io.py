import os
import tempfile
import unittest
from pathlib import Path

from engineering_core.closed_loop import ClosedLoopError, load_record
from engineering_core.safe_io import SafeInputError, read_bounded_json


class SafeIoTests(unittest.TestCase):
    def test_duplicate_members_and_nonfinite_numbers_reject(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            path.write_text('{"a":1,"a":2}')
            with self.assertRaises(SafeInputError): read_bounded_json(path, max_bytes=1024)
            path.write_text('{"a":NaN}')
            with self.assertRaises(SafeInputError): read_bounded_json(path, max_bytes=1024)

    def test_private_key_and_bearer_inputs_reject_without_echoing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"
            for secret in ("-----BEGIN PRIVATE KEY-----", "Authorization: Bearer abcdefghijklmnop"):
                path.write_text('{"note":' + repr(secret).replace("'", '"') + '}')
                with self.assertRaisesRegex(ClosedLoopError, "secret-bearing input rejected") as caught:
                    load_record(path)
                self.assertNotIn("abcdefghijklmnop", str(caught.exception))

    @unittest.skipUnless(hasattr(os, "mkfifo"), "FIFO unavailable")
    def test_fifo_rejects_without_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "input.json"; os.mkfifo(path)
            with self.assertRaises(SafeInputError): read_bounded_json(path, max_bytes=1024)


if __name__ == "__main__": unittest.main()
