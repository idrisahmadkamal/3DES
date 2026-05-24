"""
Pure Python Triple DES (3DES) Implementation
Supports ECB and CBC modes, 2-key and 3-key variants
"""

# ── DES Constants ──────────────────────────────────────────────────────────────

IP = [
    58,50,42,34,26,18,10,2, 60,52,44,36,28,20,12,4,
    62,54,46,38,30,22,14,6, 64,56,48,40,32,24,16,8,
    57,49,41,33,25,17, 9,1, 59,51,43,35,27,19,11,3,
    61,53,45,37,29,21,13,5, 63,55,47,39,31,23,15,7,
]

IP_INV = [
    40,8,48,16,56,24,64,32, 39,7,47,15,55,23,63,31,
    38,6,46,14,54,22,62,30, 37,5,45,13,53,21,61,29,
    36,4,44,12,52,20,60,28, 35,3,43,11,51,19,59,27,
    34,2,42,10,50,18,58,26, 33,1,41, 9,49,17,57,25,
]

PC1 = [
    57,49,41,33,25,17, 9, 1,58,50,42,34,26,18,
    10, 2,59,51,43,35,27,19,11, 3,60,52,44,36,
    63,55,47,39,31,23,15, 7,62,54,46,38,30,22,
    14, 6,61,53,45,37,29,21,13, 5,28,20,12, 4,
]

PC2 = [
    14,17,11,24, 1, 5, 3,28,15, 6,21,10,
    23,19,12, 4,26, 8,16, 7,27,20,13, 2,
    41,52,31,37,47,55,30,40,51,45,33,48,
    44,49,39,56,34,53,46,42,50,36,29,32,
]

SHIFTS = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

E = [
    32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
     8, 9,10,11,12,13,12,13,14,15,16,17,
    16,17,18,19,20,21,20,21,22,23,24,25,
    24,25,26,27,28,29,28,29,30,31,32, 1,
]

P = [
    16, 7,20,21,29,12,28,17, 1,15,23,26, 5,18,31,10,
     2, 8,24,14,32,27, 3, 9,19,13,30, 6,22,11, 4,25,
]

S_BOXES = [
    # S1
    [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7,
      0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8,
      4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0,
     15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13],
    # S2
    [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10,
      3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5,
      0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15,
     13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9],
    # S3
    [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8,
     13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1,
     13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7,
      1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12],
    # S4
    [ 7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15,
     13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9,
     10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4,
      3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14],
    # S5
    [ 2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9,
     14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6,
      4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14,
     11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3],
    # S6
    [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11,
     10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8,
      9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6,
      4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13],
    # S7
    [ 4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1,
     13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6,
      1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2,
      6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12],
    # S8
    [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7,
      1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2,
      7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8,
      2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11],
]

# ── Bit manipulation helpers ───────────────────────────────────────────────────

def _bytes_to_bits(data: bytes) -> list:
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def _bits_to_bytes(bits: list) -> bytes:
    result = []
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        result.append(byte)
    return bytes(result)

def _permute(block: list, table: list) -> list:
    return [block[t - 1] for t in table]

def _xor(a: list, b: list) -> list:
    return [x ^ y for x, y in zip(a, b)]

def _left_shift(bits: list, n: int) -> list:
    return bits[n:] + bits[:n]

# ── Key schedule ───────────────────────────────────────────────────────────────

def _generate_subkeys(key: bytes) -> list:
    """Generate 16 48-bit subkeys from a 64-bit DES key."""
    key_bits = _bytes_to_bits(key)
    key56 = _permute(key_bits, PC1)
    C, D = key56[:28], key56[28:]
    subkeys = []
    for shift in SHIFTS:
        C = _left_shift(C, shift)
        D = _left_shift(D, shift)
        subkeys.append(_permute(C + D, PC2))
    return subkeys

# ── DES core ───────────────────────────────────────────────────────────────────

