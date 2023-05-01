from .models import Profile_Of_User

def main(request):
    try:
        profile_of_user = Profile_Of_User.objects.get(user = request.user)
    except TypeError:
        profile_of_user = None
    return{
        'profile_of_user': profile_of_user
    }