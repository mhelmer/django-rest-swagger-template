from django.conf.urls import include, url
from django.contrib import admin

from django.contrib.auth.models import User
from rest_framework import (
    routers, serializers, viewsets, permissions
)
from rest_framework.authtoken import views as authtoken_views


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="api:user-detail",
    )

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff', )

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)
        if (hasattr(self, 'context') and 'request' in self.context and
           self.context['request'].user.is_staff):
            is_staff = True
        else:
            is_staff = False

        if not is_staff:
            for field_name in {'email', 'is_staff'}:
                self.fields.pop(field_name)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.DjangoModelPermissions, ]

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/$', authtoken_views.obtain_auth_token),
    url(r'^api/', include(router.urls, namespace='api'), ),
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
