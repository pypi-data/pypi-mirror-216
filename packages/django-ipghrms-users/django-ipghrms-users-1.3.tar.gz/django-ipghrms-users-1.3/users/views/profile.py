import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from settings_app.decorators import allowed_users
from employee.models import AddressTL, ContactInfo, CurEmpDivision, CurEmpPosition, DriverLicence,\
	EmpDependency, FIDNumber, FormalEducation, IIDNumber, LIDNumber, LocationInter, LocationTL,\
	NonFormalEducation, Photo, WorkExperience, EmployeeUser, EmpSignature,EmpSpecialize, EmpLanguage
from contract.models import Contract, EmpSalary, EmpPlacement
from users.forms import UserUpdateForm, UserUpdateForm2
from settings_app.user_utils import c_staff
from employee.forms import EmployeeForm, LIDNumberForm,ContactInfoForm, LocationTLForm, AddressTLForm, DriverLicenceForm, EmpSignatureForm
from employee.models import Employee, FIDNumber
from log.utils import log_action
@login_required
def ProfileDetail(request):
	group = request.user.groups.all()[0].name
	objects = c_staff(request.user)
	
	fidnum = FIDNumber.objects.filter(employee=objects).first()
	lidnum = LIDNumber.objects.filter(employee=objects).first()
	iidnum = IIDNumber.objects.filter(employee=objects).first()
	contactinfo = ContactInfo.objects.filter(employee=objects).first()
	loctl = LocationTL.objects.filter(employee=objects).first()
	addtl = AddressTL.objects.filter(employee=objects).first()
	locinter = LocationInter.objects.filter(employee=objects).first()
	img = Photo.objects.filter(employee=objects).first()
	driver = DriverLicence.objects.filter(employee=objects).first()
	empcont = Contract.objects.filter(employee=objects, is_active=True).last()
	empsalary = EmpSalary.objects.filter(contract=empcont).last()
	signature = EmpSignature.objects.filter(employee=objects).last()
	emppos = CurEmpPosition.objects.filter(employee=objects).first()
	empdiv = CurEmpDivision.objects.filter(employee=objects).first()
	empdepend = EmpDependency.objects.filter(employee=objects).all()
	formaledu = FormalEducation.objects.filter(employee=objects).last()
	empplacement = EmpPlacement.objects.filter(employee=objects, is_active=True).last()
	nonformaledu = NonFormalEducation.objects.filter(employee=objects).last()
	workexp = WorkExperience.objects.filter(employee=objects).last()
	emplang = EmpLanguage.objects.filter(employee=objects).all()
	empspecs = EmpSpecialize.objects.filter(employee=objects).all()
	context = {
		'group': group, 'objects': objects, 'fidnum': fidnum, 'lidnum': lidnum, 'iidnum': iidnum,
		'contactinfo': contactinfo, 'loctl':loctl, 'addtl': addtl, 'locinter':locinter, 'img': img,
		'empcont': empcont, 'empsalary': empsalary, 'emppos': emppos, 'empdiv': empdiv,
		'formaledu': formaledu, 'nonformaledu': nonformaledu, 'workexp': workexp,
		'empdepend': empdepend, 'driver': driver, 'emplang': emplang, 'empspecs': empspecs,
		'title': 'Detalha Funcionariu', 'legend': 'Detalha Funcionariu', 'empplacement':empplacement,
		 'employee': objects, 'signature':signature
	}
	return render(request, 'profile/profile.html', context)

@login_required
def AccountUpdate(request):
	group = request.user.groups.all()[0].name
	if request.method == 'POST':
		if group == "students":
			u_form = UserUpdateForm(request.POST, instance=request.user)
		else:
			u_form = UserUpdateForm2(request.POST, instance=request.user)
		if u_form.is_valid():
			u_form.save()
			messages.success(request, f'Your account has been updated!')
			return redirect('user-account')
	else:
		if group == "students":
			u_form = UserUpdateForm(instance=request.user)
		else:
			u_form = UserUpdateForm2(instance=request.user)
	context = {
		'u_form': u_form,
		'title': 'Account Info', 'legend': 'Account Info',
	}
	return render(request, 'auth/account.html', context)

