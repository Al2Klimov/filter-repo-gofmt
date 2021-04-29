from os import environ
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


if search(rb'^\s*package\s+\w+', blob.data, MULTILINE):
    proc = Popen(['gofmt'], stdin=PIPE, stdout=PIPE)
    (out, _) = proc.communicate(blob.data)

    while True:
        if proc.returncode:
            editor = environ.get('EDITOR', '').strip()

            if editor:
                with NamedTemporaryFile('wb') as f:
                    f.write(blob.data)
                    f.flush()

                    print("gofmt returned {}, assuming blob isn't Go code at all: {}"
                          .format(proc.returncode, f.name), file=stderr)

                    if input('Edit the blob and re-try? (y/N) ').strip().lower() == 'y':
                        Popen([editor, f.name]).wait()

                        with open(f.name, 'rb') as r:
                            proc = Popen(['gofmt'], stdin=r, stdout=PIPE)
                            (out, _) = proc.communicate()

                        continue
                    else:
                        print('Re-run with $EDITOR unset not to be asked.', file=stderr)
            else:
                with NamedTemporaryFile('wb', delete=False) as f:
                    f.write(blob.data)

                print("gofmt returned {}, assuming blob isn't Go code at all: {}"
                      .format(proc.returncode, f.name), file=stderr)
                print('Re-run with $EDITOR set to correct invalid syntax.', file=stderr)
        else:
            blob.data = out

        break
