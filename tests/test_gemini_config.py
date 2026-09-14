from src.extractor.extractor_gemini import create_gemini_client


def test_create_gemini_client():
    client = create_gemini_client()

    assert client is not None