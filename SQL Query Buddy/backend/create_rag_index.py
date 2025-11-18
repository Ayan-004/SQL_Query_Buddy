import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print("OPENAI_API_KEY not set. Please set it as an environment variable")
    exit()
    
print("OpenAI API key found. Proceeding with embedding...")

schema_docs = [
    Document(
        page_content="The 'customers' table stores information about customers. It includes a unique 'customer_id' (primary key), 'name', 'email', 'region' (e.g., 'California', 'New York'), and 'signup_date'.",
        metadata={"table_name": "customers"}
    ),
    Document(
        page_content="The 'products' table contains the product catalog. It has a 'product_id' (primary key), 'name' of the product, 'category' (e.g., 'Electronics', 'Furniture', 'Software'), and 'price'.",
        metadata={"table_name": "products"}
    ),
    Document(
        page_content="The 'orders' table tracks customer purchases. It includes an 'order_id' (primary key), 'customer_id' (a foreign key linking to the 'customers' table), 'order_date', and the 'total_amount' for the order.",
        metadata={"table_name": "orders"}
    ),
    Document(
        page_content="The 'order_items' table links orders to products, showing what items were in each order. It has an 'item_id' (primary key), 'order_id' (links to 'orders'), 'product_id' (links to 'products'), the 'quantity' of the product ordered, and the 'subtotal' for that line item.",
        metadata={"table_name": "order_items"}
    ),
    Document(
        page_content="To find a customer's orders, join 'customers' and 'orders' on 'customers.customer_id = orders.customer_id'.",
        metadata={"join_info": "customers_orders"}
    ),
    Document(
        page_content="To see the products in a specific order, join 'orders' and 'order_items' on 'orders.order_id = order_items.order_id', then join 'order_items' and 'products' on 'order_items.product_id = products.product_id'.",
        metadata={"join_info": "orders_items_products"}
    ),
    Document(
        page_content="You can calculate total sales for a customer by joining 'customers' and 'orders' on their 'customer_id' and summing the 'total_amount' from the 'orders' table.",
        metadata={"query_example": "total_sales_per_customer"}
    ),
    Document(
        page_content="To find sales by product category, you must join 'products', 'order_items', and 'orders' tables. Link 'products.product_id' with 'order_items.product_id', and 'order_items.order_id' with 'orders.order_id'. Then, you can group by 'products.category' and sum 'order_items.subtotal'.",
        metadata={"query_example": "sales_by_category"}
    )
]

try:
    embedding = OpenAIEmbeddings()
    
    print("Creating FAISS vector store... This may take a moment")
    vectorstore = FAISS.from_documents(schema_docs, embedding)
    
    vectorstore.save_local("faiss_index")
    
    print("\nSuccessfully created and saved FAISS index to the 'faiss_index' folder")
    print("This folder now contain your embedded schema descriptions.")
    
except Exception as e:
    print(f"\nAn error occurred: {e}")
    print("Please ensure your OPENAI_API_KEY is correct and has a valid subscription.")