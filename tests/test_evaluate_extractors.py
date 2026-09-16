from src.evaluation.evaluate_extractors import calculate_metrics
from src.evaluation.evaluate_extractors import calculate_overall_metrics

def test_perfect_prediction():
    predicted = {"Python", "SQL"}
    expected = {"Python", "SQL"}

    result = calculate_metrics(predicted, expected)

    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0


def test_partial_prediction():
    predicted = {"Python", "SQL"}
    expected = {"Python", "SQL", "Pandas"}

    result = calculate_metrics(predicted, expected)

    assert result["precision"] == 1.0
    assert result["recall"] == 2 / 3


def test_false_positive():
    predicted = {"Python", "SQL", "Docker"}
    expected = {"Python", "SQL"}

    result = calculate_metrics(predicted, expected)

    assert result["precision"] == 2 / 3
    assert result["recall"] == 1.0


def test_no_prediction():
    predicted = set()
    expected = {"Python"}

    result = calculate_metrics(predicted, expected)

    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1"] == 0.0\
        
def test_overall_metrics():
    results = [
        {
            "precision": 1.0,
            "recall": 1.0,
            "f1": 1.0,
        },
        {
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
        },
    ]

    result = calculate_overall_metrics(results)

    assert result["precision"] == 0.5
    assert result["recall"] == 0.5
    assert result["f1"] == 0.5
    
def test_overall_metrics_empty():
    result = calculate_overall_metrics([])

    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1"] == 0.0