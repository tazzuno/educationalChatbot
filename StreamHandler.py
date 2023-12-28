from langchain.schema.callbacks.base import BaseCallbackHandler


class StreamHandler(BaseCallbackHandler):
    """Gestisce la visualizzazione del testo token per token.

        Attributes:
            container: Il contenitore dove viene visualizzato il testo.
            text (str): Il testo iniziale.

        Methods:
            on_llm_new_token: Gestisce l'aggiunta di un nuovo token al testo e la visualizzazione nel contenitore.

    """
    
    def __init__(self, container, initial_text=""):
        """Inizializza il gestore di stream con un contenitore e un testo iniziale opzionale."""
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Gestisce l'aggiunta di un nuovo token al testo e la visualizzazione nel contenitore.

        Parameters:
        token (str): Il token da aggiungere al testo.

        """
        
        self.text += token
        self.container.markdown(self.text)
