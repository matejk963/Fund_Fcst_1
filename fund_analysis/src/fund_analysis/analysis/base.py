# Base analysis class for Fund Analysis

class BaseAnalysis:
    def run(self, data):
        raise NotImplementedError("BaseAnalysis.run must be implemented by subclasses")
