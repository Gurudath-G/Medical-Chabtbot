from langchain_groq import ChatGroq
from vector_database import faiss_db
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import re

# Uncomment the following if you're NOT using pipenv
#from dotenv import load_dotenv
load_dotenv()
""""""
#Step1: Setup LLM (Use DeepSeek R1 with Groq)
llm_model=ChatGroq(model="deepseek-r1-distill-llama-70b")

#Step2: Retrieve Docs

def retrieve_docs(query):
    return faiss_db.similarity_search(query)  # Make sure to call the function

def get_context(documents):
    context = "\n\n".join([doc.page_content for doc in documents])
    return context

#Step3: Answer Question

custom_prompt_template = """
Use the pieces of information provided in the context to answer user's question.
If you dont know the answer, just say that you dont know, dont try to make up an answer. 
Dont provide anything out of the given context
Question: {question} 
Context: {context} 
Answer:
"""

def answer_query(documents, model, query):
    context = get_context(documents)
    prompt = ChatPromptTemplate.from_template(custom_prompt_template)
    chain = prompt | model
    return chain.invoke({"question": query, "context": context})

question="How can we have good mental health?"
retrieved_docs=retrieve_docs(question)
print(type(retrieved_docs))
#for doc in retrieved_docs:
#    print(doc.page_content)
ans=answer_query(documents=retrieved_docs, model=llm_model, query=question)
response=ans
if isinstance(response.content, tuple):  
    content = response.content[1]  # Extract the text part from the tuple
else:
    content = response.content
cleaned_content = re.sub(r"<think>.*?</think>\n\n", "", content, flags=re.DOTALL)

# Extract thinking process
think_content_match = re.search(r"<think>([\s\S]*?)</think>", content)
think_content = think_content_match.group(1) if think_content_match else "No thinking process available."
print("lol",think_content)
print(ans,type(ans))