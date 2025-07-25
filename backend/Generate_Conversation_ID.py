# Diese Methode generiert eine 30 (15 Zahlen + 15 Buchstaben) stellige zufällige conversation_id

def generate_conversation_id(length=15) -> str:
    import random
    import string
    from datetime import datetime
    chars = string.ascii_letters + string.digits
    random_part_one = ''.join(random.choices(chars, k=length))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    random_part_two = ''.join(random.choices(chars, k=length))
    return f"{random_part_one}{timestamp}{random_part_two}"
