from rest_framework import permissions
from django.conf import settings

class IsAdminOrOrganizer(permissions.BasePermission):
    """Только администраторы и организаторы могут изменять данные"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Суперпользователь имеет полный доступ
        if request.user.is_superuser:
            return True
        
        # Проверка роли через профиль
        if hasattr(request.user, 'profilpolzovatelya'):
            return request.user.profilpolzovatelya.rol in ['admin', 'organizer']
        
        return False

class IsAuthenticatedReadOnly(permissions.BasePermission):
    """Все аутентифицированные могут читать, писать только админы/организаторы"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Чтение доступно всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Запись только для админов и организаторов
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'profilpolzovatelya'):
            return request.user.profilpolzovatelya.rol in ['admin', 'organizer']
        
        return False

class AllowAnyIfDebug(permissions.BasePermission):
    """
    Разрешает все запросы если DEBUG=True (для разработки)
    В production нужно заменить на реальную проверку прав
    """
    def has_permission(self, request, view):
        if settings.DEBUG:
            return True
        # Здесь будет реальная логика прав в production
        return request.user and request.user.is_authenticated