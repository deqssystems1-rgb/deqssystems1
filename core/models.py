from django.db import models
from datetime import date
from django.contrib.auth.models import User  # IMPORTED FOR USER AUTHENTICATION
import threading

# =====================================================
# NEW: THREAD REPOSITORY STORAGE ENGINE FOR THE MANAGER
# =====================================================
_thread_locals = threading.local()

class SchoolTenantManager(models.Manager):
    def get_queryset(self):
        # Dynamically grabs the school isolated by our middleware for this request thread
        active_school = getattr(_thread_locals, 'active_school', None)
        if active_school:
            return super().get_queryset().filter(school=active_school)
        return super().get_queryset()

# =====================================================
# NEW: MULTI-TENANT SCHOOL MODEL (THE CORE REGISTRY)
# =====================================================

class School(models.Model):
    subdomain = models.CharField(max_length=100, unique=True, help_text="e.g., 'agawo' or 'alliance'")
    name = models.CharField(max_length=255, help_text="The school's full official name")
    primary_color = models.CharField(max_length=7, default="#006633", help_text="Hex code (e.g., #FF0000)")
    logo_url = models.TextField(blank=True, null=True, help_text="URL path to their custom logo badge")

    def __str__(self):
        return self.name

# =====================================================
# SHARED CHOICES (UPDATED TO UNIFY LOWER & UPPER CLASSES)
# =====================================================

SUBJECT_CHOICES = [
    # Junior Secondary Tracks (Grades 7 - 9)
    ("Mathematics", "Mathematics"),
    ("English", "English"),
    ("Kiswahili", "Kiswahili"),
    ("Integrated Science", "Integrated Science"),
    ("Social Studies", "Social Studies"),
    ("Religious Education", "Religious Education"),
    ("Pre-Technical Studies", "Pre-Technical Studies"),
    ("Health Education", "Health Education"),
    ("Creative Arts & Sports", "Creative Arts & Sports"),
    ("Agriculture & Nutrition", "Agriculture & Nutrition"),
    
    # Lower & Upper Primary Tracks (Grades 1 - 6 CBC Core)
    ("Maths", "Maths"),
    ("Creative Art", "Creative Art"),
    ("Environmental", "Environmental"),
    ("Science", "Science"),
    ("Agriculture", "Agriculture"),
    ("Home Science", "Home Science"),
    ("CRE", "CRE"),
    ("Religious Education", "Religious Education"),
]

# Extended to include Pre-Primary options matching your front-end template configurations
GRADE_CHOICES = [
    ("PP1", "Pre-Primary 1 (PP1)"),
    ("PP2", "Pre-Primary 2 (PP2)"),
] + [(f"Grade {i}", f"Grade {i}") for i in range(1, 10)]

BOOK_PUBLISHER_CHOICES = [
    ("KLB", "Kenya Literature Bureau (KLB Top Scholar)"),
    ("Longhorn", "Longhorn Publishers"),
    ("Oxford", "Oxford University Press"),
    ("Moran", "Moran Publishers"),
    ("Spotlight", "Spotlight CBC Course Book"),
]

# =====================================================
# TEACHER MODEL (UPDATED WITH SCHOOL LINK & ENGINE MANAGER)
# =====================================================

class Teacher(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="teachers", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="teacher_profile", 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100) # REMOVED unique=True so different schools can have teachers with the same name
    phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ["name"]
        unique_together = ("school", "name") # Unique per school instead

    def __str__(self):
        return f"{self.name} ({self.school.name if self.school else 'No School'})"

# =====================================================
# STUDENT MODEL (UPDATED WITH SCHOOL LINK & ENGINE MANAGER)
# =====================================================

