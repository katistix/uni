#!/usr/bin/env python3
"""
Script pentru extragerea textului din PDF-uri
"""

import sys
import os

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 nu este instalat. Instalează cu: pip install PyPDF2")
    sys.exit(1)

def extract_text_from_pdf(pdf_path):
    """Extrage textul din PDF și îl returnează ca string"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += f"\n--- Pagina {page_num + 1} ---\n"
                text += page.extract_text()
                
        return text
    except Exception as e:
        return f"Eroare la citirea PDF-ului: {e}"

def save_text_to_file(text, output_path):
    """Salvează textul într-un fișier .txt"""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)

def main():
    if len(sys.argv) != 2:
        print("Utilizare: python extract_pdf.py <cale_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"Fișierul {pdf_path} nu există!")
        sys.exit(1)
    
    if not pdf_path.lower().endswith('.pdf'):
        print("Fișierul trebuie să aibă extensia .pdf!")
        sys.exit(1)
    
    # Generează numele fișierului de ieșire
    base_name = os.path.splitext(pdf_path)[0]
    output_path = f"{base_name}_extracted.txt"
    
    print(f"Extrag textul din {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    
    print(f"Salvez textul în {output_path}...")
    save_text_to_file(text, output_path)
    
    print(f"Gata! Textul a fost salvat în {output_path}")

if __name__ == "__main__":
    main()