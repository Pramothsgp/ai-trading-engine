from abc import ABC, abstractmethod
import pandas as pd


class Alpha(ABC):
    name: str

    @abstractmethod
    def compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Returns a score per row.
        Must be aligned with df index.
        """
        pass
