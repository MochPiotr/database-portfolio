from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, 
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
    )
from django.urls import path, include
from leads.views import landing_page, LandingPageView, SignupView, DashboardView, LeadsView, ContactListView, DealListView, ContactCreateView, ContactDetailView, ContactUpdateView, ContactDeleteView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPageView.as_view(), name='landing-page'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('deals/', DealListView.as_view(), name='deals'),
    path('leads/', include('leads.urls', namespace='leads')),
    path('agents/', include('agents.urls', namespace="agents")),
    path('contacts/', ContactListView.as_view(), name="contacts"),
    path('<int:pk>/contacts/', ContactDetailView.as_view(), name='contact-detail'),
    path('contacts/create/', ContactCreateView.as_view(), name='contact-create'),
    path('<int:pk>/contacts/update/', ContactUpdateView.as_view(), name='contact-update'),
    path('<int:pk>/contacts/delete/', ContactDeleteView.as_view(), name='contact-delete'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidp64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-ceomplete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)