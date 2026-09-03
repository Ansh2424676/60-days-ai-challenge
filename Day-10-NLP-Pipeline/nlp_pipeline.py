import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# NLTK RESOURCE SETUP
# ============================================================

nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)


# ============================================================
# MODULE 1: PREPROCESSING
# ============================================================

class PreprocessingModule:
    """
    Responsible for cleaning and normalizing raw text.

    Parameters:
        lowercase (bool):
            Convert text to lowercase.

        remove_stopwords (bool):
            Remove common English stopwords.

        lemmatize (bool):
            Convert words to their base form.
    """

    def __init__(
        self,
        lowercase=True,
        remove_stopwords=True,
        lemmatize=True
    ):
        self.lowercase = lowercase
        self.remove_stopwords = remove_stopwords
        self.lemmatize = lemmatize

        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

    def transform(self, text):
        """
        Preprocess a single text string.

        Args:
            text (str): Raw input text.

        Returns:
            str: Cleaned and normalized text.

        Raises:
            TypeError:
                If input is not a string.

            ValueError:
                If input is empty, one character,
                or contains only numbers/symbols.
        """

        if not isinstance(text, str):
            raise TypeError("Input must be a string.")

        text = text.strip()

        # Edge Case 1: Empty string
        if not text:
            raise ValueError("Input cannot be empty.")

        # Edge Case 2: Single-character input
        if len(text) == 1:
            raise ValueError(
                "Input must contain more than one character."
            )

        # Edge Case 3: Numbers/symbols only
        if not re.search(r"[A-Za-z]", text):
            raise ValueError(
                "Input must contain at least one alphabetic character."
            )

        # Lowercase
        if self.lowercase:
            text = text.lower()

        # Extract alphabetic words
        tokens = re.findall(r"[a-zA-Z]+", text)

        # Remove stopwords
        if self.remove_stopwords:
            tokens = [
                word
                for word in tokens
                if word not in self.stop_words
            ]

        # Lemmatization
        if self.lemmatize:
            tokens = [
                self.lemmatizer.lemmatize(word)
                for word in tokens
            ]

        # Check if anything meaningful remains
        if not tokens:
            raise ValueError(
                "No meaningful words remain after preprocessing."
            )

        return " ".join(tokens)


# ============================================================
# MODULE 2: VECTORIZATION + SIMILARITY
# ============================================================

class VectorizerModule:
    """
    Responsible for TF-IDF vectorization and cosine similarity.

    Parameters:
        max_features (int or None):
            Maximum number of features used by TF-IDF.
    """

    def __init__(self, max_features=None):
        self.vectorizer = TfidfVectorizer(
            max_features=max_features
        )

        self.corpus_vectors = None
        self.corpus = None

    def fit(self, corpus):
        """
        Fit TF-IDF vectorizer on the document corpus.

        Args:
            corpus (list):
                List of preprocessed documents.

        Returns:
            VectorizerModule:
                Returns self for method chaining.
        """

        if not corpus:
            raise ValueError("Corpus cannot be empty.")

        self.corpus = corpus

        self.corpus_vectors = self.vectorizer.fit_transform(
            corpus
        )

        return self

    def transform(self, query):
        """
        Transform a query and calculate similarity
        against the fitted corpus.

        Args:
            query (str):
                Preprocessed query.

        Returns:
            list:
                Similarity scores for every document.
        """

        if self.corpus_vectors is None:
            raise ValueError(
                "Vectorizer must be fitted before transform()."
            )

        query_vector = self.vectorizer.transform([query])

        scores = cosine_similarity(
            query_vector,
            self.corpus_vectors
        )[0]

        return scores


# ============================================================
# MODULE 3: COMPLETE NLP PIPELINE
# ============================================================

