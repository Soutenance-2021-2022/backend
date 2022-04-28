from django.urls import path
from .views import (signup, users, signin, AuthenticateUSer,
                    signout, PermissionViewSet, RoleViewSet, UserViewSet
                    )


urlpatterns = [
    path('register', signup),
    path('login', signin),
    path('currentuser', AuthenticateUSer.as_view()),
    path('signout', signout),
    path("permissions", PermissionViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),

    path('roles', RoleViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('role/<str:pk>', RoleViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete'
    })),
    path('users', UserViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('users/<str:pk>', UserViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'delete'
    }))

]
