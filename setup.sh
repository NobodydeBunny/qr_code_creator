#!/bin/bash
# QR Code Maker - Setup Script
# Automatically installs dependencies

echo "========================================="
echo "QR Code Maker - Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.8 or higher from https://www.python.org/downloads/"
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed!"
    echo "Please install pip before continuing"
    exit 1
fi

echo "✅ pip found: $(pip3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "This may take a minute..."
echo ""

pip3 install qrcode[pil] --break-system-packages

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation successful!"
    echo ""
    echo "========================================="
    echo "Next Steps:"
    echo "========================================="
    echo ""
    echo "1. To run the GUI:"
    echo "   python3 qr_code_maker.py"
    echo ""
    echo "2. To generate from command line:"
    echo "   python3 qr_code_maker.py --text 'Hello World' --output my_qr.png"
    echo ""
    echo "========================================="
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please try manually:"
    echo "   pip install qrcode[pil]"
    exit 1
fi
