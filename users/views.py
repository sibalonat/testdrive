# from django.shortcuts import render
from rest_framework.decorators import api_view

# Create your views here.
@api_view(['GET'])
def index(request):
    return 'hello world'
    
# return render(request, 'users/index.html')