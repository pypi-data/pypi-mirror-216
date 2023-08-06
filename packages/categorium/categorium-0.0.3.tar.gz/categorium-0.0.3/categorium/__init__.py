__version__ = '0.6.0'
__author__ = 'Luís Silva'
__license__ = 'MIT'

from .model_utils import select_language_model
from .csv_utils import select_csv_file
from .token_utils import select_token

__all__ = ['select_language_model','select_csv_file','select_token']

"""
import os

#Função com dicionario para escolher o modelo
def select_language_model(language):
    language_model_dirs = {
        'english': 'en/en_hultig_model',
        'spanish': 'es/es_hultig_model',
        'portuguese': 'pt/pt_hultig_model',
        'italian': 'it/it_hultig_model',
        'french': 'fr/fr_hultig_model',
        'german': 'de/de_hultig_model'
        # Add more language options and model directories as needed
    }
    if language in language_model_dirs:
        model_dir = language_model_dirs[language]
        model_path = os.path.join(os.path.dirname(__file__), 'modelos', model_dir)
        model_module = getattr(__import__(model_path, fromlist=['model']), 'model')
        return model_module
    else:
        raise ValueError(f"Unsupported language: {language}")
    
#Função para exportar as categorias
def select_csv_file(language):
    language_csv_files = {
        'english': 'en/en_categorias.csv',
        'spanish': 'es/es_categorias.csv',
        'portuguese': 'pt/pt_categorias.csv',
        'italian': 'it/it_categorias.csv',
        'french': 'fr/fr_categorias.csv',
        'german': 'de/de_categorias.csv'
        # Add more language options and CSV file names as needed
    }
    if language in language_csv_files:
        csv_file = language_csv_files[language]
        csv_path = os.path.join(os.path.dirname(__file__), 'csv_files', csv_file)
        return csv_path
    else:
        raise ValueError(f"Unsupported language: {language}")
    

#Função com dicionario para escolher o token
def select_token(language):
    language_token_dirs = {
        'english': 'en/hultig-bert-token-uncased_en-vocab.txt',
        'spanish': 'es/hultig-bert-token-uncased_es-vocab.txt',
        'portuguese': 'pt/hultig-bert-token-uncased_pt-vocab.txt',
        'italian': 'it/hultig-bert-token-uncased_it-vocab.txt',
        'french': 'fr/hultig-bert-token-uncased_fr-vocab.txt',
        'german': 'de/hultig-bert-token-uncased_de-vocab.txt'
        # Add more language options and model directories as needed
    }
    if language in language_token_dirs:
        token_dir = language_token_dirs[language]
        model_path = os.path.join(os.path.dirname(__file__), 'modelos', token_dir)
        token_module = getattr(__import__(model_path, fromlist=['model']), 'model')
        return token_module
    else:
        raise ValueError(f"Unsupported language: {language}")

"""