import pytest

from review_usefulness.domain.services.review_usefulness_calculator import ReviewUsefulnessCalculator
from usefulness_kernel.domain.value_objects.review import Review, ReviewContent, ReviewReactions


def _build_service() -> ReviewUsefulnessCalculator:
    return ReviewUsefulnessCalculator.build()


def test_calculate_returns_expected_usefulness_and_long_text_factor() -> None:
    service = _build_service()
    review = Review(
        reactions=ReviewReactions(likes=4, dislikes=1),
        content=ReviewContent(text="Очень хороший магазин, всё понравилось!"),
    )

    result = service.calculate(review)

    likes = 4
    dislikes = 1
    total_votes = likes + dislikes
    expected_usefulness = (
        (likes + service.bayesian_usefulness_policy.positive_prior)
        / (
            total_votes
            + service.bayesian_usefulness_policy.positive_prior
            + service.bayesian_usefulness_policy.negative_prior
        )
    ) * min(
        total_votes / service.bayesian_usefulness_policy.votes_normalization_threshold, 1
    )
    assert result.usefulness == pytest.approx(expected_usefulness)
    assert result.text_factor == 1.0


def test_calculate_caps_reliability_when_votes_are_above_threshold() -> None:
    service = _build_service()
    review = Review(
        reactions=ReviewReactions(likes=100, dislikes=0),
        content=ReviewContent(text="Очень хороший магазин, всё понравилось!"),
    )

    result = service.calculate(review)

    likes = 100
    dislikes = 0
    total_votes = likes + dislikes
    expected_usefulness = (
        (likes + service.bayesian_usefulness_policy.positive_prior)
        / (
            total_votes
            + service.bayesian_usefulness_policy.positive_prior
            + service.bayesian_usefulness_policy.negative_prior
        )
    ) * 1.0
    assert result.usefulness == pytest.approx(expected_usefulness)


def test_calculate_returns_text_factor_for_short_non_empty_text() -> None:
    service = _build_service()
    review = Review(
        reactions=ReviewReactions(likes=10, dislikes=2),
        content=ReviewContent(text="Норм"),
    )

    result = service.calculate(review)

    assert result.text_factor == 0.85


def test_calculate_returns_text_factor_for_none_text() -> None:
    service = _build_service()
    review = Review(
        reactions=ReviewReactions(likes=10, dislikes=2),
        content=ReviewContent(text=None),
    )

    result = service.calculate(review)

    assert result.text_factor == 0.7


def test_calculate_returns_text_factor_for_blank_text() -> None:
    service = _build_service()
    review = Review(
        reactions=ReviewReactions(likes=10, dislikes=2),
        content=ReviewContent(text="   "),
    )

    result = service.calculate(review)

    assert result.text_factor == 0.7
