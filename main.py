import argparse
import sys
from pathlib import Path

# Adjust path to import from src
sys.path.append(str(Path(__file__).parent))
from src.qr_generator import QRCodeGenerator

def main():
    parser = argparse.ArgumentParser(description="Gryphon QR Code Generator")
    parser.add_argument("address", nargs="?", default=None, help="The URL or text address to convert into a QR code.")
    parser.add_argument("-o", "--output", default="qrcodes/qrcode.png", help="Output file path (default: qrcodes/qrcode.png)")
    parser.add_argument("-f", "--fill-color", default="black", help="QR code color (default: black)")
    parser.add_argument("-b", "--back-color", default="white", help="Background color (default: white)")
    parser.add_argument("--cli", action="store_true", help="Força a execução via linha de comando interativa se o endereço não for passado.")
    
    args = parser.parse_args()

    # Se nenhum endereço for passado E a flag --cli não for usada, abrimos a GUI
    if not args.address and not args.cli:
        try:
            from gui import QRCodeApp
            app = QRCodeApp()
            app.mainloop()
            return # Sai do fluxo CLI
        except ImportError as e:
            print(f"Erro ao carregar a interface gráfica: {e}")
            print("Certifique-se de estar rodando o script dentro do ambiente virtual (onde customtkinter está instalado).")
            print("Tente rodar: .\\venv\\Scripts\\python.exe main.py")
            sys.exit(1)

    # Fluxo interativo/CLI
    if not args.address:
        try:
            args.address = input("Por favor, digite o endereço ou texto para gerar o QR Code: ").strip()
        except KeyboardInterrupt:
            print("\nOperação cancelada.")
            sys.exit(0)
            
        if not args.address:
            print("Erro: Nenhum endereço fornecido.")
            sys.exit(1)

    generator = QRCodeGenerator()
    
    print(f"Generating QR Code for: {args.address}")
    success = generator.generate(
        data=args.address,
        output_path=args.output,
        fill_color=args.fill_color,
        back_color=args.back_color
    )
    
    if success:
        print(f"Success! You can find your QR code at {Path(args.output).absolute()}")
    else:
        print("Failed to generate QR Code. Please check the logs.")

if __name__ == "__main__":
    main()
