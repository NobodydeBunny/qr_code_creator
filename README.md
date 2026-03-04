# QR Code Maker 🎨

A simple, elegant, and feature-rich QR code generator with both GUI and CLI support. Generate beautiful QR codes with custom styles, colors, and error correction levels.

## Features ✨

- **Live Preview** - See your QR code instantly as you type
- **Multiple Styles** - Choose from default, rounded, or circle styles
- **Custom Colors** - Customize fill and background colors
- **Error Correction** - 4 levels of error correction (L, M, Q, H)
- **Adjustable Size** - Control box size and border thickness
- **Easy to Save** - Save as PNG or JPEG
- **GUI & CLI** - Both graphical and command-line interfaces
- **Cross-Platform** - Works on Windows, macOS, and Linux

## Installation

### Option 1: Python Script (Recommended for Developers)

**Requirements:**
- Python 3.8 or higher
- pip (Python package manager)

**Step 1:** Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/qr-code-maker.git
cd qr-code-maker
```

**Step 2:** Install dependencies
```bash
pip install qrcode[pil] --break-system-packages
```

**Step 3:** Run the application
```bash
python qr_code_maker.py
```

### Option 2: Executable (Windows Only - No Python Required)

1. Download the latest `.exe` file from [Releases](https://github.com/YOUR_USERNAME/qr-code-maker/releases)
2. Double-click `QRCodeMaker.exe`
3. Done! No installation needed.

**Download:** [QRCodeMaker.exe (Latest Release)](https://github.com/YOUR_USERNAME/qr-code-maker/releases/latest)

### Option 3: Web App (Coming Soon)

A web version will be available at: `https://qr-code-maker.github.io`

## Usage

### GUI Mode (Easiest)

```bash
python qr_code_maker.py
```

Then:
1. Enter your text or URL
2. Customize colors, style, and size
3. See the preview instantly
4. Click "Save QR Code" to save it

### Command Line Mode

Generate a QR code from the terminal:

```bash
# Basic usage
python qr_code_maker.py --text "Hello World" --output my_qr.png

# With custom style
python qr_code_maker.py --text "https://example.com" --style rounded --output qr.png

# With custom colors
python qr_code_maker.py --text "Secret" --fill-color blue --back-color lightblue --output colored.png

# With error correction
python qr_code_maker.py --text "Data" --error-correction H --output secure.png
```

### Command Line Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--text` | string | - | Text or URL to encode |
| `--output` | filename | qr_code.png | Output file path |
| `--style` | default, rounded, circle | default | QR code style |
| `--error-correction` | L, M, Q, H | L | Error correction level |
| `--box-size` | 1-20 | 10 | Size of each box in pixels |
| `--border` | 0-10 | 4 | Border size in boxes |
| `--fill-color` | color name | black | QR code color |
| `--back-color` | color name | white | Background color |

**Color Examples:** black, red, blue, green, purple, white, gray, lightblue

## Error Correction Levels

- **L** (Low) - Recovers 7% of data
- **M** (Medium) - Recovers 15% of data
- **Q** (Quartile) - Recovers 25% of data
- **H** (High) - Recovers 30% of data

Use higher levels if your QR code will be printed or used in environments where it might be partially obscured.

## Screenshots

### GUI Interface
```
┌─────────────────────────────────────────┐
│  QR Code Maker                          │
├──────────────┬──────────────────────────┤
│ Controls     │  Preview                 │
│              │  [Large QR Code Preview] │
│ • Text Input │                          │
│ • Colors     │                          │
│ • Size       │                          │
│ • Buttons    │                          │
└──────────────┴──────────────────────────┘
```

## Examples

### Create a simple QR code
```bash
python qr_code_maker.py --text "Hello World"
# Creates: qr_code.png
```

### Create a styled QR code for a website
```bash
python qr_code_maker.py \
  --text "https://mywebsite.com" \
  --style rounded \
  --fill-color blue \
  --output website_qr.png
```

### Create a secure QR code with high error correction
```bash
python qr_code_maker.py \
  --text "Important Data" \
  --error-correction H \
  --box-size 12 \
  --output secure.png
```

### Create a colorful QR code
```bash
python qr_code_maker.py \
  --text "Colorful" \
  --fill-color purple \
  --back-color lightblue \
  --style circle \
  --output colorful.png
```

## Requirements

### Python Version
- Python 3.8 or higher

### Dependencies
- `qrcode[pil]` - For QR code generation and image manipulation
- `Pillow` - Image processing (included with qrcode[pil])
- `tkinter` - GUI (included with Python)

Install all dependencies:
```bash
pip install qrcode[pil] --break-system-packages
```

## Creating a Windows EXE (For Distribution)

If you want to create an executable file to share with others:

**Step 1:** Install PyInstaller
```bash
pip install pyinstaller --break-system-packages
```

**Step 2:** Build the EXE
```bash
pyinstaller --onefile --windowed --icon=icon.ico qr_code_maker.py
```

**Step 3:** Find your EXE
```
dist/qr_code_maker.exe
```

Users can then download and run this `.exe` file without needing Python installed!

## Converting to Web App

To create a web version, you can use:
- **Streamlit** - Easiest Python web framework
- **Flask** - More customizable
- **React** - For a professional web app

Example with Streamlit:
```bash
pip install streamlit --break-system-packages
streamlit run app.py
```

## Troubleshooting

### "Module not found" Error
```bash
pip install qrcode[pil] --break-system-packages
```

### GUI window doesn't appear (Linux)
```bash
sudo apt-get install python3-tk
```

### EXE file is too large
Use `--onefile` with UPX compression:
```bash
pyinstaller --onefile --upx-dir=path/to/upx qr_code_maker.py
```

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Future Features 🚀

- [ ] Web version (Streamlit/Flask)
- [ ] Batch QR code generation
- [ ] QR code with logo
- [ ] Custom fonts
- [ ] Dark mode
- [ ] More color palettes
- [ ] QR code reader/decoder
- [ ] Mobile app (Flutter)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 **Issues** - [Report bugs here](https://github.com/YOUR_USERNAME/qr-code-maker/issues)
- 💬 **Discussions** - [Ask questions here](https://github.com/YOUR_USERNAME/qr-code-maker/discussions)
- ⭐ **Star** - If you like this project, please star it!

## Author

Created with ❤️ by [Your Name](https://github.com/YOUR_USERNAME)

## Acknowledgments

- Built with [qrcode](https://github.com/lincolnloop/python-qrcode)
- Icons from [Tkinter](https://docs.python.org/3/library/tkinter.html)

---

**Made with Python 🐍 | Easy to Use | Free & Open Source**