class Pipeline:
    """
    End-to-end NLP similarity pipeline.

    The pipeline:
        Raw text
            ↓
        Preprocessing
            ↓
        TF-IDF Vectorization
            ↓
        Cosine Similarity
            ↓
        Ranked Results
    """

    def __init__(self, preprocessor=None, vectorizer=None):
        self.preprocessor = (
            preprocessor
            if preprocessor is not None
            else PreprocessingModule()
        )

        self.vectorizer = (
            vectorizer
            if vectorizer is not None
            else VectorizerModule()
        )

    def run(self, query, corpus):
        """
        Run the complete NLP similarity pipeline.

        Args:
            query (str):
                Raw search query.

            corpus (list):
                List of raw documents.

        Returns:
            list of tuples:
                Ranked results in the format:

                [
                    (document_index, document, similarity_score),
                    ...
                ]
        """

        if not corpus:
            raise ValueError("Corpus cannot be empty.")

        # Preprocess query
        processed_query = self.preprocessor.transform(query)

        # Preprocess corpus
        processed_corpus = []

        for document in corpus:
            processed_document = self.preprocessor.transform(
                document
            )
            processed_corpus.append(processed_document)

        # Fit vectorizer on corpus
        self.vectorizer.fit(processed_corpus)

        # Calculate similarity
        scores = self.vectorizer.transform(
            processed_query
        )

        # Create ranked results
        results = []

        for index, score in enumerate(scores):
            results.append(
                (
                    index,
                    corpus[index],
                    float(score)
                )
            )

        # Highest similarity first
        results.sort(
            key=lambda item: item[2],
            reverse=True
        )

        return results


# ============================================================
# SAMPLE 15-DOCUMENT CORPUS
# ============================================================

DOCUMENTS = [
    "Machine learning algorithms learn patterns from data.",
    "Deep learning uses neural networks with multiple layers.",
    "Python is a popular programming language for data science.",
    "Natural language processing helps computers understand human language.",
    "Data science combines statistics programming and machine learning.",
    "Artificial intelligence enables machines to perform intelligent tasks.",
    "Computer vision allows machines to understand images and videos.",
    "SQL is used to store query and manage structured data.",
    "Cloud computing provides scalable computing resources over the internet.",
    "Cybersecurity protects computer systems networks and data from attacks.",
    "Neural networks are inspired by the structure of the human brain.",
    "Text classification assigns documents to predefined categories.",
    "Recommendation systems suggest products movies or content to users.",
    "Big data technologies process extremely large datasets efficiently.",
    "Natural language processing includes tasks such as text classification translation and sentiment analysis."
]


# ============================================================
# TEST FUNCTION
# ============================================================

def test_pipeline():
    """
    Test the pipeline with five different queries.
    """

    pipeline = Pipeline()

    queries = [
        "machine learning and data",
        "understanding human language",
        "neural networks and deep learning",
        "protecting computer systems",
        "large datasets and cloud computing"
    ]

    print("=" * 70)
    print("DAY 10 - END-TO-END NLP PIPELINE")
    print("=" * 70)

    for query_number, query in enumerate(queries, start=1):

        print(f"\nQUERY {query_number}: {query}")
        print("-" * 70)

        results = pipeline.run(
            query,
            DOCUMENTS
        )

        for rank, (index, document, score) in enumerate(
            results,
            start=1
        ):
            print(
                f"{rank}. "
                f"Score: {score:.4f} | "
                f"Document {index + 1}: {document}"
            )


# ============================================================
# EDGE CASE TESTS
# ============================================================

def test_edge_cases():
    """
    Test required edge cases:
        1. Empty string
        2. Single character
        3. Numbers/symbols only
    """

    pipeline = Pipeline()

    print("\n")
    print("=" * 70)
    print("EDGE CASE TESTS")
    print("=" * 70)

    edge_cases = [
        "",
        "A",
        "12345!!!"
    ]

    for test_input in edge_cases:

        print(f"\nInput: {repr(test_input)}")

        try:
            results = pipeline.run(
                test_input,
                DOCUMENTS
            )

            print("Result:")
            print(results)

        except (ValueError, TypeError) as error:
            print(f"Handled correctly: {error}")


# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    test_pipeline()

    test_edge_cases()