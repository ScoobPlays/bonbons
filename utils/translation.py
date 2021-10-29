import base64

def b64_encode(text: str):
    message_bytes = text.encode("ascii")
    base64_bytes = base64.b64encode(message_bytes)
    message = base64_bytes.decode("ascii")
    return message

def b64_decode(text: str):
    b64msg = text.encode("ascii")
    message_bytes = base64.b64decode(b64msg)
    message = message_bytes.decode("ascii")
    return message
