from .models import Profile_Of_User

def main(request):
    try:
        profile_of_user = Profile_Of_User.objects.get(user = request.user)
    except:
        profile_of_user = None
        default_ = 1
    else:
        default_ = 0
    return{
        'profile_of_user': profile_of_user,
        'default_': default_
    }