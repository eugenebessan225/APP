import configparser, os, pickle
from datastats.preprocessor import dataTransformer

class WearDetectionModel:
    def __init__(self, config_path):

        config = configparser.ConfigParser()
        config.read(config_path)
        PATH_MODEL = config.get('Paths', 'PATH_MODEL')
        PATH_MODEL_SCHEMA = config.get('Paths', 'PATH_MODEL_SCHEMA')

        # Load model
        with open(PATH_MODEL, 'rb') as file:
            self.model = pickle.load(file)

        # Load model schema: feature and target names
        with open(PATH_MODEL_SCHEMA, 'rb') as file:
            self.feature_names, self.target_names = pickle.load(file)


    def predict(self, X):
        #X = self.preprocess(X)
        result = self.model.predict(X)
        return self.postprocess(result)

    def preprocess(self, b, t):
        X = dataTransformer(b, t)
        return X

    def postprocess(self, result):
        return result
