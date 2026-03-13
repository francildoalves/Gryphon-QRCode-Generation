import qrcode
import qrcode.image.svg
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """A class to handle QR Code generation."""
    
    def __init__(self, version: int = 1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size: int = 10, border: int = 4):
        # We default to ERROR_CORRECT_H (High - 30%) because it allows logos to cover
        # the center of the QR without destroying its scannability.
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )

    def generate_image(self, data: str, fill_color: str = "black", back_color: str = "white", logo_path: str = None):
        """Generates and returns the raw PIL Image object, optionally with a center logo."""
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        img = self.qr.make_image(fill_color=fill_color, back_color=back_color).convert('RGBA')

        if logo_path:
            try:
                from PIL import Image
                logo = Image.open(logo_path)
                
                # Ensure the logo has alpha channel for transparency handling
                logo = logo.convert("RGBA")
                
                # Calculate maximum logo size (e.g., 25% of QR code width/height)
                # This ensures the H-level error correction can still recover data
                max_logo_size = int(img.size[0] * 0.25)
                
                # Resize the logo while keeping aspect ratio
                logo.thumbnail((max_logo_size, max_logo_size), Image.Resampling.LANCZOS)
                
                # Calculate position (center)
                logo_pos = (
                    (img.size[0] - logo.size[0]) // 2,
                    (img.size[1] - logo.size[1]) // 2
                )
                
                # Paste the logo using its own alpha channel as the mask
                img.paste(logo, logo_pos, logo)
                
            except Exception as e:
                logger.error(f"Failed to apply logo: {e}")
                
        return img

    def generate(self, data: str, output_path: str | Path, fill_color: str = "black", back_color: str = "white") -> bool:
        """Generates a QR code and saves it to a PNG file."""
        try:
            img = self.generate_image(data, fill_color, back_color)
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(output_file))
            logger.info(f"QR Code PNG saved to: {output_file.absolute()}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate QR Code: {e}")
            return False

    def generate_svg(self, data: str, output_path: str | Path, logo_path: str = None) -> bool:
        """Generates a vector SVG QR code (always black/transparent for editing)."""
        try:
            factory = qrcode.image.svg.SvgPathImage
            self.qr.clear()
            self.qr.add_data(data)
            self.qr.make(fit=True)
            
            # recreate make_image with the specific SVG factory
            img = self.qr.make_image(image_factory=factory)
            
            xml_str = img.to_string().decode('utf-8')
            
            if logo_path:
                import base64
                from PIL import Image
                from io import BytesIO
                
                logo = Image.open(logo_path).convert("RGBA")
                
                # SVG viewBox uses modules + borders. img.width gives us the coordinate size.
                size_units = img.width
                
                # Calculate size and position to match the 25% boundary used in PNGs
                logo_size_units = size_units * 0.25
                x_pos = (size_units - logo_size_units) / 2
                y_pos = (size_units - logo_size_units) / 2
                
                # Thumbnail the logo before converting to base64 to keep SVG file size small
                max_px = 300
                logo.thumbnail((max_px, max_px), Image.Resampling.LANCZOS)
                
                buffer = BytesIO()
                logo.save(buffer, format="PNG")
                b64_str = base64.b64encode(buffer.getvalue()).decode('utf-8')
                
                # Inject the <image> tag with base64 data into the SVG XML just before closing tag
                image_tag = f'<image x="{x_pos}" y="{y_pos}" width="{logo_size_units}" height="{logo_size_units}" href="data:image/png;base64,{b64_str}" />'
                xml_str = xml_str.replace("</svg>", f"{image_tag}</svg>")
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(xml_str)
            
            logger.info(f"QR Code SVG saved to: {output_file.absolute()}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate SVG QR Code: {e}")
            return False
