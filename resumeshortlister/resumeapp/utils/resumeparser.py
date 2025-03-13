from openai import OpenAI
from PyPDF2 import PdfReader
from docx import Document
import json
import os
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from ..models import Education,Resume,Experience
from django.db.models import Q

# Initialize OpenAI API


def extract_text(file_path):
    text = ""
    # Check if the file is a PDF

    if file_path.endswith('.pdf'):
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text += page.extract_text()
        except Exception as e:
            return f"Error reading PDF file: {e}"

    # Check if the file is a Word document (.docx)
    elif file_path.endswith('.docx') or file_path.endswith('.doc'):
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + '\n'
                print("I am here")
                print(text)
        except Exception as e:
            return f"Error reading Word file: {e}"

    # Unsupported file format
    else:
        return "Unsupported file format. Please provide a .pdf or .docx file."

    return text


def parse_resume(file_path,user_message):
    client = OpenAI(
        api_key="*******"    )

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        store=True,
        messages=[
            {"role": "user", "content": user_message}
        ]
    )

    bottext = completion.choices[0].message.content.strip()
    print(bottext)
    trimmed_str = bottext.replace('```json\n', '').replace('```', '')
    start_index = bottext.find("{")
    end_index = bottext.rfind("}") + 1

    # Extract the JSON-like content
    if start_index != -1 and end_index != -1:
        json_text = bottext[start_index:end_index]
    else:
        return "No valid data found within braces."

    # Clean and convert to Python dictionary
    cleaned_data = json.loads(json_text.replace("'",'"'))
    print(cleaned_data)
    resume_dict=json.loads(cleaned_data.strip())
    return resume_dict




def process_resume(file_path):

        resume_text = extract_text(file_path)


        # Prepare message for parsing

        user_message = f"""Give the extract  details and only degrees in eductaion,company worked for experience with years ,main skills like 'name': '',
                          'email': '',
                          'phone': '',
                          'skills': [],
                          'years':,
                          'education': '',
                          'experience': '' Name:,Education,Skills,from the resume: Name, Email, Phone, Skills, Education, Experience.In eductaion fields are degree,specialization,institution and year,In expereince give position,company and years .Calculate expereince as total years of experience starting from the first job and put it in years field\n\nResume Text: {resume_text}"""

        resume_dict = parse_resume(file_path, user_message)
        print(resume_dict,"Here")
        if not resume_dict:
            print(f"Failed to extract details from {file_path}")
            return

        # Check for duplicates
        existing_resume = Resume.objects.filter(email=resume_dict['email'], phone=resume_dict['phone']).first()
        if existing_resume:
            existing_resume.is_duplicate = True
            existing_resume.save()
        else:
            print("I am here")
            # Create a new Resume
            resume = Resume.objects.create(
                name=resume_dict['name'],
                email=resume_dict['email'],
                phone=resume_dict['phone'],
                skills=", ".join(resume_dict['skills']),
                years=resume_dict["years"]

            )
            print("Resume done")
            # Create related Education entries
            for edu in resume_dict['education']:
                Education.objects.create(
                    resume=resume,
                    degree=edu['degree'],
                    field=edu['specialization'],
                    institution=edu['institution'],
                    year=edu['year']
                )
            print("Education done")
            # Create related Experience entries
            for exp in resume_dict['experience']:
                Experience.objects.create(
                    resume=resume,
                    position=exp['position'],
                    company=exp['company'],
                    duration=exp['years']
                )
            print("Experince done")
        print(f"Processed {file_path} successfully.")



def process_resumes_from_folder(folder_path):
    # Get a list of all files in the folder
    file_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]

    # Use ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor(max_workers=5) as executor:  # Adjust `max_workers` based on system capacity
        executor.map(process_resume, file_paths)

def filter_resumes_by_skills(required_skills):
    query = Q()
    for skill in required_skills:
        query &= Q(skills__icontains=skill)

    return Resume.objects.filter(query)

