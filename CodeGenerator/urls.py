from django.urls import path
from . import views

urlpatterns = [
    path('', views.sign_in_page, name='SignIn'),
    path('Operation_Selector', views.code_generator, name='Selector'),
    path('Upload_Source_File', views.upload_src_file, name='file_upload'),
    path('Code_Redirect', views.operation_selector, name='Code_Redirect'),
    path('Home', views.redirect_page, name='Redirect'),
    path('Macro_Generator', views.macro_details_page, name='Macro_details'),
    path('NumCol', views.num_cols_page, name='Num_Cols'),
    path('AddComments', views.add_comments_page, name='Add_Comments'),
    path('CodeGeneratorPKG', views.download_package, name='Download_Package'),
    path('RequestCompleted', views.get_comments, name='Comments'),
    path('SignOut', views.logout, name='LogOut'),
]
