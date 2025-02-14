import io
import fitz

class PDFTextExtract:

    def extractText(self, fileBytes):
        # print("reading file")
        pdf = io.BytesIO(fileBytes)
        doc = fitz.open(stream = pdf, filetype = "pdf")
        text = "\n".join([page.get_text("text") for page in doc])
        # print("read file text: ")
        # print(text)
        return text