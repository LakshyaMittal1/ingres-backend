# test_db.py
from app.db.conversations import create_conversation
from app.db.messages import add_message, get_messages

conv = create_conversation("Test Chat")
print("Conversation:", conv)

add_message(conv["id"], "user", "Hello")
add_message(conv["id"], "assistant", "Hi there!")

msgs = get_messages(conv["id"])
print(msgs)
