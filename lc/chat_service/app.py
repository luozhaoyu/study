# 1. Save this file as `app.py`
# 2. Make sure you have flask installed `pip install flask`
# 3. Run using `flask run -h localhost -p 5000`
"""
https://www.notion.so/Chat-Service-10e1966d9ad94950ad31fa0ba82d4b1e
"""

from flask import Flask, request

app = Flask(__name__)
name = "notion candidate"

class ChatService:
    """
    Attributes:
      room_members: key is room_id, value is name list
      messages: key is room_id, value is message list
    """
    def __init__(self):
        self.room_members = {"public": set()}
        self.messages = {}
        
    def retrieve_message(self, name, room_id):
        if self.in_room(name, room_id):
            return self.messages.get(room_id)
        print(name, "is not in: ", room_id)

    def send_message(self, name, room_id, message):
        if room_id not in self.room_members:
            return False

        if not self.in_room(name, room_id):
            return False

        if room_id in self.messages:
            self.messages[room_id].append(message)
        else:
            self.messages[room_id] = [message]

    def in_room(self, name, room_id):
        if room_id in self.room_members and name in self.room_members[room_id]:
            return True
        print("{} not in {}".format(name, room_id))
        return False
            
    def join_room(self, name, room_id):
        if room_id in self.room_members:
            self.room_members[room_id].add(name)
        else:
            self.room_members[room_id] = set([name])
        print(self.room_members)

cs = ChatService()

@app.route('/', methods=['GET'])
def index():
    return 'Hello {}'.format(name), 200

@app.route('/set_name', methods=['POST'])
def set_name():
    global name
    try: 
        payload = request.get_json()
        new_name = payload["name"]
        message = {
            "message": "Name changed!",
            "old_name": name,
            "new_name": new_name,
        }
        name = new_name
        return message, 201
    except Exception as e:
        return {"error": str(e)}, 500

@app.route('/retrieve_message', methods=['GET'])
def retrieve_message():
    """
    Args:
      name: user_name
      room_id: int
    """
    args = request.form
    name = args.get("name")
    room_id = args.get("room_id")
    messages = cs.retrieve_message(name, room_id)
    return str(messages), 200

@app.route('/join_room', methods=['PUT'])
def join_room():
    """
    Args:
      name: user_name
      room_id: int
    """
    args = request.form
    print(args)
    name = args.get("name")
    room_id = args.get("room_id")
    cs.join_room(name, room_id)
    messages = cs.retrieve_message(name, room_id)
    return str(messages), 200

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Args:
      name: user_name
      room_id: int
      message
    """
    args = request.form
    print(request, args)
    name = args.get("name")
    room_id = args.get("room_id")
    message = args.get("message")
    cs.send_message(name, room_id, message)
    return "{} said {}".format(name, message), 200
