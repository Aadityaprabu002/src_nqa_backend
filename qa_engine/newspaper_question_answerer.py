from transformers import pipeline
from util.progress_bar import ProgressBar
from langchain_core.documents import Document
from chromadb import GetResult


class NewspaperQuestionAnswerer:

    def __init__(self):
        self.model = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            tokenizer="deepset/roberta-base-squad2",
        )
        print("ArticleQuestionAnswering model loaded successfully.")

    def extract_answer_from_document(self, question, document: Document):

        progress_bar = ProgressBar(total=3, description="Extracting answer")

        page_conent = document.page_content
        qa_input = {"context": page_conent, "question": question}
        result = self.model(qa_input)

        progress_bar.update()

        left = result["start"]
        right = result["end"]

        progress_bar.update()

        while left >= 0:
            if page_conent[left] == ".":
                break
            left -= 1

        while right < len(page_conent):
            if page_conent[right] == ".":
                break
            right += 1

        sentence = page_conent[left + 1 : right + 1]
        progress_bar.update()
        progress_bar.complete()
        answer = {"answer": result, "sentence": sentence}
        return answer

    def extract_answer_from_context(self, question, context):
        document = Document(page_content=context)
        answer = self.extract_answer_from_document(question, document)
        return answer
