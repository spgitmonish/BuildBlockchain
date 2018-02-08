import hashlib
import json
from time import time

class Blockchain(object):
    # Constructor
    def __init__(self):
        self.current_transactions = []
        self.chain = []

        # Create the genesis block i.e. a block with no predecessors
        self.new_block(proof=100, previous_hash=1)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Add the new block with the transactions to the chain
        self.chain.append(block)

        # Return the block which was added to the chain
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold this transaction
        """
        # Add the transaction to the block
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        # Return the index of the block which will hold the transaction
        return self.last_block['index'] + 1

    @property
    # Decorator for implicitly allowing setters and getter on a property by
    # the same name as the function below
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    @staticmethod
    # NOTE: A static method unlike class method is immutable via inheritance
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the dictionary is ordered,
        # or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - p is the previous proof, and p' is the new proof
        :param last_proof: <int>
        :return: <int>

        NOTE: In Bitcoin, Proof of work is an algorithm which the miners race to
              solve in order to create a new block in the blockchain.
              The miners are rewarded by receiving a coin - in a transaction
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
