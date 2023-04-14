from .forms import SignUpForm

def signup_form(request):
    form = SignUpForm()
    return {'signup_form': form}