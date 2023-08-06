import os

def select_language_model(language):
    language_model_dirs = {
        'english': 'modelos/en/en_hultig_model',
        'spanish': 'modelos/es/es_hultig_model',
        'portuguese': 'modelos/pt/pt_hultig_model',
        'italian': 'modelos/it/it_hultig_model',
        'french': 'modelos/fr/fr_hultig_model',
        'german': 'modelos/de/de_hultig_model'
        # Add more language options and model directories as needed
    }
    if language in language_model_dirs:
        model_dir = language_model_dirs[language]
        model_path = os.path.join(os.path.dirname(__file__), 'modelos', model_dir)
        model_module = getattr(__import__(model_path, fromlist=['model']), 'model')
        return model_module
    else:
        raise ValueError(f"Unsupported language: {language}")