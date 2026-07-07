from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

# Local app relative imports from core/models.py
from .models import (
    Student, Mark, Teacher, Allocation,
    Book, BorrowRecord, Fine
)

# =========================
# STUDENT RESOURCE
# =========================
class StudentResource(resources.ModelResource):
    class Meta:
        model = Student
        fields = (
            'student_name',
            'admission_number',
            'assessment_number',
            'grade',
            'parent_name',
            'parent_phone',
            'year_of_birth',
        )


@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    resource_class = StudentResource

    list_display = (
        'student_name',
        'admission_number',
        'grade',
    )

    search_fields = (
        'student_name',
        'admission_number',
    )

    list_filter = ('grade',)


# =========================
# MARK RESOURCE
# =========================
class MarkResource(resources.ModelResource):
    student_name = fields.Field(column_name='Student Name')

    class Meta:
        model = Mark
        fields = (
            'student',
            'subject',
            'marks',
            'term',
            'year',
        )

    def dehydrate_student_name(self, obj):
        return obj.student.student_name


@admin.register(Mark)
class MarkAdmin(ImportExportModelAdmin):
    resource_class = MarkResource

    list_display = (
        'student',
        'subject',
        'marks',
        'term',
        'year',
    )

    search_fields = (
        'student__student_name',
        'subject',
    )

    list_filter = (
        'subject',
        'term',
        'year',
    )


# =========================
# TEACHER ADMIN
# =========================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# =========================
# ALLOCATION ADMIN
# =========================
@admin.register(Allocation)
class AllocationAdmin(admin.ModelAdmin):
    list_display = (
        'teacher',
        'subject',
        'grade',
        'singles',
        'doubles',
        'total_lessons',
    )

    list_filter = ('grade', 'subject', 'teacher')


# =========================
# 📚 BOOK ADMIN
# =========================
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'total_copies',
        'available_copies',
    )

    search_fields = ('title', 'author')
    list_filter = ('author',)


# =========================
# 📖 BORROW RECORD ADMIN
# =========================
@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = (
        'member_name',
        'member_type',
        'book',
        'copies',
        'borrow_date',
        'due_date',
        'return_date',
        'status',
    )

    list_filter = (
        'status',
        'member_type',
        'borrow_date',
        'due_date',
    )

    search_fields = (
        'member_name',
        'book__title',
    )


# =========================
# 💰 FINE ADMIN
# =========================
@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = (
        'record',
        'amount',
        'is_paid',
    )

    list_filter = ('is_paid',)

    search_fields = (
        'record__member_name',
        'record__book__title',
    )
