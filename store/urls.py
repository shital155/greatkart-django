from django.urls import path
from . import views

# urlpatterns=[
#      path('',views.store, name='store'),
#      path('category/<slug:category_slug>/',views.store, name='products_by_category'),
#      path('<slug:category_slug>/<slug:product_slug>/',views.product_detail, name='product_detail'),
#      path('search/',views.search,name='search'),
#      path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
# ]

# urlpatterns = [
#     path('store/submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
#
#     path('store/', views.store, name='store'),
#     path('store/category/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
#     path('store/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
# ]


urlpatterns = [
    path('', views.store, name='store'),
    path('search/', views.search, name='search'),

    # ✅ MUST be before product_detail
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),

    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
]
