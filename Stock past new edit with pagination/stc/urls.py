

from django.urls import path
from stc import views

from stc.views import ChangePasswordView, DepotDetail, DepotList, LogoutAllView, LogoutView, MyObtainTokenPairView, QRUpdateDetail, QrUpdate, Region_auth_Detail, Region_auth_List, RegionDetail, RegionList, UpdateProfileView, User_details_Detail, User_details_List, UserLevelDetail, UserLevelList,documentDetail, documentList, master_dataDetail, master_dataList, movementDetail, movementList

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    # ==============================common======================================================

    # path('users/', UsersDetail.as_view()),
    # path('users/<int:pk>/', UsersList.as_view()),
    
    path('userLevel/', UserLevelDetail.as_view()),
    path('userLevel/<int:pk>/', UserLevelList.as_view()),
    
    path('Region/', RegionDetail.as_view()),
    path('Region/<int:pk>/', RegionList.as_view()),
    
    path('depot/', DepotDetail.as_view()),
    path('depot/<int:pk>/', DepotList.as_view()),
    
    path('regionAuth/', Region_auth_Detail.as_view()),
    path('regionAuth/<int:pk>/', Region_auth_List.as_view()),
    
    path('userDetails/', User_details_Detail.as_view()),
    path('userDetails/<int:pk>/', User_details_List.as_view()),
    
    path('masterData/', master_dataDetail.as_view()),
    path('masterData/<int:pk>/', master_dataList.as_view()),
    
    path('document/', documentDetail.as_view()),
    path('document/<int:pk>/', documentList.as_view()),
    
    path('movement/', movementDetail.as_view()),
    path('movement/<int:pk>/', movementList.as_view()),
    
# =============== below code is to Qr =================================

    path('QR/', QrUpdate.as_view(), name='STC Qr'),
    path('qrIdUpdate/<str:visible_material_no>/', QRUpdateDetail.as_view()),
    
# ==============================Login======================================================
    
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('register/', RegisterView.as_view(), name='auth_register'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(),
         name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(),
         name='auth_update_profile'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('logout_all/', LogoutAllView.as_view(), name='auth_logout_all'),
# ====================================================================================

 
    
     
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # =============Don't use below urls===== for testing====== QR ID update delete Retrieve ====================================================
    
    # path('qrData/<int:input_number>/', QRconditionView.as_view(), name='data-view'),
    
    
    # --------------------------------below urls are for testing-------------------------------------------------------
    
    # path('persons/<str:column_name>/<str:column_value>/', testqrByColumnView.as_view(), name='testqr-by-column'),
    # path('qr/', qrDetail.as_view()),
    # path('qr/<int:pk>/', qrList.as_view()),
    # path('qr/<int:variable_id>/', views.your_view_function),

    # path('check-qr-id/<str:visible_material_no>/', CheckQRIdView.as_view(), name='check-qr-id'),
    
    # =====use this below url to add qr id====QR ID update delete Retrieve==============
    # path('checkQrId/<str:visible_material_no>/', CheckQRIdView.as_view()),
    # =========use this below new upgraded url to add qr id====QR ID update delete Retrieve=================================
    
    # path('editcheckQrId/<str:visible_material_no>/', editCheckQRIdView.as_view()),
    # path('filter_master_data/', views.filter_master_data, name='filter_master_data'),
]