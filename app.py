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

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

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

def extract_pdf_to_images(pdf_bytes: bytes, dpi: int = 200) -> list:
    """Convert PDF bytes to images for vision-based extraction"""
    try:
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=dpi)
        image_bytes = []
        
        for img in images:
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_bytes.append(buffer.getvalue())
        
        return image_bytes
    except Exception as e:
        print(f"Error converting PDF to images: {str(e)}")
        return []

def extract_text_structure(pdf_bytes: bytes) -> dict:
    """Extract text and structure from PDF bytes"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_file)
        pages_data = []
        
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            pages_data.append({
                'page': page_num + 1,
                'text': text,
                'has_images': bool(page.images)
            })
        
        return {
            'total_pages': len(reader.pages),
            'pages': pages_data,
            'has_images': any(p['has_images'] for p in pages_data)
        }
    except Exception as e:
        return {'error': str(e), 'total_pages': 0, 'pages': []}

def encode_image_to_base64(image_bytes: bytes) -> str:
    """Encode image bytes to base64"""
    return base64.standard_b64encode(image_bytes).decode('utf-8')

def analyze_document_with_vision(pdf_bytes: bytes) -> dict:
    """
    Use OpenAI's vision to analyze PDF for handwriting and content
    """
    try:
        images = extract_pdf_to_images(pdf_bytes)
        
        if not images:
            return {'error': 'Could not convert PDF to images', 'has_handwriting': False}
        
        # Process first 10 pages for analysis
        images_to_process = images[:10]
        
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
            base64_img = encode_image_to_base64(img_bytes)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_img}"
                }
            })
        
        # Call OpenAI with vision (FIXED: use chat.completions.create, not messages.create)
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
        
        # Vision analysis for handwriting
        print("Running vision analysis...")
        vision_analysis = analyze_document_with_vision(pdf_bytes)
        
        # Generate AI context
        print("Generating AI context JSON...")
        ai_context = generate_ai_context_json(pdf_bytes, vision_analysis, structure)
        
        if ai_context.get('error'):
            return jsonify({'error': f'AI context generation failed: {ai_context["error"]}'}), 400
        
        return jsonify({
            'success': True,
            'ai_context': ai_context,
            'metadata': {
                'total_pages': structure['total_pages'],
                'has_handwriting': vision_analysis.get('has_handwriting', False),
                'handwriting_pages': len(vision_analysis.get('handwritten_sections', [])),
                'handwritten_sections': vision_analysis.get('handwritten_sections', [])
            }
        }), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
