import os

from django.shortcuts import render, redirect,get_object_or_404
from .models import Resume, Education, Experience,Skill
from django.db.models import Q
from .resumeparser import parse_resume,extract_text_from_pdf
from django.db import IntegrityError,models
from pydantic import ValidationError
from .forms import SkillForm,JobListingForm,JobListing,ResumeFilterForm

def handle_uploaded_file(f):
    try:
        # Create the uploads directory if it doesn't exist
        upload_dir = os.path.join('media', 'uploads')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Construct the file path within the uploads directory
        file_path = os.path.join(upload_dir, f.name)

        # Save the uploaded file to the specified file path
        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        return file_path
    except Exception as e:
        print(f"Error handling uploaded file: {e}")
        return None
def mark_duplicates():
    # Get all resumes grouped by email and phone
    duplicates = Resume.objects.values('email', 'phone').annotate(count=models.Count('id')).filter(count__gt=1)

    for duplicate in duplicates:
        # Mark all but one resume as duplicate
        duplicate_resumes = Resume.objects.filter(email=duplicate['email'], phone=duplicate['phone'])
        for resume in duplicate_resumes[1:]:  # Leave the first one as not duplicate
            resume.is_duplicate = True
            resume.save()
def upload_resume(request):
    try:
        if request.method == 'POST':
            resume_file = request.FILES['resume']
            file_path = handle_uploaded_file(resume_file)
            resume_text = extract_text_from_pdf(file_path)
            if not file_path:
                return render(request, 'resumeapp/upload_resume.html', {'error': 'Failed to handle uploaded file.'})
            user_message = f"""Give the extract  details and only degrees in eductaion,company worked for experience with years ,main skills like 'name': '',
                    'email': '',
                    'phone': '',
                    'skills': [],
                    'years':,
                    'education': '',
                    'experience': '' Name:,Education,Skills,from the resume: Name, Email, Phone, Skills, Education, Experience.In eductaion fields are degree,specialization,institution and year,In expereince give position,company and years .Calculate expereince as total years of experience starting from the first job and put it in years field\n\nResume Text: {resume_text}"""

            resume_dict = parse_resume(file_path,user_message)

            if not resume_dict:
                return render(request, 'resumeapp/upload_resume.html', {'error': 'Failed to extract details from resume.'})

            # Check if a resume with the same email already exists
            existing_resume = Resume.objects.filter(email=resume_dict['email'], phone=resume_dict['phone']).first()


            if existing_resume:
                existing_resume.is_duplicate = True
                existing_resume.save()
            else:
                # Save new resume details to database
                resume = Resume.objects.create(
                    name=resume_dict['name'],
                    email=resume_dict['email'],
                    phone=resume_dict['phone'],
                    skills=", ".join(resume_dict['skills'])
                )

                # Create Education entries
                for edu in resume_dict['education']:
                    Education.objects.create(
                        resume=resume,
                        degree=edu['degree'],
                        field=edu['specialization'],
                        institution=edu['institution'],
                        year=edu['year']
                    )

                # Create Experience entries
                for exp in resume_dict['experience']:
                    Experience.objects.create(
                        resume=resume,
                        position=exp['position'],
                        company=exp['company'],
                        duration=exp['years']
                    )

            return redirect('resume_list')
        return render(request, 'resumeapp/upload_resume.html')

    except IntegrityError as e:
        print(f"Database Integrity Error: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': 'Database error while saving resume details.'})
    except ValidationError as e:
        print(f"Validation Error: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': f'Validation error: {e}'})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': f'An unexpected error occurred: {e}'})

def resume_list(request):
    try:
        resumes = Resume.objects.all()
        return render(request, 'resumeapp/resume_list.html', {'resumes': resumes})
    except Exception as e:
        print(f"Error fetching resumes: {e}")
        return render(request, 'resumeapp/resume_list.html', {'error': 'Failed to fetch resumes.'})
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_skill_success')
    else:
        form = SkillForm()
    return render(request, 'resumeapp/add_skill.html', {'form': form})
def add_skill_success(request):
    return render(request, 'resumeapp/add_skill_success.html')

def add_job_listing(request):
    if request.method == 'POST':
        form = JobListingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('job_listing_success')
    else:
        form = JobListingForm()
    return render(request, 'resumeapp/add_job_listing.html', {'form': form})

def shortlist_jobs(request):
    if request.method == 'POST':
        selected_skills = request.POST.getlist('skills')
        shortlisted_jobs = JobListing.objects.filter(required_skills__in=selected_skills).distinct()
        return render(request, 'shortlist_job', {'jobs': shortlisted_jobs})
    else:
        skills = Skill.objects.all()
        return render(request, 'resumeapp/shortlist_job.html', {'skills': skills})


def joblisting_list(request):
    job_listings = JobListing.objects.all()
    return render(request, 'resumeapp/job_listing_list.html', {'job_listings': job_listings})


def filter_resumes_by_skills(required_skills):
    query = Q()
    for skill in required_skills:
        query &= Q(skills__icontains=skill)

    return Resume.objects.filter(query)

def shortlist_resumes(request):
    resumes = Resume.objects.all()
    resume_details = []
    if request.method == 'POST':
        form = ResumeFilterForm(request.POST)
        if form.is_valid():
            selected_skills = form.cleaned_data['skills']
            if selected_skills:
                resumes = filter_resumes_by_skills(selected_skills)
                print(resumes)
    else:
        form = ResumeFilterForm()

    for resume in resumes:
        print(resume.id)
        education_details = Education.objects.filter(id=resume.id)
        experience_details = Experience.objects.filter(id=resume.id)
        degree_details="".join(edu.degree for edu in education_details)
        exp="".join(edu.duration for edu in experience_details)
        resume_details.append({
            'name':resume.name,
            'email': resume.email,
            'phone':resume.phone,
            'skills': resume.skills,
            'education': degree_details,
            'experience': exp
        })


    return render(request, 'resumeapp/shortlist_resumes.html', {'form': form, 'resume_details':resume_details})



def resume_list(request):
    resumes = Resume.objects.all()
    return render(request, 'resumeapp/resume_list.html', {'resumes': resumes})

def resume_education(request, id):
    resume = get_object_or_404(Resume, id=id)
    education = resume.education.all()
    return render(request, 'resumeapp/resume_education.html', {'education': education})

def resume_experience(request, id):
    resume = get_object_or_404(Resume, id=id)
    experience = resume.experience.all()
    return render(request, 'resumeapp/resume_experience.html', {'experience': experience})


