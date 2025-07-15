# Base model class for Fund Analysis

class BaseModel:
    def fit(self, X, y):
        raise NotImplementedError("BaseModel.fit must be implemented by subclasses")
    def predict(self, X):
        raise NotImplementedError("BaseModel.predict must be implemented by subclasses")
