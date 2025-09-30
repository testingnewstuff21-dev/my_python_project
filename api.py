from flask import Flask, request, jsonify
from blockchain import Blockchain, readable_time
from hashlib import sha256

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/blocks', methods=['GET'])
def get_chain(): 
    chain_data = [] # get the chain data 
    for block in blockchain.chain: # iterate through each block in the chain
        chain_data.append({ 
            'index': block.index,
            'previous_hash': block.previous_hash,
            'timestamp': block.timestamp,
            'readable_time': readable_time(block.timestamp),
            'data': block.data,
            'hash': block.hash
        })
    return jsonify(chain_data), 200

@app.route('/mine', methods=['POST'])
def add_block():
    data = request.get_json() # get the data from the request
    if not data or 'data' not in data: # if there is no data or 'data' key is not in the data
        return "Invalid data", 400

    blockchain.add_block(data['data']) # add the block to the blockchain
    blockchain.save_chain() # save the blockchain to a file
    new_block = blockchain.chain[-1] # get the newly added block
    # return the details of the new block
    block_data = {
        'index': new_block.index,
        'previous_hash': new_block.previous_hash,
        'timestamp': new_block.timestamp,
        'readable_time': readable_time(new_block.timestamp),
        'data': new_block.data,
        'hash': new_block.hash
    }
    # respond with the new block data and a 201 status code (201 = created)
    return jsonify(block_data), 201

@app.route('/validate', methods=['GET'])
# interate through the blockchain and validate each block
def validate_chain():
    for i in range(0, len(blockchain.chain)):   # start from the first block to the last block
        current = blockchain.chain[i]   # get the current block
        previous = blockchain.chain[i - 1]  # get the previous block
        if current.previous_hash != previous.hash:  # if the previous hash of the current block is not equal to the hash of the previous block
            return jsonify({
                "status": "error",
                "message": "Blockchain is invalid",
                "error": f"Block #{current.index} has invalid previous hash",
                "block": f"#{current.index}"
            }),400 # return invalid if the hashes don't match
        
        # recalculate the hash of the current block and compare it to the stored hash
        recalculated_hash = sha256(f"{current.index}{current.previous_hash}{current.timestamp}{current.data}".encode()).hexdigest()
        if current.hash != recalculated_hash:   # if the hashes don't match return the inivalid response
            return jsonify({
                "status": "error",
                "message": "Blockchain is invalid",
                "error": f"Block #{current.index} has invalid hash",
                "block": f"#{current.index}"
            }), 400   
        
        return jsonify({ # if all blocks are valid return the valid response
            "message": "Blockchain is valid"
        }), 200   # return valid if all blocks are valid

@app.route('/load', methods=['POST'])
def load_chain():
    blockchain.load_chain() # load the blockchain from the file
    return jsonify({
        "message": "Blockchain loaded from file",
        "length": len(blockchain.chain)
    }), 200

@app.route('/save', methods=['POST'])
def save_chain():
    blockchain.save_chain() # save the blockchain to the file
    return jsonify({
        "message": "Blockchain saved to file",
        "length": len(blockchain.chain)
    }), 200
     


if __name__ == '__main__':
    app.run(debug=True, port=5000) # run the app on port 5000
