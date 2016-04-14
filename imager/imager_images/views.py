from django.shortcuts import render

# Create your views here.
class ClassView(TemplateView):

    template_name = 'home.html'

    def get_context_data(self):
        try:
            img = Photo.objects.all().filter(published='public').order_by("?")[0]
        except IndexError:
            img = None
        return{'img': img}


def logout_view(request):
    logout(request)
    return redirect('home_view')
