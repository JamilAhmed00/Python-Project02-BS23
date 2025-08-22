


from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.views.generic import RedirectView

schema_view = get_schema_view(
    openapi.Info(
        title="Simple E-Commerce API",
        default_version='v1',
        description="Session-auth DRF API for products, cart, and orders.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # HTML demo pages + API app urls
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),

    # DRF session login form (for browsable API if you need)
    path('api-auth/', include('rest_framework.urls')),

    # Swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # redirect home to products list (HTML)
    path('', RedirectView.as_view(pattern_name='products:list', permanent=False)),
]
