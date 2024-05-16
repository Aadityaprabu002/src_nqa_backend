from gramformer import Gramformer
import torch
from tqdm import tqdm
from progress_bar import ProgressBar


class ContextCorrector:
    def __init__(self):
        self.__set_seed(1212)
        self.gf = Gramformer(models=1, use_gpu=False)

        print("ContextCorrector model loaded successfully.")

    def __set_seed(self, seed):
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(seed)

    def correct(self, text):
        progress_bar = ProgressBar(
            total=len(text.split("\n")), description="Context Correction"
        )
        corrected_texts = []
        for text in text.split("."):
            corrected_text = list(self.gf.correct(text, max_candidates=1))
            progress_bar.update()
            corrected_texts.append(corrected_text[-1])
        progress_bar.complete()
        return " ".join(corrected_texts)
