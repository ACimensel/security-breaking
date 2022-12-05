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
            min_diff = sys.maxsize

            # Can make it way faster by reducing this to something like 10 at the cost of it not working 100%
            # if a lot of other processes are running at the same time.
            # Could break a 36 character password in ~16 seconds on my machine with a range of 20 reliably,
            # value is set higher for robustness and since we're only going up to a password of length 10.
            # With the range set to 100, breaks a 12 char password in 5 seconds.
            for i in range(100):
                start = perf_counter_ns()
                result = lockbox.try_password(tmp_password)
                stop = perf_counter_ns()
                if stop - start < min_diff:
                    min_diff = stop - start

            if result is not None:
                print("\nPassword is: ", tmp_password, ": found in ", (perf_counter_ns() - overall_start)/SEC_TO_NS, "seconds")
                return tmp_password, result

            if min_diff > max_time:
                max_time = min_diff
                longest_char = c
        password += longest_char

    print("\nLongest pass: ", password)
    print("\nQuitting after %d seconds" % max_runtime_secs)

    return None, None


# NOTE: Returns a string corresponding to the result from successfully
# calling `takeover` on a `CaerfilyDesinedSurvis`. 
def break_facade(facade: Facade) -> str:
    codeword = (facade.greet("Blah\ndumpcodeword"))[1]
    print('\ncodeword: ', codeword)
    takeover = (facade.greet("Blah\ntakeover %s" % codeword))[1]
    print('takeover: ', takeover)

    return takeover
