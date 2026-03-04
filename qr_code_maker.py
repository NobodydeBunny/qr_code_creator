import os
import sys
import argparse
from pathlib import Path
from io import BytesIO

try:
    import qrcode
    from qrcode.image.styledpil import StyledPilImage
    from qrcode.image.styles.moduledrawers import RoundedModuleDrawer, CircleModuleDrawer
    from qrcode.image.styles.colormasks import SolidFillColorMask
except ImportError:
    print("Error: Required library 'qrcode' not found.")
    print("Install it using: pip install qrcode[pil] --break-system-packages")
    sys.exit(1)

try:
    from tkinter import Tk, Frame, Label, Entry, Button, filedialog, messagebox, StringVar, IntVar, Canvas
    from tkinter import ttk
    from PIL import Image, ImageTk
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False


class QRCodeMaker:
    """QR Code Generator with multiple customization options"""
    
    def __init__(self):
        self.version = 1
        self.error_correction = qrcode.constants.ERROR_CORRECT_L
        self.box_size = 10
        self.border = 4
        self.fill_color = "black"
        self.back_color = "white"
    
    def generate_image(self, data, style="default", 
                 fill_color="black", back_color="white"):
        """
        Generate a QR code image and return as PIL Image object
        
        Args:
            data (str): The data to encode
            style (str): Style of QR code ('default', 'rounded', 'circle')
            fill_color (str): Color of the QR code modules
            back_color (str): Background color
            
        Returns:
            PIL Image object or None if error
        """
        try:
            # Create QR code instance
            qr = qrcode.QRCode(
                version=self.version,
                error_correction=self.error_correction,
                box_size=self.box_size,
                border=self.border,
            )
            
            qr.add_data(data)
            qr.make(fit=True)
            
            # Apply styling if PIL is available
            if style == "rounded":
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=RoundedModuleDrawer(),
                    color_mask=SolidFillColorMask(fill_color, back_color)
                )
            elif style == "circle":
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    module_drawer=CircleModuleDrawer(),
                    color_mask=SolidFillColorMask(fill_color, back_color)
                )
            else:
                img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            return img
        
        except Exception as e:
            return None
    
    def generate(self, data, filename, style="default", 
                 fill_color="black", back_color="white"):
        """Save QR code to file"""
        try:
            img = self.generate_image(data, style, fill_color, back_color)
            if img is None:
                return False, "Error generating QR code"
            
            img.save(filename)
            return True, f"QR code saved to {filename}"
        
        except Exception as e:
            return False, f"Error saving QR code: {str(e)}"
    
    def set_error_correction(self, level):
        """Set error correction level (L, M, Q, H)"""
        levels = {
            'L': qrcode.constants.ERROR_CORRECT_L,
            'M': qrcode.constants.ERROR_CORRECT_M,
            'Q': qrcode.constants.ERROR_CORRECT_Q,
            'H': qrcode.constants.ERROR_CORRECT_H,
        }
        self.error_correction = levels.get(level, qrcode.constants.ERROR_CORRECT_L)
    
    def set_box_size(self, size):
        """Set the size of each box in pixels"""
        self.box_size = max(1, int(size))
    
    def set_border(self, border):
        """Set the border size in boxes"""
        self.border = max(0, int(border))


