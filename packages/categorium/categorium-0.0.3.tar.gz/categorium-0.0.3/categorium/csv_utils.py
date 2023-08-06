import os

def select_csv_file(language):
    language_csv_files = {
        'english': 'modelos/en/en_categorias.csv',
        'spanish': 'modelos/es/es_categorias.csv',
        'portuguese': 'modelos/pt/pt_categorias.csv',
        'italian': 'modelos/it/it_categorias.csv',
        'french': 'modelos/fr/fr_categorias.csv',
        'german': 'modelos/de/de_categorias.csv'
        # Add more language options and CSV file names as needed
    }
    if language in language_csv_files:
        csv_file = language_csv_files[language]
        csv_path = os.path.join(os.path.dirname(__file__), 'csv_files', csv_file)
        return csv_path
    else:
        raise ValueError(f"Unsupported language: {language}")
