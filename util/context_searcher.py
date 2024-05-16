from unidecode import unidecode
import nltk
from nltk.corpus import stopwords
import PyPDF2
import os
from progress_bar import ProgressBar


class ContextSearcher:
    MAX_SEARCH_WORDS = 12

    def __init__(self):

        try:
            nltk.data.find("stopwords")
        except:
            nltk.download("stopwords")

        self.stop_words = set(stopwords.words("english"))
        self.context_path = ""
        print("ContextSearcher intialized successfully.")

    def __extract_context(self, pdf_path):
        text = ""
        with open(pdf_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            page = pdf_reader.pages[-1]
            text = page.extract_text()
        return unidecode(text)

    def __prepare_context(self, context):

        def filter_empty_lines(s):
            return len(s) != 0

        def clean_lines(s):
            clean = " ".join(s.strip().split())
            return clean

        context = context.lower()
        context = context.split("\n")
        context = list(filter(filter_empty_lines, context))
        context = list(map(clean_lines, context))
        return context

    def __save_context(self, context, save_path):
        content = ""
        for line, sentence in enumerate(context):
            content += f"{sentence}\n"

        with open(save_path, "w") as file:
            file.write(content)

    def __prepare_search(self, search):

        def clean_search(s):
            clean = " ".join(s.strip().split())
            return clean

        search = search.lower()
        search = search.split()
        search = list(map(clean_search, search))
        return search

    def __search_in_context(self, search, context, start_from=0):

        filtered_sentences = []
        sentence_match_freq = dict()
        for line in range(0, len(context)):
            sentence = context[line].lower()
            for word in search:
                if word not in self.stop_words and sentence.find(word) != -1:
                    filtered_sentences.append((line, sentence))
                    sentence_match_freq[sentence] = 0
                    break

        for sentence, _ in sentence_match_freq.items():
            for word in search:
                if word in sentence:
                    sentence_match_freq[sentence] += 1

        result_sentence = ""
        max_word_hit = 0
        for sentence, word_hit in sentence_match_freq.items():

            if word_hit > max_word_hit:
                max_word_hit = word_hit
                result_sentence = sentence

        result = [None, None]
        for filtered_sentence in filtered_sentences:
            if filtered_sentence[1] == result_sentence:
                result = filtered_sentence
                break

        return result

    def extract_content(self, context, start_result, end_result, include_lines=1):
        return " ".join(
            context[start_result[0] - include_lines : end_result[0] + include_lines + 1]
        ).lower()

    def process_context(self, current_predict_folder_path):
        progress_bar = ProgressBar(
            len(os.listdir(current_predict_folder_path)), "Processing context setup"
        )
        for current_page_folder_name in os.listdir(current_predict_folder_path):
            progress_bar.update()
            current_page_folder_path = (
                f"{current_predict_folder_path}/{current_page_folder_name}"
            )

            current_page_folder_pdf_path = f"{current_page_folder_path}/pdf.pdf"

            context = self.__extract_context(current_page_folder_pdf_path)

            context = self.__prepare_context(context)

            current_page_folder_context_path = f"{current_page_folder_path}/context.txt"

            self.__save_context(context, current_page_folder_context_path)

        progress_bar.complete()

    def search(self, content, context):

        if content == "":
            return

        content = content.split(" ")

        start_search = self.__prepare_search(
            " ".join(content[0 : self.MAX_SEARCH_WORDS])
        )
        n = len(content)
        end_search = self.__prepare_search(" ".join(content[n - 13 : n]))

        progress_bar = ProgressBar(2, "Context searching")

        start_result = self.__search_in_context(start_search, context)
        progress_bar.update()
        end_result = self.__search_in_context(
            end_search, context, start_from=start_result[0]
        )
        progress_bar.update()
        progress_bar.complete()

        return (start_result, end_result)
