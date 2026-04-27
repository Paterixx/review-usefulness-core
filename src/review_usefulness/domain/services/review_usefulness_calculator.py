from dataclasses import dataclass

from review_usefulness.domain.policies.usefulness_aggregation import (
    BayesianUsefulnessPolicy,
    TextUsefulnessFactorPolicy,
)
from review_usefulness.domain.value_objects.review_usefulness_result import ReviewUsefulnessResult
from usefulness_kernel.domain.value_objects.review import Review


@dataclass(frozen=True)
class ReviewUsefulnessCalculator:
    bayesian_usefulness_policy: BayesianUsefulnessPolicy
    text_usefulness_factor_policy: TextUsefulnessFactorPolicy

    @classmethod
    def build(cls) -> "ReviewUsefulnessCalculator":
        return cls(
            bayesian_usefulness_policy=BayesianUsefulnessPolicy(),
            text_usefulness_factor_policy=TextUsefulnessFactorPolicy(),
        )

    def calculate(self, review: Review) -> ReviewUsefulnessResult:
        usefulness = self.bayesian_usefulness_policy.apply(
            likes=review.reactions.likes,
            dislikes=review.reactions.dislikes,
        )
        text_factor = self.text_usefulness_factor_policy.apply(review.content.text)

        return ReviewUsefulnessResult(
            usefulness=usefulness,
            text_factor=text_factor,
        )
