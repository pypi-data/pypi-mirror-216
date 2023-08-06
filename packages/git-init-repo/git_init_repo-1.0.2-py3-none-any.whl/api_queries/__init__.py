import aiohttp

url = r'https://www.toptal.com/developers/gitignore/api/'

class LanguageNotFoundError(Exception):
    """Raised when the language is not found in the API."""
    def __init__(self, language):
        self.language = language
        self.message = f'Language {language} not found in the API.'
        super().__init__(self.message)

async def get_gitignore_list(languages : str, filename : str = '.gitignore') -> None:
    """Writes a gitignore file to the current directory.

    Args:
        languages (str): Languages to get the gitignore file for. Can hold several languages separated by commas.
        filename (str, optional): Name of the file. Defaults to '.gitginore'.
    
    Raises:
        LanguageNotFoundError: If the language is not found in the API.
    """
    list_languages = languages.split(',')
    ans : list[str] = []
    
    for language in list_languages:
        async with aiohttp.ClientSession() as session:
            async with session.get(url + language.lower()) as response:
            
                if response.status != 200:
                    raise LanguageNotFoundError(language)
                text = (await response.text()).split('gitignore.io')[0]
                ans.append(text)
    
    with open(filename, 'w') as file:
        for line in ans:
            file.write(line)