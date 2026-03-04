import streamlit as st
import qrcode
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="QR Code Maker",
    page_icon="🎨",
    layout="wide"
)

st.title("🎨 QR Code Maker")
st.markdown("Generate beautiful QR codes instantly!")

# Create two columns
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("Settings")
    
    # Text input
    text_input = st.text_area(
        "Enter text or URL:",
        value="https://github.com/NobodydeBunny/qr_code_creator",
        height=100
    )
    
    st.divider()
    
    # Error Correction
    st.write("**Error Correction Level**")
    error_correction = st.radio(
        "Select level:",
        ["L - 7%", "M - 15%", "Q - 25%", "H - 30%"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    ec_map = {
        "L - 7%": qrcode.constants.ERROR_CORRECT_L,
        "M - 15%": qrcode.constants.ERROR_CORRECT_M,
        "Q - 25%": qrcode.constants.ERROR_CORRECT_Q,
        "H - 30%": qrcode.constants.ERROR_CORRECT_H,
    }
    
    st.divider()
    
    # Size settings
    st.write("**Size Settings**")
    box_size = st.slider("Box Size (pixels):", 1, 20, 10)
    border = st.slider("Border (boxes):", 0, 10, 4)
    
    st.divider()
    
    st.info("💡 Tip: Larger box size = bigger QR code, larger file size")

with col2:
    st.subheader("Preview")
    
    if text_input.strip():
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=ec_map[error_correction],
                box_size=box_size,
                border=border,
            )
            
            qr.add_data(text_input)
            qr.make(fit=True)
            
            # Generate image
            qr_image = qr.make_image(fill_color="black", back_color="white")
            
            # Display image
            st.image(qr_image, caption="QR Code", use_column_width=False, width=300)
            
            # Download PNG
            png_buffer = BytesIO()
            qr_image.save(png_buffer, format="PNG")
            png_buffer.seek(0)
            
            st.download_button(
                label="⬇️ Download as PNG",
                data=png_buffer,
                file_name="qr_code.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Download JPEG
            jpeg_buffer = BytesIO()
            qr_image.save(jpeg_buffer, format="JPEG")
            jpeg_buffer.seek(0)
            
            st.download_button(
                label="⬇️ Download as JPEG",
                data=jpeg_buffer,
                file_name="qr_code.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
            
            # Show details
            with st.expander("📊 QR Code Details"):
                st.write(f"**Data:** {text_input}")
                st.write(f"**Error Correction:** {error_correction}")
                st.write(f"**Box Size:** {box_size}px")
                st.write(f"**Border:** {border} boxes")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.write("Try with simpler text or different settings")
    else:
        st.info("👈 Enter text above to generate QR code")

st.divider()
st.markdown("""
---
**QR Code Maker** | [GitHub](https://github.com/NobodydeBunny/qr_code_creator) | [Report Issue](https://github.com/NobodydeBunny/qr_code_creator/issues)
""")
