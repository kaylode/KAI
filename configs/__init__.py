from .configs import Config

def get_config(name):
    if name == 'KAI':
        return Config('./configs/kai.yaml')