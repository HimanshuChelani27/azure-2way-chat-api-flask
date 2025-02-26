Azure Chat API with Flask

This project provides a REST API built with Flask that integrates with Azure Communication Services to facilitate real-time chat functionalities. It includes user management, chat thread creation, message exchange, and retrieval.

Features

✅ Create users and generate authentication tokens

✅ Create chat threads

✅ Add participants to a chat thread

✅ Send and receive messages

✅ Fetch chat history

Tech Stack

Backend: Flask (Python)

Cloud Services: Azure Communication Services (Chat & Identity APIs)

Prerequisites

Python 3.7+ installed on your machine.

Azure Communication Services set up with an active connection string.

Installation

Clone the repository:

git clone https://github.com/your-username/azure-chat-api-flask.git
cd azure-chat-api-flask

Install dependencies:

pip install -r requirements.txt

Replace the placeholder connection string in the script with your Azure Communication Services connection string.

Running the Application

Start the Flask server by running:

python app.py

The API will be available at http://localhost:5000.

API Endpoints

1. Create Users

POST /create_users

Response:

{
  "user1_id": "user_id_1",
  "user2_id": "user_id_2",
  "user1_token": "token_1",
  "user2_token": "token_2"
}

2. Create Chat Thread

POST /create_thread

Request:

{
  "user1_id": "user_id_1"
}

Response:

{
  "thread_id": "thread_id_123"
}

3. Add User to Thread

POST /add_user

Request:

{
  "thread_id": "thread_id_123",
  "user2_id": "user_id_2"
}

Response:

{
  "message": "User added successfully"
}

4. Send Message

POST /send_message

Request:

{
  "thread_id": "thread_id_123",
  "user_id": "user_id_1",
  "message": "Hello, World!"
}

Response:

{
  "message": "Message sent successfully"
}

5. Fetch Messages

GET /get_messages?thread_id=thread_id_123&user_id=user_id_1

Response:

{
  "messages": [
    {
      "sender": "user_id_2",
      "message": "Hi!",
      "created_on": "2024-02-26T10:00:00Z"
    }
  ]
}

6. Fetch Full Chat History

GET /get_all_messages?thread_id=thread_id_123&user_id=user_id_1

Response:

{
  "messages": [
    {
      "sender": "user_id_1",
      "message": "Hello, World!",
      "created_on": "2024-02-26T09:59:00Z"
    },
    {
      "sender": "user_id_2",
      "message": "Hi!",
      "created_on": "2024-02-26T10:00:00Z"
    }
  ]
}

Deployment

To deploy the app using Docker:

Build the Docker image:

docker build -t azure-chat-api .

Run the container:

docker run -p 5000:5000 azure-chat-api

License

This project is licensed under the MIT License.

🔗 Author: Himanshu Chelani
