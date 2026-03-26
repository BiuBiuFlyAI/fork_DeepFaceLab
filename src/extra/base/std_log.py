import sys
import os
import contextlib


@contextlib.contextmanager
def suppress_output():
    with open(os.devnull, "w") as f_null:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = f_null, f_null
        try:
            yield
        finally:
            sys.stdout, sys.stderr = old_stdout, old_stderr


@contextlib.contextmanager
def suppress_output_dup2():
    with open(os.devnull, "w") as f_null:
        old_stdout_fd, old_stderr_fd = os.dup(1), os.dup(2)
        os.dup2(f_null.fileno(), 1)
        os.dup2(f_null.fileno(), 2)

        try:
            yield
        finally:
            os.dup2(old_stdout_fd, 1)
            os.dup2(old_stderr_fd, 2)
            os.close(old_stdout_fd)
            os.close(old_stderr_fd)
