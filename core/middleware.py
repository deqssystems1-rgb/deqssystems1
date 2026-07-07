from django.http import Http404
from .models import School
from . import models as core_models  # Imports your models module directly

class SchoolTenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower()

        # 1. Identify which school folder path is being viewed
        if 'obisa' in path:
            subdomain = 'obisa'
        else:
            subdomain = 'agawo'

        try:
            # 2. Pull the active school registry record from the database
            current_school = School.objects.get(subdomain=subdomain)
            request.school = current_school
            
            # 3. FIXED ROUTING: Hard lock the school directly into the models variable
            # This forces the SchoolTenantManager to filter data seamlessly on Railway
            core_models.active_school_lock = current_school
        except School.DoesNotExist:
            raise Http404("This school portal does not exist on DEQS Systems.")

        response = self.get_response(request)
        return response
