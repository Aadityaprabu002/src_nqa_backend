import streamlit as st
import requests
import base64


def decode_image(image_base64):
    # Decode base64 image and display
    image_bytes = base64.b64decode(image_base64)
    return image_bytes


def process_pdf(file):
    # Define the URL of the FastAPI server endpoint to process PDF
    url = "http://127.0.0.1:8000/process/"

    # Send a POST request to the server with the PDF file
    files = {"file": file}
    response = requests.post(url, files=files)

    if "processed_message" in st.session_state:
        del st.session_state["processed_message"]
    if "processed_error" in st.session_state:
        del st.session_state["processed_error"]

    # Check if the request was successful
    print(response.json())
    if response.status_code == 200:
        if response.json()["status"] == "success":
            st.session_state["processed_message"] = response.json()["message"]
        else:
            st.session_state["processed_error"] = response.json()["message"]
    else:
        st.session_state["processed_error"] = "Failed to load predict from the server."


def get_answer(question, filename):
    # Define the URL of the FastAPI server endpoint to get answer
    request = {"question": question, "filename": filename}
    url = f"http://localhost:8000/answer/"

    # Send a GET request to the server with the question
    response = requests.post(url, json=request)
    # Check if the request was successful and return the response
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get answer from the server.")


def post_relevance():
    relevance_list = st.session_state.relevant_score_list
    question = st.session_state.question
    relevant_article_id_list = st.session_state.relevant_article_id_list

    request = {
        "relevance_list": relevance_list,
        "question": question,
        "relevant_article_id_list": relevant_article_id_list,
    }
    url = f"http://localhost:8000/relevance/"

    response = requests.post(url, json=request)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        st.error("Failed to post relevance.")


def get_predicts():
    url = f"http://localhost:8000/predicts"

    # Send a GET request to the server with the question
    response = requests.get(url)

    # Check if the request was successful and return the response
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get previous predicts from the server.")
        return []


def load_previous_database():
    st.session_state["processed_message"] = "Previous database loaded successfully."
    return


def main():
    st.title("📰 Newspaper Question Answering")
    if "current_result_index" not in st.session_state:
        st.session_state.current_result_index = 0
    if "articles" not in st.session_state:
        st.session_state.articles = []
    if "relevant_score_list" not in st.session_state:
        st.session_state.relevant_score_list = []
    if "question" not in st.session_state:
        st.session_state.question = ""

    if "relevant_article_id_list" not in st.session_state:
        st.session_state.relevant_article_id_list = []

    use_previous = st.checkbox("Use previous database")

    uploaded_file = None
    filename = None
    if not use_previous:
        uploaded_file = st.file_uploader(
            "Upload a newspaper article (PDF)",
            type=".pdf",
        )
        if uploaded_file is not None:
            filename = uploaded_file.name

    answer = None
    if uploaded_file is not None or use_previous:
        if use_previous:
            load_previous_database()
        elif st.button(
            "Process",
            key="button_process",
        ):
            st.session_state.process_button_disabled = False
            if uploaded_file:
                with st.spinner("Processing PDF..."):
                    process_pdf(uploaded_file)

        if "processed_message" in st.session_state:
            st.success(st.session_state["processed_message"])

        if "processed_error" in st.session_state:
            st.error(st.session_state["processed_error"])

        question = st.text_input(
            "Ask something from the newspaper article",
            placeholder="e.g., Who did what?",
        )

        st.session_state.question = question

        ask_button = st.button("Ask")
        if ask_button and question:
            if len(question.split(" ")) < 5:
                st.error("Question is too short. Please ask a detailed question.")
                return

            with st.spinner("Fetching Answers"):
                answer = get_answer(question, filename)
                if "error" in answer:
                    st.error(answer["error"])
                else:
                    st.session_state.articles = answer["articles"]
                    st.session_state.relevant_score_list = [
                        "UnAnswered" for _ in answer["articles"]
                    ]
                    st.session_state.relevant_article_id_list = [
                        article["id"] for article in answer["articles"]
                    ]
                    st.session_state.current_result_index = -1

    if len(st.session_state.articles) > 0:

        articles = st.session_state.articles

        columns = st.columns(len(articles) + 2)

        for i in range(len(columns)):
            if i == 0 or i == len(columns) - 1:
                with columns[i]:
                    st.write("")
            else:
                with columns[i]:
                    if st.button(
                        "Result " + str(i),
                        key="result_button_" + str(i),
                        help="Click to go to Result " + str(i),
                    ):
                        st.session_state.current_result_index = i - 1

        if st.session_state.current_result_index != -1:
            index = st.session_state.current_result_index

            left, right = st.columns([2, 1])

            # Display text aligned towards the right in the second column
            with right:
                st.write(
                    "Result:",
                    st.session_state.current_result_index + 1,
                    "out of",
                    len(articles),
                )

            st.subheader("Answer:")
            st.write(articles[index]["extracted-sentence"])
            st.subheader("Answer related information:")

            st.write(articles[index]["extracted-answer"])
            st.subheader("Article image extracted from newspaper:")
            st.image(decode_image(articles[index]["image"]))
            st.subheader("Additional Information:")
            st.write("Title:")
            st.write(articles[index]["title"])
            st.write("Body:")
            st.write(articles[index]["body"])
            st.write("Author:")
            st.write(articles[index]["author"])
            st.write("Page Number:", articles[index]["page-index"])
            if st.session_state.relevant_score_list[index] == "UnAnswered":
                p1, l, r, p2 = st.columns(4)
                with p1:
                    st.write("")
                with p2:
                    st.write("")
                with l:
                    if st.button("Relevant", key="relevant_button_" + str(index)):
                        st.session_state.relevant_score_list[index] = "Relevant"
                with r:
                    if st.button("Irrelevant", key="irrelevant_button_" + str(index)):
                        st.session_state.relevant_score_list[index] = "Irrelevant"

            p1, b, p2 = st.columns(3)
            print(st.session_state.relevant_score_list)
            with p1:
                st.write("")
            with p2:
                st.write("")
            with b:
                if st.button("Submit relevance"):
                    response = post_relevance()
                    if "error" in response:
                        st.error(response["error"])
                    else:
                        st.success(response["message"])

    else:
        st.write("No articles to display.")


def get_predicts():
    # Define the URL of the FastAPI server endpoint to get the list of predicts
    url = "http://localhost:8000/predicts"

    # Send a GET request to the server
    response = requests.get(url)

    # Check if the request was successful and return the response
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to get predicts from the server.")


if __name__ == "__main__":
    main()
