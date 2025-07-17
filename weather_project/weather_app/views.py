from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from .forms import MyForm

def main(request):
    template = loader.get_template('main.html')
    context = {}
    return HttpResponse(template.render(context, request))

def search(request):
    if request.method == 'POST':
        form = MyForm(request.POST)
        if form.is_valid():
            textarea_value = form.cleaned_data['my_text_area']
            # Process the textarea_value (e.g., save to database)
            return render(request, 'weather_app/blank.html', {'value': textarea_value})
    else:
        form = MyForm()
        
    return render(request, 'weather_app/main.html', {'form': form})
    template = loader.get_template('index.html')
# Create your views here.