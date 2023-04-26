from .forms import SignUpForm

def signup_form(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
    return {'signup_form': form}