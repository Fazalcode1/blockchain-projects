import datetime
import hashlib
import json
from urllib.parse import urlparse

class MyBlockchain:
    
    def __init__(self):
        self.blocks = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {
            "index": len(self.blocks) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
            "transactions": self.transactions,
        }
        hash_value = self.calculate_hash(block)
        block["hash"] = hash_value
        self.blocks.append(block)
        return block

    def get_previous_block(self):
        return self.blocks[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def calculate_hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })

    def add_node_to_network(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)
        
    def print_block(self, block_index=None):
        if block_index is None:
            for block in self.blocks:
                self._print_block_details(block)
        elif 0 <= block_index < len(self.blocks):
            block = self.blocks[block_index]
            self._print_block_details(block)
        else:
            print("Invalid block index.")

    def _print_block_details(self, block):
        print("Block Index:", block["index"])
        print("Timestamp:", block["timestamp"])
        print("Proof:", block["proof"])
        print("Previous Hash:", block["previous_hash"])
        print("Transactions:", block["transactions"])
        print("Hash:", block["hash"])
        print()
        print("Connected Nodes:")
        for node in self.nodes:
            print("- ", node)
        print()

my_blockchain = MyBlockchain()


def mine_my_block():
    previous_block = my_blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = my_blockchain.proof_of_work(previous_proof)
    previous_hash = my_blockchain.calculate_hash(previous_block)
    block = my_blockchain.create_block(proof, previous_hash)


def add_my_transaction(sender, receiver, amount):
    my_blockchain.add_transaction(sender, receiver, amount)
    return "Transaction added successfully."


def connect_my_node(node):
    my_blockchain.add_node_to_network(node)
    return "Node connected successfully.\n"


if __name__ == "__main__":
    print("Mining my block...")
    mine_my_block()

    print("Adding my transaction...")
    print(add_my_transaction("sender1", "receiver1", 10))

    print("Connecting my node...")
    print(connect_my_node("http://192.168.0.5:5000"))

    my_blockchain.print_block()
