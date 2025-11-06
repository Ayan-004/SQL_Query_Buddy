import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_core.tools import create_retriever_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
# from langchain.agents import create_agent


load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set. Please set it as an environment variable")
    exit()
    
print("Initializig core components...")
llm = ChatOpenAI(model='gpt-4o', temperature=0)
embeddings = OpenAIEmbeddings()

db = SQLDatabase.from_uri("sqlite:///retail.db")

try:
    vectorstore = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )
except ImportError:
    print("FAISS is not installed. Run 'pip install faiss-cpu'")
    exit()
except Exception as e:
    print(f"Could not load FAISS index. Did you run 'create_rag_index.py'? Error: {e}")
    exit()
    
retriever = vectorstore.as_retriever()
print("Components initialized successfully.")

schema_retriever_tool = create_retriever_tool(
    retriever,
    "schema_search",
    "Use this tool to find relevent table and column information (schema) before generating a SQL query. Pass a natural language question as the query."
)

sql_query_tool = QuerySQLDatabaseTool(db=db)

tools = [schema_retriever_tool, sql_query_tool]

system_prompt = """
You are an expert data analyst AI named 'SQL Query Buddy'.
Your goal is to help users get insights from a retail database.
You MUST follow this 4-step process for every user question:

1.  **Retrieve Schema:** Use the 'schema_search' tool. This is mandatory.
    You must use this tool to get relevant table names, column descriptions, and join info.

2.  **Generate SQL:** Based ONLY on the retrieved schema context, generate an
    accurate SQL query to answer the user's question.

3.  **Execute Query:** Use the 'QuerySQLDataBaseTool' to run the SQL query.
    You will get back the raw results.

4.  **Answer the User:** Format your final response as a single, complete
    message. Do NOT output the steps.
    Your response MUST be structured using these exact 4 parts:

    **Explanation:**
    [cite_start](Provide a beginner-friendly explanation of the SQL query [cite: 33])
    
    **SQL:**
    ```sql
    [cite_start](The generated SQL query [cite: 41])
    ```
    
    **Raw Results:**
    ```
    [cite_start](The raw query results from the tool [cite: 42])
    ```
    
    **AI-Driven Insight:**
    (This is the most important part. Analyze the raw results and provide a
    [cite_start]concise, human-like insight[cite: 26].
    Do not just repeat the numbers. Interpret them.
    For example: "Sales in California grew 15%" or
    "Electronics is the dominant category, accounting for 40%/ of sales.")

[cite_start]Remember: Maintain conversation history for follow-ups[cite: 37].
"""

prompt = ChatPromptTemplate([
    ("system", system_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# llm_with_tools = llm.bind_tools(tools)

agent = create_openai_tools_agent(llm, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

app = FastAPI(
    title="SQL Query Buddy API",
    description="API for the Codecademy GenAI Bootcamp Contest Project"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    question: str
    chat_history: List[Tuple[str, str]]
    
class ChatResponse(BaseModel):
    answer: str
    chat_history: List[Tuple[str, str]]
    
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(f"Request received: {request.question}")
    
    history_messages = []
    for human, ai in request.chat_history:
        history_messages.extend([
            HumanMessage(content=human),
            AIMessage(content=ai)
        ])
        
    try:
        response = agent_executor.invoke({
            "input": request.question,
            "chat_history": history_messages
        })
        
        ai_answer = response["output"]
        
        updated_history = request.chat_history + [(request.question,  ai_answer)]
        
        return ChatResponse(answer=ai_answer, chat_history=updated_history)
    
    except Exception as e:
        print(f"Error during agent invocation: {e}")
        return ChatResponse(
            answer=f"Sorry, an error occurred while processing your request: {e}",
            chat_history=request.chat_history
        )
        
@app.get("/")
def root():
    return {"message": "SQL Query Buddy API is running!"}

if __name__ == "__main__":
    print("Starting FastAPI server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)