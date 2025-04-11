import os
import pytest

def get_base_url():
    """
    Returns the base URL from environment variables with error handling.
    """
    try:
        # Tenta obter do ambiente primeiro
        if 'URL' in os.environ:
            return os.environ['URL']

        # Se não encontrar no ambiente, retorna uma URL padrão ou lança exceção
        raise KeyError("URL environment variable is not set.")
    except Exception as e:
        pytest.fail(f"Failed to get base URL: {str(e)}")
