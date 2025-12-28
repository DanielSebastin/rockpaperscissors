
# Rock–Paper–Scissors Game on AWS (EC2 + DynamoDB)

A multiplayer **Rock–Paper–Scissors** web application built using **Python (Flask)** and **Amazon DynamoDB**, designed to run on **AWS EC2 using IAM Roles** (no hardcoded credentials).

This project is adapted from a Tic-Tac-Toe DynamoDB reference architecture and demonstrates:

* Server-side game logic
* Conditional writes in DynamoDB
* Stateless web servers
* AWS-native authentication using IAM roles

---

## Table of Contents

1. Project Overview
2. Architecture
3. Tech Stack
4. Folder Structure
5. Game Flow
6. DynamoDB Design
7. Setup & Installation
8. Running Locally (DynamoDB Local)
9. Running on AWS EC2
10. IAM Role & Permissions
11. API Routes
12. Screens & UI Flow
13. Common Errors & Fixes
14. Future Enhancements

---

## 1. Project Overview

This application allows two users to:

1. Log in using a username (session-based)
2. Create a Rock–Paper–Scissors game
3. Submit their choice independently
4. Automatically resolve the game once both players have chosen
5. Persist game state in DynamoDB

There is **no frontend JavaScript**, **no polling**, and **no websockets**.
All state is managed via **DynamoDB conditional updates**.

---

## 2. Architecture

```
Browser
   |
   v
Flask (EC2)
   |
   v
DynamoDB (Games Table)
```

### Key Characteristics

* Stateless Flask server
* DynamoDB as the single source of truth
* IAM Role authentication (no AWS keys)
* Supports local development with DynamoDB Local

---

## 3. Tech Stack

| Layer    | Technology              |
| -------- | ----------------------- |
| Backend  | Python 3, Flask         |
| Database | Amazon DynamoDB         |
| AWS Auth | IAM Role                |
| SDK      | boto (v2)               |
| Frontend | HTML (Jinja2 templates) |

---

## 4. Folder Structure

```
rock-paper-scissors/
│
├── application.py              # Flask entry point
├── requirements.txt
├── README.md
│
├── dynamodb/
│   ├── connectionManager.py    # DynamoDB connection handling
│   ├── setupDynamoDB.py        # Table & index creation
│   └── gameController.py       # Game logic & DB operations
│
├── models/
│   └── game.py                 # Game domain model
│
├── templates/
│   ├── index.html              # Login & create game
│   ├── create.html             # Create new game
│   └── play.html               # Play RPS
│
└── static/
```

---

## 5. Game Flow

1. User logs in (username stored in session)
2. User creates a game by inviting an opponent
3. Game stored in DynamoDB with status `IN_PROGRESS`
4. Each player submits one choice:

   * `ROCK`
   * `PAPER`
   * `SCISSORS`
5. When both choices exist:

   * Winner is calculated
   * Status updated to `FINISHED`
6. Result shown to both players

---

## 6. DynamoDB Design

### Table: `Games`

#### Primary Key

```
GameId (String)  — HASH
```

#### Global Secondary Indexes

```
HostId + StatusDate
OpponentId + StatusDate
```

#### Attributes per Item

| Attribute      | Description                |
| -------------- | -------------------------- |
| GameId         | Unique game identifier     |
| HostId         | Game creator               |
| OpponentId     | Invited player             |
| StatusDate     | Game lifecycle + timestamp |
| HostChoice     | ROCK / PAPER / SCISSORS    |
| OpponentChoice | ROCK / PAPER / SCISSORS    |
| Result         | HostId / OpponentId / Tie  |

#### Status Values

```
IN_PROGRESS_<timestamp>
FINISHED_<timestamp>
```

---

## 7. Setup & Installation

### Prerequisites

* Python 3.9+
* pip
* Java (for DynamoDB Local)
* AWS Account (for EC2 deployment)

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Running Locally (DynamoDB Local)

### Step 1: Start DynamoDB Local

```bash
java -Djava.library.path=./DynamoDBLocal_lib \
     -jar DynamoDBLocal.jar -sharedDb
```

### Step 2: Create the table (one time)

```bash
python
>>> from dynamodb.connectionManager import ConnectionManager
>>> cm = ConnectionManager(mode="local")
>>> cm.createGamesTable()
```

### Step 3: Run Flask

```bash
python application.py
```

Open:

```
http://localhost:5000
```

---

## 9. Running on AWS EC2

### Step 1: Launch EC2

* Amazon Linux 2
* Open port **5000** (or use ALB)

### Step 2: Attach IAM Role

Attach a role with DynamoDB access (see below).

### Step 3: Install dependencies

```bash
sudo yum install python3 -y
pip3 install -r requirements.txt
```

### Step 4: Run application

Edit `application.py`:

```python
cm = ConnectionManager(mode="service")
```

Run:

```bash
python3 application.py
```

---

## 10. IAM Role & Permissions

### Required Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:*"
      ],
      "Resource": "*"
    }
  ]
}
```

Attach this policy to the EC2 IAM Role.

✅ No access keys required
✅ Secure by default

---

## 11. Flask Routes

| Route          | Method   | Description   |
| -------------- | -------- | ------------- |
| `/`            | GET/POST | Login         |
| `/create`      | POST     | Create game   |
| `/game/<id>`   | GET      | View game     |
| `/choose/<id>` | POST     | Submit choice |

---

## 12. UI Flow

1. Login page
2. Create game
3. Choose Rock / Paper / Scissors
4. Wait for opponent
5. See result
6. Play again

---
