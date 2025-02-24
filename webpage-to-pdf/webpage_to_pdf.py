#!/usr/bin/env python3

# Standard library imports
import sys

# Third-party imports
import pdfkit
import requests
from bs4 import BeautifulSoup

def extract_main_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the main content
        main_content = soup.find('div', class_='post-content')
        
        if not main_content:
            print("Could not find main content. Please check the URL.")
            sys.exit(1)
            
        # Add custom CSS for better formatting
        style = """
            <style>
                body {
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    margin: 40px;
                }
                h1, h2, h3, h4 {
                    color: #2C3E50;
                    margin-top: 20px;
                    margin-bottom: 10px;
                }
                p {
                    margin-bottom: 10px;
                    text-align: justify;
                }
                .verse {
                    text-align: center;
                    margin: 20px 0;
                    line-height: 1.8;
                }
                blockquote {
                    margin: 20px 40px;
                    color: #7F8C8D;
                    font-style: italic;
                }
                /* Remove underlines from links */
                a {
                    text-decoration: none;
                    color: inherit;
                }
            </style>
        """
        
        # Remove scripts, styles, iframes, and meta tags
        for element in main_content.find_all(['script', 'style', 'iframe', 'meta']):
            element.decompose()
            
        # First remove all navigation-related elements
        nav_selectors = [
            'div.fusion-sharing-box',  # Share buttons
            'div.fusion-post-navigation',  # Previous/Next navigation
            '.fusion-sharing-box',  # Any sharing elements
            '.fusion-post-pagination',  # Pagination
            '.fusion-footer',  # Footer content
            '.fusion-related-posts',  # Related posts
            'div.related-posts',  # Related posts
            'nav.fusion-post-navigation',  # Navigation between posts
            '.post-navigation',  # Generic post navigation
            '.navigation',  # Any navigation
            '.fusion-post-nav',  # Navigation container
            '.fusion-post-nav-prev',  # Previous post
            '.fusion-post-nav-next',  # Next post
            '.fusion-post-previous',  # Previous link
            '.fusion-post-next',  # Next link
            '[class*="post-navigation"]',  # Any class containing post-navigation
            '[class*="post-nav"]',  # Any class containing post-nav
        ]
        
        # Remove elements by selectors
        for selector in nav_selectors:
            for element in main_content.select(selector):
                element.decompose()
        
        # Remove any element containing navigation-related text
        nav_texts = ['Previous Chapter', 'Next Chapter', 'Previous', 'Next']
        for text in nav_texts:
            # Find elements containing this text (case-insensitive)
            elements = main_content.find_all(lambda tag: tag.string and text.lower() in tag.string.lower())
            for element in elements:
                # Get the parent container
                parent = element.find_parent(['div', 'nav', 'section'])
                if parent:
                    parent.decompose()
                else:
                    element.decompose()
        
        # Also remove any images that might be part of navigation
        nav_images = main_content.find_all('img', alt=lambda x: x and any(text.lower() in x.lower() for text in ['previous', 'next', 'arrow']))
        for img in nav_images:
            parent = img.find_parent(['div', 'nav', 'a'])
            if parent:
                parent.decompose()
            else:
                img.decompose()
        
        # Convert verses (paragraphs with line breaks) to properly formatted elements
        for p in main_content.find_all('p'):
            if '<br' in str(p) or '\n' in p.get_text():
                p['class'] = p.get('class', []) + ['verse']
        
        # Create the final HTML
        html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                {style}
            </head>
            <body>
                {main_content}
            </body>
            </html>
        """
        
        return html
        
    except requests.RequestException as e:
        print(f"Error fetching webpage: {e}")
        sys.exit(1)

def create_pdf(html, output_file):
    # Configure PDF options
    options = {
        'page-size': 'Letter',
        'margin-top': '25mm',
        'margin-right': '25mm',
        'margin-bottom': '25mm',
        'margin-left': '25mm',
        'encoding': 'UTF-8',
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    try:
        # Convert HTML to PDF
        pdfkit.from_string(html, output_file, options=options)
        print("PDF created successfully!")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <url>")
        sys.exit(1)
        
    url = sys.argv[1]
    output_file = f"output_{url.split('/')[-2]}.pdf"
    
    print(f"Fetching content from {url}...")
    html = extract_main_content(url)
    
    print(f"Creating PDF: {output_file}")
    create_pdf(html, output_file)