from googletrans import Translator


def translate(text, dest_language):
    tranlator = Translator()
    return tranlator.translate(text, dest=dest_language).text
