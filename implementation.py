import datetime
import hashlib
import json
from uuid import uuid4
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
        self.transactions = []
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

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.calculate_hash(previous_block):
                return False
            previous_proof = previous_block["proof"]
            proof = block["proof"]
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            "sender": sender,
            "receiver": receiver,
            "amount": amount
        })
        previous_block = self.get_previous_block()
        return previous_block["index"] + 1

    def add_node_to_network(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


my_blockchain = MyBlockchain()


node_address = str(uuid4()).replace('-', '')


def mine_my_block():
    previous_block = my_blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = my_blockchain.proof_of_work(previous_proof)
    previous_hash = my_blockchain.calculate_hash(previous_block)
    my_blockchain.add_transaction(sender=node_address, receiver="Miner", amount=10)
    block = my_blockchain.create_block(proof, previous_hash)
    return block


def add_my_transaction(sender, receiver, amount):
    my_blockchain.add_transaction(sender, receiver, amount)
    return "Transaction added successfully."


def connect_my_node(node):
    my_blockchain.add_node_to_network(node)
    return "Node connected successfully."


if __name__ == "__main__":
    print("Mining my block...")
    print(mine_my_block())

    print("Adding my transaction...")
    print(add_my_transaction("sender1", "receiver1", 10))

    print("Connecting my node...")
    print(connect_my_node("http://192.168.0.5:5000"))
