from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # Global Admin Panel
    path('admin/', admin.site.urls),

    # ================= TEMPORARY SETUP GATEWAY =================
    # path('setup-obisa-secret-key-system-route/', views.create_obisa_admin_backdoor),

    # ================= AUTHENTICATION =================
    path('agawo/login/', views.login_view, name='login'),
    path('obisa/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ================= DASHBOARD CORE SYSTEM =================
    path('agawo/dashboard/', views.dashboard, name='dashboard'),
    path('obisa/dashboard/', views.dashboard, name='obisa_dashboard'),
    
    path('agawo/teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('obisa/teacher-dashboard/', views.teacher_dashboard, name='obisa_teacher_dashboard'),

    # ================= STUDENT ERP MANAGEMENT =================
    path('agawo/grades/<str:grade>/', views.grade_students, name='grade_students'),
    path('obisa/grades/<str:grade>/', views.grade_students, name='obisa_grade_students'),
    
    path('agawo/student/add/', views.add_student, name='add_student'),
    path('obisa/student/add/', views.add_student, name='obisa_add_student'),

    # Standard global routes for background processing actions
    path('student/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('student/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('add-students-bulk/', views.add_students_bulk, name='add_students_bulk'),

    # ================= MARKS & ASSESSMENTS =================
    path('marks-entry/', views.marks_entry, name='marks_entry'),
    path('marks/add/', views.add_mark, name='add_mark'),
    path('teacher/enter-mark/<int:student_id>/<str:subject>/', views.teacher_enter_mark, name='teacher_enter_mark'),

    # ================= REPORTS =================
    path('marks/view-list/', views.view_list, name='view_list'),
    path('marks/view-list/pdf/', views.download_view_list_pdf, name='download_view_list_pdf'),
    path('report-card/<int:id>/', views.report_card, name='report_card'),
    path('reports/print-all/', views.print_all_reports, name='print_all_reports'),

    # ================= TEACHERS =================
    path('teachers/', views.teachers, name='teachers'),
    path('delete_teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('teachers/registry/', views.teachers_registry, name='teachers_registry'),

    # ================= LESSON ALLOCATION =================
    path('allocate/', views.lesson_allocation, name='lesson_allocation'),
    path('allocate/delete/<int:allocation_id>/', views.delete_allocation, name='delete_allocation'),

    # ================= LIBRARY =================
    path('library/', views.library, name='library'),
    path('library/manage/', views.manage_books, name='manage_books'),
    path('library/book/<int:book_id>/delete/', views.delete_book, name='delete_book'),

    # ================= ACADEMIC MODULES =================
    path("course-books/", views.course_books, name="course_books"),
    path("story-books/", views.story_books, name="story_books"),
    path("schemes/", views.schemes, name="schemes"),
    path('reports/', views.reports, name='reports'),
    path('fees/', views.fees, name='fees'),
    path('timetable/generate/', views.generate_timetable, name='generate_timetable'),

    # ================= PRO DOCS =================
    path('pro-docs/', views.pro_docs, name='pro_docs'),
    path('pro-docs/generate-lesson-plan/', views.generate_lesson_plan, name='generate_lesson_plan'),

    # ================= PORTALS =================
    path('students-portal/', views.students_portal_view, name='students_portal'),
    path('students-portal/library/', views.digital_library_view, name='digital_library'),

    # ================= API =================
    path('api/get-grade-subjects/', views.get_grade_subjects_api, name='api_get_grade_subjects'),
    
    # Root Fallback
    path('', views.login_view),
]
