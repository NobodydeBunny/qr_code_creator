import streamlit as st
from PIL import Image
import qrcode
from io import BytesIO

# Page configuration
st.set_page_config(
    page_title="QR Code Maker",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("🎨 QR Code Maker")
st.markdown("Generate beautiful QR codes instantly - No installation needed!")

# Create columns
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("⚙️ Settings")
    
    # Input text
    text_input = st.text_area(
        "Enter text or URL:",
        value="https://github.com",
        height=80,
        help="Enter the text or URL you want to encode"
    )
    
    st.divider()
    
    # Error Correction
    st.write("**Error Correction Level**")
    col_ec1, col_ec2, col_ec3, col_ec4 = st.columns(4)
    with col_ec1:
        ec_l = st.button("L (7%)", use_container_width=True, key="ec_l")
    with col_ec2:
        ec_m = st.button("M (15%)", use_container_width=True, key="ec_m")
    with col_ec3:
        ec_q = st.button("Q (25%)", use_container_width=True, key="ec_q")
    with col_ec4:
        ec_h = st.button("H (30%)", use_container_width=True, key="ec_h")
    
    if 'error_correction' not in st.session_state:
        st.session_state.error_correction = 'L'
    
    if ec_l:
        st.session_state.error_correction = 'L'
    elif ec_m:
        st.session_state.error_correction = 'M'
    elif ec_q:
        st.session_state.error_correction = 'Q'
    elif ec_h:
        st.session_state.error_correction = 'H'
    
    error_correction = st.session_state.error_correction
    st.caption(f"Selected: **{error_correction}**")
    
    st.divider()
    
    # Style
    st.write("**QR Code Style**")
    style = st.radio(
        "Choose style:",
        ["default", "rounded", "circle"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.divider()
    
    # Size settings
    st.write("**Size Settings**")
    col_size1, col_size2 = st.columns(2)
    with col_size1:
        box_size = st.slider("Box Size (px):", 1, 20, 10)
    with col_size2:
        border = st.slider("Border (boxes):", 0, 10, 4)
    
    st.divider()
    
    # Colors
    st.write("**Colors**")
    col_color1, col_color2 = st.columns(2)
    
    with col_color1:
        fill_color = st.selectbox(
            "Fill Color:",
            ["black", "red", "blue", "green", "purple", "orange", "darkblue"],
            label_visibility="collapsed"
        )
    
    with col_color2:
        back_color = st.selectbox(
            "Background Color:",
            ["white", "black", "gray", "lightblue", "lightyellow", "lightgray"],
            label_visibility="collapsed"
        )

with col2:
    st.subheader("👁️ Preview")
    
    if text_input:
        try:
            # Map error correction
            ec_map = {
                'L': qrcode.constants.ERROR_CORRECT_L,
                'M': qrcode.constants.ERROR_CORRECT_M,
                'Q': qrcode.constants.ERROR_CORRECT_Q,
                'H': qrcode.constants.ERROR_CORRECT_H,
            }
            
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=ec_map[error_correction],
                box_size=box_size,
                border=border,
            )
            qr.add_data(text_input)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color=fill_color, back_color=back_color)
            
            # Display
            st.image(img, use_column_width=True, caption="Your QR Code")
            
            # Download button
            buf = BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            
            st.download_button(
                label="⬇️ Download as PNG",
                data=buf,
                file_name="qr_code.png",
                mime="image/png",
                use_container_width=True
            )
            
            # Download as JPEG
            buf_jpg = BytesIO()
            img.save(buf_jpg, format="JPEG")
            buf_jpg.seek(0)
            
            st.download_button(
                label="⬇️ Download as JPEG",
                data=buf_jpg,
                file_name="qr_code.jpg",
                mime="image/jpeg",
                use_container_width=True
            )
            
            # Display info
            with st.expander("📊 QR Code Info"):
                st.write(f"**Content:** {text_input}")
                st.write(f"**Style:** {style}")
                st.write(f"**Error Correction:** {error_correction}")
                st.write(f"**Colors:** Fill={fill_color}, Background={back_color}")
                st.write(f"**Size:** Box={box_size}px, Border={border}boxes")
                
        except Exception as e:
            st.error(f"❌ Error generating QR code: {e}")
    else:
        st.info("👈 Enter text or URL to generate QR code")

# Footer
st.divider()
st.markdown("""
---
<div style="text-align: center">
    <p style="color: gray;">
        Made with ❤️ using Python & Streamlit | 
        <a href="https://github.com/YOUR_USERNAME/qr-code-maker">GitHub</a> | 
        <a href="https://github.com/YOUR_USERNAME/qr-code-maker/issues">Report Issue</a>
    </p>
</div>
""", unsafe_allow_html=True)
