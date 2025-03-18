from django.shortcuts import render, redirect
from ..models import Skill, JobListing,Resume
from ..forms import SkillForm, JobListingForm

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
        return render(request, 'resumeapp/shortlist_job.html', {'jobs': shortlisted_jobs})
    else:
        skills = Skill.objects.all()
        return render(request, 'resumeapp/shortlist_job.html', {'skills': skills})

def joblisting_list(request):
    job_listings = JobListing.objects.all()
    return render(request, 'resumeapp/job_listing_list.html', {'job_listings': job_listings})





def search_keyword_view(request):
    # Dictionary to store job listings and their matching resumes
    job_matches = []

    # Fetch all job listings
    job_listings = JobListing.objects.all()

    for job in job_listings:
        # Get the skills required for the job
        job_skills = job.required_skills.values_list('name', flat=True)

        # Find resumes that match the job skills
        matching_resumes = []
        for resume in Resume.objects.all():
            # Convert resume skills (comma-separated) into a list
            resume_skills = resume.skills.lower().split(',')
            check=False
            # Initialize experience as 0 if resume.experience is None
            experience = resume.years if resume.years else 0

            check=True

            # Check if experience meets the job's required experience
            if check:

                # Check if any job skill matches the resume skills
                if any(skill.strip().lower() in skillset.lower() for skillset in resume_skills for skill in job_skills):
                    # Append the matching resume details
                    print("matching")
                    matching_resumes.append({
                        'name': resume.name,
                        'skill': resume.skills,  # Ensure this field matches your model
                        'email': resume.email,
                        'phone': resume.phone,
                        'experience': experience  # Use the processed `experience` variable
                    })

        # Append the job and matching resumes

        job_matches.append({
                'job_id': job.id,
                'job_title': job.title,
                'matching_resumes': matching_resumes
            })

    # Pass job matches to the template
    return render(request, 'resumeapp/job_matches.html', {'job_matches': job_matches})



