import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agawo_junior.settings')

# 1. Initialize Django settings modules
django.setup()

# 2. RUN AUTOMATIC MULTI-TENANT INITIALIZATION SCRIPT
try:
    from django.contrib.auth.models import User
    from core.models import School, Teacher

    # Ensure Obisa School profile exists in your database volume
    obisa_school, _ = School.objects.get_or_create(
        subdomain="obisa",
        defaults={"name": "Obisa School", "primary_color": "#0000FF"}
    )

    # Ensure Agawo School profile exists in your database volume
    agawo_school, _ = School.objects.get_or_create(
        subdomain="agawo",
        defaults={"name": "Agawo School", "primary_color": "#006633"}
    )

    # Automatically build the administrative login profile for Obisa
    user, u_created = User.objects.get_or_create(
        username="obisa_admin",
        defaults={
            "is_staff": True,
            "is_superuser": True
        }
    )

    if u_created:
        user.set_password("ObisaPass2026!")
        user.save()

    # Connect the user to the Obisa teacher register anchor profile
    Teacher.objects.get_or_create(
        school=obisa_school,
        name="Obisa Headteacher",
        defaults={"user": user}
    )
    print("--- MULTI-TENANT ACCOUNTS PROVISIONED SUCCESSFULLY ON BOOT ---")
except Exception as e:
    print(f"Startup initialization skipped: {e}")

# 3. Hand off execution tracking back to the WSGI application layer
application = get_wsgi_application()
