ython -m venv /app/.venv
$ pip install -r requirements.txt
 
Deploy
──────────
$ gunicorn app:app
 
 
Successfully prepared Railpack plan for build
 
 
context: 8s4l-38Cd

load build definition from railpack-plan.json
0ms

install apt packages: poppler-utils
16s
Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
Get:2 http://deb.debian.org/debian bookworm-updates InRelease [55.4 kB]
Get:3 http://deb.debian.org/debian-security bookworm-security InRelease [48.0 kB]
Get:4 http://deb.debian.org/debian bookworm/main amd64 Packages [8791 kB]
Get:5 http://deb.debian.org/debian bookworm-updates/main amd64 Packages [6924 B]
Get:6 http://deb.debian.org/debian-security bookworm-security/main amd64 Packages [290 kB]
Fetched 9343 kB in 1s (7130 kB/s)
Reading package lists...

Reading package lists...

Building dependency tree...

Reading state information...

The following additional packages will be installed:
  fontconfig-config fonts-dejavu-core libbrotli1 libbsd0 libcairo2 libdeflate0
  libexpat1 libfontconfig1 libfreetype6 libjbig0 libjpeg62-turbo liblcms2-2
  liblerc4 libnspr4 libnss3 libopenjp2-7 libpixman-1-0 libpng16-16
  libpoppler126 libsqlite3-0 libtiff6 libwebp7 libx11-6 libx11-data libxau6
  libxcb-render0 libxcb-shm0 libxcb1 libxdmcp6 libxext6 libxrender1
  poppler-data
Suggested packages:
  liblcms2-utils ghostscript fonts-japanese-mincho | fonts-ipafont-mincho
  fonts-japanese-gothic | fonts-ipafont-gothic fonts-arphic-ukai
  fonts-arphic-uming fonts-nanum
The following NEW packages will be installed:
  fontconfig-config fonts-dejavu-core libbrotli1 libbsd0 libcairo2 libdeflate0
  libexpat1 libfontconfig1 libfreetype6 libjbig0 libjpeg62-turbo liblcms2-2
  liblerc4 libnspr4 libnss3 libopenjp2-7 libpixman-1-0 libpng16-16
  libpoppler126 libsqlite3-0 libtiff6 libwebp7 libx11-6 libx11-data libxau6
  libxcb-render0 libxcb-shm0 libxcb1 libxdmcp6 libxext6 libxrender1
  poppler-data poppler-utils
