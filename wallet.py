import pickle
import requests
from bee_coin import Wallet, Transaction

NODE_URL = "http://127.0.0.1:5000"
WALLET_FILE = "my_wallet.dat"

def create_wallet():
    """Creates a new wallet and saves it to a file."""
    wallet = Wallet()
    with open(WALLET_FILE, "wb") as f:
        pickle.dump(wallet, f)
    print("Wallet created and saved to my_wallet.dat")
    print(f"Your new public address is: {wallet.get_public_key_hex()}")
    return wallet

def load_wallet():
    """Loads an existing wallet from a file."""
    try:
        with open(WALLET_FILE, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("No wallet file found. Creating a new one.")
        return create_wallet()

def get_balance(address):
    """Gets the balance of an address from the node."""
    try:
        response = requests.get(f"{NODE_URL}/balance/{address}")
        if response.status_code == 200:
            print(f"Balance for address {address[:10]}... is: {response.json()['balance']} HNY")
        else:
            print(f"Error fetching balance: {response.json()['message']}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the node.")

def send_transaction(wallet, recipient, amount, fee):
    """Creates, signs, and sends a transaction to a node."""
    print("Creating transaction...")
    tx = Transaction(wallet.get_public_key_hex(), recipient, amount, fee)
    
    print("Signing transaction...")
    tx.sign_transaction(wallet)

    tx_data = tx.__dict__.copy()
    tx_data['signature'] = tx.signature.hex() 

    print("Broadcasting transaction to the network...")
    try:
        response = requests.post(f"{NODE_URL}/transactions/new", json=tx_data)
        if response.status_code == 201:
            print("Transaction submitted successfully!")
        else:
            print(f"Error: {response.json()['message']}")
    except requests.exceptions.ConnectionError:
        print("Could not connect to the node.")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python wallet.py <command> [options]")
        print("Commands: create, balance, send")
        sys.exit(1)

    command = sys.argv[1]
    
    if command == 'create':
        create_wallet()
    elif command == 'balance':
        wallet = load_wallet()
        get_balance(wallet.get_public_key_hex())
    elif command == 'send':
        if len(sys.argv) != 5:
            print("Usage: python wallet.py send <recipient_address> <amount> <fee>")
            sys.exit(1)
        wallet = load_wallet()
        recipient = sys.argv[2]
        amount = int(sys.argv[3])
        fee = int(sys.argv[4])
        send_transaction(wallet, recipient, amount, fee)
    else:
        print("Unknown command.")