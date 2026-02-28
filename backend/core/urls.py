from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import ProzhivanieStatistikaView, SettlementViewSet, TransferStatistikaView
from .views import ProgramPDFView

router = DefaultRouter()

# Основные сущности
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
router.register(r'uchastnik-prozhivanie', views.UchastnikProzhivanieViewSet, basename='uchastnik-prozhivanie')

# Финансовый модуль
router.register(r'tarifs', views.TarifViewSet, basename='tarif')
router.register(r'platezhi', views.PlatezhViewSet, basename='platezh')
router.register(r'scheta', views.SchetViewSet, basename='schet')

# Уведомления
router.register(r'email-shablony', views.EmailShablonViewSet, basename='email-shablon')
router.register(r'uvedomlenie-log', views.UvedomlenieLogViewSet, basename='uvedomlenie-log')

# Роли
router.register(r'profili', views.ProfilPolzovatelyaViewSet, basename='profil')

# Импорт
router.register(r'import', views.ImportViewSet, basename='import')

router.register(r'settlement', views.SettlementViewSet, basename='settlement')

urlpatterns = [
    path('', include(router.urls)),
    path('import/participants/', views.ImportViewSet.as_view({'post': 'participants'}), name='import-participants'),
    path('konferentsiyas/<int:konferentsiya_id>/program-pdf/', 
         ProgramPDFView.as_view(), 
         name='program-pdf'),
    path('konferentsiyas/<int:konferentsiya_id>/prozhivanie-stats/', 
         ProzhivanieStatistikaView.as_view(), 
         name='prozhivanie-stats'),
    path('konferentsiyas/<int:konferentsiya_id>/transfer-stats/', 
         TransferStatistikaView.as_view(), 
         name='transfer-stats'),
]

