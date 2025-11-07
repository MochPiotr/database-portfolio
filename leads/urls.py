from django.urls import path
from .views import (
    LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView, LeadCategoryUpdateView, DealListView, DealDetailView, DealDeleteView,
    LeadsView, DealCreateView, DealUpdateView
)
app_name = "leads"

urlpatterns = [
    path('', LeadsView.as_view(), name='leads'),        
    path('<int:pk>/', LeadDetailView.as_view(), name='lead-detail'),
    path('<int:pk>/update/', LeadUpdateView.as_view(), name='lead-update'),
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name='category-detail'),
    path('deals/', DealListView.as_view(), name="lead-deal"),
    path('deals/create/', DealCreateView.as_view(), name="deal-create"),
    path('<int:pk>/deals/detail/', DealDetailView.as_view(), name="deal-detail"),
    path('<int:pk>/deals/update/', DealUpdateView.as_view(), name="deal-update"),
    path('<int:pk>/deals/delete/', DealDeleteView.as_view(), name="deal-delete"),
]
