from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
finance = [
	{'id': 1, 'name': 'cat', 'amount': 20, 'type': 'out'},
	{'id': 2, 'name': 'mouse', 'amount': 200, 'type': 'in'}
]

def index(request):
	return HttpResponse('233')
	#return render(request, 'index.html', {'depts_list': finance})