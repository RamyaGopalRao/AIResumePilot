import os
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db import IntegrityError,models
from django.db.models import Case, When,Value
from pydantic import ValidationError
from ..models import Resume, Education, Experience
from ..forms import ResumeFilterForm
from ..utils.utils import handle_uploaded_file, mark_duplicates
from ..utils.resumeparser import extract_text,parse_resume,process_resume,process_resumes_from_folder
from django.http import JsonResponse

from django.core.serializers import serialize
from django.shortcuts import render

def resume_list_view(request):
    resumes = Resume.objects.all().values(
        'id', 'name', 'email', 'phone', 'skills', 'is_duplicate'
    )
    return render(request, 'resumeapp/resume_list.html', {'resumes': list(resumes)})

def upload_resumes(request):
    try:
        if request.method == 'POST':
            # Check for single file upload
            if 'resume' in request.FILES:
                single_file = request.FILES['resume']
                file_path = handle_uploaded_file(single_file)  # Save the file
                process_resume(file_path)  # Process the resume

            # Check for folder upload
            if 'folder' in request.FILES:
                folder_files = request.FILES.getlist('folder')  # Get all files in the folder
                for file in folder_files:
                    file_path = handle_uploaded_file(file)  # Save each file
                    process_resume(file_path)  # Process each file

            return redirect('resume_list')

    except Exception as e:
        print(f"Error during upload: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': 'An error occurred during upload.'})

    return render(request, 'resumeapp/upload_resume.html')


def upload_folder(request):
    if request.method == 'POST':
        folder_path = request.POST.get('folder_path')
        if not folder_path or not os.path.exists(folder_path):
            return render(request, 'resumeapp/upload_folder.html', {'error': 'Invalid folder path.'})

        # Process the folder
        process_resumes_from_folder(folder_path)

        return redirect('resume_list')
    return render(request, 'resumeapp/upload_folder.html')


def upload_resume(request):
    try:
        if request.method == 'POST':
            resume_file = request.FILES['resume']
            file_path = handle_uploaded_file(resume_file)
            resume_text = extract_text(file_path)

            if not file_path:
                return render(request, 'resumeapp/upload_resume.html', {'error': 'Failed to handle uploaded file.'})

            user_message = f"""Extract details from the resume: {resume_text}"""
            resume_dict = parse_resume(file_path, user_message)

            if not resume_dict:
                return render(request, 'resumeapp/upload_resume.html',
                              {'error': 'Failed to extract details from resume.'})

            # Check for duplicates
            existing_resume = Resume.objects.filter(email=resume_dict['email'], phone=resume_dict['phone']).first()
            if existing_resume:
                existing_resume.is_duplicate = True
                existing_resume.save()
            else:
                # Save resume details
                resume = Resume.objects.create(
                    name=resume_dict['name'],
                    email=resume_dict['email'],
                    phone=resume_dict['phone'],
                    skills=", ".join(resume_dict['skills'])
                )
                # Save education and experience
                for edu in resume_dict['education']:
                    Education.objects.create(
                        resume=resume,
                        degree=edu['degree'],
                        field=edu['specialization'],
                        institution=edu['institution'],
                        year=edu['year']
                    )
                for exp in resume_dict['experience']:
                    Experience.objects.create(
                        resume=resume,
                        position=exp['position'],
                        company=exp['company'],
                        duration=exp['years']
                    )
            return redirect('resume_list')

        return render(request, 'resumeapp/upload_resume.html')

    except (IntegrityError, ValidationError) as e:
        print(f"Error: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': str(e)})
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return render(request, 'resumeapp/upload_resume.html', {'error': 'An unexpected error occurred.'})




def resume_list(request):
    resumes = Resume.objects.all().values(
        "id", "name", "email", "phone", "skills", "is_duplicate"
    )

    # Add additional fields like Education and Experience as strings
    data = []
    for resume in resumes:
        education_details = Education.objects.filter(resume_id=resume['id'])
        experience_details = Experience.objects.filter(resume_id=resume['id'])

        # Format education and experience data
        education_str = ", ".join(
            [f"{edu.degree} ({edu.year})" for edu in education_details]
        )
        experience_str = ", ".join(
            [f"{exp.position} at {exp.company} ({exp.duration})" for exp in experience_details]
        )

        # Append full record for each resume
        data.append({
            "id": resume["id"],
            "name": resume["name"],
            "email": resume["email"],
            "phone": resume["phone"],
            "skills": resume["skills"],
            "education": education_str,
            "experience": experience_str,
            "is_duplicate": "Yes" if resume["is_duplicate"] else "No"
        })

    return JsonResponse(data, safe=False)

def resume_list_data(request):
    try:
        resumes = Resume.objects.annotate(
            is_duplicate_label=Case(
                When(is_duplicate=True, then=Value("Yes")),
                When(is_duplicate=False, then=Value("No")),
                output_field=models.CharField(),
            ))
        return render(request, 'resumeapp/resume_list.html', {'resumes': resumes})
    except Exception as e:
        print(f"Error: {e}")
        return render(request, 'resumeapp/resume_list.html', {'error': 'Failed to fetch resumes.'})


def resume_education(request, id):
    resume = get_object_or_404(Resume, id=id)
    education = resume.education.all()
    return render(request, 'resumeapp/resume_education.html', {'education': education})


def resume_experience(request, id):
    resume = get_object_or_404(Resume, id=id)
    experience = resume.experience.all()
    return render(request, 'resumeapp/resume_experience.html', {'experience': experience})


def shortlist_resumes(request):
    resumes = Resume.objects.all()
    resume_details = []

    if request.method == 'POST':
        form = ResumeFilterForm(request.POST)
        if form.is_valid():
            selected_skills = form.cleaned_data['skills']
            if selected_skills:
                resumes = filter_resumes_by_skills(selected_skills)
    else:
        form = ResumeFilterForm()

    for resume in resumes:
        education_details = Education.objects.filter(resume=resume)
        experience_details = Experience.objects.filter(resume=resume)
        degree_details = ", ".join(edu.degree for edu in education_details)
        exp = ", ".join(exp.duration for exp in experience_details)
        resume_details.append({
            'name': resume.name,
            'email': resume.email,
            'phone': resume.phone,
            'skills': resume.skills,
            'education': degree_details,
            'experience': exp
        })

    return render(request, 'resumeapp/shortlist_resumes.html', {'form': form, 'resume_details': resume_details})
