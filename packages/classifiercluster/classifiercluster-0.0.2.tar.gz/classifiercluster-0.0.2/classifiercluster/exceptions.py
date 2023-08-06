class BadAPIResponseException(Exception):
    def __init__(self, message:str):
        super().__init__(f'Error on API Response: {message}')
