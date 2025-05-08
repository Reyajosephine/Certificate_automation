import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Configuration
CERTIFICATE_TEMPLATE = r"templates/Certificate1.jpg"  # Ensure correct path
OUTPUT_FOLDER = "output"
EXCEL_FILE = "logo forge 1.xlsx"
FONT_PATH = r"C:\Windows/Fonts/arial.ttf"  # Update if needed
FONT_SIZE = 55
TEXT_X, TEXT_Y = 800, 550  # Adjust coordinates as needed
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Load sender credentials (Use environment variables for security)
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your-mail@gmail.co")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "app password")  # Update securely

# Create output folder if not exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Read Excel data
data = pd.read_excel(EXCEL_FILE)
data.columns = data.columns.str.strip()  # Remove any trailing spaces

# Ensure required columns exist
if "Name" not in data.columns or "Email" not in data.columns:
    print("❌ ERROR: 'Name' or 'Email' column not found in the Excel file!")
    exit()

# Generate certificates
def generate_certificate(name, output_path):
    try:
        template = Image.open(CERTIFICATE_TEMPLATE)
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

        # Add name to certificate
        draw.text((TEXT_X, TEXT_Y), name, fill="black", font=font)

        # Save certificate
        template.save(output_path)
        print(f"✅ Certificate generated for {name}")
    except Exception as e:
        print(f"❌ Error generating certificate for {name}: {e}")

# Send email with attachment
def send_email(to_email, name, certificate_path):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = "Your Certificate of Participation"

        body = f"Dear {name},\n\nCongratulations! Please find attached your certificate of participation.\n\nBest Regards,\nFDCI Team"
        msg.attach(MIMEText(body, "plain"))

        # Attach certificate
        with open(certificate_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(certificate_path)}")
            msg.attach(part)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, to_email, msg.as_string())

        print(f"📧 Email sent to {to_email} successfully!")
    except Exception as e:
        print(f"❌ Error sending email to {to_email}: {e}")

# Main process
for index, row in data.iterrows():
    name = row["Name"]
    email = row["Email"]
    certificate_name = f"{name.replace(' ', '_')}.png"
    certificate_path = os.path.join(OUTPUT_FOLDER, certificate_name)

    # Generate certificate
    generate_certificate(name, certificate_path)

    # Send email
    send_email(email, name, certificate_path)

print("🎉 All certificates generated and emails sent successfully!")
