from django.urls import path

from .views.resume_views import resume_list_view,resume_education,resume_experience,shortlist_resumes,upload_resumes,resume_list_data
from .views.job_views import add_skill,add_skill_success,joblisting_list,add_job_listing,shortlist_jobs,search_keyword_view
from .views.utility_view import send_email_view,send_whatsapp_view
urlpatterns = [
    path('uploadfiles/',upload_resumes,name='upload'),
    path('send-email/', send_email_view, name='send_email'),
    path('send-whatsapp/', send_whatsapp_view, name='send_whatsapp'),
    path('resumes/', resume_list_view, name='resume_list'),
    path('resumes/data/', resume_list_data, name='resume_list_data'),
    path('job_matches/', search_keyword_view, name='job_matches'),
    path('add_skill/', add_skill, name='add_skill'),
    path('add_skill_success/', add_skill_success, name='add_skill_success'),
    path('add_job_listing/', add_job_listing, name='add_job_listing'),
    path('job_listing_success/',joblisting_list,name="job_listing_success"),
    path('shortlist_jobs/', shortlist_jobs, name='shortlist_jobs'),
    path('shortlist_resumes/', shortlist_resumes, name='shortlist_resumes'),
    path('resumes/<int:id>/education/', resume_education, name='resume_education'),
    path('resumes/<int:id>/experience/',resume_experience, name='resume_experience'),
    # Add this line
]


