class Sha:
    """ Class implements the SHA-512 cryptographic hash algorithm  """
 
    @staticmethod
    def __initialize_constants() -> list:
        """ Private moethod return initial hash and round constants"""
        hash_constants = (
            0x6a09e667f3bcc908,
            0xbb67ae8584caa73b,
            0x3c6ef372fe94f82b,
            0xa54ff53a5f1d36f1,
            0x510e527fade682d1,
            0x9b05688c2b3e6c1f,
            0x1f83d9abfb41bd6b,
            0x5be0cd19137e2179,
        )

        round_constants = (
            0x428a2f98d728ae22, 0x7137449123ef65cd, 0xb5c0fbcfec4d3b2f,
            0xe9b5dba58189dbbc, 0x3956c25bf348b538, 0x59f111f1b605d019,
            0x923f82a4af194f9b, 0xab1c5ed5da6d8118, 0xd807aa98a3030242,
            0x12835b0145706fbe, 0x243185be4ee4b28c, 0x550c7dc3d5ffb4e2,
            0x72be5d74f27b896f, 0x80deb1fe3b1696b1, 0x9bdc06a725c71235,
            0xc19bf174cf692694, 0xe49b69c19ef14ad2, 0xefbe4786384f25e3,
            0x0fc19dc68b8cd5b5, 0x240ca1cc77ac9c65, 0x2de92c6f592b0275,
            0x4a7484aa6ea6e483, 0x5cb0a9dcbd41fbd4, 0x76f988da831153b5,
            0x983e5152ee66dfab, 0xa831c66d2db43210, 0xb00327c898fb213f,
            0xbf597fc7beef0ee4, 0xc6e00bf33da88fc2, 0xd5a79147930aa725,
            0x06ca6351e003826f, 0x142929670a0e6e70, 0x27b70a8546d22ffc,
            0x2e1b21385c26c926, 0x4d2c6dfc5ac42aed, 0x53380d139d95b3df,
            0x650a73548baf63de, 0x766a0abb3c77b2a8, 0x81c2c92e47edaee6,
            0x92722c851482353b, 0xa2bfe8a14cf10364, 0xa81a664bbc423001,
            0xc24b8b70d0f89791, 0xc76c51a30654be30, 0xd192e819d6ef5218,
            0xd69906245565a910, 0xf40e35855771202a, 0x106aa07032bbd1b8,
            0x19a4c116b8d2d0c8, 0x1e376c085141ab53, 0x2748774cdf8eeb99,
            0x34b0bcb5e19b48a8, 0x391c0cb3c5c95a63, 0x4ed8aa4ae3418acb,
            0x5b9cca4f7763e373, 0x682e6ff3d6b2b8a3, 0x748f82ee5defb2fc,
            0x78a5636f43172f60, 0x84c87814a1f0ab72, 0x8cc702081a6439ec,
            0x90befffa23631e28, 0xa4506cebde82bde9, 0xbef9a3f7b2c67915,
            0xc67178f2e372532b, 0xca273eceea26619c, 0xd186b8c721c0c207,
            0xeada7dd6cde0eb1e, 0xf57d4f7fee6ed178, 0x06f067aa72176fba,
            0x0a637dc5a2c898a6, 0x113f9804bef90dae, 0x1b710b35131c471b,
            0x28db77f523047d84, 0x32caab7b40c72493, 0x3c9ebe0a15c9bebc,
            0x431d67c49c100d4c, 0x4cc5d4becb3e42b6, 0x597f299cfc657e2a,
            0x5fcb6fab3ad6faec, 0x6c44198c4a475817,
        )

        return [round_constants, hash_constants]
    
    @staticmethod
    def __shift_right(x: int, n: int) -> int: 
        """ Private method shift bits in x variable n times """
        return x >> n

    @staticmethod
    def __right_rotate(x: int, n: int) -> int:
        " Private method rotate bits in x variable n times "
        return (x >> n) | (x << (64 - n)) & 0xFFFFFFFFFFFFFFFF
    
    @staticmethod
    def hash_message(message: str) -> str:
        "Hash given message"

        # Initialize round constants
        round_constants = Sha.__initialize_constants()[0]

        # Raise error if input message is not string
        if type(message) is not str:
            raise TypeError('Given message should be a string.')
    
        # Convert message to array of bytes
        message_array =  bytearray(message.encode('utf-8'))

        message_len = len(message_array) << 3

        # Add 1 bit at the end of the message        
        message_array.append(0x80)

        # Add 0 bit at the end of the message until message "lenght mod 1024 == 896"
        message_array.extend([0x0] * (112 - len(message_array) % 128))

        # Add length of the message as 128 bit at the end of the message
        message_array.extend(message_len.to_bytes(16))

        # Initialize initial hash constants
        hash = Sha.__initialize_constants()[1]

        # For every part of message which is 1024 bits block
        for chunk_start in range(0, len(message_array), 128):
            chunk = message_array[chunk_start:chunk_start + 128]

        # Split chunk into words of 64 bits each            
            w = []
            for i in range(0,80):
                if i < 16:
                    w.append(int.from_bytes(chunk[i * 8:(i + 1) * 8]))
                else:
                    w.append([0])

            # Extend words into table of 80 words 
            for i in range(16, 80):
                s0 = (Sha.__right_rotate(w[i - 15], 1) ^ Sha.__right_rotate(w[i - 15], 8) ^ Sha.__shift_right(w[i - 15], 7))
                s1 = (Sha.__right_rotate(w[i - 2], 19) ^ Sha.__right_rotate(w[i - 2], 61) ^ Sha.__shift_right(w[i - 2], 6))
                w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & 0xFFFFFFFFFFFFFFFF

            # Initialize initial_hash
            a, b, c, d, e, f, g, h = Sha.__initialize_constants()[1]

            # Main proccess of the hash algorithm
            for i in range(80):
                sum1 = (Sha.__right_rotate(e, 14) ^ Sha.__right_rotate(e, 18) ^ Sha.__right_rotate(e, 41))
                ch = (e & f) ^ (~e & g)
                temp1 = h + sum1 + ch + round_constants[i] + w[i]
                sum0 = (Sha.__right_rotate(a, 28) ^ Sha.__right_rotate(a, 34) ^ Sha.__right_rotate(a, 39))
                maj = (a & b) ^ (a & c) ^ (b & c)
                temp2 = sum0 + maj
                h = g
                g = f
                f = e
                e = (d + temp1) & 0xFFFFFFFFFFFFFFFF
                d = c
                c = b
                b = a
                a = (temp1 + temp2) & 0xFFFFFFFFFFFFFFFF

            # Add value of temporary varabiles to hash state
            hash = [
                (x + y) & 0xFFFFFFFFFFFFFFFF
                for x, y in zip(hash, (a, b, c, d, e, f, g, h))
            ]
        
        # Convert hashed message parts from integer into binary
        hash = [bin(i)[2:] for i in hash]

        # Add leading zeros to hashed message part if they were lost in conversion from integer to binary 
        hash = ''.join(64 % len(i) * '0' + i for i in hash)

        # Convert hashed messaged from binary to hexadecimal string
        hashed_message = '%0*x' % ((len(hash) + 3) // 4, int(hash, 2))

        # Return hashed_message
        return hashed_message
    
    @staticmethod
    def compare_to_hash(message: str, hash: str) -> bool:
        """ Check if given message hash is equal to given hash """

        return Sha.hash_message(message) == hash
    
# Class functionality test
if __name__ == "__main__":
    assert Sha.hash_message('Moja') == '14426416d8c25da4b186535c9ca1bd1e985cab25f2d1cac209641aafdf0f6ab2001623a08eb7e2430c453d8c8265c0ef1ef5d12896c4bb9df528b157787aa128'
    assert Sha.hash_message('Moja wiadomość') == '35ef55469e3056577ce1cd52458edf95e9cd5223ed82171db06c7ba4311e42b10ddf519b239914da8045c631c3de62ed4db059ec0895499fa376b01de59fd822'
    assert Sha.hash_message('Moja') == Sha.hash_message('Moja')
    assert Sha.hash_message('Moja wiadomość') == Sha.hash_message('Moja wiadomość')
    assert Sha.compare_to_hash('Moja', Sha.hash_message('Moja')) == True
    assert Sha.compare_to_hash('Moja wiadomość', Sha.hash_message('Moja wiadomość')) == True
    assert Sha.compare_to_hash('Moja', Sha.hash_message('Moja wiadomość')) == False
    assert Sha.compare_to_hash('Moja wiadomość', Sha.hash_message('Moja')) == False