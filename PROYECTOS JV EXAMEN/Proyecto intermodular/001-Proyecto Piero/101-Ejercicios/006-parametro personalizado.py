import requests
from bs4 import BeautifulSoup
import os
import re
from urllib.parse import urljoin, urlparse, quote
import time
import random

# ----------------------------
# CONFIG
# ----------------------------
SEARCH_QUERY = input("Introduce el termino que quieres buscar: ").strip()
if not SEARCH_QUERY:
    print("Error: debes introducir un término de búsqueda.")
    exit(1)
OUTPUT_DIR = "google_images"
RESULTS_PER_PAGE = 20

# Headers to mimic real browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# ----------------------------
# Google Images URL Builder
# ----------------------------
def build_google_images_url(query, start=0):
    """Build Google Images search URL"""
    base_url = "https://www.google.com/search"
    params = {
        'q': query,
        'tbm': 'isch',  # Image search
        'hl': 'en',
        'ijn': '0',
        'start': start,
        'client': 'firefox-b-d'
    }
    return f"{base_url}?{'&'.join(f'{k}={quote(str(v))}' for k, v in params.items())}"

# ----------------------------
# Create output directory
# ----------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# Session with cookies
# ----------------------------
session = requests.Session()
session.headers.update(HEADERS)

# ----------------------------
# Download HTML from Google Images
# ----------------------------
def download_google_images(query, num_images=20):
    all_image_urls = set()
    start = 0
    
    while len(all_image_urls) < num_images:
        url = build_google_images_url(query, start)
        print(f"Descargando página desde: {url}")
        
        try:
            # Random delay to avoid detection
            time.sleep(random.uniform(2, 5))
            
            response = session.get(url, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Method 1: Extract from img tags
            for img in soup.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and src.startswith('http'):
                    # Filter out Google's own images and icons
                    if 'google.com' not in src or 'logo' not in src.lower():
                        all_image_urls.add(src)
                        print(f"Found image: {src}")
            
            # Method 2: Extract from JSON data (Google stores image URLs in script tags)
            script_tags = soup.find_all('script')
            for script in script_tags:
                script_content = script.string
                if script_content:
                    # Look for URLs in the script content
                    url_patterns = [
                        r'\"(https://[^\"]*\.(?:jpg|jpeg|png|gif|webp)[^\"]*)\"',
                        r'\"(http://[^\"]*\.(?:jpg|jpeg|png|gif|webp)[^\"]*)\"',
                    ]
                    for pattern in url_patterns:
                        matches = re.findall(pattern, script_content, re.IGNORECASE)
                        for match in matches:
                            if 'google' not in match or 'logo' not in match.lower():
                                all_image_urls.add(match)
            
            # Method 3: Look for base64 encoded images in data attributes
            for img in soup.find_all('img', {'src': True}):
                src = img['src']
                if src.startswith('data:image/'):
                    all_image_urls.add(src)
            
            print(f"Total images found so far: {len(all_image_urls)}")
            
            # Check if we should continue to next page
            if len(all_image_urls) >= num_images:
                break
                
            start += RESULTS_PER_PAGE
            
            # Safety limit
            if start > 100:  # Don't go too deep
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Error downloading page: {e}")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    return list(all_image_urls)[:num_images]

# ----------------------------
# Download images
# ----------------------------
def download_images(image_urls):
    print(f"\nDescargando {len(image_urls)} imágenes...")
    
    success_count = 0
    for i, img_url in enumerate(image_urls):
        try:
            # Create filename
            if img_url.startswith('data:image/'):
                # Handle base64 images
                extension = re.findall(r'data:image/(\w+);', img_url)
                ext = extension[0] if extension else 'png'
                filename = f"image_{i}_base64.{ext}"
            else:
                parsed_url = urlparse(img_url)
                filename = os.path.basename(parsed_url.path)
                if not filename or '.' not in filename:
                    ext = 'jpg'  # default extension
                    filename = f"image_{i}.{ext}"
            
            # Clean filename
            filename = re.sub(r'[^\w\.-]', '_', filename)
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Avoid overwriting
            counter = 1
            original_filepath = filepath
            while os.path.exists(filepath):
                name, ext = os.path.splitext(original_filepath)
                filepath = f"{name}_{counter}{ext}"
                counter += 1
            
            # Download image
            if img_url.startswith('data:image/'):
                # Handle base64 images
                import base64
                base64_data = img_url.split(',')[1]
                image_data = base64.b64decode(base64_data)
                with open(filepath, "wb") as f:
                    f.write(image_data)
            else:
                img_response = session.get(img_url, timeout=10, stream=True)
                img_response.raise_for_status()
                
                # Check if it's actually an image
                content_type = img_response.headers.get('content-type', '')
                if content_type and not content_type.startswith('image/'):
                    print(f"✘ No es una imagen: {img_url}")
                    continue
                
                with open(filepath, "wb") as f:
                    for chunk in img_response.iter_content(chunk_size=8192):
                        f.write(chunk)
            
            file_size = os.path.getsize(filepath)
            print(f"✔ [{i+1}/{len(image_urls)}] Guardada: {filename} ({file_size} bytes)")
            success_count += 1
            
            # Random delay between downloads
            time.sleep(random.uniform(1, 3))
            
        except Exception as e:
            print(f"✘ Error con imagen {i+1}: {e}")
    
    return success_count

# ----------------------------
# Main execution
# ----------------------------
if __name__ == "__main__":
    print("🔍 Buscando imágenes en Google...")
    print("⚠️  ADVERTENCIA: Esto puede violar los términos de servicio de Google")
    
    # Get image URLs
    image_urls = download_google_images(SEARCH_QUERY, num_images=20)
    
    if image_urls:
        print(f"\n🎯 Encontradas {len(image_urls)} URLs de imágenes")
        
        # Download images
        success_count = download_images(image_urls)
        
        print(f"\n✅ Terminado! {success_count}/{len(image_urls)} imágenes descargadas en '{OUTPUT_DIR}/'")
    else:
        print("❌ No se encontraron imágenes")
