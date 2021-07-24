import random
import string
import math

def generate_otp(otp_len = 6)-> str:
    # generates a random string of numbers based on the provided length
    val =[]
    if otp_len > 9 or otp_len <= 0:
        msg = f"Invalid otp length {otp_len}"
        raise RuntimeError(msg)
    for i in range(otp_len):
        val.append(str(math.floor(random.random()*10)))
    random.shuffle(val)
    val.reverse()
    random.shuffle(val)
    return ''.join(val)


def generateRandomeString():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
