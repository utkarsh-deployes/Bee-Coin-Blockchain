import hashlib
import json
from time import time
from datetime import datetime

class Transaction:
    """Represents a transaction structure."""
    def __init__(self, from_address, to_address, amount, fee=0, signature=None, timestamp=None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.fee = fee
        self.timestamp = timestamp or time()
        self.signature = signature

    def calculate_hash(self):
        """Calculates the hash of the transaction."""
        from_address_str = self.from_address if self.from_address is not None else ""
        transaction_data = f"{from_address_str}{self.to_address}{self.amount}{self.fee}{self.timestamp}"
        return hashlib.sha256(transaction_data.encode()).hexdigest()

class Block:
    """Represents a single block in our blockchain."""
    def __init__(self, timestamp, transactions, previous_hash=''):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculates the hash of the entire block."""
        transaction_hashes = "".join([tx.calculate_hash() for tx in self.transactions])
        block_data = f"{self.timestamp}{transaction_hashes}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_data.encode()).hexdigest()

    def mine_block(self, difficulty):
        """The 'Proof of Work' algorithm."""
        difficulty_prefix = '0' * difficulty
        while not self.hash.startswith(difficulty_prefix):
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined! Hash: {self.hash}")

class BeeBlockchain:
    """Manages the entire Bee Coin blockchain."""
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.difficulty = 4
        self.mining_reward = 100

    def create_genesis_block(self):
        """Creates the very first block in the chain."""
        return Block(timestamp=datetime.now().isoformat(), transactions=[], previous_hash="0")

    def get_latest_block(self):
        """Returns the most recent block in the chain."""
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        """Creates a SHA-256 hash of a Block dictionary."""
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def add_transaction(self, transaction):
        """Adds a new transaction to the list of pending transactions."""
        self.pending_transactions.append(transaction)
        return self.get_latest_block().hash

    def mine_pending_transactions(self, miner_reward_address):
        """
        Mines a new block, processes transactions, and awards fees.
        This version allows mining empty blocks.
        """
        total_fees = sum(tx.fee for tx in self.pending_transactions)
        reward_tx = Transaction(from_address=None, to_address=miner_reward_address, amount=self.mining_reward + total_fees)
        
        block_transactions = self.pending_transactions + [reward_tx]
        
        new_block = Block(
            timestamp=datetime.now().isoformat(),
            transactions=block_transactions,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        
        print("Block successfully mined and added to the chain.")
        self.chain.append(new_block)
        
        self.pending_transactions = []
        return new_block

    def is_chain_valid(self, chain_to_validate):
        """
        Determine if a given blockchain (as a list of dictionaries) is valid.
        """
        genesis_block = chain_to_validate[0]

        if genesis_block['previous_hash'] != "0":
            return False

        for i in range(1, len(chain_to_validate)):
            current_block_data = chain_to_validate[i]
            previous_block_data = chain_to_validate[i-1]
            
            if current_block_data['previous_hash'] != self.hash(previous_block_data):
                return False
            if not current_block_data['hash'].startswith('0' * self.difficulty):
                return False
        
        return True