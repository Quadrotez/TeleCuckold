import json

with open("data/ignore.json", "r") as f:
    ignore = json.loads(f.read())

with open("data/answer.json", "r") as f:
    answer = json.loads(f.read())

def check_ignore(message: str) -> bool:
    for msg in ignore:
        match msg["type"]:
            case "strict":
                if message == msg["message"]:
                    return True
            case "startswith":
                if message.startswith(msg["message"]):
                    return True

            case "endswith":
                if message.endswith(msg["message"]):
                    return True
    return False

def check_answer(message: str):
    for msg in answer:
        
        match msg["type"]:
            case "strict":
                if message == msg["message"]:
                    return True, msg["answer_r"], msg["answer_r"]
            case "startswith":
                if message.startswith(msg["message"]):
                    return True, msg["answer"], msg["answer_r"]

            case "endswith":
                if message.endswith(msg["message"]):
                    return True, msg["answer"], msg["answer_r"]
    return False, None
