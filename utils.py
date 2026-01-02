import uuid


def generate_game_id():
    return str(uuid.uuid4())


def decide_winner(choice1,choice2):
    if choice1==choice2:
        return "DRAW"

    rules={
        "rock":"scissors",
        "scissors":"paper",
        "paper":"rock"
    }

    if rules[choice1]==choice2:
        return "WIN"
    else:
        return "LOSE"
