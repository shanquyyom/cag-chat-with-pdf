# 🧠 Chat With Your PDF – CAG Project

Interact with your PDF files using natural language! This project allows you to upload any PDF document and ask questions, powered by FastAPI, LangChain, OpenAI, and PyMuPDF. Designed for developers and learners exploring real-world applications of LLMs.

---

## 📸 Demo

*(Add video or image here — optional)*  
👉 Example: `demo.mp4` or a Google Drive / YouTube link

---

## 🚀 Features

- Upload any PDF and ask questions
- Uses LangChain and OpenAI for contextual answers
- FastAPI-based backend
- Clean modular code (routers, utils)
- Real-time response system

---

## 🛠️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/cag-chat-with-pdf.git
cd cag-chat-with-pdf

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate    # Windows
# source venv/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the FastAPI app
uvicorn main:app --reload

Then open browser at:
📍 http://127.0.0.1:8000/docs — for interactive Swagger UI.

📁 Folder Structure
cag-chat-with-pdf/
├── main.py
├── requirements.txt
├── README.md
└── src/
    ├── routers/
    │   └── data_handler.py
    └── utils/
        ├── llm_client.py
        └── pdf_processor.py

🧰 Tech Stack
Python 3

FastAPI

LangChain

OpenAI API

PyMuPDF (fitz)

Uvicorn


✨ Use Cases
Chatbot for documents

AI assistants for students, lawyers, researchers

Backend service for PDF Q&A

NLP + Document AI Projects

👨‍💻 Author
Shan Quyyoom
📍 Jhang, Pakistan
https://www.linkedin.com/in/shan-quyyoom-452923365
📧 shanquyyoom99@gmail.com

📜 License
This project is open-source and available under the MIT License.

❤️ Support
If you find this project useful, feel free to ⭐ star the repo and share it!




