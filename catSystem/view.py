from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import render ,redirect
from finance.models import User
from finance.utils import to_md5_hex




class LoginForm(forms.Form):
	username = forms.CharField(min_length=4, max_length=20)
	password = forms.CharField(min_length=8, max_length=20)

	def clean_username(self):
		username = self.cleaned_data['username']
		return username

	def clean_password(self):
		return to_md5_hex(self.cleaned_data['password'])


def login(request):
	if request.method == 'GET':
		request.session.set_test_cookie()
		return render(request, 'login.html')
	if request.method == 'POST':
		# check if browser support cookies or not
		if request.session.test_cookie_worked():
			request.session.delete_test_cookie()
			# login function
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['username']
				password = form.cleaned_data['password']
				user = User.objects.filter(userid=username, password=password)
				if user:
					request.session['is_login'] = True
					request.session['username'] = username
					return redirect('/finance/index/')
				else:
					return render(request, 'login.html', {"hint": 'Wrong password, please try again!'})
		else:
			return HttpResponse("Please enable cookies and try again.")
		
		# else:
		# 	print(form.is_bound)
		# 	print(form.errors)
	return HttpResponse(None)
	

