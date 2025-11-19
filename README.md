# 🤖 SQL Query Buddy
### Your AI-Powered Data Analyst & Insight Generator

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![React](https://img.shields.io/badge/React-Vite-61DAFB)
![LangChain](https://img.shields.io/badge/LangChain-v0.1-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-orange)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-3.0-38B2AC)

**SQL Query Buddy** is a full-stack Generative AI application that empowers users to chat with their database. Built for the **Codecademy GenAI Bootcamp Contest**, it converts natural language into optimized SQL, executes it against a live database, and visualizes the results with dynamic bar charts.

---

## ✨ Key Features

* **🗣️ Natural Language to SQL:** Translate complex questions like *"Who are the top 5 customers by sales?"* into accurate SQL queries automatically.
* **🧠 RAG-Powered Context:** Uses **FAISS** vector search to "read" the database schema (tables, columns, relationships) before generating queries, ensuring high accuracy.
* **📊 Dynamic Bar Charts:** Automatically detects comparable data trends and renders interactive **Bar Charts** using Recharts.
* **💬 Conversational Memory:** Supports follow-up questions (e.g., *"Show me the top region."* -> *"Now show me the top products in that region."*).
* **✨ Prompt Refining:** Includes an AI-powered "Magic Wand" feature that rewrites vague user prompts into precise analytical questions.

---

## 🛠️ Tech Stack

### **Backend**
* **Framework:** FastAPI (Python)
* **AI Orchestration:** LangChain v0.1 (New `create_agent` architecture)
* **LLM:** OpenAI GPT-4o
* **Vector Store:** FAISS (for Schema RAG)
* **Database:** SQLite (`retail.db`)
* **ORM:** SQLAlchemy

### **Frontend**
* **Framework:** React (Vite)
* **Styling:** Tailwind CSS
* **Visualization:** Recharts
* **Utilities:** `react-markdown`

---

## 🚀 Local Installation & Setup

Follow these steps to run the project locally on your machine.

### 1. Prerequisites
* Python 3.10 or higher
* Node.js and npm
* An [OpenAI API Key](https://platform.openai.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/Ayan-004/SQL_Query_Buddy.git
cd SQL_Query_Buddy
```

### 3. Backend Setup
1. Navigate to the root directory.
2. Create and activate a virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```
3. Install Python dependencies:
```bash
pip install -r requirements.txt
```
4. Set up your environment variables:
* Create a file named .env in the root directory.
* Add your API key:
```bash
OPENAI_API_KEY="sk-your-actual-openai-key-here"
```
5. (Optional) Reset the Database:
* The repo comes with a pre-filled retail.db. If you want to reset it:
```bash
python setup_db.py
python create_rag_index.py
```
6. Start the Server:
```bash
python main.py
```
*The server will start at http://localhost:8000*

### 4. Frontend Setup
1. Open a new terminal window.
2. Navigate to the frontend folder:
```bash
cd frontend
```
3. Install dependencies:
```bash
npm install
```
4. Start the React app:
```bash
npm run dev
```
*The app will open at http://localhost:5173*

---

## 💡 How to Use
1. Ask a Question: Type a question into the chat bar.
* Example: "What are the total sales by product category?"
2. View Insights: The AI will generate the SQL, run it, and explain the results.
3. See Charts: If the data allows, a dynamic interactive chart will appear.
4. Refine: If your question is vague (e.g., "sales info"), click the Magic Wand icon to let AI rewrite it for you.
5. Follow Up: Say "Yes" to the AI's suggested follow-up question to dive deeper.
  
### 🧪 Example Scenarios to Test

| Scenario | User Prompt | Expected Outcome |
| :--- | :--- | :--- |
| **Top Rankings** | "Show me the top 5 customers by total spend." | Explanation, SQL, Results, Insight + **Bar Chart**. |
| **Category Comparison** | "What is the total sales revenue per product category?" | Explanation, SQL, Results, Insight + **Bar Chart**. |
| **Time Grouping** | "Show me total sales grouped by month for 2024." | Explanation, SQL, Results, Insight + **Bar Chart**. |
| **Single Value** | "What was the total revenue for the entire year of 2024?" | Explanation, SQL, Results, Insight (**No Chart**). |
| **Memory** | *After the category query:* "Which products sold best in the top category?" | Explanation, SQL, Results, Insight + **Bar Chart**. |

---

## 📂 Project Structure

```text
sql-query-buddy/
├── Database/
│   └── retail.db           # The SQLite database file
├── faiss_index/            # The vector store for RAG schema search
├── frontend/               # React frontend code
│   ├── src/
│   │   ├── App.jsx         # Main UI logic & BarChart rendering
│   │   └── main.jsx        # Entry point
├── main.py                 # FastAPI Backend & LangChain Agent
├── setup_db.py             # Script to seed database
├── create_rag_index.py     # Script to embed schema
└── requirements.txt        # Python dependencies
```

---

## 🏆 Acknowledgements
Developed by [Ayan Shaikh] for the Codecademy Generative AI Bootcamp. Special thanks to the instructors and the open-source community behind LangChain and Recharts.

---

*Note for Instructors/Reviewers: If running locally, please ensure you have a valid OpenAI API Key with credits available.*
