from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Import all your core models safely
from .models import Teacher, Student, Allocation, Mark, Book, BorrowRecord, Fine

# =====================================================
# 👤 TEACHER USER LINKING GATEWAY (INLINE OVERRIDE)
# =====================================================

class TeacherProfileInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Portal Link Profile'
    fk_name = 'user'

class UserAdmin(BaseUserAdmin):
    inlines = (TeacherProfileInline, )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_teacher_phone')
    
    def get_teacher_phone(self, obj):
        try:
            return obj.teacher_profile.phone
        except:
            return "-"
    get_teacher_phone.short_description = 'Linked Phone Contact'

# Unregister the default User Admin configuration and apply our custom link gateway
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# =====================================================
# 📊 SCHOOL MANAGEMENT REGISTRIES
# =====================================================

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone')
    search_fields = ('name', 'phone')

@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'grade', 'total_lessons')
    list_filter = ('grade', 'subject', 'teacher')
    search_fields = ('teacher__name', 'subject')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'student_name', 'grade', 'parent_name')
    list_filter = ('grade',)
    search_fields = ('student_name', 'admission_number', 'parent_phone')

@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'marks', 'term', 'year')
    list_filter = ('term', 'year', 'subject')
    search_fields = ('student__student_name', 'student__admission_number', 'subject')

# =====================================================
# 📚 LIBRARY ERP MODULE REGISTRIES
# =====================================================

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'grade', 'available_copies', 'total_copies')
    list_filter = ('grade',)
    search_fields = ('title', 'author')

@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'member_type', 'book', 'status', 'borrow_date', 'due_date')
    list_filter = ('status', 'member_type')
    search_fields = ('member_name', 'book__title')

@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('record', 'amount', 'is_paid')
    list_filter = ('is_paid',)

# Keep your DigitalBook model registered at the bottom
try:
    from .models import DigitalBook
    @admin.register(DigitalBook)
    class DigitalBookAdmin(admin.ModelAdmin):
        list_display = ('title', 'subject', 'book_type', 'uploaded_at')
        search_fields = ('title', 'subject')
        list_filter = ('book_type', 'subject')
except ImportError:
    pass
