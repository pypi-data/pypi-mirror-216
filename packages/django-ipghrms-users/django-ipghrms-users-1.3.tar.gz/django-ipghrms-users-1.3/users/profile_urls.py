from django.urls import path
from . import views

urlpatterns = [
	path('profile/', views.ProfileDetail, name="user-profile"),
	path('profile/update/<str:hashid>/', views.StaffEmployeeUpdate, name="user-profile-update"),
	path('profile/lidnum-update/<str:hashid>/', views.StaffLIDNumberUpdate, name="user-profile-lidnum-update"),
	path('profile/contact-update/<str:hashid>/', views.StaffContactInfoUpdate, name="user-profile-contact-update"),
	path('profile/locationtl-update/<str:hashid>/', views.StaffLocationTLUpdate, name="user-profile-locationtl-update"),
	path('profile/address-update/<str:hashid>/', views.StaffAddressTLUpdate, name="user-profile-address-update"),
	path('profile/driverlic-update/<str:hashid>/', views.StaffDriverLicenceUpdate, name="user-profile-driverlic-update"),
	path('profile/signature-add/<str:hashid>/', views.StaffEmployeeAddSignature, name="user-profile-signatur-add"),
	path('profile/signature-update/<str:hashid>/<int:pk>/', views.StaffEmployeeUpdateSignature, name="user-profile-signatur-update"),
]


