import os

class Config:
    host: str = '0.0.0.0'
    port: int = 80
    pickles_path: str = './pickles'

    def __init__(self) -> None:
        port = os.getenv('PORT')
        if port:
            self.port = int(port)

        host = os.getenv('HOST')
        if host:
            self.host = host

        pickles_path = os.getenv('PICKLES_PATH')
        if pickles_path:
            self.pickles_path = pickles_path

