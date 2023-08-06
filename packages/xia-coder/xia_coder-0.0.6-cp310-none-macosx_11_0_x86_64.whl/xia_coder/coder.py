import io
import gzip
import json
from _json import scanstring
from typing import List
from xia_engine import Document


class Coder:
    """Default data coder

    Using display data:
        * gzip compressed
        * record format (list of dictionary)
    """
    supported_encodes = ["gzip"]
    supported_formats = ['record']
    default_encode = "gzip"
    default_format = "record"
    decoder = json.JSONDecoder()

    def __init__(self, doc_class, data_encode: str = None, data_format: str = None):
        data_encode = self.default_encode if not data_encode else data_encode
        data_format = self.default_format if not data_format else data_format
        if data_encode not in self.supported_encodes:
            raise TypeError(f"Encode {data_encode} is not supported by {self.__class__.__name__}")
        if data_format not in self.supported_formats:
            raise TypeError(f"Format {data_format} is not supported by {self.__class__.__name__}")

        self.doc_class = doc_class
        self.data_encode = data_encode
        self.data_format = data_format
        self.write_io = None
        self.error_log = []

    def encode(self, doc_list: List[Document], file_obj) -> int:
        """Encode the list of document into bytes

        Args:
            doc_list: document list
            file_obj: file-like object to write with

        Returns:
            Encoded data size
        """
        size_counter = 0
        for doc in [item for item in doc_list if item]:
            size_counter += self.append_content(doc, file_obj)
        if self.write_io:
            self.write_io.write(']'.encode())
            self.write_io.close()  # End of write on self.file_obj
            size_counter += 1
        return size_counter

    def append_content(self, doc: Document, file_obj) -> int:
        """Append document to content

        Returns:
            Appended data size
        """
        doc._runtime = {}  # Remove document's runtime data
        content = json.dumps(doc.get_display_data(show_hidden=True), ensure_ascii=False)
        if self.write_io is None:
            self.write_io = gzip.GzipFile(mode='wb', fileobj=file_obj)
            self.write_io.write(('[' + content).encode())
        else:
            self.write_io.write((',' + content).encode())
        return len(content) + 1

    def parse_content(self, file_obj):
        if not file_obj:
            return  # Nothing to return if no objects
        read_io = gzip.GzipFile(fileobj=file_obj)
        for record in self.io_to_record(read_io):
            yield self.doc_class.from_display(**record)

    @classmethod
    def io_to_utf8(cls, file_obj):
        """Read block by block until it is possible to be parsed as a valid

        Args:
            file_obj: python file-like object
        """
        raw_line = b""
        while True:
            raw_line += file_obj.read(2 ** 12)
            if not raw_line:
                break
            try:
                decode_line = raw_line.decode()
                yield decode_line
                raw_line = "".encode()
            except UnicodeDecodeError:
                pass
        yield None

    def io_to_record(self, file_obj):
        """A very special json parser as each segment is in the form of list of dictionary
        """
        file_obj.seek(1)  # Should start after the first [
        remain = ""
        eof, seg, idx, offset, pos, err_pos, limit, cnt = False, "", 0, 0, 1, 0, len(remain), 0
        while True:
            # Step 1: Workspace preparation
            while not eof and limit - idx <= 2 ** 16:
                line = next(self.io_to_utf8(file_obj))
                if not line:
                    eof = True
                else:
                    remain = remain[idx:] + line
                    idx = 0
                    err_pos = 0
                    limit = len(remain)
            # Step 2: Line level parse
            try:
                if not remain or remain[idx] == "]":
                    # Extreme case, chunk ends with } and the ] is loaded right afterward
                    break
                if remain[idx] in [" ", "\n", "\r"]:
                    # Json load do no support leading spaces
                    idx += 1
                    continue
                record, offset = self.decoder.raw_decode(remain[idx:], 0)
                idx += offset
                if idx >= limit:
                    # Case 2.2.1: Chunk ends with }
                    remain = ""
                    idx = 1
                elif remain[idx] == ",":
                    # Case 2.2.2: should start a new chunk
                    idx = idx + 1
                elif remain[offset] == "]":
                    # Case 2.2.3: End of document, yield and quit
                    yield record
                    cnt += 1
                    break
                yield record
                cnt += 1
                # print(tracemalloc.get_traced_memory())
                err_pos = idx
                continue
            except json.JSONDecodeError as e:
                if err_pos == idx + e.pos:
                    if remain[:err_pos].strip()[-1] == ":":
                        # Value Error, replace the wrong value to something
                        err_seg, err_offset = scanstring(remain[err_pos:], 0, True)
                        err_seg_o = err_seg.rstrip(",]}{ ")
                        correction = {}.get(err_seg_o, "null")
                        # Most cases are the value format that is not supported by json
                        prefix = remain[:err_pos]
                        suffix = remain[err_pos + err_offset - len(err_seg) + len(err_seg_o) - 1:]
                        remain = prefix + correction + suffix
                        # Trace error
                        self.error_log.append({
                            "no": cnt + 1, "info_1": str(e), "info_2": err_seg,
                            "info_3": correction, "info_4": prefix + err_seg + suffix[:64]
                        })
                    else:
                        # Unrecoverable Exception
                        raise e
                else:
                    err_pos = idx + e.pos
                    continue
