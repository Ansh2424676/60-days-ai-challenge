from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


MOCK_RESPONSE = "Python is a programming language."


# --------------------------------------------------
# TEST 1 — Root endpoint
# --------------------------------------------------

def test_root_endpoint():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert "message" in data


# --------------------------------------------------
# TEST 2 — Chat endpoint
# --------------------------------------------------

@patch(
    "app.main.generate_answer",
    return_value=MOCK_RESPONSE,
)
def test_chat_pipeline(mock_generate):

    response = client.post(
        "/chat",
        json={
            "query": "What is Python?"
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == MOCK_RESPONSE

    assert "retrieval_method" in data

    assert "fallback" in data

    mock_generate.assert_called_once()


# --------------------------------------------------
# TEST 3 — TF-IDF fallback
# --------------------------------------------------

@patch(
    "app.main.generate_answer",
    return_value=MOCK_RESPONSE,
)
def test_chat_uses_tfidf_when_faiss_fails(
    mock_generate,
):

    with patch.object(
        app,
        "retriever",
    ) as mock_retriever:

        mock_retriever.search.return_value = {
            "results": [
                "Python is a programming language."
            ],
            "method": "tfidf",
            "fallback": True,
        }

        response = client.post(
            "/chat",
            json={
                "query": "Python programming"
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["fallback"] is True

    assert data["retrieval_method"] == "tfidf"

    mock_generate.assert_called_once()


# --------------------------------------------------
# TEST 4 — OpenAI response is mocked
# --------------------------------------------------

@patch(
    "app.main.generate_answer",
    return_value="FastAPI is a Python web framework.",
)
def test_openai_response_is_mocked(
    mock_generate,
):

    response = client.post(
        "/chat",
        json={
            "query": "What is FastAPI?"
        },
    )

    assert response.status_code == 200

    assert response.json()["answer"] == (
        "FastAPI is a Python web framework."
    )

    mock_generate.assert_called_once()


# --------------------------------------------------
# TEST 5 — Invalid request
# --------------------------------------------------

def test_invalid_chat_request():

    response = client.post(
        "/chat",
        json={},
    )

    assert response.status_code == 422