from django.shortcuts import render

def index_view(request):
    # Add logic here if needed (e.g., fetching data from the database)
    context = {
        'welcome_message': 'Welcome to my Django + TensorFlow Tutorial App!'
    }
    return render(request, 'index.html', context)
