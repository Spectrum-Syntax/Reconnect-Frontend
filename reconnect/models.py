import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    enrollment_number = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        default='',
    )

    # Profile fields
    department = models.CharField(max_length=100, blank=True, default='')
    passed_out_year = models.PositiveIntegerField(null=True, blank=True)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    working_status = models.CharField(max_length=100, blank=True, default='')
    phone = models.CharField(max_length=20, blank=True, default='')
    date_of_birth = models.DateField(null=True, blank=True)
    register_number = models.CharField(max_length=50, blank=True, default='')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    USERNAME_FIELD = "enrollment_number"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.enrollment_number} ({self.role})"

    def get_initials(self):
        first = self.first_name[:1].upper() if self.first_name else ''
        last = self.last_name[:1].upper() if self.last_name else ''
        return first + last or self.enrollment_number[:2].upper()


# ─── Chat Models ─────────────────────────────────────────────────────────────

class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, blank=True, default='')
    is_group = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_conversations',
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='ConversationParticipant',
        related_name='conversations',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f"Chat {self.id}"

    def last_message(self):
        return self.messages.order_by('-timestamp').first()


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='membership')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chat_memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"{self.user} in {self.conversation}"


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} @ {self.timestamp:%H:%M}: {self.content[:30]}"


# ─── Event & Announcement Models ─────────────────────────────────────────────

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('Reunion', 'Reunion'),
        ('Networking', 'Networking'),
        ('Mentorship', 'Mentorship'),
        ('Placement', 'Placement'),
        ('Sports', 'Sports'),
        ('Seminar', 'Seminar'),
        ('Cultural', 'Cultural'),
        ('Other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    date_display = models.CharField(max_length=50, help_text="Display date, e.g. 'OCT 24, 2024'")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    image_url = models.URLField(max_length=500, blank=True, default='')
    description = models.TextField(blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_events',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.date_display})"


class EventTimelineItem(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='timeline')
    time = models.CharField(max_length=50)
    activity = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.time} - {self.activity}"


class Announcement(models.Model):
    IMPORTANCE_CHOICES = [
        ('info', 'Info'),
        ('urgent', 'Urgent'),
        ('opportunity', 'Opportunity'),
        ('event', 'Event Linked'),
    ]

    title = models.CharField(max_length=200)
    body = models.TextField()
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='info')
    display_day = models.CharField(max_length=10, help_text="Day number, e.g. '22'")
    display_month = models.CharField(max_length=10, help_text="Month abbreviation, e.g. 'Feb'")
    action_link = models.URLField(max_length=500, blank=True, default='')
    action_label = models.CharField(max_length=100, blank=True, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_announcements',
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.importance.upper()}] {self.title}"