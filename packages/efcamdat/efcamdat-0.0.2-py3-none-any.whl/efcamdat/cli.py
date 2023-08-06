from typer import Typer

app = Typer()

@app.callback()
def callback():
    """
        boom boom pow
    """

@app.command()
def rawXMLtoJSON(filepath: str, output_path: str):
    '''
        given a input XML file and an output_path 
        create a json file in the output path
    '''
