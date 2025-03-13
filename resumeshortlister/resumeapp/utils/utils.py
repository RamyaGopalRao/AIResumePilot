import os
from django.db.models import Q
from ..models import Resume, Education, Experience,Skill,JobListing
def handle_uploaded_file(f):
    upload_dir = os.path.join('media', 'uploads')
    upload_dir = os.path.join(os.path.dirname(os.getcwd()), 'media', 'uploads')

    print("Hanlde upload")
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f.name)

    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    print(file_path)
    return file_path

def mark_duplicates():
    duplicates = Resume.objects.values('email', 'phone').annotate(count=models.Count('id')).filter(count__gt=1)
    for duplicate in duplicates:
        duplicate_resumes = Resume.objects.filter(email=duplicate['email'], phone=duplicate['phone'])
        for resume in duplicate_resumes[1:]:
            resume.is_duplicate = True
            resume.save()


from django.db.models import Q


def match_resumes_to_jobs():
    # Dictionary to store matching results
    matching_results = {}

    # Fetch all job listings
    job_listings = JobListing.objects.all()

    for job in job_listings:
        # Fetch required skills for the job
        job_skills = job.required_skills.values_list('name', flat=True)

        # Fetch all resumes
        resumes = Resume.objects.all()

        # List to store matching resumes for the current job
        matched_resumes = []

        for resume in resumes:
            # Convert resume.skills (TextField) into a list of skills
            resume_skills = resume.skills.split(',')

            # Check if any skill in the resume matches the required skills
            if any(skill.strip() in job_skills for skill in resume_skills):
                matched_resumes.append({
                    'resume_id': resume.id,
                    'name': resume.name,
                    'email': resume.email,
                    'phone': resume.phone
                })

        # Add job ID and matched resumes to results
        matching_results[job.id] = matched_resumes

    return matching_results


# Example Usage



