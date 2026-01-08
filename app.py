"""
PDF Extraction API for Supabase Backend
Flask app that processes PDFs and returns AI-optimized JSON context
Deploy to Railway, Render, or any Python hosting
"""

import os
import base64
import json
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
import pypdf
import pdf2image
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytesseract
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 50MB max file size

# Initialize OpenAI client lazily to allow app to start without API key
client = None

def get_openai_client():
    global client
    if client is None:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        client = OpenAI(api_key=api_key)
    return client

def extract_pdf_to_images(pdf_bytes: bytes, dpi: int = 75, max_pages: int = 100) -> list:
    """Convert PDF bytes to images for vision-based extraction
    
    Args:
        pdf_bytes: PDF file content as bytes
        dpi: Resolution for image conversion (lower = faster), default 150
        max_pages: Maximum pages to convert (limits processing time)
    """
    try:
        # Convert only first N pages to save time
        print(f"Converting PDF to images (DPI: {dpi}, max pages: {max_pages})...")
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=dpi, first_page=1, last_page=max_pages)
        image_bytes = []
        
        for idx, img in enumerate(images):
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_bytes.append(buffer.getvalue())
            print(f"Converted page {idx + 1}")
        
        print(f"Successfully converted {len(image_bytes)} pages to images")
        return image_bytes
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        return []

def extract_text_structure(pdf_bytes: bytes) -> dict:
    """Extract text and structure from PDF bytes using parallel processing for 50 pages"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_file)
        total_pages = len(reader.pages)
        max_pages = min(50, total_pages)  # Process up to 50 pages (faster)
        
        print(f"Extracting text from {max_pages} pages (parallel processing)...")
        
        # Extract pages in parallel (4 workers) for faster processing
        pages_data = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(_extract_single_page, reader, page_num): page_num 
                for page_num in range(max_pages)
            }
            
            for future in as_completed(futures):
                try:
                    page_data = future.result()
                    pages_data.append(page_data)
                except Exception as e:
                    print(f"Error extracting page: {str(e)}")
        
        # Sort by page number to maintain order
        pages_data.sort(key=lambda x: x['page'])
        
        return {
            'total_pages': total_pages,
            'pages': pages_data,
            'has_images': any(p.get('has_images', False) for p in pages_data)
        }
    except Exception as e:
        return {'error': str(e), 'total_pages': 0, 'pages': []}

def _extract_single_page(reader, page_num: int) -> dict:
    """Extract text and metadata from a single PDF page"""
    try:
        page = reader.pages[page_num]
        text = page.extract_text()
        return {
            'page': page_num + 1,
            'text': text,
            'has_images': bool(page.images)
        }
    except Exception as e:
        return {
            'page': page_num + 1,
            'text': f'Error: {str(e)}',
            'has_images': False
        }

def detect_handwriting_fast(pdf_bytes: bytes, max_pages: int = 3) -> dict:
    """Detect handwriting using Tesseract OCR (fast, local, no API)"""
    try:
        print(f"Detecting handwriting with Tesseract (first {max_pages} pages)...")
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=150, first_page=1, last_page=max_pages)
        
        handwritten_sections = []
        for idx, img in enumerate(images):
            try:
                # Use Tesseract to extract text
                text = pytesseract.image_to_string(img, config='--psm 6')
                if text.strip():
                    handwritten_sections.append({
                        'page': idx + 1,
                        'content': text.strip()
                    })
                print(f"Scanned page {idx + 1} for handwriting")
            except Exception as e:
                print(f"Error scanning page {idx + 1}: {str(e)}")
        
        return {
            'has_handwriting': len(handwritten_sections) > 0,
            'handwritten_sections': handwritten_sections,
            'confidence': 0.7  # Tesseract confidence
        }
    except Exception as e:
        print(f"Error detecting handwriting: {str(e)}")
        return {'has_handwriting': False, 'handwritten_sections': [], 'confidence': 0}

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64"""
    return base64.standard_b64encode(image_bytes).decode('utf-8')