class UserPasswordChangeView(PasswordChangeView):
	template_name = 'auth/change_password.html'
	success_url = reverse_lazy('user-change-password-done')

class UserPasswordChangeDoneView(PasswordResetDoneView):
	template_name = 'auth/change_password_done.html'



@login_required
def StaffEmployeeUpdate(request, hashid):
	objects = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		form = EmployeeForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			log_action(request, model=Employee._meta.model_name, action="Update",field_id=objects.pk)
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = EmployeeForm(instance=objects)
	context = {
		'form': form, 'objects':objects,
		'title': 'Altera Funcionariu', 'legend': 'Altera Funcionariu'
	}
	return render(request, 'profile/form.html', context)


@login_required
def StaffLIDNumberUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = LIDNumber.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = LIDNumberForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = LIDNumberForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera ID Nacional', 'legend': 'Altera ID Nacional'
	}
	return render(request, 'profile/form2.html', context)

@login_required
def StaffContactInfoUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = ContactInfo.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = ContactInfoForm(request.POST, instance=objects)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.user = request.user
			instance.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = ContactInfoForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Kontaktu', 'legend': 'Altera Informasaun Kontaktu'
	}
	return render(request, 'employee/form3.html', context)


@login_required
def StaffLocationTLUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = LocationTL.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = LocationTLForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = LocationTLForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Naturalidade', 'legend': 'Altera Naturalidade'
	}
	return render(request, 'profile/form_location.html', context)


@login_required
def StaffAddressTLUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = AddressTL.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = AddressTLForm(request.POST, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = AddressTLForm(instance=objects)
	context = {
		'hashid':hashid, 'form': form, 'emp': emp,
		'title': 'Altera Enderesu', 'legend': 'Altera Enderesu iha Timor Leste'
	}
	return render(request, 'profile/form_address.html', context)


@login_required
def StaffDriverLicenceUpdate(request, hashid):
	emp = get_object_or_404(Employee, hashed=hashid)
	objects = DriverLicence.objects.filter(employee=emp).first()
	if request.method == 'POST':
		form = DriverLicenceForm(request.POST, request.FILES, instance=objects)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = DriverLicenceForm(instance=objects)
	context = {
		'hashid': hashid, 'emp': emp, 'form': form,
		'title': 'Altera Karta Kondusaun', 'legend': 'Altera Karta Kondusaun'
	}
	return render(request, 'profile/form2.html', context)


@login_required
def StaffEmployeeAddSignature(request, hashid):
	employee = get_object_or_404(Employee, hashed=hashid)
	if request.method == 'POST':
		form = EmpSignatureForm(request.POST, request.FILES)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.employee = employee
			instance.save()
			messages.success(request, f'Aumenta sucessu.')
			return redirect('user-profile')
	else: form = EmpSignatureForm()
	context = {
		'form': form, 'page':'signature',
		'title': 'Aumenta Asinatura', 'legend': 'Aumenta Asinatura'
	}
	return render(request, 'profile/form.html', context)


@login_required
def StaffEmployeeUpdateSignature(request, hashid, pk):
	signature = get_object_or_404(EmpSignature, pk=pk)
	if request.method == 'POST':
		form = EmpSignatureForm(request.POST, request.FILES, instance=signature)
		if form.is_valid():
			form.save()
			messages.success(request, f'Altera sucessu.')
			return redirect('user-profile')
	else: form = EmpSignatureForm(instance=signature)
	context = {
		'form': form,
		'title': 'Altera Asinatura', 'legend': 'Altera Asinatura'
	}
	return render(request, 'profile/form.html', context)