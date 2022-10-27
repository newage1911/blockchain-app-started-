import datetime, json, hashlib
from flask import Flask, jsonify

class Blockchain:
    def __init__(self):
        # save all blockchain
        self.chain = []
        self.transaction = 0 # cash amount
        # create genesis block
        self.create_block(nonce = 1, previous_hash = "0")

    # create block in blockchain system
    def create_block(self, nonce, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp":  str(datetime.datetime.now()),
            "nonce": nonce,
            "data": self.transaction,
            # "nonce": str(random.choice(range(0, 65535))),
            "previous_hash": previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def hash(self, block):
        encode_block = json.dumps(block, sort_keys=True).encode() # convert pyObj(dict) => jsonObj
        return hashlib.sha256(encode_block).hexdigest()

    # proof of work (Mining)
    def proof_of_work(self, previous_nonce):
        new_nonce = 1 
        check_proof = False
    
        while check_proof is False:
            hashoperation = hashlib.sha256(str(new_nonce**2 - previous_nonce**2).encode()).hexdigest()
            if hashoperation[:4] == "0000":
                check_proof = True
            else: 
                new_nonce += 1
        return new_nonce
   
    # ตรวจสอบ block
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block["previous_hash"] != self.hash(previous_block):
                return False
            previous_nonce = previous_block["nonce"] # nonce ก่อนหน้า
            nonce = block["nonce"] # nonce ของ block ที่ถูกตรวจสอบ
            hashoperation = hashlib.sha256(str(nonce**2 - previous_nonce**2).encode()).hexdigest()
            
            if hashoperation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True

# init flask web server
app = Flask(__name__)

blockchain = Blockchain()
# print("Blockchain ->> ",blockchain.chain)
# print(blockchain.hash(blockchain.chain[0]))


# routing
@app.route('/')
def hello():
    return "<h1> Hello Blockchain </h1>"

@app.route('/get_chain')
def get_chain():
    response = {
        "chain": blockchain.chain,
        "length": len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/mining',methods=["GET"])
def mining_block():

    amount = 1000000 # cash in transaction
    blockchain.transaction = blockchain.transaction + amount
    # proof of work 
    previous_block = blockchain.get_previous_block()
    previous_nonce = previous_block["nonce"]

    # nonce
    nonce = blockchain.proof_of_work(previous_nonce)

    # hashed previous block 
    previous_hash = blockchain.hash(previous_block)

    # update a new block
    block = blockchain.create_block(nonce,previous_hash)
    response = {
        "message":"Complete Mining block",
        "index":block["index"],
        "timestamp":block["timestamp"],
        "data": block["data"],
        "nonce":block["nonce"],
        "previous_hash":block["previous_hash"]
    }
    return jsonify(response),200

@app.route('/is_valid', methods=["GET"])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {"message": "valid blockchain"}
    else: 
        response = {"message": "invalid blockchain, has problem"}
    return jsonify(response), 200

# run server
if __name__ == "__main__":
    app.run()
    