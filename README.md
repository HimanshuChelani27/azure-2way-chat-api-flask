# Azure Chat API with Flask

This project provides a **REST API** built with **Flask** that integrates with **Azure Communication Services** to facilitate real-time chat functionalities. It includes user management, chat thread creation, message exchange, and retrieval.

## Features ✅

- **Create users** and generate authentication tokens  
- **Create chat threads**  
- **Add participants** to a chat thread  
- **Send and receive messages**  
- **Fetch chat history**  

## Tech Stack 🛠️

- **Backend:** Flask (Python)  
- **Cloud Services:** Azure Communication Services (Chat & Identity APIs)  

---

## Prerequisites ⚙️

Ensure you have the following:

- Python **3.7+** installed on your machine  
- **Azure Communication Services** set up with an active **connection string**  

---

## Installation 🏗️

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/HimanshuChelani27/azure-chat-api-flask.git
cd azure-chat-api-flask
2️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Configure Azure Communication Services
Replace the placeholder connection string in the script with your Azure Communication Services connection string.

Running the Application ▶️
Start the Flask server by running:

bash
Copy
Edit
python app.py
The API will be available at:
➡️ http://localhost:5000

API Endpoints 🚀
1️⃣ Create Users
POST /create_users

Response:

json
Copy
Edit
{
  "user1_id": "user_id_1",
  "user2_id": "user_id_2",
  "user1_token": "token_1",
  "user2_token": "token_2"
}
2️⃣ Create Chat Thread
POST /create_thread

Request:

json
Copy
Edit
{
  "user1_id": "user_id_1"
}
Response:

json
Copy
Edit
{
  "thread_id": "thread_id_123"
}
3️⃣ Add User to Thread
POST /add_user

Request:

json
Copy
Edit
{
  "thread_id": "thread_id_123",
  "user2_id": "user_id_2"
}
Response:

json
Copy
Edit
{
  "message": "User added successfully"
}
4️⃣ Send Message
POST /send_message

Request:

json
Copy
Edit
{
  "thread_id": "thread_id_123",
  "user_id": "user_id_1",
  "message": "Hello, World!"
}
Response:

json
Copy
Edit
{
  "message": "Message sent successfully"
}
5️⃣ Fetch Messages
GET /get_messages?thread_id=thread_id_123&user_id=user_id_1

Response:

json
Copy
Edit
{
  "messages": [
    {
      "sender": "user_id_2",
      "message": "Hi!",
      "created_on": "2024-02-26T10:00:00Z"
    }
  ]
}
6️⃣ Fetch Full Chat History
GET /get_all_messages?thread_id=thread_id_123&user_id=user_id_1

Response:

json
Copy
Edit
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

License 📜
This project is licensed under the MIT License.

🔗 Author
Himanshu Chelani
