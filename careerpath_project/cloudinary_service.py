# cloudinary_service.py
# Clean and safe Cloudinary upload integration

import os
import re
from io import BytesIO
from typing import Optional

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# --- Early check for missing credentials ---
def assert_cloudinary_config():
    if not all([CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET]):
        raise EnvironmentError("❌ Cloudinary credentials are missing or incomplete in .env file.")
    print("✅ Cloudinary credentials loaded successfully.")

assert_cloudinary_config()

# --- Configure Cloudinary SDK ---
cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)

# --- Utility to sanitize filenames ---
def sanitize_filename(filename: str) -> str:
    """
    Sanitizes the filename to remove spaces and unsafe characters for Cloudinary.
    """
    name, ext = os.path.splitext(filename)
    name = re.sub(r'[^A-Za-z0-9_-]', '_', name)  # allow alphanum, _ and -
    return f"{name}{ext}"

# --- Upload Function ---
# --- Upload Function ---
# --- Upload Function ---
def upload_file_to_cloudinary(file_contents: bytes, filename: str, mimetype: str) -> Optional[str]:
    """
    Uploads a file (PDF, DOCX, PNG, JPG) to Cloudinary and returns its secure URL.
    Uses BytesIO stream to avoid signature errors.
    """
    try:
        safe_name = sanitize_filename(filename)

        print(f"📤 Uploading '{safe_name}' to Cloudinary...")

        upload_result = cloudinary.uploader.upload(
            file=BytesIO(file_contents),  # ✅ SAFE: use stream, not tuple
            folder="jri_career_world_resumes",
            resource_type="auto"
        )

        secure_url = upload_result.get("secure_url")
        print(f"✅ Upload successful. File URL: {secure_url}")
        return secure_url

    except Exception as e:
        print(f"❌ Error uploading file to Cloudinary: {e}")
        return None