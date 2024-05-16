from transformers import pipeline
import torch
from tqdm import tqdm
from progress_bar import ProgressBar


class ContextSummarizer:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        print("ContextSummarizer model loaded successfully.")

    def summarize(self, text):
        progress_bar = ProgressBar(total=2, description="Context Correction")
        progress_bar.update()
        summarized_text = self.summarize(
            text, max_length=40, min_length=30, do_sample=True
        )
        progress_bar.update()
        progress_bar.complete()
        return summarized_text
