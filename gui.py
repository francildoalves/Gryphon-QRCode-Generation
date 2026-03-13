import customtkinter as ctk
from PIL import Image
import os
from pathlib import Path

# Imporing from local src
from src.qr_generator import QRCodeGenerator

class QRCodeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup Theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        # Window Config
        self.title("Gryphon QR Generator")
        self.geometry("600x750")
        self.resizable(False, False)
        
        # Generator Instance
        self.generator = QRCodeGenerator()
        
        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Header
        self.header_label = ctk.CTkLabel(
            self, 
            text="Gryphon QR Code Generator", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(pady=(30, 10))

        self.subtitle_label = ctk.CTkLabel(
            self, 
            text="Transforme seus links e textos em QR Códigos instantaneamente",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        self.subtitle_label.pack(pady=(0, 30))

        # Input Frame
        self.input_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.input_frame.pack(fill="x", padx=40)

        self.input_label = ctk.CTkLabel(
            self.input_frame, 
            text="Endereço (URL ou Texto):", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.input_label.pack(anchor="w", pady=(0, 5))

        self.url_entry = ctk.CTkEntry(
            self.input_frame, 
            placeholder_text="https://github.com/fsoares",
            height=45,
            font=ctk.CTkFont(size=14)
        )
        self.url_entry.pack(fill="x", pady=(0, 20))

        # Logo Selection Frame
        self.logo_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.logo_frame.pack(fill="x", padx=40, pady=(0, 20))
        
        self.logo_btn = ctk.CTkButton(
            self.logo_frame,
            text="🖼️ Selecionar Logomarca (Opcional)",
            command=self.select_logo,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "gray90")
        )
        self.logo_btn.pack(side="left")
        
        self.logo_label = ctk.CTkLabel(
            self.logo_frame,
            text="Nenhuma logo selecionada",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.logo_label.pack(side="left", padx=(10, 0))

        # Generate Button
        self.generate_btn = ctk.CTkButton(
            self, 
            text="Gerar QR Code", 
            height=45,
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.handle_generate
        )
        self.generate_btn.pack(pady=10)

        # Status Label
        self.status_label = ctk.CTkLabel(
            self, 
            text="", 
            font=ctk.CTkFont(size=13)
        )
        self.status_label.pack(pady=(5, 5))

        # QR Code Display Area
        self.qr_display_frame = ctk.CTkFrame(self, width=250, height=250, corner_radius=15)
        self.qr_display_frame.pack(pady=(5, 15))
        self.qr_display_frame.pack_propagate(False) # Keep size even if empty

        self.qr_image_label = ctk.CTkLabel(self.qr_display_frame, text="Nenhum QR Code gerado ainda", text_color="gray")
        self.qr_image_label.pack(expand=True)
        
        # Action Buttons Frame (Hidden initially, shown after generation)
        self.actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        
        self.btn_copy = ctk.CTkButton(self.actions_frame, text="Copiar (Área de Transferência)", command=self.copy_to_clipboard, width=200)
        self.btn_copy.grid(row=0, column=0, columnspan=2, pady=5, padx=5)
        
        self.btn_save_png = ctk.CTkButton(self.actions_frame, text="Salvar PNG", command=self.save_png, width=95)
        self.btn_save_png.grid(row=1, column=0, pady=5, padx=5)
        
        self.btn_save_svg = ctk.CTkButton(self.actions_frame, text="Salvar SVG (Vetor)", command=self.save_svg, width=95)
        self.btn_save_svg.grid(row=1, column=1, pady=5, padx=5)

        self.current_address = ""
        self.current_pil_image = None
        self.current_logo_path = None

    def select_logo(self):
        file_path = ctk.filedialog.askopenfilename(
            title="Selecione sua Logomarca",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg *.ico")]
        )
        if file_path:
            self.current_logo_path = file_path
            short_name = Path(file_path).name
            if len(short_name) > 20:
                short_name = short_name[:17] + "..."
            self.logo_label.configure(text=f"✅ {short_name}")

    def handle_generate(self):
        self.current_address = self.url_entry.get().strip()
        
        if not self.current_address:
            self.show_status("⚠️ Por favor, insira um endereço.", color="red")
            return
            
        self.show_status("Gerando...", color="gray")
        self.update() # Force UI update

        try:
            # Generate raw image wrapper from qrcode with optional logo
            raw_qr = self.generator.generate_image(
                data=self.current_address, 
                fill_color="black", 
                back_color="white",
                logo_path=self.current_logo_path
            )
            
            # Extract the actual PIL Image object so it's compatible with CustomTkinter and our clipboard tools
            if hasattr(raw_qr, "get_image"):
                self.current_pil_image = raw_qr.get_image()
            else:
                self.current_pil_image = raw_qr
            
            # Display it
            self.display_qr(self.current_pil_image)
            self.show_status("✅ QR Code gerado!", color="green")
            
            # Show action buttons
            self.actions_frame.pack(pady=10)
            
        except Exception as e:
            self.show_status("❌ Falha ao gerar QR Code.", color="red")
            print(f"Error: {e}")

    def show_status(self, text, color):
        self.status_label.configure(text=text, text_color=color)

    def display_qr(self, qr_image):
        try:
            # Extrair a verdadeira imagem do Pillow do wrapper do qrcode
            if hasattr(qr_image, "get_image"):
                real_pil_image = qr_image.get_image()
            else:
                real_pil_image = qr_image

            # Criar a imagem CTk e guardar uma referência em self para 
            # não ser varrida pelo Garbage Collector do Python
            self.current_ctk_image = ctk.CTkImage(light_image=real_pil_image, dark_image=real_pil_image, size=(200, 200))
            
            self.qr_image_label.configure(image=self.current_ctk_image, text="")
        except Exception as e:
            self.show_status(f"Erro ao exibir imagem: {e}", color="red")

    def copy_to_clipboard(self):
        from src.clipboard import copy_image_to_clipboard
        if self.current_pil_image:
            success = copy_image_to_clipboard(self.current_pil_image)
            if success:
                self.show_status("✅ Copiado para a Área de Transferência!", color="green")
            else:
                self.show_status("❌ Falha ao copiar formato.", color="red")
                
    def save_png(self):
        if not self.current_pil_image: return
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialfile="qrcode.png",
            title="Salvar QR Code como Imagem"
        )
        if file_path:
            self.current_pil_image.save(file_path)
            self.show_status("✅ PNG Salvo com sucesso!", color="green")

    def save_svg(self):
        if not self.current_address: return
        file_path = ctk.filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("Scalable Vector Graphics", "*.svg")],
            initialfile="qrcode_vetor.svg",
            title="Salvar QR Code como Vetor"
        )
        if file_path:
            success = self.generator.generate_svg(self.current_address, file_path)
            if success:
                self.show_status("✅ SVG Salvo com sucesso! Editável no Canva.", color="green")
            else:
                self.show_status("❌ Falha ao salvar SVG.", color="red")

if __name__ == "__main__":
    app = QRCodeApp()
    app.mainloop()
