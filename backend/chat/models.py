from django.db import models
from django.conf import settings
from django.db.models import Count, Q
import random

class ChatCategory(models.Model):
    """
    Represents a category for a support chat ticket, e.g., 'Technical Support'.
    Admins are assigned to these categories.
    """
    name = models.CharField(max_length=100, unique=True)
    admins = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chat_categories',
        limit_choices_to={'is_staff': True}
    )

    def __str__(self):
        return self.name

class ChatTicket(models.Model):
    """
    Represents a single support chat session between a user and an admin.
    """
    class TicketStatus(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        CLOSED = 'CLOSED', 'Closed'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chat_tickets', on_delete=models.CASCADE)
    assigned_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tickets',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'is_staff': True}
    )
    category = models.ForeignKey(ChatCategory, related_name='tickets', on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=TicketStatus.choices, default=TicketStatus.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket #{self.id} ({self.user.username} in {self.category.name})"

    @staticmethod
    def assign_admin(category):
        """
        Finds the best admin for a new ticket based on category and workload.
        """
        admins = category.admins.all()
        if not admins:
            return None

        # Annotate each admin with the count of their non-closed tickets
        admins_with_load = admins.annotate(
            open_tickets=Count('assigned_tickets', filter=Q(assigned_tickets__status__in=['OPEN', 'IN_PROGRESS']))
        ).order_by('open_tickets')

        min_tickets = admins_with_load.first().open_tickets
        best_admins = [admin for admin in admins_with_load if admin.open_tickets == min_tickets]

        return random.choice(best_admins)


class ChatMessage(models.Model):
    """
    Represents a single message within a chat ticket.
    """
    ticket = models.ForeignKey(ChatTicket, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender.username} in Ticket #{self.ticket.id}"
