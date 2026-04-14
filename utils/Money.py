import re

class Money:
    @staticmethod
    def removeSpaceChar(text):
        match = re.search(r"R\$\s*([\d\.,]+)", text)
        value = None
        if match:
            value = match.group(1)
        
        return value.strip().replace(".", "").replace(",", ".") if value else None