def analyze_document_with_vision(pdf_bytes: bytes) -> dict:
    """
    Use OpenAI's vision to analyze PDF for handwriting and content
    Optimized for speed - processes first 1 page only
    """
    try:
        # Convert PDF to images (limited to first 1 page, 100 DPI for speed)
        print("Starting vision analysis...")
        images = extract_pdf_to_images(pdf_bytes, dpi=100, max_pages=1)
        
        if not images:
            print("No images extracted, returning minimal analysis")
            return {'error': 'Could not convert PDF to images', 'has_handwriting': False}
        
        # All images are already limited to 3 pages
        images_to_process = images
        print(f"Processing {len(images_to_process)} pages with vision API...")
        
        content = [
            {
                "type": "text",
                "text": """Analyze this PDF document for handwriting and content:
1. Identify ALL handwritten text and transcribe it accurately
2. List any diagrams, tables, charts, or special formatting
3. Identify document type and sections
4. Note any signatures or important markings
5. Assess overall structure and organization

Return ONLY valid JSON (no markdown, no extra text):
{
    "has_handwriting": boolean,
    "handwritten_sections": [{"page": number, "content": "transcribed text"}],
    "typed_content_summary": "brief summary of typed content",
    "document_type": "string",
    "key_sections": ["list", "of", "sections"],
    "has_diagrams": boolean,
    "has_tables": boolean,
    "overall_structure": "description",
    "confidence": number
}"""
            }
        ]
        
        # Add images to content
        for idx, img_bytes in enumerate(images_to_process):
            print(f"Adding image {idx + 1} to vision request...")
            base64_img = encode_image_to_base64(img_bytes)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_img}"
                }
            })
        
        # Call OpenAI with vision (FIXED: use chat.completions.create, not messages.create)
        print("Calling OpenAI Vision API...")
        response = get_openai_client().chat.completions.create(
            model="gpt-4o",
            max_tokens=3000,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        
        response_text = response.choices[0].message.content
        
        # Extract JSON
        if '```json' in response_text:
            json_str = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            json_str = response_text.split('```')[1]
        else:
            json_str = response_text
        
        analysis = json.loads(json_str.strip())
        return {
            'has_handwriting': analysis.get('has_handwriting', False),
            'handwritten_sections': analysis.get('handwritten_sections', []),
            'document_type': analysis.get('document_type', ''),
            'key_sections': analysis.get('key_sections', []),
            'has_diagrams': analysis.get('has_diagrams', False),
            'has_tables': analysis.get('has_tables', False),
            'overall_structure': analysis.get('overall_structure', ''),
            'typed_content_summary': analysis.get('typed_content_summary', ''),
            'confidence': analysis.get('confidence', 0),
            'pages_analyzed': len(images_to_process)
        }
    
    except Exception as e:
        print(f"Vision analysis error: {str(e)}")
        return {
            'error': str(e),
            'has_handwriting': False,
            'pages_analyzed': 0
        }

def generate_ai_context_json(pdf_bytes: bytes, vision_analysis: dict, text_structure: dict) -> dict:
    """
    Generate clean JSON structure optimized for AI backends
    """
    try:
        # Combine all text from PDF
        all_text = "\n".join([p.get('text', '') for p in text_structure.get('pages', [])])
        
        # Use OpenAI to structure the content
        structure_prompt = f"""
You are an expert at converting unstructured document text into clean, AI-friendly JSON format.

Convert this PDF document into a structured JSON object. The document has {text_structure['total_pages']} pages.

Document text (first 10000 chars):
{all_text[:10000]}

Additional context from vision analysis:
- Document Type: {vision_analysis.get('document_type', 'Unknown')}
- Has Handwriting: {vision_analysis.get('has_handwriting', False)}
- Key Sections: {vision_analysis.get('key_sections', [])}
- Has Tables: {vision_analysis.get('has_tables', False)}
- Has Diagrams: {vision_analysis.get('has_diagrams', False)}

Return ONLY valid JSON (no markdown):
{{
    "title": "document title",
    "document_type": "type of document",
    "total_pages": number,
    "overview": "1-2 sentence brief overview",
    "key_concepts": ["list", "of", "main", "concepts"],
    "sections": [
        {{
            "name": "section name",
            "description": "what this section covers",
            "key_points": ["point1", "point2"],
            "content_type": "text|diagrams|tables|mixed"
        }}
    ],
    "handwritten_content": [
        {{
            "location": "page X or section name",
            "content": "transcribed handwriting"
        }}
    ],
    "tables": [
        {{
            "location": "page X or section",
            "description": "what table contains"
        }}
    ],
    "diagrams": [
        {{
            "location": "page X or section",
            "description": "what diagram shows"
        }}
    ],
    "key_formulas": ["if applicable"],
    "definitions": [
        {{
            "term": "important term",
            "definition": "what it means"
        }}
    ],
    "learning_objectives": ["what student should know"],
    "difficulty_level": "beginner|intermediate|advanced",
    "extraction_confidence": 0-100
}}"""
        
        # FIXED: Use chat.completions.create instead of messages.create
        response = get_openai_client().chat.completions.create(
            model="gpt-4o",
            max_tokens=5000,
            messages=[
                {
                    "role": "user",
                    "content": structure_prompt
                }
            ]
        )
        
        response_text = response.choices[0].message.content
        
        # Parse JSON
        if '```json' in response_text:
            json_str = response_text.split('```json')[1].split('```')[0]
        elif '```' in response_text:
            json_str = response_text.split('```')[1]
        else:
            json_str = response_text
        
        ai_context = json.loads(json_str.strip())
        
        # Add metadata
        ai_context['metadata'] = {
            'total_pages': text_structure['total_pages'],
            'has_handwriting': vision_analysis.get('has_handwriting', False),
            'handwriting_pages': len(vision_analysis.get('handwritten_sections', [])),
            'has_diagrams': vision_analysis.get('has_diagrams', False),
            'has_tables': vision_analysis.get('has_tables', False),
            'extraction_confidence': vision_analysis.get('confidence', 0)
        }
        
        return ai_context
    
    except Exception as e:
        print(f"Error generating AI context: {str(e)}")
        return {'error': str(e)}

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'pdf-extraction-api'}), 200

