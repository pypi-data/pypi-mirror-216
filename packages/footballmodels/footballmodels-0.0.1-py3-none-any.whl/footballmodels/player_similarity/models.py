from abc import ABC, abstractmethod
from typing import List
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import pandas as pd
from footballmodels.definitions.templates import TemplateAttribute
from footballmodels.utils.distance import (
    cartesian_distance,
    weighted_cartesian_distance,
)


class SimilarityAlgorith(ABC):
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._transformed_data = None

    @abstractmethod
    def transform(self):
        pass

    @abstractmethod
    def find(self, player: str, squad: str, season: int, comp: str, n: int = 10):
        pass


class TemplateSimilarityAlgorithm(SimilarityAlgorith):
    """
    Finds similar players based on features specified by
    positional tempate
    """

    def __init__(self, data: pd.DataFrame, template: List[TemplateAttribute]):
        super().__init__(data)
        self._template = template

    def transform(self):
        self._transformed_data = pd.DataFrame(
            {
                "player": self._data["player"],
                "squad": self._data["squad"],
                "season": self._data["season"],
                "comp": self._data["comp"],
                "age": self._data["age"],
                "gender": self._data["gender"],
            }
        )
        for attr in self._template:
            self._transformed_data[attr.name] = attr.apply(self._data)
            self._transformed_data[attr.name] = self._transformed_data[attr.name].rank(
                pct=True,
                ascending=attr.ascending_rank,
                method="min",
            )
        self._transformed_data[[attr.name for attr in self._template]] = MinMaxScaler().fit_transform(
            self._transformed_data[[attr.name for attr in self._template]]
        )

    def find(self, player: str, squad: str, season: int, comp: str, n: int = 10):
        if self._transformed_data is None:
            self.transform()
        player_data = self._transformed_data[
            (self._transformed_data["player"] == player)
            & (self._transformed_data["squad"] == squad)
            & (self._transformed_data["season"] == season)
            & (self._transformed_data["comp"] == comp)
        ]
        player_data = player_data.drop(["player", "squad", "season", "comp", "age", "gender"], axis=1)
        distances = cartesian_distance(
            player_data.values,
            self._transformed_data[[attr.name for attr in self._template]].values,
        )
        self._transformed_data["distance"] = MinMaxScaler().fit_transform(distances.reshape(-1, 1))
        return self._transformed_data.iloc[distances.argsort()[:n]]


class WeightedTemplateSimilarityAlgorithm(TemplateSimilarityAlgorithm):
    def find(self, player: str, squad: str, season: int, comp: str, n: int = 10):
        if self._transformed_data is None:
            self.transform()
        player_data = self._transformed_data[
            (self._transformed_data["player"] == player)
            & (self._transformed_data["squad"] == squad)
            & (self._transformed_data["season"] == season)
            & (self._transformed_data["comp"] == comp)
        ]
        player_data = player_data.drop(["player", "squad", "season", "comp", "age", "gender"], axis=1)
        distances = weighted_cartesian_distance(
            player_data.values,
            self._transformed_data[[attr.name for attr in self._template]].values,
            player_data.values,
        )
        self._transformed_data["distance"] = MinMaxScaler().fit_transform(distances.reshape(-1, 1))
        return self._transformed_data.iloc[distances.argsort()[:n]]
