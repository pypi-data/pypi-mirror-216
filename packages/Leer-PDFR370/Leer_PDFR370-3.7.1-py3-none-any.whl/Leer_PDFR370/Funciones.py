import fitz #librería pymupdf

def leer_pdf(path):
    try:
        with fitz.open(path) as file:
            text = ''
            for page in file:
                text += page.getText()
        print(text)
    except:
        pass