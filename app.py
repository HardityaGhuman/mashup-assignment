import streamlit as st
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import zipfile
from mashup import create_mashup


def validate_email(email):
    """
    Validate email address format.
    
    Args:
        email: Email address string
    
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def create_zip(file_path):
    """
    Create a zip file containing the mashup.
    
    Args:
        file_path: Path to the mashup file
    
    Returns:
        Path to the created zip file
    """
    zip_path = file_path.replace('.mp3', '.zip')
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    
    return zip_path


def send_email(recipient_email, zip_file_path, singer_name):
    """
    Send email with zip file attachment.
    
    Args:
        recipient_email: Recipient's email address
        zip_file_path: Path to zip file to attach
        singer_name: Singer name for email subject
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Use secrets from st.secrets (loaded at top of file)
        sender = st.secrets["EMAIL_USER"]
        password = st.secrets["EMAIL_PASSWORD"]
        smtp_srv = st.secrets["SMTP_SERVER"]
        smtp_prt = int(st.secrets["SMTP_PORT"])
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = recipient_email
        msg['Subject'] = f"Your {singer_name} Mashup - YouTube Mashup Creator"
        
        # Email body
        body = f"""
Hello!

Your YouTube mashup for {singer_name} is ready!

Please find the attached zip file containing your mashup.

Enjoy your music!

---
YouTube Mashup Creator
Roll Number: 102303230
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach zip file
        with open(zip_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'zip')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename={os.path.basename(zip_file_path)}'
            )
            msg.attach(part)
        
        # Send email using secrets configuration
        server = smtplib.SMTP(smtp_srv, smtp_prt)
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
        server.quit()
        
        return True
    
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False


def main():
    """Main Streamlit app function."""
    
    # Page configuration
    st.set_page_config(
        page_title="YouTube Mashup Creator",
        page_icon="🎵",
        layout="centered"
    )
    
    # Title and description
    st.title("YouTube Mashup Creator")
    st.markdown("**Roll Number:** 102303230")
    st.markdown("---")
    
    # Input form
    with st.form("mashup_form"):
        st.subheader("Create Your Mashup")
        
        singer_name = st.text_input(
            "Singer Name *",
            placeholder="e.g., Ed Sheeran",
            help="Enter the name of the singer/artist"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_videos = st.number_input(
                "Number of Videos *",
                min_value=1,
                max_value=50,
                value=5,
                help="Number of videos to download (1-50)"
            )
        
        with col2:
            duration = st.number_input(
                "Duration (seconds) *",
                min_value=5,
                max_value=600,
                value=20,
                help="Duration to cut from each video (5-600)"
            )
        
        email = st.text_input(
            "Email Address *",
            placeholder="your.email@example.com",
            help="We'll send the mashup zip file to this email"
        )
        
        st.markdown("---")
        submit_button = st.form_submit_button("Create Mashup", use_container_width=True)
    
    # Process form submission
    if submit_button:
        # Validate inputs
        errors = []
        
        if not singer_name or singer_name.strip() == "":
            errors.append("❌ Singer name is required")
        
        if not email or email.strip() == "":
            errors.append("❌ Email address is required")
        elif not validate_email(email):
            errors.append("❌ Invalid email address format")
        
        if errors:
            for error in errors:
                st.error(error)
        else:
            # Show progress
            progress_text = st.empty()
            progress_bar = st.progress(0)
            
            try:
                # Create mashup
                progress_text.text("Downloading videos...")
                progress_bar.progress(20)
                
                output_file = f"mashup_{singer_name.replace(' ', '_')}.mp3"
                
                progress_text.text("Processing audio...")
                progress_bar.progress(40)
                
                mashup_file = create_mashup(singer_name, num_videos, duration, output_file)
                
                progress_text.text("Creating zip file...")
                progress_bar.progress(70)
                
                zip_file = create_zip(mashup_file)
                
                progress_text.text("Sending email...")
                progress_bar.progress(90)
                
                # Send email
                if send_email(email, zip_file, singer_name):
                    progress_bar.progress(100)
                    progress_text.empty()
                    
                    st.success("Mashup created and sent successfully!")
                    
                    st.info(f"Check your email: {email}")
                    
                    # Offer download option
                    with open(zip_file, 'rb') as f:
                        st.download_button(
                            label="Download Mashup (Zip)",
                            data=f,
                            file_name=os.path.basename(zip_file),
                            mime="application/zip"
                        )
                    
                    # Cleanup
                    try:
                        os.remove(mashup_file)
                        os.remove(zip_file)
                    except:
                        pass
                else:
                    st.warning("⚠️ Mashup created but email sending failed. You can download it below.")
                    
                    with open(zip_file, 'rb') as f:
                        st.download_button(
                            label="⬇️ Download Mashup (Zip)",
                            data=f,
                            file_name=os.path.basename(zip_file),
                            mime="application/zip"
                        )
            
            except Exception as e:
                progress_text.empty()
                progress_bar.empty()
                st.error(f"❌ Error: {str(e)}")
                st.info("Please try again with different parameters.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: gray; font-size: 0.9em;'>
            YouTube Mashup Creator | Roll No: 102303230<br>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
