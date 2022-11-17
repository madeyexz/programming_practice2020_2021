import time
import re

start = time.time()

def is_prime(n = 57077):
    return not re.match(r'^.?$|^(..+?)\1+?$', '1'*n)
print(is_prime())


print("Total run time: ", time.time() - start )