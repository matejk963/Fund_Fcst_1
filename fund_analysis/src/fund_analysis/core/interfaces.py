# Abstract base classes for Fund Analysis core interfaces

from abc import ABC, abstractmethod

class DataLoader(ABC):
    @abstractmethod
    def load(self, source):
        pass

class ScenarioGenerator(ABC):
    @abstractmethod
    def generate(self, params):
        pass

class Model(ABC):
    @abstractmethod
    def fit(self, X, y):
        pass
    @abstractmethod
    def predict(self, X):
        pass

class Analysis(ABC):
    @abstractmethod
    def run(self, data):
        pass
