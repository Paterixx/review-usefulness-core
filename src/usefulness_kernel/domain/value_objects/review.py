from dataclasses import dataclass

from usefulness_kernel.domain.exceptions import InvalidReactionCountError


@dataclass(frozen=True)
class ReviewReactions:
    likes: int
    dislikes: int

    def __post_init__(self) -> None:
        if self.likes < 0 or self.dislikes < 0:
            raise InvalidReactionCountError("Лайки и дизлайки не могут быть отрицательными")


@dataclass(frozen=True)
class ReviewContent:
    text: str | None


@dataclass(frozen=True)
class Review:
    reactions: ReviewReactions
    content: ReviewContent
