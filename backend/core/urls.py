from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'konferentsiyas', views.KonferentsiyaViewSet, basename='konferentsiya')
router.register(r'uchastniks', views.UchastnikViewSet, basename='uchastnik')
router.register(r'prozhivanies', views.ProzhivanieViewSet, basename='prozhivanie')
router.register(r'transfers', views.TransferViewSet, basename='transfer')
router.register(r'doklads', views.DokladViewSet, basename='doklad')
router.register(r'otkazs', views.OtkazViewSet, basename='otkaz')
router.register(r'uchastnik-transfers', views.UchastnikTransferViewSet, basename='uchastnik-transfer')
router.register(r'prozhivanie-transfers', views.ProzhivanieTransferViewSet, basename='prozhivanie-transfer')
router.register(r'programmas', views.ProgrammaViewSet, basename='programma')
router.register(r'programs', views.ProgramViewSet, basename='program')
router.register(r'sekciyas', views.SekciyaViewSet, basename='sekciya')

urlpatterns = [
    path('', include(router.urls)),
]