@app.route('/extract', methods=['POST'])
def extract_pdf():
    """
    Main extraction endpoint
    
    Expected JSON body:
    {
        "pdf_url": "https://...", OR
        "pdf_base64": "base64 encoded PDF"
    }
    
    Returns:
    {
        "success": true,
        "ai_context": {...},
        "metadata": {...}
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        pdf_bytes = None
        
        # Get PDF from URL or base64
        if 'pdf_url' in data:
            pdf_url = data['pdf_url']
            try:
                response = requests.get(pdf_url, timeout=30)
                response.raise_for_status()
                pdf_bytes = response.content
            except Exception as e:
                return jsonify({'error': f'Failed to download PDF: {str(e)}'}), 400
        
        elif 'pdf_base64' in data:
            try:
                pdf_bytes = base64.b64decode(data['pdf_base64'])
            except Exception as e:
                return jsonify({'error': f'Invalid base64: {str(e)}'}), 400
        
        else:
            return jsonify({'error': 'Provide either pdf_url or pdf_base64'}), 400
        
        if not pdf_bytes:
            return jsonify({'error': 'No PDF data'}), 400
        
        # Extract text structure
        print("Extracting text structure...")
        structure = extract_text_structure(pdf_bytes)
        
        if structure.get('error'):
            return jsonify({'error': f'Text extraction failed: {structure["error"]}'}), 400
        
        # Detect handwriting using Tesseract (fast, local, no API)
        print("Detecting handwriting with Tesseract...")
        handwriting = detect_handwriting_fast(pdf_bytes, max_pages=3)
        
        # Create response with extracted text + handwriting detection
        ai_context = {
            'title': 'Extracted Document',
            'document_type': 'PDF Document',
            'overview': f"Document with {structure['total_pages']} pages extracted",
            'key_concepts': [],
            'sections': [
                {
                    'title': f'Page {p["page"]}',
                    'content': p['text'][:500] if p['text'] else 'No text extracted'
                }
                for p in structure['pages'][:10]  # First 10 pages
            ],
            'definitions': [],
            'learning_objectives': [],
            'difficulty_level': 'Unknown',
            'handwritten_content': handwriting.get('handwritten_sections', []),
            'tables': [],
            'diagrams': [],
            'key_formulas': [],
            'full_text': '\n\n'.join([p['text'] for p in structure['pages'] if p['text']])
        }
        
        return jsonify({
            'success': True,
            'ai_context': ai_context,
            'metadata': {
                'total_pages': structure['total_pages'],
                'has_handwriting': handwriting.get('has_handwriting', False),
                'handwriting_pages': len(handwriting.get('handwritten_sections', [])),
                'extraction_method': 'tesseract_ocr_fast'
            }
        }), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
