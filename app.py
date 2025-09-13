from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests
import json

from bee_coin import BeeBlockchain, Transaction, Block

app = Flask(__name__)


node_identifier = str(uuid4()).replace('-', '')

blockchain = BeeBlockchain()

nodes = set()


def resolve_conflicts():
    """
    This is our consensus algorithm, it resolves conflicts
    by replacing our chain with the longest one in the network.
    """
    neighbours = nodes
    new_chain = None
    max_length = len(blockchain.chain)

    for node in neighbours:
        try:
            response = requests.get(f'http://{node}/chain', timeout=3)
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and blockchain.is_chain_valid(chain):
                    max_length = length
                    new_chain = chain
        except requests.exceptions.RequestException:
            continue

    if new_chain:
        
        blockchain.chain = []
        for block_data in new_chain:
            transactions = [Transaction(**tx) for tx in block_data['transactions']]
            block = Block(
                timestamp=block_data['timestamp'],
                transactions=transactions,
                previous_hash=block_data['previous_hash']
            )
            block.nonce = block_data['nonce']
            block.hash = block_data['hash']
            blockchain.chain.append(block)
        return True

    return False

def serialize_chain(chain):
    """Helper to serialize the blockchain with object attributes."""
    serialized = []
    for block in chain:
        block_data = block.__dict__.copy()
        block_data['transactions'] = [tx.__dict__ for tx in block.transactions]
        serialized.append(block_data)
    return serialized


@app.route('/mine', methods=['GET'])
def mine():
    block = blockchain.mine_pending_transactions(miner_reward_address=node_identifier)
    response = {
        'message': "New Block Forged",
        'block': serialize_chain([block])[0]
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount', 'fee']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    tx = Transaction(
        from_address=values['sender'],
        to_address=values['recipient'],
        amount=values['amount'],
        fee=values['fee']
    )
    blockchain.add_transaction(tx)
    
    response = {'message': 'Transaction will be added to the next block.'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': serialize_chain(blockchain.chain),
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    new_nodes = values.get('nodes')
    if new_nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in new_nodes:
        nodes.add(urlparse(node).netloc)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = resolve_conflicts()
    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': serialize_chain(blockchain.chain)
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': serialize_chain(blockchain.chain)
        }
    return jsonify(response), 200

if __name__ == '__main__':
    from sys import argv
    port = int(argv[1]) if len(argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port)