from django.urls import path, include
from . import views

urlpatterns = [
    path('bookmarklet/', views.bookmarklet, name='bookmarklet'),
    path('chrome_extension/', views.chrome_extension, name='chrome_extension'),
    path('documentation/', views.documentation, name='documentation'),
    path('documentation/jsonschema/', views.jsonschema_documentation, name='jsonschema_documentation'),
    path('terms_of_service/', views.terms_of_service, name='terms_of_service'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
    path('stats/', views.stats_view, name='stats'),
    path('contributors_and_partners/', views.contributors_and_partners, name='contributors_and_partners'),
    path('framed/', views.framed, name='framed'),
]
