from django import template

register = template.Library()

@register.filter
def filter_notifications(notifications, notification_type):
    return notifications.filter(type=notification_type) 