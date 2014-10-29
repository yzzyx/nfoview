import struct

class SAUCE:
    """ Read SAUCE-information from a file

    Based on information from here:
    http://www.acid.org/info/sauce/sauce.htm

    Currently only handles ASCII/ANSI fileflags
    """
    sauce_id = ""
    version = ""
    title = ""
    author = ""
    group = ""
    date = ""
    filesize = 0
    datatype = 0
    filetype = 0
    tinfo1 = 0
    tinfo2 = 0
    tinfo3 = 0
    tinfo4 = 0
    comments_count = 0
    tflags = 0
    tinfos = 0

    comments = []

    # Flags for ASCII/ANSI-files
    screen_width = 0
    line_count = 0
    ansiflags = 0
    screen_height = 0
    fontname = ""

    is_valid = False

    def __init__(self, file_handle = None):
        if file_handle:
            self.read_from_file(file_handle)

    def read_from_file(self, file_handle):
        # Check for SAUCE-record
        # Go to end of file
        file_handle.seek(0, 2)
        file_sz = file_handle.tell()
        if file_sz > 128:
            # We only want the last 128 bytes
            file_handle.seek(-128, 2)
            data = file_handle.read(128)
            (self.sauce_id,
                    self.version,
                    self.title,
                    self.author,
                    self.group,
                    self.date,
                    self.filesize,
                    self.datatype,
                    self.filetype,
                    self.tinfo1,
                    self.tinfo2,
                    self.tinfo3,
                    self.tinfo4,
                    self.comments_count,
                    self.tflags,
                    self.tinfos) = \
                            struct.unpack("<5s 2s 35s 20s 20s 8s I B B H H H H B B 22s", data)
            if self.sauce_id == b'SAUCE' and self.version == b'00':
                self.is_valid = True
                self.title = self.title.decode("cp437")
                self.author = self.author.decode("cp437")
                self.group = self.group.decode("cp437")

                # Load comments
                if self.comments_count > 0 and self.comments_count < 256 and \
                    (self.comments_count*64 + 5 + 128) < file_sz:
                    # Go to comments
                    file_handle.seek(-128 - self.comments_count*64 - 5, 2)
                    data = file_handle.read(5)
                    if data == b"COMNT":
                        for c in range(0,self.comments_count):
                            comment = file_handle.read(64).decode("cp437")
                            self.comments.append(comment)

                # We only care about ANSI and ASCII files
                if self.datatype == 1: # Character datatype
                    if self.filetype == 0 or self.filetype == 1: # ASCII or ANSI
                        self.screen_width = self.tinfo1
                        self.line_count = self.tinfo2
                        self.ansiflags = self.tflags
                        self.fontname = self.tinfos.decode("cp437")
                    elif self.filetype == 2:
                        self.screen_width = self.tinfo1
                        self.screen_height = self.tinfo2
                        self.ansiflags = self.tflags
                        self.fontname = self.tinfos.decode("cp437")
            else:
                self.is_valid = False
