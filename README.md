# Gryphon QR Code Generator

Solução em Python para gerar QR Codes a partir de endereços (URLs ou textos), com suporte nativo a Interface Gráfica (GUI) moderna e exportações em Vetor (SVG) integradas.

## 🌟 Funcionalidades
- **GUI Moderna**: Interface rica gerada com `CustomTkinter` em Dark Mode e responsiva.
- **Vetor Nativo (SVG)**: Exporte QR Codes perfeitos sem perda de qualidade para edição no Canva/Illustrator com fundos puramente transparentes (`SvgPathImage`).
- **Imagem Direta (PNG / Clipboard)**: Gere as imagens em memória, permitindo cópia direta (`Ctrl+V`) para a Área de Transferência do Windows através da API nativa da Microsoft.
- **Interface CLI Integrada**: Caso rodado com opções, a mesma arquitetura atua via terminal puro para automação - o script deduz pela inicialização.
- **Architecture de Código Limpa**: Separação clara entre Lógica de Geração (`src/`), Interface Gráfica (`gui.py`) e Ponto de Entrada de Script (`main.py`).

## 🏗️ Estrutura

- `src/qr_generator.py`: Módulo core que contém a lógica de geração dos Pixels (PNG) e Vectors (SVG).
- `src/clipboard.py`: Utilitário para lidar com o *buffer* de memória DIB do ecossistema Microsoft Windows.
- `gui.py`: Classe modular separada responsável por orquestrar a visualização CTK, botões e callbacks dinâmicos.
- `main.py`: Ponto de entrada Híbrido. Aciona a CLI caso existam argumentos textuais anexados na thread original, e se omissos aciona a janela interativa com `customtkinter`.
- `requirements.txt`: Arquivo com as dependências isoladas (qrcode, pillow, customtkinter, pywin32).

## 🚀 Como usar

### 1. Pré-requisitos
Acesse o diretório do projeto e instale as dependências. Recomenda-se o uso de um ambiente virtual (venv).

```bash
python -m venv venv
.\venv\Scripts\pip install -r requirements.txt
```

### 2. Uso da Interface Gráfica
Basta executar o projeto sem propriedades extras. Uma interface limpa será aberta.

```bash
.\venv\Scripts\python.exe main.py
```

### 3. Automação e Terminal CLI
Se quiser enviar via terminal direto:
```bash
.\venv\Scripts\python.exe main.py "https://anadejesus.com" -o "meu_link.png" -f "darkblue" -b "white"
```
Ou forçar CLI com input assistido caso vazio no terminal:
```bash
.\venv\Scripts\python.exe main.py --cli
```

