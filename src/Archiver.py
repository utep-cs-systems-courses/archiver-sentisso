import sys
import os
from typing import List

STATIC_HEADER_SIZE = 2
FILE_HEADER_SIZE = 9
FILE_READ_BUFFER = 1024

DEBUG = True


def errprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class Archiver:
    def __init__(self):
        self.byteorder = "little"

    def archive(self, fnames: List[str]):
        """
        Write the archive to the stdout.
        :param fnames:
        :return:
        """
        if len(fnames) > 65536:
            errprint("Too many files to archive! Exiting...")
            sys.exit(1)

        if DEBUG:
            errprint("Writing %d files..." % len(fnames))

        sys.stdout.buffer.write(
            int.to_bytes(len(fnames), 2, self.byteorder)
        )

        for fname in fnames:
            if DEBUG:
                errprint("Writing \"%s\" to the archive..." % fname)

            self.__write_filename(fname)
            self.__write_file(fname)

    def __write_filename(self, fname: str):
        """
        Writes the filename to stdout.
        :param fname:
        :return:
        """
        if len(fname) > 255:
            errprint("Filename \"%s\" is too long! Exiting..." % fname)
            sys.exit(1)

        if DEBUG:
            errprint("Filename is %d bytes long" % len(fname))

        sys.stdout.buffer.write(
            int.to_bytes(len(fname), 1, self.byteorder)
        )
        sys.stdout.buffer.write(
            bytearray(fname, "utf-8")
        )

    def __write_file(self, fname: str):
        """
        Reads the file as binary and writes its content to stdout.
        :param fname:
        :return:
        """
        fd = os.open(fname, os.O_RDONLY)

        # write the file size
        file_size = os.fstat(fd).st_size

        if file_size > 2 ** 64:
            errprint("File \"%s\" is too big! Exiting..." % fname)
            sys.exit(1)

        if DEBUG:
            errprint("File size is %d bytes" % file_size)

        sys.stdout.buffer.write(
            int.to_bytes(file_size, 8, self.byteorder)
        )

        # write the file contents
        while True:
            buffer = os.read(fd, FILE_READ_BUFFER)
            if not buffer:
                break

            sys.stdout.buffer.write(buffer)

        os.close(fd)

    def extract(self, archive: str):
        """
        Extract the archive to the current directory.
        :param archive:
        :return:
        """
        if DEBUG:
            errprint("Reading header...")

        fd = os.open(archive, os.O_RDONLY)

        num_of_files = int.from_bytes(os.read(fd, 2), self.byteorder)

        if DEBUG:
            errprint("Number of files: %d" % num_of_files)

        for i in range(num_of_files):
            fname = self.__read_filename(fd)
            self.__read_file(fd, fname)

    def __read_filename(self, fd: int):
        """
        Reads the filename from the archive.
        :param fd: file descriptor at the beginning of the filename
        :return:
        """
        fname_len = int.from_bytes(os.read(fd, 1), self.byteorder)
        fname = os.read(fd, fname_len).decode("utf-8")

        if DEBUG:
            errprint("Filename is %d bytes long" % fname_len)
            errprint("Filename is \"%s\"" % fname)

        return fname

    def __read_file(self, fd: int, fname: str):
        file_size = int.from_bytes(os.read(fd, 8), self.byteorder)

        out_fd = os.open(fname, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)

        if DEBUG:
            errprint("File size is %d bytes" % file_size)

        while file_size > 0:
            to_read = min(file_size, FILE_READ_BUFFER)

            buffer = os.read(fd, to_read)
            os.write(out_fd, buffer)

            file_size -= to_read

        os.close(out_fd)
