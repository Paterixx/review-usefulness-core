from dataclasses import dataclass


@dataclass(frozen=True)
class ReviewUsefulnessResult:
    usefulness: float
    text_factor: float
