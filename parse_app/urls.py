from django.contrib import admin
from django.urls import path
from parse_recipes import views as pe_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('parse_ctrl/', pe_views.parse_ctrl, name='parse_ctrl_pg'),
    path('parse_left/<int:img_index>/', pe_views.trim_left, name='parse_left_pg'),
    path('parse_right/<int:img_index>/', pe_views.trim_right, name='parse_right_pg'),
    path('parse_top/<int:img_index>/', pe_views.trim_top, name='parse_top_pg'),
    path('parse_bottom/<int:img_index>/', pe_views.trim_bottom, name='parse_bottom_pg'),
    path('parse_header/<int:img_index>/', pe_views.trim_header, name='parse_header_pg'),
    path('parse_footer/<int:img_index>/', pe_views.trim_footer, name='parse_footer_pg'),
    path('split_vertical/<int:img_index>/', pe_views.split_recipe_vertical, name='split_vertical_pg'),
	path('trim_recipes/<int:img_index>/', pe_views.trim_recipes, name='trim_recipes_pg'),
    path('run_ocr_all_imgs/', pe_views.run_ocr_all_imgs, name='run_ocr_all_imgs_pg'),
    path('inspect_recipe/<str:recipe_id>', pe_views.inspect_recipe, name='inspect_recipe_pg'),
    path('ajax_request', pe_views.ajax_request_view, name='ajax_request_pg'),
    path('inspect_all_recipes/', pe_views.inspect_all_recipes, name='inspect_all_recipes_pg'),
]
