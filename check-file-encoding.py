import sys, os, codecs

# Convert the file encoding to the default UTF-8 without BOM.
def check_BOM(filename):
    BUFSIZE = 4096
    BOMLEN = len(codecs.BOM_UTF8)

    with open(filename, "r+b") as fp:
        chunk = fp.read(BUFSIZE)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[BOMLEN:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(BOMLEN, os.SEEK_CUR)
                chunk = fp.read(BUFSIZE)
            fp.seek(-BOMLEN, os.SEEK_CUR)
            fp.truncate()
            print("\n" + filename + ": this file's encoding has been converted to UTF-8 without BOM to avoid broken metadata display.")

if __name__ == "__main__":

    for filename in sys.argv[1:]:
        if os.path.isfile(filename):
            check_BOM(filename)