from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView,TokenVerifyView)
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/verify/',TokenVerifyView.as_view(),name='token_verify'),
    path('user-auth/',include("user_authentication.urls",namespace="user_auth")),   
    path('product/',include("product.urls",namespace="product")),
    path('cart/',include("cart.urls",namespace="cart")),
    path('user-admin/',include("admin_api.urls",namespace="user_admin"))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
