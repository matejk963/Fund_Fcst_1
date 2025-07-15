# Base scenario class for Fund Analysis

class BaseScenario:
    def generate(self, params):
        raise NotImplementedError("BaseScenario.generate must be implemented by subclasses")
