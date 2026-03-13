import qrcode
import qrcode.image.svg
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

class QRCodeGenerator:
    """A class to handle QR Code generation."""
    
    def __init__(self, version: int = 1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size: int = 10, border: int = 4):
        self.qr = qrcode.QRCode(
            version=version,
            error_correction=error_correction,
            box_size=box_size,
            border=border,
        )

    def generate_image(self, data: str, fill_color: str = "black", back_color: str = "white"):
        """Generates and returns the raw PIL Image object."""
        self.qr.clear()
        self.qr.add_data(data)
        self.qr.make(fit=True)
        return self.qr.make_image(fill_color=fill_color, back_color=back_color)

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

    def generate_svg(self, data: str, output_path: str | Path) -> bool:
        """Generates a vector SVG QR code (always black/transparent for editing)."""
        try:
            factory = qrcode.image.svg.SvgPathImage
            self.qr.clear()
            self.qr.add_data(data)
            self.qr.make(fit=True)
            
            # recreate make_image with the specific SVG factory
            img = self.qr.make_image(image_factory=factory)
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            img.save(str(output_file))
            
            logger.info(f"QR Code SVG saved to: {output_file.absolute()}")
            return True
        except Exception as e:
            logger.error(f"Failed to generate SVG QR Code: {e}")
            return False