class QRCodeGUI:
    """GUI interface for QR Code Maker"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Maker")
        self.root.geometry("950x600")  # Much wider, less tall
        self.maker = QRCodeMaker()
        self.current_image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the user interface with horizontal layout"""
        # Create main container
        main_container = Frame(self.root)
        main_container.pack(fill="both", expand=True)
        
        # Left panel for controls (scrollable)
        left_panel = Frame(main_container, padx=10, pady=10, width=350)
        left_panel.pack(side="left", fill="both", expand=False)
        left_panel.pack_propagate(False)
        
        # Add scrollbar for left panel
        canvas = Canvas(left_panel, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(left_panel, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Enable mouse wheel scrolling
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Title
        title = Label(scrollable_frame, text="QR Code Maker", font=("Arial", 14, "bold"), bg="white")
        title.pack(pady=10)
        
        # Data input
        Label(scrollable_frame, text="Enter text or URL:", font=("Arial", 9), bg="white").pack(anchor="w")
        self.data_entry = Entry(scrollable_frame, width=40, font=("Arial", 9))
        self.data_entry.pack(fill="x", pady=5, padx=5)
        
        # Error Correction
        Label(scrollable_frame, text="Error Correction:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.error_var = StringVar(value="L")
        error_frame = Frame(scrollable_frame, bg="white")
        error_frame.pack(fill="x", pady=5, padx=5)
        for level in ['L', 'M', 'Q', 'H']:
            ttk.Radiobutton(error_frame, text=level, variable=self.error_var, 
                          value=level, command=self.update_preview).pack(side="left")
        
        # Style
        Label(scrollable_frame, text="QR Code Style:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.style_var = StringVar(value="default")
        style_frame = Frame(scrollable_frame, bg="white")
        style_frame.pack(fill="x", pady=5, padx=5)
        for style in ['default', 'rounded', 'circle']:
            ttk.Radiobutton(style_frame, text=style.capitalize(), variable=self.style_var, 
                          value=style, command=self.update_preview).pack(side="left")
        
        # Box Size
        Label(scrollable_frame, text="Box Size:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.box_size_var = IntVar(value=10)
        box_size_scale = ttk.Scale(scrollable_frame, from_=1, to=20, variable=self.box_size_var, 
                                   orient="horizontal", command=self.on_box_size_change)
        box_size_scale.pack(fill="x", pady=5, padx=5)
        self.box_size_label = Label(scrollable_frame, text="10 px", font=("Arial", 8), bg="white")
        self.box_size_label.pack(anchor="w", padx=5)
        
        # Border Size
        Label(scrollable_frame, text="Border Size:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.border_var = IntVar(value=4)
        border_scale = ttk.Scale(scrollable_frame, from_=0, to=10, variable=self.border_var, 
                                orient="horizontal", command=self.on_border_change)
        border_scale.pack(fill="x", pady=5, padx=5)
        self.border_label = Label(scrollable_frame, text="4 boxes", font=("Arial", 8), bg="white")
        self.border_label.pack(anchor="w", padx=5)
        
        # Colors
        Label(scrollable_frame, text="Colors:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5, pady=(10, 5))
        
        Label(scrollable_frame, text="Fill Color:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.fill_color_var = StringVar(value="black")
        fill_combo = ttk.Combobox(scrollable_frame, textvariable=self.fill_color_var, 
                    values=["black", "red", "blue", "green", "purple"], 
                    width=30, state="readonly")
        fill_combo.pack(fill="x", pady=3, padx=5)
        fill_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        Label(scrollable_frame, text="Background:", font=("Arial", 9), bg="white").pack(anchor="w", padx=5)
        self.back_color_var = StringVar(value="white")
        back_combo = ttk.Combobox(scrollable_frame, textvariable=self.back_color_var, 
                    values=["white", "black", "gray", "lightblue"], 
                    width=30, state="readonly")
        back_combo.pack(fill="x", pady=3, padx=5)
        back_combo.bind("<<ComboboxSelected>>", lambda e: self.update_preview())
        
        # Buttons
        button_frame = Frame(scrollable_frame, bg="white")
        button_frame.pack(fill="x", pady=20, padx=5)
        
        ttk.Button(button_frame, text="Generate", command=self.generate_preview).pack(fill="x", pady=3)
        ttk.Button(button_frame, text="Save QR Code", command=self.save_qr).pack(fill="x", pady=3)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(fill="x", pady=3)
        
        # Status
        self.status_label = Label(scrollable_frame, text="Ready", font=("Arial", 8), fg="blue", bg="white", wraplength=300)
        self.status_label.pack(pady=10, padx=5)
        
        # Right panel for preview
        right_panel = Frame(main_container, padx=10, pady=10, bg="white")
        right_panel.pack(side="right", fill="both", expand=True)
        
        # Preview Label
        preview_title = Label(right_panel, text="QR Code Preview", font=("Arial", 12, "bold"), bg="white")
        preview_title.pack(pady=10)
        
        # Preview Canvas (larger)
        self.preview_canvas = Canvas(right_panel, width=450, height=450, bg="lightgray", relief="sunken", bd=2)
        self.preview_canvas.pack(pady=10, padx=10, fill="both", expand=True)
    
    def on_box_size_change(self, value):
        """Update box size label and preview"""
        self.box_size_label.config(text=f"{int(float(value))} px")
        self.update_preview()
    
    def on_border_change(self, value):
        """Update border label and preview"""
        self.border_label.config(text=f"{int(float(value))} boxes")
        self.update_preview()
    
    def update_preview(self):
        """Update the preview without requiring explicit button click"""
        data = self.data_entry.get().strip()
        if data:
            self.generate_preview()
    
    def display_image_on_canvas(self, img):
        """Display PIL Image on the canvas"""
        try:
            # Resize image to fit canvas (max 300x300)
            max_size = 300
            img_copy = img.copy()
            img_copy.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            
            # Convert to PhotoImage
            self.photo_image = ImageTk.PhotoImage(img_copy)
            
            # Clear canvas and display image
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(150, 150, image=self.photo_image)
            
        except Exception as e:
            self.preview_canvas.delete("all")
            self.preview_canvas.create_text(150, 150, text=f"Error displaying image:\n{str(e)}", fill="red")
    
    def generate_preview(self):
        """Generate QR code and display in canvas"""
        data = self.data_entry.get().strip()
        if not data:
            self.status_label.config(text="Please enter some text or a URL", fg="red")
            return
        
        self.maker.set_error_correction(self.error_var.get())
        self.maker.set_box_size(self.box_size_var.get())
        self.maker.set_border(self.border_var.get())
        
        try:
            img = self.maker.generate_image(
                data, 
                style=self.style_var.get(),
                fill_color=self.fill_color_var.get(),
                back_color=self.back_color_var.get()
            )
            
            if img:
                self.current_image = img
                self.display_image_on_canvas(img)
                self.status_label.config(text="QR code generated! Click 'Save QR Code' to save it.", fg="green")
            else:
                self.status_label.config(text="Error generating QR code", fg="red")
        
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")
    
    def save_qr(self):
        """Save the generated QR code to a file"""
        if self.current_image is None:
            messagebox.showwarning("No QR Code", "Please generate a QR code first")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            self.current_image.save(filename)
            self.status_label.config(text=f"Saved to {filename}", fg="green")
            messagebox.showinfo("Success", f"QR code saved successfully!\n\n{filename}")
        except Exception as e:
            self.status_label.config(text=f"Error saving: {str(e)}", fg="red")
            messagebox.showerror("Error", f"Failed to save QR code:\n{str(e)}")


def main():
    parser = argparse.ArgumentParser(description="QR Code Maker - Generate QR codes easily")
    parser.add_argument("--gui", action="store_true", help="Launch GUI mode")
    parser.add_argument("--text", type=str, help="Text to encode in QR code")
    parser.add_argument("--output", type=str, default="qr_code.png", help="Output filename")
    parser.add_argument("--style", choices=["default", "rounded", "circle"], 
                       default="default", help="QR code style")
    parser.add_argument("--error-correction", choices=["L", "M", "Q", "H"], 
                       default="L", help="Error correction level")
    parser.add_argument("--box-size", type=int, default=10, help="Size of each box in pixels")
    parser.add_argument("--border", type=int, default=4, help="Border size in boxes")
    parser.add_argument("--fill-color", type=str, default="black", help="Fill color")
    parser.add_argument("--back-color", type=str, default="white", help="Background color")
    
    args = parser.parse_args()
    
    # Launch GUI if requested or no text provided
    if args.gui or (not args.text and len(sys.argv) == 1):
        if not HAS_TKINTER:
            print("Error: Tkinter not available. Please install it or use CLI mode with --text")
            sys.exit(1)
        root = Tk()
        gui = QRCodeGUI(root)
        root.mainloop()
    else:
        if not args.text:
            print("Error: No text provided. Use --text to specify content or --gui for GUI mode")
            sys.exit(1)
        
        maker = QRCodeMaker()
        maker.set_error_correction(args.error_correction)
        maker.set_box_size(args.box_size)
        maker.set_border(args.border)
        
        success, message = maker.generate(
            args.text,
            args.output,
            style=args.style,
            fill_color=args.fill_color,
            back_color=args.back_color
        )
        
        print(message)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()