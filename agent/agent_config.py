from agents import Agent, Runner, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from vector_store import load_vectorstore
import asyncio

# 🛡️ API Key our Model
API_KEY = "your-openrouter-api-key"
BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-2.0-flash-lite-preview-02-05:free"

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)

# Agent function
async def run_agent(question):
    vectordb = load_vectorstore()
    docs = vectordb.similarity_search(question, k=2)
    context = "\n".join([doc.page_content for doc in docs])

    agent = Agent(
        name="StudyAssistant",
        instructions="Tum ek madadgar educational agent ho jo context se smart jawab deta hai.",
        model=OpenAIChatCompletionsModel(model=MODEL, openai_client=client),
    )

    result = await Runner.run(agent, f"{context}\n\nSawal: {question}")
    print(result.final_output)