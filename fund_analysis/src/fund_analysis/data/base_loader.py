# Base data loader for Fund Analysis

class BaseLoader:
    def load(self, source):
        raise NotImplementedError("BaseLoader.load must be implemented by subclasses")
