from pathlib import Path
import pandas as pd
import PyPDF2



def extract_text_from_pdfs(pdf_dir, political_leaning ):
    pdf_paths = list(Path(pdf_dir).glob('*.pdf'))
    text_list = []
    for pdf_path in pdf_paths:
        try:
            with pdf_path.open('rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ''.join(page.extract_text() or '' for page in reader.pages)
        except Exception as e:
            print(f"Error processing {pdf_path.name}: {e}")
            text = ''
        # Commas causes issues when writing the csv later 
        # Error: need to escape, but no escapechar set
        text_list.append(text.replace(',', ''))
    return pd.DataFrame({'political_leaning': political_leaning,
                         'source': [pdf_path.name.split('_')[0] for pdf_path in pdf_paths],
                          'text': text_list, 
                          'title': [pdf_path.name for pdf_path in pdf_paths],
                          'type':'news_articles'})