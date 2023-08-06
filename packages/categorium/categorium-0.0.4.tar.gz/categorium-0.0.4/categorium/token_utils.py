import os

def select_token(language):
    language_token_dirs = {
        'english': 'en.hultig-bert-token-uncased_en-vocab.txt',
        'spanish': 'es.hultig-bert-token-uncased_es-vocab.txt',
        'portuguese': 'pt.hultig-bert-token-uncased_pt-vocab.txt',
        'italian': 'it.hultig-bert-token-uncased_it-vocab.txt',
        'french': 'fr.hultig-bert-token-uncased_fr-vocab.txt',
        'german': 'de.hultig-bert-token-uncased_de-vocab.txt'
        # Add more language options and model directories as needed
    }
    if language in language_token_dirs:
        token_dir = language_token_dirs[language]
        model_path = os.path.join(os.path.dirname(__file__), 'modelos', token_dir)
        token_module = getattr(__import__(model_path, fromlist=['model']), 'model')
        return token_module
    else:
        raise ValueError(f"Unsupported language: {language}")
