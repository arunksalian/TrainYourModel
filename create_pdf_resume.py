from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_resume_pdf(output_path):
    # Create the PDF object
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    # Set font
    c.setFont("Helvetica-Bold", 14)
    
    # Header
    current_height = height - inch
    c.drawString(inch, current_height, "Alex Thompson")
    current_height -= 20
    c.setFont("Helvetica", 12)
    c.drawString(inch, current_height, "Machine Learning Engineer")
    
    # Contact Information
    current_height -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, current_height, "CONTACT INFORMATION")
    c.setFont("Helvetica", 11)
    current_height -= 20
    c.drawString(inch, current_height, "Email: alex.thompson@email.com")
    current_height -= 15
    c.drawString(inch, current_height, "Phone: (555) 987-6543")
    current_height -= 15
    c.drawString(inch, current_height, "LinkedIn: linkedin.com/in/alexthompson")
    
    # Summary
    current_height -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, current_height, "SUMMARY")
    c.setFont("Helvetica", 11)
    current_height -= 20
    summary = "Experienced Machine Learning Engineer with 5 years of experience in developing "
    summary += "and deploying AI models. Proficient in Python, TensorFlow, and PyTorch."
    c.drawString(inch, current_height, summary)
    
    # Education
    current_height -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, current_height, "EDUCATION")
    c.setFont("Helvetica", 11)
    current_height -= 20
    c.drawString(inch, current_height, "Master of Science in Computer Science")
    current_height -= 15
    c.drawString(inch, current_height, "Stanford University, 2018-2020")
    current_height -= 15
    c.drawString(inch, current_height, "- Specialization in Artificial Intelligence")
    current_height -= 15
    c.drawString(inch, current_height, "- GPA: 3.9/4.0")
    
    # Experience
    current_height -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, current_height, "WORK EXPERIENCE")
    c.setFont("Helvetica", 11)
    
    # Job 1
    current_height -= 20
    c.setFont("Helvetica-Bold", 11)
    c.drawString(inch, current_height, "Senior Machine Learning Engineer, AI Solutions Inc.")
    c.setFont("Helvetica", 11)
    current_height -= 15
    c.drawString(inch, current_height, "2020-Present")
    current_height -= 15
    c.drawString(inch, current_height, "- Lead a team of 5 ML engineers in developing computer vision models")
    current_height -= 15
    c.drawString(inch, current_height, "- Improved model accuracy by 35% using advanced optimization techniques")
    
    # Skills
    current_height -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(inch, current_height, "SKILLS")
    c.setFont("Helvetica", 11)
    current_height -= 20
    c.drawString(inch, current_height, "- Programming: Python, Java, C++")
    current_height -= 15
    c.drawString(inch, current_height, "- ML/DL: TensorFlow, PyTorch, Scikit-learn")
    current_height -= 15
    c.drawString(inch, current_height, "- Tools: Docker, Kubernetes, Git")
    current_height -= 15
    c.drawString(inch, current_height, "- Cloud: AWS, GCP")
    
    # Save the PDF
    c.save()

if __name__ == "__main__":
    # Create the PDF resume
    output_path = "test_documents/test_resume.pdf"
    create_resume_pdf(output_path)
    print(f"Created PDF resume at: {output_path}")
