# Webpage to PDF Converter

A Python script that converts web pages to well-formatted PDFs while preserving special characters and formatting.

## Features

- Clean HTML to PDF conversion using `pdfkit` and `wkhtmltopdf`
- Preserves special characters and diacritical marks
- Maintains proper formatting of verses and stanzas
- Removes navigation elements and unwanted content
- Custom CSS styling for better readability

## Requirements

- Python 3.x
- `wkhtmltopdf` must be installed on your system

## Installation

1. Install wkhtmltopdf:
   ```bash
   # On macOS
   brew install wkhtmltopdf

   # On Ubuntu/Debian
   sudo apt-get install wkhtmltopdf
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python converter.py <url>
```

The script will generate a PDF file in the current directory with a name based on the URL.

## Example

```bash
python converter.py https://example.com/article
```

This will create `output_article.pdf` in the current directory.
