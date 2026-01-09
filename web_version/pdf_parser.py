import pdfplumber
import pandas as pd

def pdf_to_dataframe(filepath):
    with pdfplumber.open(filepath) as pdf:
        all_text = ""
        tables = []
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                tables.append(pd.DataFrame(table[1:], columns=table[0]))
        
        if tables:
            df = pd.concat(tables, ignore_index=True)
            df.columns = [c.lower() for c in df.columns]
            return df
        else:
            raise ValueError("No table found in PDF.")
