"""
PDF Extraction API for Supabase Backend
Flask app that processes PDFs and returns AI-optimized JSON context
Deploy to Railway, Render, or any Python hosting
Fast handwriting detection with 10-page chunk processing
Supports async background OCR processing with progress updates
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
import easyocr
from PIL import Image
import numpy as np
import threading

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 30 * 1024 * 1024  # 50MB max file size

# Supabase configuration for direct database updates
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.environ.get('SUPABASE_SERVICE_ROLE_KEY')

def update_material_progress(material_id: str, progress: int, status: str = 'processing', extra_data: dict = None):
    """Update material processing progress in Supabase"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY or not material_id:
        print(f"⚠️ Cannot update progress - missing config or material_id")
        return False
    
    try:
        url = f"{SUPABASE_URL}/rest/v1/study_materials?id=eq.{material_id}"
        headers = {
            'apikey': SUPABASE_SERVICE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_KEY}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal'
        }
        
        data = {
            'processing_progress': progress,
            'processing_status': status
        }
        
        if extra_data:
            data.update(extra_data)
        
        response = requests.patch(url, json=data, headers=headers)
        if response.status_code in [200, 204]:
            print(f"✅ Updated progress: {progress}% (status: {status})")
            return True
        else:
            print(f"⚠️ Failed to update progress: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"⚠️ Error updating progress: {str(e)}")
        return False

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

# Initialize EasyOCR reader ONCE at startup (takes time but only once)
print("🚀 Initializing EasyOCR reader at startup...")
ocr_reader = easyocr.Reader(['en'], gpu=False)
print("✓ EasyOCR reader ready")

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
    """Extract text and structure from PDF bytes using parallel processing for ALL pages"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = pypdf.PdfReader(pdf_file)
        total_pages = len(reader.pages)
        # Process ALL pages
        max_pages = total_pages
        
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

def detect_handwriting_fast(pdf_bytes: bytes, max_pages: int = None) -> dict:
    """Detect handwriting using EasyOCR (fast, lightweight, best for handwriting)"""
    try:
        print(f"Extracting handwriting with EasyOCR (all pages)...")
        
        # Convert ALL pages to images
        images = pdf2image.convert_from_bytes(pdf_bytes, dpi=100)
        max_pages_to_process = len(images) if max_pages is None else min(max_pages, len(images))
        
        print(f"Processing {max_pages_to_process} pages with EasyOCR...")
        handwritten_sections = []
        
        for idx in range(max_pages_to_process):
            try:
                img = images[idx]
                # Convert PIL Image to numpy array for EasyOCR
                img_array = np.array(img)
                # EasyOCR extract text
                results = ocr_reader.readtext(img_array, detail=0)  # detail=0 gives just text
                text = '\n'.join(results)
                
                if text.strip():
                    handwritten_sections.append({
                        'page': idx + 1,
                        'content': text.strip()
                    })
                
                if (idx + 1) % 10 == 0:
                    print(f"Extracted {idx + 1}/{max_pages_to_process} pages")
                    
            except Exception as e:
                print(f"Error on page {idx + 1}: {str(e)}")
        
        print(f"EasyOCR extraction complete: {len(handwritten_sections)} pages with content")
        return {
            'has_handwriting': len(handwritten_sections) > 0,
            'handwritten_sections': handwritten_sections,
            'confidence': 0.85  # EasyOCR confidence
        }
    except Exception as e:
        print(f"Error detecting handwriting: {str(e)}")
        return {'has_handwriting': False, 'handwritten_sections': [], 'confidence': 0}

def detect_handwriting_only(pdf_bytes: bytes) -> dict:
    """Ultra-fast handwriting detection - samples only 1 page at very low resolution
    
    Designed to complete in under 10 seconds to avoid Railway timeout.
    Uses minimal DPI and only checks the first page as a representative sample.
    """
    try:
        print("🔍 Ultra-fast handwriting detection (1-page sample)...")
        
        has_handwriting = False
        
        try:
            # Convert ONLY first page at very low DPI (faster conversion)
            images = pdf2image.convert_from_bytes(
                pdf_bytes, 
                dpi=30,  # Ultra-low DPI for speed
                first_page=1, 
                last_page=1
            )
            
            if images:
                img = images[0]
                # Resize to even smaller if needed (max 400px width)
                max_width = 400
                if img.width > max_width:
                    ratio = max_width / img.width
                    new_size = (int(img.width * ratio), int(img.height * ratio))
                    img = img.resize(new_size, Image.Resampling.LANCZOS)
                
                img_array = np.array(img)
                print(f"Processing image: {img_array.shape}")
                
                # Quick OCR check
                results = ocr_reader.readtext(img_array, detail=1)
                
                # Check if any detected text has low confidence (likely handwriting)
                for result in results:
                    confidence = result[2]
                    if confidence < 0.4:  # Low confidence = likely handwriting
                        has_handwriting = True
                        print(f"Handwriting detected (confidence: {confidence})")
                        break
                        
        except Exception as e:
            print(f"Error in handwriting check: {str(e)}")
        
        print(f"✓ Handwriting detection complete: {has_handwriting}")
        return {
            'has_handwriting': has_handwriting,
            'handwritten_sections': [],
            'confidence': 0.7
        }
    except Exception as e:
        print(f"Error in quick handwriting detection: {str(e)}")
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
    Main extraction endpoint - FRONTEND-FIRST ARCHITECTURE
    
    The frontend (pdfExtractor.js) handles all text extraction.
    Railway ONLY does handwriting detection (fast, under 30s timeout).
    
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
        
        print(f"📋 Railway: Fast handwriting detection only (text extraction by frontend)")
        
        pdf_bytes = None
        
        # Get PDF from URL, base64, or chunk
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
        
        elif 'pdf_chunk' in data:
            # Handle REAL chunked PDF from frontend
            # Chunk is now actual PDF bytes (base64 encoded), not JSON with page metadata
            try:
                pdf_bytes = base64.b64decode(data['pdf_chunk'])
                chunk_index = data.get('chunk_index', 0)
                chunk_count = data.get('chunk_count', 1)
                print(f"📦 Processing REAL PDF chunk {chunk_index + 1}/{chunk_count} ({len(pdf_bytes)} bytes)")
            except Exception as e:
                return jsonify({'error': f'Invalid chunk data: {str(e)}'}), 400
        
        else:
            return jsonify({'error': 'Provide pdf_url, pdf_base64, or pdf_chunk'}), 400
        
        if not pdf_bytes:
            return jsonify({'error': 'No PDF data'}), 400
        
        # ALWAYS use fast handwriting detection (frontend does text extraction)
        print("⚡ Running fast handwriting detection...")
        handwriting = detect_handwriting_only(pdf_bytes)
        
        ai_context = {
            'title': 'Handwriting Analysis',
            'document_type': 'PDF Document',
            'overview': f"Handwriting detection: {handwriting.get('has_handwriting', False)}",
            'key_concepts': [],
            'sections': [],
            'definitions': [],
            'learning_objectives': [],
            'difficulty_level': 'Unknown',
            'handwritten_content': handwriting.get('handwritten_sections', []),
            'tables': [],
            'diagrams': [],
            'key_formulas': []
        }
        
        return jsonify({
            'success': True,
            'ai_context': ai_context,
            'metadata': {
                'has_handwriting': handwriting.get('has_handwriting', False),
                'extraction_method': 'railway_handwriting_only',
                'note': 'Text extraction performed by frontend (pdfExtractor.js)'
            }
        }), 200
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


def process_ocr_background(pdf_bytes: bytes, material_id: str, total_pages: int):
    """Background task to process OCR on all pages and update progress"""
    try:
        print(f"🔄 Starting background OCR for material {material_id} ({total_pages} pages)")
        
        all_text = []
        chunk_size = 5  # Process 5 pages at a time
        
        for chunk_start in range(0, total_pages, chunk_size):
            chunk_end = min(chunk_start + chunk_size, total_pages)
            progress = int((chunk_start / total_pages) * 100)
            
            # Update progress in Supabase
            update_material_progress(material_id, progress)
            
            print(f"📄 Processing pages {chunk_start + 1}-{chunk_end} ({progress}%)...")
            
            try:
                # Convert chunk to images
                images = pdf2image.convert_from_bytes(
                    pdf_bytes,
                    dpi=100,
                    first_page=chunk_start + 1,
                    last_page=chunk_end
                )
                
                for img_idx, img in enumerate(images):
                    page_num = chunk_start + img_idx + 1
                    try:
                        # Resize for faster OCR
                        max_width = 1000
                        if img.width > max_width:
                            ratio = max_width / img.width
                            new_size = (int(img.width * ratio), int(img.height * ratio))
                            img = img.resize(new_size, Image.Resampling.LANCZOS)
                        
                        img_array = np.array(img)
                        results = ocr_reader.readtext(img_array, detail=0)
                        
                        page_text = ' '.join(results)
                        if page_text.strip():
                            all_text.append(f"[Page {page_num}]\n{page_text}")
                            
                    except Exception as e:
                        print(f"⚠️ Error on page {page_num}: {str(e)}")
                        
            except Exception as e:
                print(f"⚠️ Error processing chunk {chunk_start}-{chunk_end}: {str(e)}")
        
        # Combine all OCR text
        full_ocr_text = '\n\n'.join(all_text)
        
        # Update final progress and mark as completed
        update_material_progress(
            material_id, 
            100, 
            'completed',
            {'content': full_ocr_text[:50000]} if full_ocr_text else None  # Limit to 50k chars
        )
        
        print(f"✅ Background OCR complete for {material_id}: {len(full_ocr_text)} chars extracted")
        
    except Exception as e:
        print(f"❌ Background OCR failed for {material_id}: {str(e)}")
        update_material_progress(material_id, 0, 'failed')


@app.route('/extract-async', methods=['POST'])
def extract_async():
    """
    Start async OCR processing in background
    Returns immediately, updates database with progress
    """
    try:
        print("📋 Railway: Async OCR extraction request")
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        material_id = data.get('material_id')
        if not material_id:
            return jsonify({'error': 'material_id required for async processing'}), 400
        
        # Get PDF bytes
        pdf_bytes = None
        total_pages = 0
        
        if 'pdf_url' in data:
            response = requests.get(data['pdf_url'], timeout=30)
            if response.status_code != 200:
                return jsonify({'error': f'Failed to fetch PDF: {response.status_code}'}), 400
            pdf_bytes = response.content
        elif 'pdf_base64' in data:
            pdf_bytes = base64.b64decode(data['pdf_base64'])
        else:
            return jsonify({'error': 'Provide pdf_url or pdf_base64'}), 400
        
        # Get total pages
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = pypdf.PdfReader(pdf_file)
            total_pages = len(reader.pages)
        except Exception as e:
            return jsonify({'error': f'Failed to read PDF: {str(e)}'}), 400
        
        # Mark as processing
        update_material_progress(material_id, 5, 'processing')
        
        # Start background thread
        thread = threading.Thread(
            target=process_ocr_background,
            args=(pdf_bytes, material_id, total_pages)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'OCR processing started',
            'material_id': material_id,
            'total_pages': total_pages
        }), 202  # 202 Accepted
    
    except Exception as e:
        print(f"❌ Error starting async processing: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
