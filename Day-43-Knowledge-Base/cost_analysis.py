from pathlib import Path
import tiktoken


PROCESSED_DIR = Path("data/processed")

MODEL = "text-embedding-3-small"

# Current price:
# $0.02 per 1 million input tokens
PRICE_PER_MILLION_TOKENS = 0.02


def calculate_tokens():

    encoding = tiktoken.get_encoding("cl100k_base")

    total_tokens = 0
    total_documents = 0

    for file_path in PROCESSED_DIR.glob("*.txt"):

        text = file_path.read_text(
            encoding="utf-8"
        )

        tokens = len(
            encoding.encode(text)
        )

        total_tokens += tokens
        total_documents += 1

    return total_documents, total_tokens


def calculate_cost(tokens):

    return (
        tokens / 1_000_000
    ) * PRICE_PER_MILLION_TOKENS


if __name__ == "__main__":

    documents, tokens = calculate_tokens()

    initial_cost = calculate_cost(tokens)

    monthly_cost = initial_cost

    ten_x_tokens = tokens * 10

    ten_x_cost = calculate_cost(
        ten_x_tokens
    )

    print("=" * 60)
    print("DAY 43 EMBEDDING COST ANALYSIS")
    print("=" * 60)

    print(f"Embedding model: {MODEL}")

    print(
        f"Documents: {documents}"
    )

    print(
        f"Total input tokens: {tokens:,}"
    )

    print(
        f"Price per 1M tokens: "
        f"${PRICE_PER_MILLION_TOKENS}"
    )

    print("\nCOST ESTIMATES")

    print(
        f"Initial ingestion cost: "
        f"${initial_cost:.8f}"
    )

    print(
        f"Monthly full re-embedding cost: "
        f"${monthly_cost:.8f}"
    )

    print(
        f"10x document volume cost: "
        f"${ten_x_cost:.8f}"
    )

    print("=" * 60)