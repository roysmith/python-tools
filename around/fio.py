"File I/O operations"

import os
import logging

logger = logging.getLogger("fio")

class SeekError(Exception):
    pass

class TextRecordFile:
    """A read-only wrapper around a Python file object which treats
    the file as a random-access sequence of variable-length records
    (i.e. lines of text).

    Wen you read a line, it is guaranteed to always return a complete
    line.  You can seek to an arbitrary location in the file (using
    the standard byte offsets), and the next read will return the line
    which contains that offset.  Imagine the following file (where $'s
    indicate newlines):

                 1         2         3         4
        1234567890123456789012345678901234567890
        This is the first line$And the second$An

                 5         6         7         8
        1234567890123456789012345678901234567890
        d this is the third$

    The file is 60 characters long, and contains 3 records.  Some
    illustrative operation sequences and what they return are:

    seek(23)
    readline() => "This is the first line\n"

    seek(24)
    readline() => "And the second\n"

    seed(25)
    readline() => "And the second\n"

    NOTE: unlike normal files, a seek() immediately followed by a
    tell() will *not* necessarially return the offset seeked to.
    Instead, it will return the position of the beginning of the line
    which contains the offset.

    This impementation assumes a Unix-like environment, with newlines
    as terminators and sane seek()/tell() behavior.  I have no idea if
    this will work on Windows.  Nor do I particularly care :-)

    It is assumed that the file is not being modified while we're
    reading it.

    """
    def __init__(self, path):
        self.file = open(path)
        self.size = self.get_size()

    def close(self):
        self.file.close()

    def seek(self, offset):
        """Move to a location in the file.

        Offset is an integer, as returned by file.tell().  The
        location moved to is the beginning of the line which contains
        the requested offset.

        Unlike standard file objects, all seeks are absolute (as per
        os.SEEK_SET).

        """
        # Validate offset
        if offset < 0:
            raise ValueError("Offset (%r) must be a positive integer")
        if offset == 0:
            self.file.seek(0)
            return

        # Read a chunk of data in front of the current position.
        chunk_size = 1024
        start_of_buffer = max(0, offset - chunk_size)
        self.file.seek(start_of_buffer)
        buf_size = offset - start_of_buffer
        assert 0 < buf_size <= chunk_size
        buffer = self.file.read(buf_size)
        assert len(buffer) == buf_size

        # If there's no newline in the buffer, either we're in the
        # first line of the file (which is OK), or we've blown the
        # assumption that no line is longer than chunk_size.
        try:
            index = buffer.rindex('\n')
        except ValueError:
            if start_of_buffer == 0:
                # We're good; it's the first line of the file
                self.file.seek(0)
                return
            else:
                raise SeekError("no newline found (start=%d, size=%d)" \
                                % (start_of_buffer, buf_size))

        # There's at least one newline in the buffer; we want to be
        # right after the last one.
        self.file.seek(start_of_buffer + index + 1)
        return


    def readline(self):
        return self.file.readline()

    def get_size(self):
        """Discover the size of the file.

        Returns an integer suitable for passing to file.seek() as an
        offset..

        """
        # This may not be the most efficient way, but it works.
        current_position = self.file.tell()
        self.file.seek(0, os.SEEK_END)
        size = self.file.tell()
        self.file.seek(current_position, os.SEEK_SET)
        return size
