from fastapi import FastAPI
import ollama
from fastapi.responses import FileResponse  
from fpdf import FPDF  
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain_community.llms.ollama import Ollama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from PDF import PDF

CHROMA_PATH = "Data/Chroma"
RAW_PROMPT =  PromptTemplate.from_template(
    """  
    You are a technical assistant specializing in creating Letters of Intent (LOIs)   
    Your task is to generate a new LOI based on the user's query and the existing LOIs stored in our database.  
      
    Here are the steps you should follow:  
  
    1. Identify the name of the user company from the input.  
    2. The name of the other company involved in the LOI will be provided in the user's input.  
    3. Use the existing LOIs to understand the writing style and structure. Make sure the new LOI follows the same pattern.  
  
    Below is an example of an existing LOI:  
    ---  
    {context}  
    ---  
  
    Now, based on the user's input, create a new LOI. Make sure to maintain the same writing style and structure.   
    The user's input is: "{input}"  
      
    Please generate the new LOI below. Return only the text of the LOI without any additional text or introductions:   
    """
) 

app = FastAPI()
cached_llm = Ollama(model="mistral")

@app.post("/generate")
def generate(prompt: str):
    embedding = FastEmbedEmbeddings()
    db = Chroma(
        persist_directory=CHROMA_PATH, embedding_function=embedding
    )
    retriever = db.as_retriever(
        search_kwargs={"k": 3}
        )
    document_chain = create_stuff_documents_chain(cached_llm, RAW_PROMPT)
    chain = create_retrieval_chain(retriever, document_chain)

    response = chain.invoke({"input": prompt})
    loi_text = response["answer"]
    pdf_path = generate_pdf(loi_text) 
    return FileResponse(pdf_path, media_type='application/pdf', filename='generated_loi.pdf')

    #response_answer = {"answer": response["answer"]}
    #return response_answer

def generate_pdf(text: str, filename: str = "generated_loi.pdf") -> str:  
    pdf = PDF()  
    pdf.add_page()  
    pdf.set_auto_page_break(auto=True, margin=15)  
    pdf.set_font("Arial", size=12)  
    pdf.multi_cell(0, 10, text)  
    pdf.output(filename)  
    return filename 