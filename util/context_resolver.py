from context_corrector import ContextCorrector
from context_searcher import ContextSearcher
from progress_bar import ProgressBar


class ContextResolver:
    def __init__(
        self, context_searcher: ContextSearcher, context_corrector: ContextCorrector
    ) -> None:
        self.context_searcher = context_searcher
        self.context_corrector = context_corrector
        print("Context Resolver intialized successfully.")
        pass

    def resolve(self, current_page_folder_path, info):
        context_path = f"{current_page_folder_path}/context.txt"
        with open(context_path, "r") as file:
            context = file.readlines()

        for i in range(len(info["articles"])):
            print("Article:", i + 1)
            article_components = dict(info["articles"][i]["article-components"])

            for component_name, component in article_components.items():
                for j, content in enumerate(component):
                    extracted_content = content["extracted-content"].strip()
                    if extracted_content == "":
                        continue

                    # print("Processing : Context searcher")
                    # start_result, end_result = self.context_searcher.search(
                    #     extracted_content, context
                    # )
                    # actual_content = ""

                    # if None not in start_result and None not in end_result:
                    #     actual_content = self.context_searcher.extract_content(
                    #         context, start_result, end_result, include_lines=1
                    #     )

                    # else:
                    # print("Context not found switching to Context Corrector")

                    actual_content = self.context_corrector.correct(extracted_content)

                    info["articles"][i]["article-components"][component_name][j][
                        "actual-content"
                    ] = actual_content.lower()

        print("Correction process finished")
