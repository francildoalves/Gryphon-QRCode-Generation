import win32clipboard
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def copy_image_to_clipboard(pil_image):
    """
    Copies a PIL Image to the Windows Clipboard in DIB (Device Independent Bitmap) format.
    """
    try:
        # Convert the image to RGB (remove alpha/transparency if it exists)
        # Because clipboard DIB does not play well with alpha channels usually
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
            
        output = BytesIO()
        # Save as BMP
        pil_image.save(output, 'BMP')
        data = output.getvalue()[14:]  # BMP header is 14 bytes, we only need the DIB part
        output.close()

        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
        
        return True
    except Exception as e:
        logger.error(f"Failed to copy image to clipboard: {e}")
        try:
            win32clipboard.CloseClipboard()
        except:
            pass
        return False
