from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
import json
import base64

sys.path.append("./model")
sys.path.append("./util")
sys.path.append("./trained_model")
sys.path.append("./qa_engine")

from qa_engine import *
from trained_model import *
from util import *
from app_config import config

from newspaper_query_assistant import NewspaperQueryAssistant


current_filename = ""
newspaper_query_assistant = NewspaperQueryAssistant()


os.makedirs("input", exist_ok=True)


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.post("/answer/")
async def answer(request: Request):
    global current_filename
    request_data = await request.json()
    question = request_data["question"]

    # if filename != current_filename:
    #     return {"error": "Please process the PDF first"}

    answers, documents = newspaper_query_assistant.answer(question)
    articles = []
    for index, document in enumerate(documents):

        page_content = document.page_content

        title = page_content.split("Body:")[0].split("Title:")[1]
        body = page_content.split("Body:")[1].split("Author:")[0]
        author = page_content.split("Author:")[1]
        image_path = document.metadata["article-image-path"]
        page_index = document.metadata["article-page-index"]
        id = document.metadata["article-id"]
        image = None

        with open(image_path, "rb") as file:
            image = file.read()

        image_base64 = base64.b64encode(image).decode("utf-8")

        article = {
            "title": title,
            "body": body,
            "author": author,
            "pageIndex": page_index,
            "image": image_base64,
            "extractedSentence": answers[index]["sentence"],
            "extractedAnswer": answers[index]["answer"],
            "id": id,
        }
        articles.append(article)

    response = {"articles": articles}

    return response


@app.post("/process/")
async def process(file: UploadFile = File(...)):
    global current_filename
    if file.filename.endswith(".pdf"):

        with open("input/received.pdf", "wb") as f:
            current_filename = file.filename
            f.write(await file.read())

        progress_bar = ProgressBar(1, "Processing PDF")
        newspaper_query_assistant.process_pdf("input/received.pdf")
        progress_bar.update()
        progress_bar.complete()

        return {"message": "File processed successfully", "status": "success"}
    else:
        return {
            "message": "Unsupported file format. Please upload a PDF file",
            "status": "failed",
        }


# @app.post("/load")
# async def load(request: Request):

#     request_data = await request.json()
#     predict = request_data["predict"]
#     global current_filename
#     progress_bar = ProgressBar(1, "Loading PDF")
#     loaded = newspaper_query_assistant.load_newspaper_database(predict)
#     progress_bar.update()
#     progress_bar.complete()
#     current_filename = predict
#     if loaded:
#         return {
#             "message": f"{predict} loaded successfully",
#             "status": "success",
#         }
#     return {
#         "message": f"{predict} not found",
#         "status": "failed",
#     }


@app.get("/predicts")
def predicts():
    return {"predicts": os.listdir(config["RootOutputPath"])}


@app.post("/relevance")
async def relevance(request: Request):
    request_data = await request.json()
    if "relevance_list" not in request_data:
        return {"error": "Relevance list not found"}

    relevance_list = request_data["relevance_list"]
    relevant_article_id_list = request_data["relevant_article_id_list"]
    question = request_data["question"]

    newspaper_query_assistant.add_relevance_score(
        question, relevance_list, relevant_article_id_list
    )

    return {"message": "Successfully added relevance score"}
