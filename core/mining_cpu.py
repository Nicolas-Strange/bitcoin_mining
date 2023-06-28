import binascii
import hashlib
import os.path
import time

from utils.files_op import save_csv


class Block:
    def __init__(self, version: str, bits: int, previous_hash: str,
                 merkle_root: str, timestamp: int, init_nonce: int, end_nonce: int):
        """
        Initialize a Block object.

        Args:
            version (str): The version of the block.
            bits (int): The bits value of the block.
            previous_hash (str): The hash of the previous block.
            merkle_root (str): The Merkle root of the block.
            timestamp (int): The timestamp of the block.
            init_nonce (int): The initial nonce value.
            end_nonce (int): The last nonce value.
        """
        self._version = binascii.hexlify(
            binascii.unhexlify(version)[::-1]
        )
        self._previous_hash = binascii.hexlify(
            binascii.unhexlify(previous_hash)[::-1]
        )
        self._merkle_root = binascii.hexlify(
            binascii.unhexlify(merkle_root)[::-1]
        )
        self._timestamp = binascii.hexlify(
            binascii.unhexlify(hex(int(timestamp))[2:].rjust(8, '0'))[::-1]
        )
        self._bits = binascii.hexlify(
            binascii.unhexlify(hex(bits)[2:].rjust(8, '0'))[::-1]
        )

        self._init_nonce = init_nonce
        self._end_nonce = end_nonce
        self._path_save = f"./data/{merkle_root}.csv"

    def compute_hash(self, nonce: int) -> str:
        """Compute the hash of the new block using the header.
        Args:
            nonce (int): nonce value.

        Returns:
            str: The computed hash value.
        """

        nonce = binascii.hexlify(
            binascii.unhexlify(hex(nonce)[2:].rjust(8, '0'))[::-1]
        )

        header = (
            self._version +
            self._previous_hash +
            self._merkle_root +
            self._timestamp +
            self._bits +
            nonce
        )

        header = binascii.unhexlify(header)

        hash_256 = hashlib.sha256(hashlib.sha256(header).digest()).digest()
        hash_256 = binascii.hexlify(hash_256)
        hash_256 = binascii.hexlify(binascii.unhexlify(hash_256)[::-1]).decode()

        return hash_256

    def mine_block(self, target_difficulty) -> int:
        """Mine the block.

        Args:
            target_difficulty (int): The number of zeros the target hash should start with.

        Returns:
            int: The number of hash checked
        """
        target_hash = "0" * target_difficulty  # Example: Difficulty 4 => Target hash starts with 4 zeros
        if not os.path.isfile(self._path_save):
            save_csv(path=self._path_save, row=["nonce", "nb_zeros"])

        nh_hash = 0
        for nonce in range(self._init_nonce, self._end_nonce, 1):
            block_hash = self.compute_hash(nonce=nonce)
            nb_zero = self.count_zeros(block_hash)
            if nb_zero >= 1:
                save_csv(path=self._path_save, row=[nonce, nb_zero])

            nh_hash += 1
            if block_hash[:target_difficulty] == target_hash:
                print("Block mined successfully!")
                print("Block Hash:", block_hash)
                print("Nonce:", nonce)
                break
        return nh_hash

    @staticmethod
    def count_zeros(hash_value: str) -> int:
        """Count the number of 0 at the beginning of the hash.

        Args:
            hash_value (str): The hash value.

        Returns:
            int: The number of zeros at the beginning of the hash.
        """
        ct = 0
        for c in hash_value:
            try:
                if int(c) == 0:
                    ct += 1
                else:
                    break
            except ValueError:
                break
        return ct


def run():
    target_difficulty = 65

    t_init = time.time()
    # Create a block with initial values
    block = Block(
        version="00000001",
        bits=437129626,
        previous_hash="00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
        merkle_root="935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
        timestamp=1322131230,
        init_nonce=0,
        end_nonce=4294967295
    )

    # Mine the block
    nb_hash = block.mine_block(target_difficulty)
    total_time = time.time()-t_init
    print(f"Found in: {total_time}s --- {(nb_hash / total_time) / 1000} MH/s")


if __name__ == '__main__':
    run()
