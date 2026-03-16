from django.db import models
from django.contrib.auth.models import User
import uuid


# tickets/models.py
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from .utils import generate_pdf


class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('sent_post_dhl', 'Sent per Post/DHL'),
        ('waiting_approval', 'Waiting Client Approval'),
        ('approved', 'Approved'),
        ('closed', 'Closed'),
    ]

    tracking_id = models.CharField(
        max_length=50,   # increase length to avoid "value too long" error
        unique=True
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    client = models.ForeignKey(User, on_delete=models.CASCADE)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='open'
    )

    device_type = models.CharField(max_length=50, blank=True, null=True)
    device_model = models.CharField(max_length=100, blank=True, null=True)
    client_phone = models.CharField(max_length=50, blank=True, null=True)

    estimated_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    device_photo = models.ImageField(upload_to='device_photos/', blank=True, null=True)

    agreement_pdf = models.FileField(upload_to='agreements/', blank=True, null=True)
    client_approved = models.BooleanField(default=False)

    repair_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def profit(self):
        return max(0, self.estimated_price - self.repair_cost)

    def save(self, *args, **kwargs):
        if not self.tracking_id:
            self.tracking_id = uuid.uuid4().hex.upper()[:12]
        
        super().save(*args, **kwargs)
        
        # Auto-generate agreement PDF if not exists
        if not self.agreement_pdf:
            pdf_buffer = generate_pdf(self)
            self.agreement_pdf.save(
                f'agreement_{self.tracking_id}.pdf',
                ContentFile(pdf_buffer.read()),
                save=False
            )
            self.save(update_fields=['agreement_pdf'])


    def __str__(self):
        return f"{self.tracking_id} - {self.client.username}"


class Note(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='notes')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
