from re import MULTILINE, search
from subprocess import PIPE, Popen
from sys import stderr
from tempfile import NamedTemporaryFile


try:
    blob
except NameError:
    # Won't be ever run, but makes IDEs not complaining
    # about the blob.data occurrences below.

    class Blob:
        def __init__(self):
            self.data = b''

    blob = Blob()


if search(rb'^package \w+$', blob.data, MULTILINE):
    proc = Popen(['gofmt'], stdin=PIPE, stdout=PIPE)
    (out, _) = proc.communicate(blob.data)

    if proc.returncode:
        with NamedTemporaryFile('wb', delete=False) as f:
            f.write(blob.data)

        print("gofmt returned {}, assuming blob isn't Go code at all: {}"
              .format(proc.returncode, f.name), file=stderr)
    else:
        blob.data = out
