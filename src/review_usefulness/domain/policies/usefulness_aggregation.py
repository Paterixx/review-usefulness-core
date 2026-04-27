from dataclasses import dataclass


@dataclass(frozen=True)
class BayesianUsefulnessPolicy:
    positive_prior: int = 1
    negative_prior: int = 2
    votes_normalization_threshold: int = 10

    def apply(self, likes: int, dislikes: int) -> float:
        total_votes = likes + dislikes
    
        reliability = min(total_votes / self.votes_normalization_threshold, 1.0)
        probability = (
            (likes + self.positive_prior) /
            (total_votes + self.positive_prior + self.negative_prior)
        )

        return probability * reliability


@dataclass(frozen=True)
class TextUsefulnessFactorPolicy:
    long_text_threshold: int = 30
    long_text_factor: float = 1.0
    short_text_factor: float = 0.85
    empty_text_factor: float = 0.7

    def apply(self, text: str | None) -> float:
        if text is None or not text.strip():
            return self.empty_text_factor

        if len(text.strip()) >= self.long_text_threshold:
            return self.long_text_factor

        return self.short_text_factor
