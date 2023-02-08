#!/usr/bin/env python3

import secrets
from typing import Literal

class Functions:
    def invert(x: int | float) -> (int | float):
        """
        Invert the algebraic sign of `x`.
        """
        return -1 * x

    def is_even(n: int) -> bool:
        """
        Test if `n` is an even number.
        """
        return not n & 1

    def is_odd(n: int) -> bool:
        """
        Test if `n` is an odd number.
        """
        return bool(n & 1)

    def is_prime(n: int) -> bool:
        """
        Test whether the number `n` is prime or not.
        """
        if n <= 1: return False

        i = 2
        while i ** 2 <= n:
            if n % i == 0:
                return False
            i += 1

        return True

    def __inner_miller_rabin(n: int, r: int) -> bool:
        m = n - 1 # = (n - 1) / 2^k
        while not m & 1:
            m >>= 1

        if pow(r, m, n) == 1:
            return True

        while m < n - 1:
            if pow(r, m, n) == n - 1:
                return True
            m <<= 1

        return False

    def miller_rabin(n: int, k: int = 40) -> bool:
        """
        Test whether a number `n >= 2` is composite, i.e. not prime. Return `True`
        if `n` passes `k` rounds of the Miller-Rabin primality test and assert that
        a number `n` might possibly be prime, else return `False` if `n` is proved
        to be a composite.
        """
        if n < 2: raise ValueError()
        if n <= 3: return True

        for _ in range(k):
            if not Functions.__inner_miller_rabin(n, r=secrets.choice(range(2, n - 1))):
                return False

        return True

    def sign(x: int | float) -> Literal[-1, 0, 1]:
        """
        Extract the sign of a real number.
        """
        return x and (-1 if x < 0 else 1)
