import os
import json
from pprint import pprint
import math

path = "./feedbacks/"
feedbacks = []
for file in os.listdir(path):
    file_path = os.path.join(path, file)
    with open(file_path, "r") as f:
        feedback = json.load(f)
        feedbacks.extend(feedback)

score = 0
relevant = 0
for feedback in feedbacks:
    relevant += feedback["relevancy-list"].count(1)

print("Total number of Relevant Article:", relevant)
print("Total Question Count:", len(feedbacks))
print("Answers produced per question:", 5)
print(
    "Total number of Answers produced (5 * Total Question Count):", 5 * len(feedbacks)
)

system_accuracy = relevant / (5 * len(feedbacks))

print("Formula: Total Number of Relevant Articles / Total number of Answers produced")
print("System Accuracy:", system_accuracy)
