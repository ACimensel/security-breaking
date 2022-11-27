import sys
from typing import Tuple
from time import perf_counter_ns
from string import ascii_lowercase

import scipy
import numpy

from e5utils import LockBox, Facade

SEC_TO_NS = 1000000000


# NOTE: Returns a pair (password, contents) corresponding to
#  the password that opens the lockbox and the actual contents of the
#  lockbox. The only action that it can take with a `LockBox` is
#  calling the `try_password` method. Any other properties (like
#  field names, number of fields, etc.) can change at test time.
def break_lockbox(lockbox: LockBox) -> Tuple[str, str]:
    max_runtime_secs = 30

    password = ""
    overall_start = perf_counter_ns()

    result = lockbox.try_password("")
    if result is not None:
        print("\nPassword is: ", password, ": found in ", (perf_counter_ns() - overall_start)/SEC_TO_NS, "seconds")
        return "", result

    while perf_counter_ns() - overall_start < max_runtime_secs * SEC_TO_NS:
        max_time = -sys.maxsize - 1
        longest_char = ""
        for c in ascii_lowercase:
            tmp_password = password + c

            start = perf_counter_ns()
            result = lockbox.try_password(tmp_password)
            stop = perf_counter_ns()

            if result is not None:
                print("\nPassword is: ", tmp_password, ": found in ", (perf_counter_ns() - overall_start)/SEC_TO_NS, "seconds")
                return tmp_password, result

            diff = stop - start
            if stop - start > max_time:
                max_time = diff
                longest_char = c
        password += longest_char

    print("\nLongest pass: ", password)
    print("\nQuitting after 30 seconds")

    return None, None


# NOTE: Returns a string corresponding to the result from successfully
# calling `takeover` on a `CaerfilyDesinedSurvis`. 
def break_facade(facade: Facade) -> str:
    return ''

# test one by one since length not constant? should be some way to know when a character is correct
# look at imports, perf_counter_ns?
# try all characters and find minimum return time?
# o
# op
# ope
# open
# opens
# opense
# openses
# opensesa
# opensesam
# opensesami
# ...
