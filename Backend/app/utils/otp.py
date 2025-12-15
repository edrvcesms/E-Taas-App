import random

def generate_otp(length=6):
    if length <= 0:
        raise ValueError("OTP length must be a positive integer")
    
    otp = ''.join([str(random.randint(0, 9)) for _ in range(length)])
    return otp