def _f(R: list, subkey: list) -> list:
    """DES Feistel function."""
    expanded = _permute(R, E)
    xored = _xor(expanded, subkey)
    output = []
    for i in range(8):
        chunk = xored[i*6:(i+1)*6]
        row = (chunk[0] << 1) | chunk[5]
        col = (chunk[1] << 3) | (chunk[2] << 2) | (chunk[3] << 1) | chunk[4]
        val = S_BOXES[i][row * 16 + col]
        for j in range(3, -1, -1):
            output.append((val >> j) & 1)
    return _permute(output, P)

def _des_block(block: bytes, subkeys: list) -> bytes:
    """Encrypt or decrypt a single 8-byte block with DES."""
    bits = _permute(_bytes_to_bits(block), IP)
    L, R = bits[:32], bits[32:]
    for sk in subkeys:
        L, R = R, _xor(L, _f(R, sk))
    final = _permute(R + L, IP_INV)
    return _bits_to_bytes(final)

def des_encrypt_block(block: bytes, key: bytes) -> bytes:
    return _des_block(block, _generate_subkeys(key))

def des_decrypt_block(block: bytes, key: bytes) -> bytes:
    return _des_block(block, list(reversed(_generate_subkeys(key))))

# ── Padding (PKCS#7) ──────────────────────────────────────────────────────────

def _pad(data: bytes) -> bytes:
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def _unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

# ── Triple DES ────────────────────────────────────────────────────────────────

class TripleDES:
    """
    Triple DES implementation supporting:
    - 2-key mode (16 bytes): K1=K3, K2 independent
    - 3-key mode (24 bytes): K1, K2, K3 all independent
    - ECB and CBC block modes
    """

    def __init__(self, key: bytes, mode: str = "CBC", iv: bytes = None):
        if len(key) == 16:
            self.k1, self.k2, self.k3 = key[:8], key[8:], key[:8]
            self.key_mode = "2-key"
        elif len(key) == 24:
            self.k1, self.k2, self.k3 = key[:8], key[8:16], key[16:]
            self.key_mode = "3-key"
        else:
            raise ValueError("Key must be 16 bytes (2-key) or 24 bytes (3-key)")

        if mode not in ("ECB", "CBC"):
            raise ValueError("Mode must be 'ECB' or 'CBC'")
        self.mode = mode
        self.iv = iv or bytes(8)

    def _ede_encrypt(self, block: bytes) -> bytes:
        """Encrypt–Decrypt–Encrypt with K1, K2, K3."""
        step1 = des_encrypt_block(block, self.k1)
        step2 = des_decrypt_block(step1, self.k2)
        step3 = des_encrypt_block(step2, self.k3)
        return step3

    def _ede_decrypt(self, block: bytes) -> bytes:
        """Decrypt–Encrypt–Decrypt with K3, K2, K1 (reverse EDE)."""
        step1 = des_decrypt_block(block, self.k3)
        step2 = des_encrypt_block(step1, self.k2)
        step3 = des_decrypt_block(step2, self.k1)
        return step3

    def encrypt(self, plaintext: bytes) -> bytes:
        data = _pad(plaintext)
        blocks = [data[i:i+8] for i in range(0, len(data), 8)]
        result = b""
        prev = self.iv

        for block in blocks:
            if self.mode == "CBC":
                block = bytes(a ^ b for a, b in zip(block, prev))
            enc = self._ede_encrypt(block)
            if self.mode == "CBC":
                prev = enc
            result += enc

        return result

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) % 8 != 0:
            raise ValueError("Ciphertext length must be a multiple of 8")
        blocks = [ciphertext[i:i+8] for i in range(0, len(ciphertext), 8)]
        result = b""
        prev = self.iv

        for block in blocks:
            dec = self._ede_decrypt(block)
            if self.mode == "CBC":
                dec = bytes(a ^ b for a, b in zip(dec, prev))
                prev = block
            result += dec

        return _unpad(result)
