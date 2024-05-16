from app_config import config
from langchain.chat_models.openai import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain


class NewspaperQuestionAnswererTry:
    def __init__(self) -> None:
        self.__model_name = "gpt-3.5-turbo"
        self.__model = ChatOpenAI(
            model_name=self.__model_name, api_key=config["OpenAIKey"]
        )
        self.__chain = load_qa_chain(llm=self.__model, chain_type="stuff", verbose=True)
        print("NewspaperQuestionAnswerer initialized successfully.")

    def answer(self, question, documents):
        answer = self.__chain.run(input_documents=documents, question=question)
        return answer
