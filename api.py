#Creating API end points
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.prompts import PromptTemplate
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import SemanticSimilarityExampleSelector
from langchain_core.output_parsers import StrOutputParser
from few_shots import few_shots
from prompts import in_context_prompt,few_shot_prompt
from dotenv import load_dotenv
import os
import uvicorn

# Load environment variables
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Configuring Langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Load the LLM - Gemini Pro
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

#Initilializing the output parser
output_parser = StrOutputParser()

#Defining the prompt

my_prompt = few_shot_prompt

# Define FastAPI app
app = FastAPI()

# Define request body model
class InputQuestion(BaseModel):
    question: str

#Function for generating the response based on fine tuning the LLM using few shot examples
def get_few_shot_response(input_question):
    #defining the prompt - example prompt
    example_prompt = PromptTemplate(
        input_variables=['Question','Answer'],
        template="\nQuestion: {Question}\nAnswer: {Answer}",
    )

    #Embedding the few shot examples
    embeddings=GoogleGenerativeAIEmbeddings(model='models/embedding-001')
    # creating a blob of all the sentences
    to_vectorize = [" ".join(example.values()) for example in few_shots]
    #generating a vector store: 
    vector_store=FAISS.from_texts(to_vectorize, embeddings, metadatas=few_shots)

    #Checking sematic similarity: # Helping to pull similar looking queries
    example_selector = SemanticSimilarityExampleSelector(
        vectorstore = vector_store,
        k=2, #number of examples
    )

    example_selector.select_examples({"Question": "What is the total amount of money withdrawn?"})


    PROMPT_SUFFIX = """

    Question: {input}\n

    """

    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix= my_prompt,
        suffix=PROMPT_SUFFIX,
        input_variables=['input'],
    )

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=few_shot_prompt,verbose=True)

    response = chain.run(input=input_question)
    #Printing the response
    #print(response)
    #Extracting the code bit
    python_code = response.split(": ")[1].strip("'")
    
    return python_code

#Function for ugenerate_responsesing in prompt context
def get_in_cotext_reponse(input_question):
    #getting the few shot examples
    examples = str(few_shots)
    
    my_prompt = in_context_prompt
  
    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['question','examples'],template=my_prompt)

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

    response = chain.run(question=input_question,examples=examples)

    python_code = response.split(": ")[1].strip("'")

    return python_code

#index route: Opens automaticaly on http://127.0.0.1:8000
@app.get('/')
async def index():
    return {'message':'Get Started: Chatting with your Mpesa Statements'}


# Defining the API endpoint: that listens for POST requests at the '/generate_response
@app.post("/generate_response")
async def generate_response(input_question: InputQuestion):
    code = get_in_cotext_reponse(input_question.question)
    return {"code": code}

#Run with: uvicorn api:app --reload