class Student(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="students", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    student_name = models.CharField(max_length=200)
    admission_number = models.CharField(max_length=20) # REMOVED unique=True so School B can use an admission number that School A already has
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    parent_name = models.CharField(max_length=200, blank=True, null=True)
    parent_phone = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        ordering = ["student_name"]
        unique_together = ("school", "admission_number") # Adm number is unique only inside the same school

    def __str__(self):
        return f"{self.student_name} ({self.admission_number}) - {self.school.name if self.school else ''}"

# =====================================================
# ALLOCATION & MARKS (UPDATED WITH SCHOOL LINKS & ENGINE MANAGERS)
# =====================================================

class Allocation(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="allocations", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="allocations")
    subject = models.CharField(max_length=100)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    singles = models.PositiveIntegerField(default=0)
    doubles = models.PositiveIntegerField(default=0)
    total_lessons = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["teacher", "grade"]

    def save(self, *args, **kwargs):
        self.total_lessons = self.singles + (self.doubles * 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher.name} - {self.subject} ({self.grade})"

class Mark(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="marks", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="marks")
    subject = models.CharField(max_length=100)
    marks = models.PositiveIntegerField(default=0)
    term = models.PositiveIntegerField(default=1)
    year = models.PositiveIntegerField(default=date.today().year)

    class Meta:
        unique_together = ("student", "subject", "term", "year")
        ordering = ["student", "subject"]

    def __str__(self):
        return f"{self.student.student_name} - {self.subject}: {self.marks} (Term {self.term}, {self.year})"

# =====================================================
# BOOK MODEL (UPDATED WITH SCHOOL LINK & ENGINE MANAGER)
# =====================================================

class Book(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="books", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    title = models.CharField(max_length=200) # REMOVED unique=True so different schools can own the same book title
    author = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, blank=True, null=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["title"]
        unique_together = ("school", "title", "grade") # Unique combo within the school library

    def save(self, *args, **kwargs):
        if not self.pk:
            self.available_copies = self.total_copies
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.school.name if self.school else ''}"

# =====================================================
# BORROW RECORD MODEL (UPDATED WITH SCHOOL LINK & ENGINE MANAGER)
# =====================================================

class BorrowRecord(models.Model):
    MEMBER_TYPES = (("Student", "Student"), ("Teacher", "Teacher"))
    STATUS = (("Borrowed", "Borrowed"), ("Returned", "Returned"), ("Overdue", "Overdue"))

    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="borrow_records", null=True, blank=True)
    objects = SchoolTenantManager() # ANTI-ZERAKI AUTOMATED FILTER LOOKUP
    
    member_name = models.CharField(max_length=200)
    member_type = models.CharField(max_length=10, choices=MEMBER_TYPES)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")
    copies = models.PositiveIntegerField(default=1)
    borrow_date = models.DateField(default=date.today)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="Borrowed")

    class Meta:
        ordering = ["-borrow_date"]

    def save(self, *args, **kwargs):
        if self.status == "Borrowed" and self.due_date < date.today():
            self.status = "Overdue"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.member_name} borrowed {self.book.title}"

# =====================================================
# FINE MODEL
# =====================================================

class Fine(models.Model):
    record = models.OneToOneField(BorrowRecord, on_delete=models.CASCADE, related_name="fine")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"Fine: {self.amount} ({'Paid' if self.is_paid else 'Unpaid'})"

# =====================================================
# LESSON PLAN CURRICULUM DATA CONTENT MODEL
# =====================================================

class CurriculumBookContent(models.Model):
    # This model doesn't need a school link manager because it's the global curriculum database shared by everyone
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    learning_area = models.CharField(max_length=100) 
    book_type = models.CharField(max_length=50, choices=BOOK_PUBLISHER_CHOICES)
    
    strand = models.CharField(max_length=255)
    sub_strand = models.CharField(max_length=255)
    learning_outcome = models.TextField(help_text="What the learner should achieve by end of lesson.")
    learning_activities = models.TextField(help_text="Step-by-step tasks executed during the period.")

    class Meta:
        ordering = ["grade", "learning_area", "book_type"]
        verbose_name = "Curriculum Book Content"
        verbose_name_plural = "Curriculum Book Contents"

    def __str__(self):
        return f"{self.grade} - {self.learning_area} ({self.book_type})"
