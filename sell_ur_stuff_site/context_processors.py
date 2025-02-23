from profiles.models import Notification


def unread_notifications(request):
    """
    Add the number of unread notifications to the context of all templates.
    """
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(
            user=request.user, is_read=False
        ).count()
    else:
        unread_count = 0
    return {"unread_notifications": unread_count}
