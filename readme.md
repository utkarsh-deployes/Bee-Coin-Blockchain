# Bee Coin (HNY) - A Python Blockchain

![Bee Coin Logo](assets\bee-coin-banner.png)

**The Currency of the Hive.**

## Description

Bee Coin (HNY) is a fully functional cryptocurrency and blockchain built from scratch in Python. Conceived as "The Currency of the Hive," this project simulates a decentralized digital ecosystem where diligent work is rewarded with tangible value. It was developed as a hands-on exploration of the core principles that power real-world cryptocurrencies.

The project began as a simple, single-file script and evolved incrementally to include all the critical components of a modern blockchain. We implemented a robust Proof-of-Work algorithm to secure the network, a peer-to-peer system for nodes to broadcast information and achieve consensus, and a secure client-side wallet for user-controlled transactions. Going beyond a simple clone, Bee Coin's most unique feature is its "Hive Mind," a built-in on-chain governance system that empowers the community to democratically guide the protocol's future. Every feature is designed to reflect the central theme: just as bees work together to build a strong and productive hive, so too can a decentralized community build and maintain value.

## About The Currency & Project Goal

Bee Coin (HNY) is a digital currency designed to reward computational work within a decentralized community, much like bees are rewarded with honey for their labor in a hive. The primary goal of this project was to build a complete cryptocurrency from the ground up to gain a fundamental understanding of how blockchain technology works—from the first signed transaction to a multi-node network that can resolve conflicts on its own.

## Mission

* **To Reward Diligent Work:** To create a digital economy that fairly rewards verifiable computational effort and meaningful participation in the network.
* **To Empower the Community:** To build a truly decentralized system where governance is in the hands of its users, not a central authority, through an accessible on-chain voting mechanism.
* **To Foster Understanding:** To serve as an open and accessible project that demystifies blockchain technology, making it tangible and understandable for developers and enthusiasts alike.

## Core Features

* **Decentralized Peer-to-Peer Network:** Nodes can discover each other, broadcast information, and resolve conflicts.
* **Proof-of-Work (PoW) Consensus:** The network is secured by a mining algorithm based on computational work. The "longest-chain rule" is used to resolve forks.
* **Two-Tiered Economic Model:** Miners are incentivized through a combination of fixed block rewards (newly minted HNY) and variable transaction fees (the "Pollination Bonus").
* **On-Chain Governance ("The Hive Mind"):** A unique feature that allows HNY holders to vote on proposals to change the protocol's rules, such as the mining difficulty.
* **Client-Side Wallet & Signing:** A separate command-line wallet application handles the secure creation and storage of private keys, ensuring all transactions are cryptographically signed before being broadcast.

## Technology Stack

* **Backend:** Python 3
* **API:** Flask
* **Cryptography:** `ecdsa` library for digital signatures (SECP256k1 curve)
* **Networking:** `requests` library for node communication