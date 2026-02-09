from typing import Optional
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from src.core.config import settings


model = OllamaLLM(model=settings.LLM_MODEL_NAME)

def answer_prompt(question: str, context: Optional[str] = ""):
    template = """
        Ты русскоязычный помощник. Используй предоставленный ниже контекст для ответа на вопрос пользователя.
        
        Если не можешь ответить, честно скажи:  
        "Извините, у меня нет точной информации по этому вопросу."
        
        Отвечай строго на русском языке. Не используй английские слова. Избегай домыслов.
                
        Контекст: {context}
        
        Вопрос пользователя: {question}
        
        Ответ:
        """

    prompt = ChatPromptTemplate.from_template(template, model=model)

    chain = prompt | model

    result = chain.invoke({"context": context, "question": question})

    return result
