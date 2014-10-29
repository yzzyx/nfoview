import nfoview

TYPE_ASCII = 0
TYPE_ANSI = 1
TYPE_ANSIMATION = 2

class NfoFile:
    path = ""
    encoding = ""
    data = ""
    sauce = nfoview.sauce.SAUCE()
    filetype = TYPE_ASCII

    def __init__(self, path):
        self.path = path
        self.encoding = nfoview.util.detect_encoding(path)

        with open(path, "rb") as f:
            self.data = f.read()
            self.sauce.read_from_file(f)
            if self.sauce.is_valid:
                if self.sauce.datatype == 1 and self.sauce.filetype == 1:
                    self.filetype = TYPE_ANSI
                elif self.sauce.datatype == 1 and self.sauce.filetype == 2:
                    self.filetype = TYPE_ANSIMATION
                else: # Default to ASCII
                    self.filetype = TYPE_ASCII
            else:
                # Check for ANSI escape codes
                if "\033[" in self.data:
                    self.filetype = TYPE_ANSI
                else:
                    self.filetype = TYPE_ASCII
            self.data = self.data.decode(self.encoding)

        # For viewing purposes, we don't care about anything after EOF (e.g. SAUCE)
        eof_marker = self.data.find("\032")
        if eof_marker:
            self.data = self.data[:eof_marker]
