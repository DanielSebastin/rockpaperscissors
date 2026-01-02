# Rock Paper Scissors – AWS Project

## Overview
This project implements a multiplayer Rock Paper Scissors game using:
- AWS EC2 (Amazon Linux 2023)
- IAM Role
- DynamoDB
- Python Flask backend

## Architecture
- EC2 runs the Flask application
- IAM role provides secure access to DynamoDB
- DynamoDB stores game state
- Same GameId is shared by both players

## Workflow
1. Player 1 creates a game
2. GameId is generated and stored
3. Player 2 accepts or rejects invite
4. Both players submit choices
5. Server calculates result
6. DynamoDB updates game status

## How to Run
1. Attach IAM role with DynamoDB access
2. Open port 5000 in EC2 security group
3. Install dependencies:
