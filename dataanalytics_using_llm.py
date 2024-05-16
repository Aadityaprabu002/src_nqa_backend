import json
from collections import defaultdict
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Load the fine-tuned model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(
    "IT-community/distilBART_cnn_news_text_classification")
model = AutoModelForSequenceClassification.from_pretrained(
    "IT-community/distilBART_cnn_news_text_classification")

# Load the JSON data
with open("newspaper_info.json", "r") as json_file:
    data = json.load(json_file)

# Get the number of labels from the model's configuration
num_labels = model.config.num_labels

# Define the label map (you may need to adjust this based on your model's label mapping)
label_map = {0: "business", 1: "entertainment",
             2: "health", 3: "news", 4: "politics", 5: "sport"}

# Function to classify text into categories using the model


def classify_text(text):
    inputs = tokenizer(text, padding=True, truncation=True,
                       return_tensors="pt")
    outputs = model(**inputs)
    predicted_class = outputs.logits.argmax().item()
    return predicted_class


# Initialize counts for each category
category_counts = defaultdict(int)

# Iterate through articles and classify each one into a category
for article in data["articles"]:
    # Concatenate title and body to form the input text
    text = article["article-title"] + " " + article["article-body"]
    # Classify the text into a category
    predicted_category = classify_text(text)
    # Increment the count for the predicted category
    category_counts[label_map[predicted_category]] += 1

# Print the counts for each category
for category, count in category_counts.items():
    print(f"{category}: {count}")
