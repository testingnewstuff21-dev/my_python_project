#---------------------------
# Importing necessary libraries
#---------------------------

from time import time
from hashlib import sha256
from datetime import datetime
import json
import os


def readable_time(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

#---------------------------
# Blockchain and Block classes
#---------------------------


class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index # index of the block in the chain    
        self.previous_hash = previous_hash # hash of the previous block
        self.timestamp = timestamp # when the block was created
        self.data = data # the data in the block 
        self.hash = hash # the hash of the block

class Blockchain:
    def __init__(self):
        self.chain = [] # list where blocks will be stored
        if os.path.exists("blockchain.json"): # if the blockchain file exists
            self.load_chain() # load the existing blockchain from the file
        else:
            self.create_genesis_block()
            self.save_chain() #save the chain 

    def create_genesis_block(self):
        index = 0 # first block has index 0
        previous_hash = "0" # empty previous hash for genesis block
        timestamp = int(time()) # current time as timestamp
        data = "Genesis Block" # arbitrary data for genesis block
        hash = sha256(f"{index}{previous_hash}{timestamp}{data}".encode()).hexdigest() # hashes all the block's contents
        genesis_block = Block(index, previous_hash, timestamp, data, hash)  # creates the genesis block
        self.chain.append(genesis_block) # adds the genesis block to the chain
    
    def add_block(self, data):
        index = len(self.chain) # length of the chain is the index of the new block
        previous_hash = self.chain[-1].hash  # hash of the last block in the chain
        timestamp = int(time()) # the current time as timestamp
        hash = sha256(f"{index}{previous_hash}{timestamp}{data}".encode()).hexdigest() # hashes all the block's contents
        new_block = Block(index, previous_hash, timestamp, data, hash)  # creates the new block
        self.chain.append(new_block)
        self.save_chain()   # add the new block to the chain
    
    def print_chain(self):
         print("=== Blockchain ===")  
         for block in self.chain: # iterate through each block in the chain
            # print all the details of the block 
            print(f"Block #{block.index}")  
            print(f"  Timestamp     : {block.timestamp}")
            print(f"  Readable Time : {readable_time(block.timestamp)}")
            print(f"  Data          : {block.data}")
            print(f"  Previous Hash : {block.previous_hash}")
            print(f"  Hash          : {block.hash}")
            print("-" * 40)
    
    def save_chain(self, filename="blockchain.json"):
        chain_data = [] # list to hold the chain data
        for block in self.chain: #iterate through the block chian 
            chain_data.append({    # add each block's details to the list
                'index': block.index,
                'previous_hash': block.previous_hash,
                'timestamp': block.timestamp,
                'data': block.data,
                'hash': block.hash
            })
        with open(filename, 'w') as f: # open the file in write mode
            json.dump(chain_data, f, indent=4) # write the chain data to the file in JSON format
    
    def load_chain(self, filename="blockchain.json"):
        try:
            with open(filename, 'r') as f: # open the file in read mode
                chain_data = json.load(f) # load the chain data from the file
                self.chain = []  # reset the chain
                for block in chain_data: # iterate through each block in the loaded data
                    block = Block( 
                        block['index'],
                        block['previous_hash'],
                        block['timestamp'],
                        block['data'],
                        block['hash']
                    )
                    self.chain.append(block)   # add the block to the chain

        except FileNotFoundError: # if the file does not exist
            self.chain = []     #start with new chain   
            self.create_genesis_block() # create the genesis block


if __name__ == "__main__":
    blockchain = Blockchain() # create a new blockchain instance
    blockchain.add_block("First real block") # add a block with some data
    blockchain.add_block("Second real block") # add another block with some data
    blockchain.print_chain() # print the entire blockchain