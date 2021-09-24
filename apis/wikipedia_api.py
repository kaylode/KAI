import wikipedia
from .base import API

wikipedia.set_lang("vi")

class WikipediaAPI(API):
    """
    Search query from wikipedia
    https://github.com/goldsmith/Wikipedia
    """
    def __init__(self) -> None:
        super().__init__()
        self.triggers = ["$wiki"]

    def do_command(self, command, trigger):
        """
        Execute command
        """
        response = None
        reply = True

        # Example call: $wiki python programming 
        query = command.split('wiki')[-1].lstrip().rstrip()

        try:
            response = wikipedia.summary(query, sentences=5)
            # page = wikipedia.page(query)
            # page.url
            # page.images[0]  
        except wikipedia.exceptions.DisambiguationError as e:
            response = "Try one of these options: \n" 
            for idx, opt in enumerate(e.options[:5]):
                response += f"{idx}. {opt}\n"
        except wikipedia.exceptions.PageError as e:
            response = f"{query} not found on Wikipedia"

        return response, reply
        