class Blockchain(object):
    # Constructor
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        # Creates a new Block and adds it to the chain
        pass

    def new_transaction(self):
        # Adds a new transaction to the list of transactions
        pass

    @staticmethod
    # NOTE: A static method unlike class method is immutable via inheritance
    def hash(block):
        # Hashes a Block
        pass

    @property
    # Decorator for implicitly allowing setters and getter on a property by
    # the same name as the function below
    def last_block(self):
        # Returns the last Block in the chain
        pass