0 upgraded, 33 newly installed, 0 to remove and 0 not upgraded.
Need to get 12.9 MB of archives.
After this operation, 42.3 MB of additional disk space will be used.
Get:1 http://deb.debian.org/debian bookworm/main amd64 poppler-data all 0.4.12-1 [1601 kB]
Get:2 http://deb.debian.org/debian bookworm/main amd64 fonts-dejavu-core all 2.37-6 [1068 kB]
Get:3 http://deb.debian.org/debian bookworm/main amd64 fontconfig-config amd64 2.14.1-4 [315 kB]
Get:4 http://deb.debian.org/debian bookworm/main amd64 libbrotli1 amd64 1.0.9-2+b6 [275 kB]
Get:5 http://deb.debian.org/debian bookworm/main amd64 libbsd0 amd64 0.11.7-2 [117 kB]
Get:6 http://deb.debian.org/debian bookworm/main amd64 libexpat1 amd64 2.5.0-1+deb12u2 [99.9 kB]
Get:7 http://deb.debian.org/debian-security bookworm-security/main amd64 libpng16-16 amd64 1.6.39-2+deb12u1 [276 kB]
Get:8 http://deb.debian.org/debian bookworm/main amd64 libfreetype6 amd64 2.12.1+dfsg-5+deb12u4 [398 kB]
Get:9 http://deb.debian.org/debian bookworm/main amd64 libfontconfig1 amd64 2.14.1-4 [386 kB]
Get:10 http://deb.debian.org/debian bookworm/main amd64 libpixman-1-0 amd64 0.42.2-1 [546 kB]
Get:11 http://deb.debian.org/debian bookworm/main amd64 libxau6 amd64 1:1.0.9-1 [19.7 kB]
Get:12 http://deb.debian.org/debian bookworm/main amd64 libxdmcp6 amd64 1:1.1.2-3 [26.3 kB]
Get:13 http://deb.debian.org/debian bookworm/main amd64 libxcb1 amd64 1.15-1 [144 kB]
Get:14 http://deb.debian.org/debian bookworm/main amd64 libx11-data all 2:1.8.4-2+deb12u2 [292 kB]
Get:15 http://deb.debian.org/debian bookworm/main amd64 libx11-6 amd64 2:1.8.4-2+deb12u2 [760 kB]
Get:16 http://deb.debian.org/debian bookworm/main amd64 libxcb-render0 amd64 1.15-1 [115 kB]
Get:17 http://deb.debian.org/debian bookworm/main amd64 libxcb-shm0 amd64 1.15-1 [105 kB]
Get:18 http://deb.debian.org/debian bookworm/main amd64 libxext6 amd64 2:1.3.4-1+b1 [52.9 kB]
Get:19 http://deb.debian.org/debian bookworm/main amd64 libxrender1 amd64 1:0.9.10-1.1 [33.2 kB]
Get:20 http://deb.debian.org/debian bookworm/main amd64 libcairo2 amd64 1.16.0-7 [575 kB]
Get:21 http://deb.debian.org/debian bookworm/main amd64 libdeflate0 amd64 1.14-1 [61.4 kB]
Get:22 http://deb.debian.org/debian bookworm/main amd64 libjbig0 amd64 2.1-6.1 [31.7 kB]
Get:23 http://deb.debian.org/debian bookworm/main amd64 libjpeg62-turbo amd64 1:2.1.5-2 [166 kB]
Get:24 http://deb.debian.org/debian bookworm/main amd64 liblcms2-2 amd64 2.14-2 [154 kB]
Get:25 http://deb.debian.org/debian bookworm/main amd64 liblerc4 amd64 4.0.0+ds-2 [170 kB]
Get:26 http://deb.debian.org/debian bookworm/main amd64 libnspr4 amd64 2:4.35-1 [113 kB]
Get:27 http://deb.debian.org/debian bookworm/main amd64 libsqlite3-0 amd64 3.40.1-2+deb12u2 [839 kB]
Get:28 http://deb.debian.org/debian bookworm/main amd64 libnss3 amd64 2:3.87.1-1+deb12u1 [1331 kB]
Get:29 http://deb.debian.org/debian bookworm/main amd64 libopenjp2-7 amd64 2.5.0-2+deb12u2 [189 kB]
Get:30 http://deb.debian.org/debian bookworm/main amd64 libwebp7 amd64 1.2.4-0.2+deb12u1 [286 kB]
Get:31 http://deb.debian.org/debian-security bookworm-security/main amd64 libtiff6 amd64 4.5.0-6+deb12u3 [316 kB]
Get:32 http://deb.debian.org/debian bookworm/main amd64 libpoppler126 amd64 22.12.0-2+deb12u1 [1853 kB]
Get:33 http://deb.debian.org/debian bookworm/main amd64 poppler-utils amd64 22.12.0-2+deb12u1 [191 kB]
debconf: delaying package configuration, since apt-utils is not installed
Fetched 12.9 MB in 0s (66.4 MB/s)
Selecting previously unselected package poppler-data.
(Reading database ... 
(Reading database ... 5%
(Reading database ... 10%
(Reading database ... 15%
(Reading database ... 20%
(Reading database ... 25%
(Reading database ... 30%
(Reading database ... 35%
(Reading database ... 40%
(Reading database ... 45%
(Reading database ... 50%
(Reading database ... 55%
(Reading database ... 60%
(Reading database ... 65%
(Reading database ... 70%
(Reading database ... 75%
(Reading database ... 80%
(Reading database ... 85%
(Reading database ... 90%
(Reading database ... 95%
(Reading database ... 100%
(Reading database ... 6622 files and directories currently installed.)
Preparing to unpack .../00-poppler-data_0.4.12-1_all.deb ...
Unpacking poppler-data (0.4.12-1) ...
Selecting previously unselected package fonts-dejavu-core.
Preparing to unpack .../01-fonts-dejavu-core_2.37-6_all.deb ...
Unpacking fonts-dejavu-core (2.37-6) ...
Selecting previously unselected package fontconfig-config.
Preparing to unpack .../02-fontconfig-config_2.14.1-4_amd64.deb ...
Unpacking fontconfig-config (2.14.1-4) ...
Selecting previously unselected package libbrotli1:amd64.
Preparing to unpack .../03-libbrotli1_1.0.9-2+b6_amd64.deb ...
Unpacking libbrotli1:amd64 (1.0.9-2+b6) ...
Selecting previously unselected package libbsd0:amd64.
Preparing to unpack .../04-libbsd0_0.11.7-2_amd64.deb ...
Unpacking libbsd0:amd64 (0.11.7-2) ...
Selecting previously unselected package libexpat1:amd64.
Preparing to unpack .../05-libexpat1_2.5.0-1+deb12u2_amd64.deb ...
Unpacking libexpat1:amd64 (2.5.0-1+deb12u2) ...
Selecting previously unselected package libpng16-16:amd64.
Preparing to unpack .../06-libpng16-16_1.6.39-2+deb12u1_amd64.deb ...
Unpacking libpng16-16:amd64 (1.6.39-2+deb12u1) ...
Selecting previously unselected package libfreetype6:amd64.
Preparing to unpack .../07-libfreetype6_2.12.1+dfsg-5+deb12u4_amd64.deb ...
Unpacking libfreetype6:amd64 (2.12.1+dfsg-5+deb12u4) ...
Selecting previously unselected package libfontconfig1:amd64.
Preparing to unpack .../08-libfontconfig1_2.14.1-4_amd64.deb ...
Unpacking libfontconfig1:amd64 (2.14.1-4) ...
Selecting previously unselected package libpixman-1-0:amd64.
Preparing to unpack .../09-libpixman-1-0_0.42.2-1_amd64.deb ...
Unpacking libpixman-1-0:amd64 (0.42.2-1) ...
Selecting previously unselected package libxau6:amd64.
Preparing to unpack .../10-libxau6_1%3a1.0.9-1_amd64.deb ...
Unpacking libxau6:amd64 (1:1.0.9-1) ...
Selecting previously unselected package libxdmcp6:amd64.
Preparing to unpack .../11-libxdmcp6_1%3a1.1.2-3_amd64.deb ...
Unpacking libxdmcp6:amd64 (1:1.1.2-3) ...
Selecting previously unselected package libxcb1:amd64.
Preparing to unpack .../12-libxcb1_1.15-1_amd64.deb ...
Unpacking libxcb1:amd64 (1.15-1) ...
Selecting previously unselected package libx11-data.
Preparing to unpack .../13-libx11-data_2%3a1.8.4-2+deb12u2_all.deb ...
Unpacking libx11-data (2:1.8.4-2+deb12u2) ...
Selecting previously unselected package libx11-6:amd64.
Preparing to unpack .../14-libx11-6_2%3a1.8.4-2+deb12u2_amd64.deb ...
Unpacking libx11-6:amd64 (2:1.8.4-2+deb12u2) ...
Selecting previously unselected package libxcb-render0:amd64.
Preparing to unpack .../15-libxcb-render0_1.15-1_amd64.deb ...
Unpacking libxcb-render0:amd64 (1.15-1) ...
Selecting previously unselected package libxcb-shm0:amd64.
Preparing to unpack .../16-libxcb-shm0_1.15-1_amd64.deb ...
Unpacking libxcb-shm0:amd64 (1.15-1) ...
Selecting previously unselected package libxext6:amd64.
Preparing to unpack .../17-libxext6_2%3a1.3.4-1+b1_amd64.deb ...
Unpacking libxext6:amd64 (2:1.3.4-1+b1) ...
Selecting previously unselected package libxrender1:amd64.
Preparing to unpack .../18-libxrender1_1%3a0.9.10-1.1_amd64.deb ...
Unpacking libxrender1:amd64 (1:0.9.10-1.1) ...
Selecting previously unselected package libcairo2:amd64.
Preparing to unpack .../19-libcairo2_1.16.0-7_amd64.deb ...
Unpacking libcairo2:amd64 (1.16.0-7) ...
Selecting previously unselected package libdeflate0:amd64.
Preparing to unpack .../20-libdeflate0_1.14-1_amd64.deb ...
Unpacking libdeflate0:amd64 (1.14-1) ...
Selecting previously unselected package libjbig0:amd64.
Preparing to unpack .../21-libjbig0_2.1-6.1_amd64.deb ...
Unpacking libjbig0:amd64 (2.1-6.1) ...
Selecting previously unselected package libjpeg62-turbo:amd64.
Preparing to unpack .../22-libjpeg62-turbo_1%3a2.1.5-2_amd64.deb ...
Unpacking libjpeg62-turbo:amd64 (1:2.1.5-2) ...
Selecting previously unselected package liblcms2-2:amd64.
Preparing to unpack .../23-liblcms2-2_2.14-2_amd64.deb ...
Unpacking liblcms2-2:amd64 (2.14-2) ...
Selecting previously unselected package liblerc4:amd64.
Preparing to unpack .../24-liblerc4_4.0.0+ds-2_amd64.deb ...
Unpacking liblerc4:amd64 (4.0.0+ds-2) ...
Selecting previously unselected package libnspr4:amd64.
Preparing to unpack .../25-libnspr4_2%3a4.35-1_amd64.deb ...
Unpacking libnspr4:amd64 (2:4.35-1) ...
Selecting previously unselected package libsqlite3-0:amd64.
Preparing to unpack .../26-libsqlite3-0_3.40.1-2+deb12u2_amd64.deb ...
Unpacking libsqlite3-0:amd64 (3.40.1-2+deb12u2) ...
Selecting previously unselected package libnss3:amd64.
Preparing to unpack .../27-libnss3_2%3a3.87.1-1+deb12u1_amd64.deb ...
Unpacking libnss3:amd64 (2:3.87.1-1+deb12u1) ...
Selecting previously unselected package libopenjp2-7:amd64.
Preparing to unpack .../28-libopenjp2-7_2.5.0-2+deb12u2_amd64.deb ...
Unpacking libopenjp2-7:amd64 (2.5.0-2+deb12u2) ...
Selecting previously unselected package libwebp7:amd64.
Preparing to unpack .../29-libwebp7_1.2.4-0.2+deb12u1_amd64.deb ...
Unpacking libwebp7:amd64 (1.2.4-0.2+deb12u1) ...
Selecting previously unselected package libtiff6:amd64.
Preparing to unpack .../30-libtiff6_4.5.0-6+deb12u3_amd64.deb ...
Unpacking libtiff6:amd64 (4.5.0-6+deb12u3) ...
Selecting previously unselected package libpoppler126:amd64.
Preparing to unpack .../31-libpoppler126_22.12.0-2+deb12u1_amd64.deb ...
Unpacking libpoppler126:amd64 (22.12.0-2+deb12u1) ...
Selecting previously unselected package poppler-utils.
Preparing to unpack .../32-poppler-utils_22.12.0-2+deb12u1_amd64.deb ...
Unpacking poppler-utils (22.12.0-2+deb12u1) ...
Setting up libexpat1:amd64 (2.5.0-1+deb12u2) ...
Setting up liblcms2-2:amd64 (2.14-2) ...
Setting up libpixman-1-0:amd64 (0.42.2-1) ...
Setting up libxau6:amd64 (1:1.0.9-1) ...
Setting up liblerc4:amd64 (4.0.0+ds-2) ...
Setting up libbrotli1:amd64 (1.0.9-2+b6) ...
Setting up libsqlite3-0:amd64 (3.40.1-2+deb12u2) ...
Setting up libdeflate0:amd64 (1.14-1) ...
Setting up libjbig0:amd64 (2.1-6.1) ...
Setting up poppler-data (0.4.12-1) ...
Setting up libjpeg62-turbo:amd64 (1:2.1.5-2) ...
Setting up libx11-data (2:1.8.4-2+deb12u2) ...
Setting up libnspr4:amd64 (2:4.35-1) ...
Setting up libpng16-16:amd64 (1.6.39-2+deb12u1) ...
Setting up fonts-dejavu-core (2.37-6) ...
Setting up libwebp7:amd64 (1.2.4-0.2+deb12u1) ...
Setting up libtiff6:amd64 (4.5.0-6+deb12u3) ...
Setting up libopenjp2-7:amd64 (2.5.0-2+deb12u2) ...
Setting up libbsd0:amd64 (0.11.7-2) ...
Setting up libxdmcp6:amd64 (1:1.1.2-3) ...
Setting up libxcb1:amd64 (1.15-1) ...
Setting up libxcb-render0:amd64 (1.15-1) ...
Setting up fontconfig-config (2.14.1-4) ...
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC contains: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.36.0 /usr/local/share/perl/5.36.0 /usr/lib/x86_64-linux-gnu/perl5/5.36 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.36 /usr/share/perl/5.36 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 7.)
debconf: falling back to frontend: Teletype
Setting up libnss3:amd64 (2:3.87.1-1+deb12u1) ...
Setting up libxcb-shm0:amd64 (1.15-1) ...
Setting up libfreetype6:amd64 (2.12.1+dfsg-5+deb12u4) ...
Setting up libx11-6:amd64 (2:1.8.4-2+deb12u2) ...
Setting up libfontconfig1:amd64 (2.14.1-4) ...
Setting up libxrender1:amd64 (1:0.9.10-1.1) ...
Setting up libxext6:amd64 (2:1.3.4-1+b1) ...
Setting up libcairo2:amd64 (1.16.0-7) ...
Setting up libpoppler126:amd64 (22.12.0-2+deb12u1) ...
Setting up poppler-utils (22.12.0-2+deb12u1) ...
Processing triggers for libc-bin (2.36-9+deb12u13) ...

install mise packages: python cached
0ms

copy /mise/shims, /root/.local/state/mise, /etc/mise/config.toml, /usr/local/bin/mise, /mise/installs cached
0ms

python -m venv /app/.venv cached
0ms

copy requirements.txt
33ms

pip install -r requirements.txt
16s
ERROR: Failed to build 'Pillow' when getting requirements to build wheel
ERROR: failed to build: failed to solve: process "pip install -r requirements.txt" did not complete successfully: exit code: 1
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
