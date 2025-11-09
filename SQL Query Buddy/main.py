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
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langchain_core.tools import create_retriever_tool
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_agent


load_dotenv()
if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set. Please set it as an environment variable")
    exit()
    
print("Initializig core components...")
llm = ChatOpenAI(model='gpt-4o', temperature=0)
embeddings = OpenAIEmbeddings()

db = SQLDatabase.from_uri("sqlite:///Database/retail.db")

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

agent = create_agent(llm, tools, system_prompt=system_prompt)

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
    
class EnhanceRequest(BaseModel):
    prompt: str
    
class ChatResponse(BaseModel):
    answer: str
    chat_history: List[Tuple[str, str]]
    
@app.post("/enhance-prompt")
async def enhance_prompt(request: EnhanceRequest):
    print(f"Refining prompt: {request.prompt}")
    
    enhance_system_prompt = """
    You are an expert AI Data Analyst assistant. Your specific task is to take a short, vague, or incomplete natural-language query from a user about a **retail database** and rewrite it into a clear, specific, and unambiguous question that a data analysis model can effectively answer.

    **Core Enhancement Rules:**
    1.**Infer Metrics:** If a metric is missing, add the most logical one. (e.g., "top customers" -> "top customers by **total sales revenue**").
    2.**Add Grouping:** If a user asks for a broad metric, add a logical grouping. (e.g.,"product sales" -> "total sales **per product category**").
    3.**Specify Timeframes:** If no timeframe is given, default to a common, relevant one.(e.g., "how are sales?" -> "What is the total sales revenue **for the last 30 days**?").
    4.**Resolve Ambiguity:** Replace vague words like "best" or "popular" with specific metrics. (e.g., "best products" -> "top 10 products by **units sold**").

    Return ONLY the single, enhanced query. Do not include any explanation, preamble, or markdown.

    Example 1:
    User: "top 5 customers"
    Enhanced: "Show me the top 5 customers by total purchase amount for the last 90 days."

    Example 2:
    User: "products sales"
    Enhanced: "What is the total sales revenue per product category for the current month?"

    Example 3:
    User: "how are we doing?"
    Enhanced: "What is the total sales revenue and total number of orders for the last 30 days compared to the previous 30 days?"

    Example 4:
    User: "most popular items"
    Enhanced: "List the top 10 products by total units sold in the last 30 days."
    """
    
    try:
        response = llm.invoke([
            HumanMessage(content=enhance_system_prompt),
            HumanMessage(content=request.prompt)
        ])
        
        enhanced_prompt = response.content
        return {"enhanced_prompt": enhanced_prompt}
    except Exception as e:
        print(f"Error enhancing prompt: {e}")
        return {"enhanced_prompt": request.prompt}
    
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    print(f"Request received: {request.question}")
    
    history_messages = []
    for item in request.chat_history:
        if isinstance(item, list) and len(item) == 2:
            human, ai = item
            history_messages.append(HumanMessage(content=human))
            history_messages.append(AIMessage(content=ai))
        
    history_messages.append(HumanMessage(content=request.question))
    
    try:
        response = agent.invoke({
            "messages": history_messages
        })
        
        ai_answer = response["messages"][-1].content
        
        updated_history = request.chat_history + [[request.question,  ai_answer]]
        
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