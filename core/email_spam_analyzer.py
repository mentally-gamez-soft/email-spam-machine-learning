"""Define the class and members to train a classifier ML for spam/ham emails."""

import joblib
import matplotlib.pyplot as plt
import nltk
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from wordcloud import WordCloud

from core.utils.data_sanitizer import DataSanitizer


class EmailSpamAnalyzer:
    """The api that will be used to train emails spam and ham."""

    def __init__(
        self, emails_filename: str, download_libraries: bool = False
    ) -> None:
        """Initialize the ml model trainer.

        Args:
            emails_filename (str): the dataset file to train the model.
        """
        self.df = pd.read_csv(emails_filename)
        self.data_sanitizer = DataSanitizer(self.df["EmailText"].str)
        self.df["length"] = self.df.EmailText.str.len()
        self.SVM = None
        self.tf_vec = None
        self.features = None
        self.model_accuracy_score = None
        self.y_test = None
        self.y_pred = None
        if download_libraries:
            self.__setup_nltk()

    def __setup_nltk(self):
        """Set the list of nltk libraries."""
        nltk.download("stopwords")
        nltk.download("wordnet")
        nltk.download("punkt")
        nltk.download("averaged_perceptron_tagger")

    def display_ratio_non_spam_email(self):
        """Display the percentage of non spam emails in the dataset."""
        print(
            "The ratio for non spam email is: ",
            round(
                len(self.df[self.df["Label"] == 0]) / len(self.df["Label"]), 2
            )
            * 100,
            "%",
        )

    def display_ratio_spam_email(self):
        """Display the percentage of spam emails in the dataset."""
        print(
            "The ratio for spam email is: ",
            round(
                len(self.df[self.df["Label"] == 1]) / len(self.df["Label"]), 2
            )
            * 100,
            "%",
        )

    def display_classification_report(self):
        """Display a report of classification."""
        print("<<<<<<<<<<<<<<   Classification Report  >>>>>>>>>>>>>>>")
        print(classification_report(self.y_test, self.y_pred))

    def display_model_accuracy_score(self):
        """Display the accuracy of the model."""
        print("<<<<<<<<<<<<<<   Accuracy Score  >>>>>>>>>>>>>>>")
        print("Final score: ", self.model_accuracy_score)

    def display_data_length_info(self):
        """Display the infos about the dataset before and after data sanitizing."""
        self.df["clean_length"] = self.df.EmailText.str.len()
        original_length = self.df.length.sum()
        cleaned_length = self.df.clean_length.sum()
        # print(df.head())
        print("Original data length:", original_length)
        print("Cleaned data length:", cleaned_length)
        print("Total words removed:", (original_length - cleaned_length))

    def display_all_messages(self):
        """Display all the possible information."""
        self.display_data_length_info()
        self.display_ratio_non_spam_email()
        self.display_ratio_spam_email()
        self.display_model_accuracy_score()
        self.display_classification_report()

    def graph_display_number_of_labels(self):
        """Display a chart comparison between spam and ham."""
        plt.figure(figsize=(6, 4))
        sns.countplot(self.df["Label"], palette="Reds")
        plt.title("Counting the number of labels", fontsize=15)
        plt.xticks(rotation="horizontal")
        plt.show()
        print(self.df.Label.value_counts())

    def graph_display_message_distribution_before_data_sanitizing(self):
        """Display charts of dataset before sanitizing data."""
        f, ax = plt.subplots(1, 2, figsize=(15, 8))
        sns.distplot(
            self.df[self.df["Label"] == 1]["length"],
            bins=20,
            ax=ax[0],
            label="Spam Message Distribution before data sanitizing",
            color="r",
        )
        ax[0].set_xlabel("spam message length before data sanitizing")
        ax[0].legend()

        sns.distplot(
            self.df[self.df["Label"] == 0]["length"],
            bins=20,
            ax=ax[1],
            label="No Spam Message Distribution before data sanitizing",
            color="b",
        )
        ax[1].set_xlabel("No spam message length before data sanitizing")
        ax[1].legend()

        plt.show()

    def graph_display_message_distribution_after_data_sanitizing(self):
        """Display charts of dataset after sanitizing data."""
        f, ax = plt.subplots(1, 2, figsize=(15, 8))
        sns.distplot(
            self.df[self.df["Label"] == 1]["clean_length"],
            bins=20,
            ax=ax[0],
            label="Spam Message Distribution after data sanitizing",
            color="y",
        )
        ax[0].set_xlabel("spam message length after data sanitizing")
        ax[0].legend()

        sns.distplot(
            self.df[self.df["Label"] == 0]["clean_length"],
            bins=20,
            ax=ax[1],
            label="No Spam Message Distribution after data sanitizing",
            color="g",
        )
        ax[1].set_xlabel("No spam message length after data sanitizing")
        ax[1].legend()

        plt.show()

    def display_wordcloud_for_spam_emails(self):
        """Display a wordcloud of the words defining a spam."""
        spams = self.df["EmailText"][self.df["Label"] == 1]

        spam_cloud = WordCloud(
            width=1024, height=768, background_color="white", max_words=500
        ).generate("".join(spams))
        plt.figure(figsize=(11, 9), facecolor="b")
        plt.imshow(spam_cloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def display_wordcloud_for_non_spam_emails(self):
        """Display a wordcloud of the words defining a ham."""
        no_spams = self.df["EmailText"][self.df["Label"] == 0]

        no_spam_cloud = WordCloud(
            width=1024, height=768, background_color="white", max_words=500
        ).generate("".join(no_spams))
        plt.figure(figsize=(11, 9), facecolor="b")
        plt.imshow(no_spam_cloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        plt.show()

    def display_confusion_matrix(self):
        """Display the 4 quadrants confusion matrix of real/false positive."""
        conf_mat = confusion_matrix(self.y_test, self.y_pred)
        ax = plt.subplot()
        sns.heatmap(
            conf_mat, annot=True, ax=ax, linewidths=5, linecolor="g", center=0
        )
        ax.set_xlabel("predicted labels")
        ax.set_ylabel("True labels")
        ax.set_title("Confusion Matrix")
        ax.xaxis.set_ticklabels(["not spam", "spam"])
        ax.yaxis.set_ticklabels(["not spam", "spam"])
        plt.show()

    def __remove_stop_words(self):
        from nltk.corpus import stopwords

        stopwords = set(
            stopwords.words("english")
            + ["u", "ur", "4", "2", "im", "dont", "doin", "ure", "ü"]
        )
        self.df["EmailText"] = self.df["EmailText"].apply(
            lambda x: " ".join(
                term for term in x.split() if term not in stopwords
            )
        )

    def sanitize_data(self):
        """Sanitize the dataset with a set of rules."""
        self.df["EmailText"] = self.data_sanitizer.sanitize_web_url(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_email(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_currency(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_leading_whitespace(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_number(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_phonenumber(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_punctuation(
            overwright_text=True
        )
        self.df["EmailText"] = (
            self.data_sanitizer.sanitize_trailing_whitespace(
                overwright_text=True
            )
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_whitespace(
            overwright_text=True
        )
        self.df["EmailText"] = self.data_sanitizer.sanitize_font(
            overwright_text=True
        )
        self.__remove_stop_words()

    def generate_model(self):
        """Create the model."""
        self.tf_vec = TfidfVectorizer()
        self.SVM = SVC(C=1.0, kernel="linear", degree=3, gamma="auto")
        self.features = self.tf_vec.fit_transform(self.df["EmailText"])

    def train_model(self):
        """Train our model."""
        x = self.features
        y = self.df["Label"]

        x_train, x_test, y_train, self.y_test = train_test_split(
            x, y, random_state=42
        )
        self.SVM.fit(x_train, y_train)
        self.y_pred = self.SVM.predict(x_test)
        self.model_accuracy_score = accuracy_score(self.y_test, self.y_pred)

    def save_model(
        self, filename: str = "email_spam_detector_model.joblib"
    ) -> bool:
        """Store our model."""
        if filename:
            joblib.dump(
                self.SVM, "core/machine_learning/ml_model_export/" + filename
            )
            joblib.dump(
                self.tf_vec,
                "core/machine_learning/ml_model_export/tf_vectorizer.joblib",
            )
            return True
        else:
            return False


# email_spam_analyzer = EmailSpamAnalyzer('core/machine_learning/data/spam_test.csv')
# email_spam_analyzer.sanitize_data()
# email_spam_analyzer.display_data_length_info()
# email_spam_analyzer.graph_display_number_of_labels()
# email_spam_analyzer.graph_display_message_distribution_before_data_sanitizing()
# email_spam_analyzer.graph_display_message_distribution_after_data_sanitizing()
# email_spam_analyzer.display_wordcloud_for_spam_emails()
# email_spam_analyzer.display_wordcloud_for_non_spam_emails()
# email_spam_analyzer.generate_model()
# email_spam_analyzer.train_model()
# email_spam_analyzer.save_model()
# email_spam_analyzer.display_all_messages()
# email_spam_analyzer.display_confusion_matrix()
