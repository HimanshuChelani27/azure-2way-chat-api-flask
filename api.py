from flask import Flask, request, jsonify
from azure.communication.identity import CommunicationIdentityClient
from azure.communication.chat import ChatClient, CommunicationTokenCredential, ChatParticipant
from datetime import datetime, timezone
import threading
import time

app = Flask(__name__)

# ✅ Replace with your Azure Communication Services connection string
CONNECTION_STRING = "YOUR_AZURE_COMMUNICATION_SERVICE_STRING"

# ✅ Initialize identity client
identity_client = CommunicationIdentityClient.from_connection_string(CONNECTION_STRING)

# ✅ Store active users & chat threads
users = {}
chat_threads = {}
last_fetched_time = {}

# ✅ Helper function to create chat client
def get_chat_client(token):
    endpoint = CONNECTION_STRING.split(';')[0].replace('endpoint=', '')
    return ChatClient(endpoint, CommunicationTokenCredential(token))

# ✅ API: Create Users & Generate Tokens
@app.route("/create_users", methods=["POST"])
def create_users():
    try:
        user1 = identity_client.create_user()
        user2 = identity_client.create_user()

        token1 = identity_client.get_token(user1, ["chat"]).token
        token2 = identity_client.get_token(user2, ["chat"]).token

        users[user1.properties["id"]] = token1
        users[user2.properties["id"]] = token2

        return jsonify({
            "user1_id": user1.properties["id"],
            "user2_id": user2.properties["id"],
            "user1_token": token1,
            "user2_token": token2
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API: Create a Chat Thread
@app.route("/create_thread", methods=["POST"])
def create_thread():
    try:
        data = request.json
        user1_id = data["user1_id"]
        user1_token = users[user1_id]

        chat_client = get_chat_client(user1_token)
        topic = "Manual Two-Way Chat"
        thread_result = chat_client.create_chat_thread(topic)
        thread_id = thread_result.chat_thread.id

        chat_threads[thread_id] = {"users": [user1_id], "messages": []}
        return jsonify({"thread_id": thread_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
from azure.communication.chat import CommunicationUserIdentifier
# ✅ API: Add User to Thread
@app.route("/add_user", methods=["POST"])
def add_user():
    try:
        data = request.json
        thread_id = data["thread_id"]
        user2_id = data["user2_id"]

        if thread_id not in chat_threads or user2_id not in users:
            return jsonify({"error": "Invalid thread ID or User ID"}), 400

        user1_id = chat_threads[thread_id]["users"][0]
        user1_token = users[user1_id]

        chat_client = get_chat_client(user1_token)
        thread_client = chat_client.get_chat_thread_client(thread_id)

        # ✅ Convert user2_id from string to CommunicationUserIdentifier
        participant = ChatParticipant(
            identifier=CommunicationUserIdentifier(user2_id),  # FIXED ✅
            display_name="User 2",
            share_history_time=datetime.now(timezone.utc)  # ✅ Fix deprecated utcnow()
        )
        thread_client.add_participants([participant])

        chat_threads[thread_id]["users"].append(user2_id)
        return jsonify({"message": "User added successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ API: Send Message
@app.route("/send_message", methods=["POST"])
def send_message():
    try:
        data = request.json
        thread_id = data["thread_id"]
        user_id = data["user_id"]
        message = data["message"]

        if user_id not in users:
            return jsonify({"error": "Invalid user ID"}), 400

        chat_client = get_chat_client(users[user_id])
        thread_client = chat_client.get_chat_thread_client(thread_id)

        thread_client.send_message(content=message, sender_display_name=user_id)

        chat_threads[thread_id]["messages"].append({"sender": user_id, "content": message})
        return jsonify({"message": "Message sent successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get_messages", methods=["GET"])
def get_messages():
    try:
        thread_id = request.args.get("thread_id")
        user_id = request.args.get("user_id")

        if thread_id not in chat_threads:
            return jsonify({"error": "Invalid thread ID"}), 400

        chat_client = get_chat_client(users[user_id])
        thread_client = chat_client.get_chat_thread_client(thread_id)

        global last_fetched_time
        if thread_id not in last_fetched_time:
            last_fetched_time[thread_id] = datetime.now(timezone.utc)  # ✅ Ensure it is a `datetime` object

        messages = thread_client.list_messages()
        new_messages = []

        for msg in messages:
            if msg.content and msg.content.message:  # ✅ Ignore empty messages
                msg_time = msg.created_on.replace(tzinfo=timezone.utc)  # ✅ Ensure consistent timezone

                if msg_time > last_fetched_time[thread_id]:
                    new_messages.append({
                        "sender": msg.sender_display_name,
                        "message": msg.content.message,
                        "created_on": msg_time.isoformat()  # ✅ Include timestamp for debugging
                    })

        # ✅ Fix: Store `last_fetched_time` as a `datetime` object, not a string
        if new_messages:
            last_fetched_time[thread_id] = max(datetime.fromisoformat(msg["created_on"]) for msg in new_messages)

        return jsonify({"messages": new_messages})  # ✅ Returns [] if no new messages
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/get_all_messages", methods=["GET"])
def get_all_messages():
    try:
        thread_id = request.args.get("thread_id")
        user_id = request.args.get("user_id")

        if thread_id not in chat_threads:
            return jsonify({"error": "Invalid thread ID"}), 400

        chat_client = get_chat_client(users[user_id])
        thread_client = chat_client.get_chat_thread_client(thread_id)

        messages = thread_client.list_messages()
        chat_history = []

        for msg in messages:
            if msg.content and msg.content.message:  # ✅ Ignore empty messages
                msg_time = msg.created_on.replace(tzinfo=timezone.utc)  # ✅ Ensure consistent timezone

                chat_history.append({
                    "sender": msg.sender_display_name,
                    "message": msg.content.message,
                    "created_on": msg_time.isoformat()  # ✅ Include timestamp for ordering
                })

        # ✅ Sort messages by time (oldest to newest)
        chat_history.sort(key=lambda x: x["created_on"])

        return jsonify({"messages": chat_history})  # ✅ Returns full conversation history

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# ✅ API: Start Flask Server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
