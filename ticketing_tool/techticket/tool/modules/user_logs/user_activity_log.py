from tool.models import user_activity_log


def user_activity(user_name, useraction, event, resultcode ):
    user_activity_log.objects.create(username=user_name, action=useraction, event=event, resultcode=resultcode)
    return True




