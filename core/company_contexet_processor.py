from .models import Company , Notification


def get_company_data(request):
    data = Company.objects.last()
    return {'company_data': data }



# def notifications_processor(request):
#     if request.user.is_authenticated:
#         notifications = Notification.objects.filter(user=request.user).order_by('-date')[:10]
#         unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
#     else:
#         notifications = []
#         unread_count = 0

#     return {
#         "notifications": notifications,
#         "unread_count": unread_count,
#     }

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = (
            Notification.objects.filter(user=request.user)
            .select_related('sender__kyc')
            .order_by('-date')[:10]
        )
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    else:
        notifications = []
        unread_count = 0

    processed_notifications = []
    for n in notifications:
        processed_notifications.append({
            "id": n.id,
            "amount": n.amount,
            "notification_type": n.notification_type,
            "date": n.date,
            "is_read": n.is_read,
            "sender_full_name": n.sender_full_name, 
            "sender_image_url": n.sender_image_url or '/static/assets1/images/user-1.png'
        })

    return {
        "notifications": processed_notifications,
        "unread_count": unread_count,
    }