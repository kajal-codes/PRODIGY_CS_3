import streamlit as st
import numpy as np
from PIL import Image
import io
import base64

# Set page configuration
st.set_page_config(
    page_title="Security Tools Suite",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 20px;
    }
    .tool-header {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .success-msg {
        color: #10B981;
        font-weight: bold;
    }
    .error-msg {
        color: #EF4444;
        font-weight: bold;
    }
    .info-box {
        background-color: #E0F2FE;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .password-strong {
        color: #10B981;
        font-weight: bold;
    }
    .password-medium {
        color: #F59E0B;
        font-weight: bold;
    }
    .password-weak {
        color: #EF4444;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-title">Security Tools Suite</p>', unsafe_allow_html=True)

# Sidebar for tool selection
st.sidebar.title("Security Tools")
selected_tool = st.sidebar.radio(
    "Select a tool:",
    ["Caesar Cipher", "Image Encryption", "Password Strength Checker"]
)

# Function definitions
# 1. Caesar Cipher Functions
def caesar_encrypt(text, shift):
    """Encrypt a message using Caesar cipher."""
    result = ""
    
    for char in text:
        if char.isalpha():
            # Determine the ASCII offset based on case
            ascii_offset = ord('A') if char.isupper() else ord('a')
            
            # Apply the shift and wrap around using modulo
            shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            result += chr(shifted)
        else:
            # Keep non-alphabetic characters unchanged
            result += char
            
    return result

def caesar_decrypt(text, shift):
    """Decrypt a message using Caesar cipher."""
    # Decryption is just encryption with the negative shift
    return caesar_encrypt(text, -shift)

# 2. Image Encryption Functions
def encrypt_image(image, key):
    """Encrypt an image by manipulating its pixels."""
    try:
        # Convert to RGB if image has an alpha channel
        if image.mode == 'RGBA':
            image = image.convert('RGB')
            
        # Convert image to numpy array
        img_array = np.array(image)
        
        # Simple encryption: XOR each pixel value with the key
        encrypted_array = np.bitwise_xor(img_array, key).astype(np.uint8)
        
        # Create the encrypted image
        encrypted_img = Image.fromarray(encrypted_array)
        
        return encrypted_img, None
        
    except Exception as e:
        return None, str(e)

def decrypt_image(image, key):
    """Decrypt an image that was encrypted using the encrypt_image function."""
    # For XOR encryption, the decryption process is identical to encryption
    # (using the same key)
    return encrypt_image(image, key)

# 3. Password Strength Checker Functions
def check_password_strength(password):
    """Assess the strength of a password based on various criteria."""
    # Initialize score and feedback list
    score = 0
    feedback = []
    
    # Check length
    length = len(password)
    if length < 8:
        feedback.append("Password is too short. Add more characters.")
    elif length < 12:
        score += 10
        feedback.append("Password has acceptable length, but longer is better.")
    elif length < 16:
        score += 20
        feedback.append("Good password length.")
    else:
        score += 25
        feedback.append("Excellent password length.")
    
    # Check for uppercase letters
    if any(c.isupper() for c in password):
        score += 15
    else:
        feedback.append("Add uppercase letters.")
    
    # Check for lowercase letters
    if any(c.islower() for c in password):
        score += 15
    else:
        feedback.append("Add lowercase letters.")
    
    # Check for numbers
    if any(c.isdigit() for c in password):
        score += 15
    else:
        feedback.append("Add numbers.")
    
    # Check for special characters
    special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?\\"
    if any(c in special_chars for c in password):
        score += 15
    else:
        feedback.append("Add special characters (e.g., !@#$%^&*).")
    
    # Check for common patterns
    common_patterns = ["123", "abc", "qwerty", "password", "admin", "welcome"]
    if any(pattern in password.lower() for pattern in common_patterns):
        score -= 15
        feedback.append("Avoid common patterns and sequences.")
    
    # Check for repeated characters
    if any(password.count(c) > 2 for c in password):
        score -= 10
        feedback.append("Avoid repeating characters.")
    
    # Determine overall strength
    if score < 40:
        strength = "Weak"
        strength_class = "password-weak"
    elif score < 70:
        strength = "Moderate"
        strength_class = "password-medium"
    elif score < 90:
        strength = "Strong"
        strength_class = "password-strong"
    else:
        strength = "Very Strong"
        strength_class = "password-strong"
    
    # If no specific feedback was given (high score), add a positive message
    if not feedback and score >= 90:
        feedback.append("Excellent password!")
    elif not feedback:
        feedback.append("Good password, but could be improved.")
    
    # Ensure score is within 0-100 range
    score = max(0, min(score, 100))
    
    return score, feedback, strength, strength_class

def generate_strong_password():
    """Generate a strong password."""
    import random
    import string
    
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()-_=+[]"
    
    # Ensure at least one of each type
    password = [
        random.choice(lowercase),
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(digits),
        random.choice(special),
        random.choice(special)
    ]
    
    # Add additional random characters
    all_chars = lowercase + uppercase + digits + special
    password.extend(random.choice(all_chars) for _ in range(12))
    
    # Shuffle the password characters
    random.shuffle(password)
    
    # Convert list to string
    return ''.join(password)

def get_image_download_link(img, filename, text):
    """Generate a link to download the image."""
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{img_str}" download="{filename}">{text}</a>'
    return href

# Main app logic based on selected tool
if selected_tool == "Caesar Cipher":
    st.markdown('<p class="tool-header">Caesar Cipher Tool</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    The Caesar cipher is one of the simplest encryption techniques. 
    It works by shifting each letter in the plaintext by a fixed number of positions in the alphabet.
    </div>
    """, unsafe_allow_html=True)
    
    operation = st.radio("Select operation:", ["Encrypt", "Decrypt"])
    
    message = st.text_area("Enter your message:", height=150)
    shift = st.slider("Select shift value:", 1, 25, 3)
    
    if st.button(f"{operation} Message"):
        if not message:
            st.error("Please enter a message.")
        else:
            if operation == "Encrypt":
                result = caesar_encrypt(message, shift)
                st.success("Message encrypted successfully!")
            else:
                result = caesar_decrypt(message, shift)
                st.success("Message decrypted successfully!")
                
            st.text_area("Result:", result, height=150)
            
            # Explanation
            st.markdown("### How it works")
            st.write(f"Each letter in your message was shifted {shift} positions {'forward' if operation == 'Encrypt' else 'backward'} in the alphabet.")
            st.write("For example:")
            
            if operation == "Encrypt":
                example_char = 'A'
                shifted_char = caesar_encrypt(example_char, shift)
                st.write(f"'{example_char}' → '{shifted_char}' (shifted {shift} positions forward)")
            else:
                example_char = 'D'
                shifted_char = caesar_decrypt(example_char, shift)
                st.write(f"'{example_char}' → '{shifted_char}' (shifted {shift} positions backward)")

elif selected_tool == "Image Encryption":
    st.markdown('<p class="tool-header">Image Encryption Tool</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    This tool encrypts images by applying an XOR operation to each pixel value using a numeric key.
    The same key is required for decryption.
    </div>
    """, unsafe_allow_html=True)
    
    operation = st.radio("Select operation:", ["Encrypt", "Decrypt"])
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png", "bmp"])
    key = st.slider("Select encryption key (0-255):", 0, 255, 127)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Display the original image
        st.write("Original Image:")
        st.image(image, width=400)
        
        if st.button(f"{operation} Image"):
            # Process the image
            if operation == "Encrypt":
                result_image, error = encrypt_image(image, key)
            else:
                result_image, error = decrypt_image(image, key)
                
            if error:
                st.error(f"Error processing image: {error}")
            else:
                st.success(f"Image {operation.lower()}ed successfully!")
                
                # Display the processed image
                st.write(f"{operation}ed Image:")
                st.image(result_image, width=400)
                
                # Provide download link
                st.markdown(
                    get_image_download_link(
                        result_image, 
                        f"{operation.lower()}ed_image.png", 
                        f"Download {operation.lower()}ed image"
                    ), 
                    unsafe_allow_html=True
                )
                
                # Explanation
                st.markdown("### How it works")
                st.write("The encryption process applies an XOR operation between each pixel value and your chosen key.")
                st.write("Since XOR is its own inverse, the same key and operation can be used for both encryption and decryption.")

else:  # Password Strength Checker
    st.markdown('<p class="tool-header">Password Strength Checker</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-box">
    This tool evaluates password strength based on length, character diversity, and common patterns.
    Strong passwords use a mix of character types and avoid predictable patterns.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        password = st.text_input("Enter a password to check:", type="password")
    
    with col2:
        if st.button("Generate Strong Password"):
            generated_password = generate_strong_password()
            st.code(generated_password)
            st.info("Copy this password and paste it in the password field to check its strength.")
    
    if password:
        score, feedback, strength, strength_class = check_password_strength(password)
        
        # Display strength with proper styling
        st.markdown(f"<h3>Password Strength: <span class='{strength_class}'>{strength}</span> ({score}/100)</h3>", unsafe_allow_html=True)
        
        # Display progress bar
        st.progress(score/100)
        
        # Display feedback
        st.subheader("Feedback:")
        for item in feedback:
            st.write(f"- {item}")
        
        # Display guidelines
        st.subheader("Guidelines for a strong password:")
        st.write("- At least 12 characters long")
        st.write("- Mix of uppercase and lowercase letters")
        st.write("- Include numbers and special characters")
        st.write("- Avoid common patterns and repeated characters")
        
        # Visualization of password composition
        st.subheader("Password Composition:")
        
        # Prepare data for visualization
        upper_count = sum(1 for c in password if c.isupper())
        lower_count = sum(1 for c in password if c.islower())
        digit_count = sum(1 for c in password if c.isdigit())
        special_chars = "!@#$%^&*()-_=+[]{}|;:'\",.<>/?\\"
        special_count = sum(1 for c in password if c in special_chars)
        
        # Create horizontal bar chart
        composition_data = {
            "Uppercase Letters": upper_count,
            "Lowercase Letters": lower_count,
            "Numbers": digit_count,
            "Special Characters": special_count
        }
        
        # Display the composition data
        for category, count in composition_data.items():
            st.write(f"{category}: {count}")
            st.progress(min(1.0, count/4))  # Scale to make even 1 character visible