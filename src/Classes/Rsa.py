from random import getrandbits, randint, randrange

class Rsa:
    """ Class implements the Rsa asymmetric encryption algorithm """

    @staticmethod
    def __is_prime(n: int, k: int = 10) -> bool:
        """ Private method check if numer is prime """
        
        if n <= 1:
            return False
        if n <= 3:
            return True

        if n % 2 == 0:
            return False

        r = 0
        d = n - 1
        while d % 2 == 0:
            r += 1
            d //= 2

        for _ in range(k):
            a = randint(2, n - 2)
            x = pow(a, d, n)

            if x == 1 or x == n - 1:
                continue

            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False

        return True

    @staticmethod
    def __generate_primes(bits: int) -> list:
        """ Generate pair of prime numbers p i q whose total length is bits  """
        
        p = getrandbits(bits // 2) | 1
        q = getrandbits(bits // 2) | 1

        while Rsa.__is_prime(p) == False or p == q:
            p = getrandbits(bits // 2) | 1

        while Rsa.__is_prime(q) == False or p == q:
            q = getrandbits(bits // 2) | 1

        return [p, q]

    @staticmethod
    def __gcd(a: int, b: int) -> int:
        """ Private method - calculate greatest common divisor function of two numbers """
        
        while b != 0:
            a, b = b, a % b

        return a

    @staticmethod
    def __extended_gcd(a: int, b: int) -> list:
        """ Private method - calculates the greatest common divisor (gcd) of two integers 
        while simultaneously finding the coefficients that satisfy Bézout's identity """
        
        x, y, u, v = 0, 1, 1, 0

        while a != 0:
            q, r = b // a, b % a
            m, n = x - u * q, y - v * q
            b, a, x, y, u, v = a, r, u, v, m, n
        gcd = b

        return [gcd, x, y]

    @staticmethod
    def __mod_inverse(a: int, m: int) -> int:
        """ Private method calculates the modular inverse of a number modulo a given modulus """
        
        g, x, y = Rsa.__extended_gcd(a, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist.")
        return x % m

    @staticmethod
    def generate_key_pair(bits: int = 2048) -> list:
        """ Generates public and private keys"""

        if bits == 0 or bits % 256 != 0:
            raise ValueError("Bits must be divisible by 256")

        p, q = Rsa.__generate_primes(bits)

        n = p * q
        phi = (p - 1) * (q - 1)

        # Select e such that 1 < e < phi and gcd(e, phi) = 1
        e = randrange(1, phi)
        while Rsa.__gcd(e, phi) != 1:
            e = randrange(1, phi)

        # Calculate d such that (d * e) % phi = 1
        d = Rsa.__mod_inverse(e, phi)

        # Return public and private key pairs
        public_key = (e, n)
        private_key = (d, n)
        return public_key, private_key

    @staticmethod
    def encrypt(message: str, public_key: list) -> int:
        """ Encrypt message with given public key """
        
        try:
            M_bytes = message.encode()
            int_message = int.from_bytes(M_bytes, 'big')
            encrypted_message = pow(int_message, public_key[0], public_key[1])
        except:
            return None
        
        return encrypted_message

    @staticmethod
    def decrypt(encrypted_message: str, private_key: list):
        """ Decrypt encrypted message with given private key """

        try:
            decrypted_message = pow(encrypted_message, private_key[0], private_key[1])

            x = (decrypted_message.bit_length() + 7) // 8
            M_bytes = decrypted_message.to_bytes(x, 'big')

            decrypted_message = M_bytes.decode()
        except:
            return None
        
        return decrypted_message

# Class functionality test
if __name__ == "__main__":
    message = "Test message to be encrypted"

    public_key, private_key = Rsa.generate_key_pair(512)

    encrypted_message = Rsa.encrypt(message, public_key)
    decrypted_message = Rsa.decrypt(encrypted_message, private_key)
    encrypted_message_again = Rsa.encrypt(decrypted_message, public_key)

    assert message == decrypted_message
    assert encrypted_message == encrypted_message_again