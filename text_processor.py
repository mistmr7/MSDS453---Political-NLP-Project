import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd


# Download stopwords if you haven't already
nltk.download("stopwords")
nltk.download("punkt_tab")

df = pd.read_excel("RedditExcelOutput.xlsx")

conservative_texts = df[df["Political Leaning"] == "Conservative"]["Comment Text"]
liberal_texts = df[df["Political Leaning"] == "Liberal"]["Comment Text"]

# Training data
documents_A = [item for item in conservative_texts if isinstance(item, str)]
documents_B = [item for item in liberal_texts if isinstance(item, str)]


# Combine data and labels
documents = documents_A + documents_B
labels = [0] * len(documents_A) + [1] * len(documents_B)  # 0 = Class A, 1 = Class B

# Preprocess documents
stop_words = set(stopwords.words("english"))


def preprocess_text(text):
    try:
        tokens = word_tokenize(text.lower())
        filtered_tokens = [
            word for word in tokens if word.isalnum() and word not in stop_words
        ]
        return " ".join(filtered_tokens)
    except AttributeError:
        pass


processed_documents = [preprocess_text(doc) for doc in documents]
# print(processed_documents)
# Vectorize using TF-IDF
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_documents)

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, labels, test_size=0.2, random_state=0
)

# Initialize the model
model = LogisticRegression()

# Train the model
model.fit(X_train, y_train)

test_docs_df = pd.read_csv("corpus.csv")
test_text_series = test_docs_df["text"]


def calculate_prediction_accuracy(predictions, con_length, lib_length):
    list_preds = [int(pred) for pred in predictions]
    value = 0
    for i in range(len(list_preds[0:con_length])):
        if list_preds[i] == 0:
            value += 1
    print(
        f"Conservative documents predicted correctly {round(value/con_length * 100, 2)}%\n"
    )
    value2 = 0
    for i in range(0, len(list_preds[con_length:])):
        if list_preds[i] == 1:
            value += 1
            value2 += 1
    print(f"Liberal documents predicted correctly {round(value2/lib_length * 100, 2)}%")
    return f"{round(value / len(list_preds) * 100, 2)} %"


# New test documents
new_documents = [item for item in test_text_series if isinstance(item, str)]

# Preprocess and vectorize
new_processed_docs = [preprocess_text(doc) for doc in new_documents]
new_X = vectorizer.transform(new_processed_docs)

con_length = len(
    test_docs_df[test_docs_df["political_leaning"] == "Conservative"].index
)
lib_length = len(test_docs_df[test_docs_df["political_leaning"] == "Liberal"].index)
# Predict
predictions = model.predict(new_X)
print("Predictions:", predictions)
print(
    f"\nLogistic Regression Prediction Accuracy: {calculate_prediction_accuracy(predictions, con_length, lib_length)}"
)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy:{accuracy}")
print(
    f"\nLogistic Regression Classification Report:\n{classification_report(y_test, y_pred)}\n"
)

model = MultinomialNB()  # for Naive Bayes
# Train the model
model.fit(X_train, y_train)

test_docs_df = pd.read_csv("corpus.csv")
test_text_series = test_docs_df.text


# New test documents
new_documents = [item for item in test_text_series if isinstance(item, str)]

# Preprocess and vectorize
new_processed_docs = [preprocess_text(doc) for doc in new_documents]
new_X = vectorizer.transform(new_processed_docs)

# Predict
predictions = model.predict(new_X)
print(f"Predictions: {predictions}")
print(
    f"\nNaive Bayes Prediction Accuracy: {calculate_prediction_accuracy(predictions, con_length, lib_length)}"
)
# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy:{accuracy}")
print(f"\nNaive Bayes Classification Report:\n{classification_report(y_test, y_pred)}")


model = SVC()  # for Support Vector Machine
# Train the model
model.fit(X_train, y_train)

test_docs_df = pd.read_csv("corpus.csv")
test_text_series = test_docs_df.text


# New test documents
new_documents = [item for item in test_text_series if isinstance(item, str)]

# Preprocess and vectorize
new_processed_docs = [preprocess_text(doc) for doc in new_documents]
new_X = vectorizer.transform(new_processed_docs)

# Predict
predictions = model.predict(new_X)
print("Predictions:", predictions)
print(
    f"\nSVM Prediction Accuracy: {calculate_prediction_accuracy(predictions, con_length, lib_length)}"
)
# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate
accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy:{accuracy}")
print(f"\nSVM Classification Report:\n{classification_report(y_test, y_pred)}")
