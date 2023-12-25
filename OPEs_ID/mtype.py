from collections.abc import Callable, Iterable
from typing import Protocol, TypeVar, Optional, cast
import tqdm

T = TypeVar("T")


class ProgressFunc(Protocol[T]):
    """Protocal that a progress function needs to follow."""

    def __call__(
        self, iterable: Iterable[T], total: Optional[int] = None
    ) -> Iterable[T]:
        ...


def check_progress(progress: ProgressFunc | bool) -> ProgressFunc:
    if progress is True:
        progress = cast(ProgressFunc, tqdm.tqdm)
    elif progress is False:
        progress = lambda iterable, total=None: iterable
    return progress
