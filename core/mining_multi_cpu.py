import binascii
import hashlib
import time
from multiprocessing import Pool, Manager, Value


class Block:
    def __init__(
        self,
        version: str,
        bits: int,
        previous_hash: str,
        merkle_root: str,
        timestamp: int
    ) -> None:
        """
        Initializes a Block object.

        Args:
            version (str): The version of the block.
            bits (int): The bits value of the block.
            previous_hash (str): The hash of the previous block.
            merkle_root (str): The Merkle root of the block.
            timestamp (int): The timestamp of the block.

        Returns:
            None
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

        self._path_save = f"./data/{self._merkle_root}.csv"

    def compute_hash(self, nonce: int) -> str:
        """
        Computes the hash value of the block.

        Args:
            nonce (int): The nonce value.

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

    def search_nonce(
        self,
        start_nonce: int,
        end_nonce: int,
        target_difficulty: int,
        found_nonce: Value
    ) -> None:
        """
        Searches for a valid nonce within a given range.

        Args:
            start_nonce (int): The starting nonce value for the search.
            end_nonce (int): The ending nonce value for the search.
            target_difficulty (int): The target difficulty level (number of leading zeros in the hash).
            found_nonce (Value): A shared Value object to store the found nonce.

        Returns:
            None
        """
        nonce = start_nonce
        while nonce <= end_nonce:
            if found_nonce.value != -1:
                break

            hash_value = self.compute_hash(nonce=nonce)
            if self.count_zeros(hash_value) >= target_difficulty:
                found_nonce.value = nonce
                break
            nonce += 1

    def mine_block(
        self,
        target_difficulty: int,
        nb_process: int,
        init_nonce: int,
        end_nonce: int
    ) -> int:
        """
        Mines the block by searching for a valid nonce.

        Args:
            target_difficulty (int): The target difficulty level (number of leading zeros in the hash).
            nb_process (int): The number of processes to use for mining.
            init_nonce (int): The initial nonce value for mining.
            end_nonce (int): The last nonce value.

        Returns:
            int: The found nonce value.
        """
        with Manager() as manager:
            found_nonce = manager.Value('i', -1)
            ranges = []

            step = (end_nonce - init_nonce) // nb_process
            for i in range(nb_process):
                start_nonce = init_nonce + step * i
                ranges.append(
                    (
                        start_nonce,
                        start_nonce + step,
                        target_difficulty,
                        found_nonce
                    )
                )
            with Pool(processes=nb_process) as pool:
                pool.starmap(self.search_nonce, ranges)

            return found_nonce.value

    @staticmethod
    def count_zeros(hash_value: str) -> int:
        """
        Counts the number of leading zeros in the hash value.

        Args:
            hash_value (str): The hash value.

        Returns:
            int: The number of leading zeros.
        """
        count = 0
        for c in hash_value:
            try:
                if int(c) == 0:
                    count += 1
                else:
                    break
            except ValueError:
                break
        return count


def run() -> None:
    """
    Runs the mining process for a block and prints the results.

    Returns:
        None
    """
    target_difficulty = 13

    t_init = time.time()
    block = Block(
        version="00000001",
        bits=437129626,
        previous_hash="00000000000007d0f98d9edca880a6c124e25095712df8952e0439ac7409738a",
        merkle_root="935aa0ed2e29a4b81e0c995c39e06995ecce7ddbebb26ed32d550a72e8200bf5",
        timestamp=1322131230
    )

    found_nonce = block.mine_block(
        target_difficulty=target_difficulty,
        nb_process=1000,
        init_nonce=0,
        end_nonce=4294967295
    )
    total_time = time.time() - t_init
    print(f"Found nonce: {found_nonce}")
    print(f"Total time: {total_time}s")


if __name__ == '__main__':
    run()
