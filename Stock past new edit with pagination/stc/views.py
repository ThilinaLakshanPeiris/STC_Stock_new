from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from stc.models import depot, document, master_data, movement, region, region_auth, user_details, user_level
from .serializers import ChangePasswordSerializer, MasterDataSerializer, MyTokenObtainPairSerializer, QRUpdateSerializer, QrDataSerializer, UpdateUserSerializer, documentSerializer, master_dataSerializer, movementSerializer, region_authSerializer, regionSerializer, testqrSerializer, user_detailsSerializer, user_levelSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from stc.serializers import depotSerializer

from stc import serializers

# Create your views here.

# Users


# class UsersDetail(generics.ListCreateAPIView):
#     serializer_class = usersSerializer
#     queryset = users.objects.all()
#     pagination_class = LimitOffsetPagination


# class UsersList(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = usersSerializer
#     queryset = users.objects.all()

# UserLevel


class UserLevelDetail(generics.ListCreateAPIView):
    serializer_class = user_levelSerializer
    queryset = user_level.objects.all()
    pagination_class = LimitOffsetPagination


class UserLevelList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = user_levelSerializer
    queryset = user_level.objects.all()

# Region


class RegionDetail(generics.ListCreateAPIView):
    serializer_class = regionSerializer
    queryset = region.objects.all()
    pagination_class = LimitOffsetPagination


class RegionList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = regionSerializer
    queryset = region.objects.all()

# Depot


class DepotDetail(generics.ListCreateAPIView):
    serializer_class = depotSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        querySet = depot.objects.all()
        region_id = self.request.query_params.get('region')

        if region_id is not None:
            querySet = querySet.filter(region_id=region_id)
            if not querySet:
                raise serializers.ValidationError(
                    {"authorize": "No Records Found."})
        return querySet


class DepotList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = depotSerializer
    queryset = depot.objects.all()

# Region_auth


class Region_auth_Detail(generics.ListCreateAPIView):
    serializer_class = region_authSerializer
    queryset = region_auth.objects.all()
    pagination_class = LimitOffsetPagination


class Region_auth_List(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = region_authSerializer
    queryset = region_auth.objects.all()

# User_details


class User_details_Detail(generics.ListCreateAPIView):
    serializer_class = user_detailsSerializer
    queryset = user_details.objects.all()
    pagination_class = LimitOffsetPagination


class User_details_List(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = user_detailsSerializer
    queryset = user_details.objects.all()

# master_data


class master_dataDetail(generics.ListCreateAPIView):
    serializer_class = master_dataSerializer
    queryset = master_data.objects.all()
    pagination_class = LimitOffsetPagination


class master_dataList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = master_dataSerializer
    queryset = master_data.objects.all()

# document


class documentDetail(generics.ListCreateAPIView):
    serializer_class = documentSerializer
    queryset = document.objects.all()
    pagination_class = LimitOffsetPagination


class documentList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = documentSerializer
    queryset = document.objects.all()

# movement


class movementDetail(generics.ListCreateAPIView):
    serializer_class = movementSerializer
    queryset = movement.objects.all()
    pagination_class = LimitOffsetPagination


class movementList(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = movementSerializer
    queryset = movement.objects.all()



class QRUpdateDetail(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = QRUpdateSerializer
    # Use the 'visible_material_no' field for lookups
    lookup_field = 'visible_material_no'
    queryset = master_data.objects.all()
    
    
# ============================get data through api and check============= 9/19=====================================
        
class QrUpdate(APIView):

    def post(self, request):
        # Deserialize the JSON data
        serializer = QrDataSerializer(data=request.data)

        if serializer.is_valid():
            # Get values from the serializer

            depot = serializer.validated_data.get('depot')
            visible_material_no = serializer.validated_data.get('visible_material_no')
            # email = serializer.validated_data.get('email')
            
            # Perform the search query
            if visible_material_no and depot:
              
                # Use the filter method to search for records by the specified column
                results_queryset  = master_data.objects.filter(visible_material_no=visible_material_no, depot=depot)      
                          
                # Convert the QuerySet to a list of dictionaries
                results_data = list(results_queryset.values())


            
                if results_data[0]['material_no'] !=  None or results_data[0]['material_no'] !=  "":
                    if results_data[0]['active'] == 1:
                        if results_data[0]['qr_id'] is None or results_data[0]['qr_id'] == "":
                       
                            # Make a GET request to another URL
                            other_url = 'http://127.0.0.1:8000/stc/qrIdUpdate/' + visible_material_no + '/'   # Replace with the actual URL
                            response = requests.get(other_url)

                            if response.status_code == 200:
                                return redirect(other_url)
                                # return Response({'message': 'QR ID updated'}, status=status.HTTP_200_OK)
                            else:
                                # Handle unsuccessful response
                                return Response({'message': 'QR ID not updated'}, status=status.HTTP_200_OK)
                        else:
                            return Response({"qr_id is already assigned":results_data[0]['qr_id']})    
                    else:
                        return Response({'Not Active(active satus is) ':results_data[0]['active']})
                else:
                    return Response("Material number is not assigned")
               
            else:
                return Response({"error": "Missing column_name_value parameter"}, status=400)

            # return Response({'message': 'Data received and processed successfully', "depot": depot, "visible_material_no": visible_material_no}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
# ================================Extend user and authontication===================================================   
""" 

Extend user and authontication


 """
class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# class RegisterView(generics.CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (AllowAny,)
#     serializer_class = usersSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LogoutAllView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user_id=request.user.id)
        for token in tokens:
            t, _ = BlacklistedToken.objects.get_or_create(token=token)

        return Response(status=status.HTTP_205_RESET_CONTENT)


 
# ==============================================================================================================================





























# =================Qr=====================================

# class qrDetail(generics.ListCreateAPIView):
#     serializer_class = qrSerializer
#     queryset = master_data.objects.all()
#     pagination_class = LimitOffsetPagination

# ================================================================

# class qrList(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = qrSerializer
#     queryset = master_data.objects.all()

# # ==============================================================================================================================
# class QRUpdateDetail(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = QRUpdateSerializer
#     lookup_field = 'visible_material_no'  # Use the 'visible_material_no' field for lookups
#     queryset = master_data.objects.all()

#     def update(self, request, *args, **kwargs):

#         # Get the instance based on the visible_material_no
#         instance = self.get_object()

#         # Check your conditions based on the material_no field
#         if instance("material_no ") != '':
#             # Update qr_id field
#             print("material_no is not empty")
#             # return self.partial_update(request, *args, **kwargs)
#         else:
#             print("material_no is empty")
#             # return Response({"message": "You do not have permission to update qr_id."}, status=status.HTTP_403_FORBIDDEN)

# # QR Checking function

# class QRconditionView(APIView):

#     def get(self, request, input_number):
#         # Get the input number from the frontend
#         # global input_number
#         try:
#             #  input_number = int(input('enter visible material number :- '))
#             input_number = int(input_number)
#         except Exception as e:
#             # Handle exceptions and return an appropriate response
#             error_data = {'error': str(e)}
#             return JsonResponse(error_data, status=500)

#         # input_number = int(46)

#         queryset = master_data.objects.all()
#         serializer = master_dataSerializer(queryset, many=True)
#         data = serializer.data
#         index = 0
#         try:
#             while index < len(data):
#                 if input_number == int(data[index].get('visible_material_no')):
#                     try:

#                         if data[index].get('material_no') is not None:
#                             try:
#                                 if data[index].get('active') == 1:
#                                     # new_qr_id = input('Enter new QR Code (integer) :- ')
#                                     if data[index].get('qr_id') == "":
#                                         # lastely added 8/8
#                                      # ======Call this API===========  qrIdUpdate/<str:visible_material_no>/', QRUpdateDetail.as_view(),=========================

#                                         return Response({"visible_material_no ": data[index].get('visible_material_no'),
#                                                         "material_no": data[index].get('material_no'),
#                                                          "active(1) or not(2) ": data[index].get('active'),
#                                                          "index is ": index,
#                                                          "available ": True,
#                                                          # "QR ID ":data[index].get('qr_id'),
#                                                          "use this URL to update the qr_id": "path('qrIdUpdate/<str:visible_material_no> or visible_material_no/', QRUpdateDetail.as_view())"})

#                                     else:
#                                         return Response({"visible_material_no ": data[index].get('visible_material_no'),
#                                                         "material_no": data[index].get('material_no'),
#                                                          "active(1) or not(2) ": data[index].get('active'),
#                                                          "index is ": index,
#                                                          "available ": False,
#                                                          "Comment": ' qr_id is already there'
#                                                          # "QR ID ":new_qr_id +' qr_id is already there'
#                                                          })
#                                         # logging.warning('qr_id is already there')
#                                         # break
#                                 else:
#                                     return Response({"visible_material_no ": data[index].get('visible_material_no'),
#                                                     "material_no": data[index].get('material_no'),
#                                                      "active(1) or notactive(2 any num) ": data[index].get('active'),
#                                                      "index is ": index})
#                                     # logging.warning('active state is not (1) material number is out of stock')
#                                     # break
#                                 # return Response({"visible_material_no ":data[index].get('visible_material_no'), "index is ":index, "available ":True})
#                             except Exception as e:
#                                 # Handle exceptions and return an appropriate response
#                                 error_data = {'error': str(e)}
#                                 # Use an appropriate status code
#                                 return JsonResponse(error_data, status=500)

#                         else:
#                             return Response({"visible_material_no ": False})
#                             # print('material_no is not there')
#                             # break

#                     except Exception as e:
#                         # Handle exceptions and return an appropriate response
#                         error_data = {'error': str(e)}
#                         # Use an appropriate status code
#                         return JsonResponse(error_data, status=500)

#                 else:

#                     index += 1
#             return Response({"visible_material_no ": False})

#         except Exception as e:
#             # Handle exceptions and return an appropriate response
#             error_data = {'error': str(e)}
#             return JsonResponse(error_data, status=500)

# ===============================================================================================


# class testqrByColumnView(APIView):
#     def get(self, request, column_name, column_value):
#         try:
#             queryset = master_data.objects.filter(
#                 **{column_name: column_value})
#             serializer = testqrSerializer(queryset, many=True)

#             # Access the value of the visible_material_no field in each serialized object
#             visible_material_nos = [item['visible_material_no']
#                                     for item in serializer.data]

#             return Response({'visible_material_no': visible_material_nos})

#             # return Response(serializer.data)
#         except master_data.DoesNotExist:
#             return Response(status=404)


# =================================below code working to add qr_id ==============================================================

# class CheckQRIdView(generics.RetrieveAPIView):
#     serializer_class = MasterDataSerializer
#     # Use 'visible_material_no' as the lookup field
#     lookup_field = 'visible_material_no'

#     def get_queryset(self):
#         return master_data.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()

#         visible_material_no = str(instance.visible_material_no)

#         if instance.material_no:
#             if instance.active == 1:
#                 if not instance.qr_id:
#                    # Make a GET request to another URL
#                     other_url = 'http://127.0.0.1:8000/stc/qrIdUpdate/' + \
#                         visible_material_no + '/'   # Replace with the actual URL
#                     response = requests.get(other_url)

#                     if response.status_code == 200:
#                         # Successful response from the other URL
#                         # ... your logic ...
#                         return redirect(other_url)
#                         # return Response({'message': 'QR ID updated'}, status=status.HTTP_200_OK)
#                     else:
#                         # Handle unsuccessful response
#                         # ... your logic ...
#                         return Response({'message': 'QR ID not updated'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'message': 'QR ID is not empty', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_200_OK)

#             else:
#                 return Response({'message': ' Not active', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'message': 'material_no is empty'}, status=status.HTTP_204_NO_CONTENT)

# =============================================9/18==============================================================
# class editCheckQRIdView(generics.RetrieveAPIView):
#     serializer_class = MasterDataSerializer
#     # Use 'visible_material_no' as the lookup field
#     lookup_field = 'visible_material_no'

#     def get_queryset(self):
#         return master_data.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()

#         visible_material_no = str(instance.visible_material_no)

#         depot_id = instance.depot
#         # depot_id = depot.depot_id

#         if instance.material_no:
#             if instance.active == 1:
#                 if not instance.qr_id:
#                    # Make a GET request to another URL
#                     other_url = 'http://127.0.0.1:8000/stc/qrIdUpdate/' + \
#                         visible_material_no + '/'   # Replace with the actual URL
#                     response = requests.get(other_url)

#                     if response.status_code == 200:

#                         return redirect(other_url)
#                         # return Response({'message': 'QR ID updated'}, status=status.HTTP_200_OK)
#                     else:
#                         # Handle unsuccessful response
#                         # ... your logic ...
#                         return Response({'message': 'QR ID not updated'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response({'message': 'QR ID is not empty', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_200_OK)

#             else:
#                 return Response({'message': ' Not active', 'active': instance.active, 'material_no': instance.material_no, 'depot_id': depot_id}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'message': 'material_no is empty'}, status=status.HTTP_204_NO_CONTENT)

# ==============================================================================================================================



        
        

# ====================================================================================================================

# def filter_master_data(request):
#     # Get parameters from the request (you can use request.GET for GET parameters)
#     depot = request.GET.get('depot')
#     visible_material_no = request.GET.get('visible_material_no')

#     # Filter data based on the provided parameters
#     filtered_data = master_data.objects.filter(
#         depot=depot, visible_material_no=visible_material_no)

#     # Create a list to store the filtered data
#     filtered_data_list = []

#     # Iterate through the filtered data and convert it to a dictionary
#     for item in filtered_data:
#         data_dict = {
#             'material_no': item.material_no,
#             'length': float(item.length) if item.length is not None else None,
#             'girth': float(item.girth) if item.girth is not None else None,
#             # Add other fields as needed
#         }
#         filtered_data_list.append(data_dict)

#     # Return the filtered data as a JSON response
#     return JsonResponse({'filtered_data': filtered_data_list})

    # serializer_class = MasterDataSerializer
    # lookup_field = 'visible_material_no'  # Use 'visible_material_no' as the lookup field

    # def get_queryset(self):
    #     return master_data.objects.all()

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()

    #     visible_material_no = str(instance.visible_material_no)

    #     if instance.material_no:
    #         if instance.active == 1:
    #             if not instance.qr_id:
    #                # Make a GET request to another URL
    #                 other_url = 'http://127.0.0.1:8000/stc/qrIdUpdate/' + visible_material_no +'/'   # Replace with the actual URL
    #                 response = requests.get(other_url)

    #                 if response.status_code == 200:
    #                     # Successful response from the other URL
    #                     # ... your logic ...
    #                     return redirect(other_url)
    #                     # return Response({'message': 'QR ID updated'}, status=status.HTTP_200_OK)
    #                 else:
    #                     # Handle unsuccessful response
    #                     # ... your logic ...
    #                     return Response({'message': 'QR ID not updated'}, status=status.HTTP_200_OK)
    #             else:
    #                 return Response({'message': 'QR ID is not empty', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_200_OK)

    #         else:
    #             return Response({'message': ' Not active', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_204_NO_CONTENT)
    #     else:
    #         return Response({'message': 'material_no is empty'}, status=status.HTTP_204_NO_CONTENT)


#  +++++++++++ Json object ++++++++++++++++++++++++++++
#  {
#   "depot" : "A104",
#   "visible_material_no" : "1-2991BS"
#  }

    # return Response(data[2])

# ==========================================================================================
    # if input_number is not None:
    #     try:
    #         queryset = master_data.objects.all()
    #         serializer = master_dataSerializer(queryset, many=True)
    #         data = serializer.data
    #         data_length = len(data)  # Get the length of the data array using len()
    #         result_list = []
    #         index = 0
    #         # return Response({"message": "ok"})
    #         while index < data_length :
    #             visible_material_no = int(data[index].get('visible_material_no'))
    #             # if data[index].get('visible_material_no') is not None :
    #             if  visible_material_no != input_number:
    #                 # Get the qr_id from the current record
    #                 qr_id_data = data[index].get('qr_id')
    #                 material_no_data = data[index].get('material_no')
    #                 visible_material_no = data[index].get('visible_material_no')
    #                 # Log the qr_id and the length of the data array together
    #                 logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length},\n {index}")
    #                 # logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length}, \n dataIndex:{data[index]}, {index}")
    #                 print(visible_material_no)
    #                 result_list.append({
    #                     "qr_id": qr_id_data,
    #                     "material_no": material_no_data,
    #                     "visible_material_no": visible_material_no
    #                 })
    #                 index += 1
    #             else:
    #                 return Response({
    #                     "nooooooooooooooooooooooo visible_material_no",data_length

    #                 })

    #         logging.warning(result_list)
    #         return Response({"material NUM": 'true'})
    #         # return Response(result_list,{"material NUM": 'true'})

    #     except master_data.DoesNotExist:
    #         error_msg = "Data not found."
    #         return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
    # else:
    #     error_msg = "Input number not provided."
    #     return Response({"error": error_msg}, status=status.HTTP_400_BAD_REQUEST)

# ======================================================================================================

# class QRconditionView(APIView):
#     def get(self, request):
#         # Your condition to check against the database

#         if master_data.visible_material_no is not None:

#             try:
#                 queryset = master_data.objects.all()
#                 serializer = master_dataSerializer(queryset, many=True)
#                 data =serializer.data
#                 data_length = len(data)  # Get the length of the data array using len()
#                 index = 0
#                 result_list = []
#                 while index < data_length :
#                     if data[index].get('visible_material_no') is not None:
#                         # Get the qr_id from the current record
#                         qr_id_data = data[index].get('qr_id')
#                         material_no_data = data[index].get('material_no')
#                         # Log the qr_id and the length of the data array together
#                         logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length},\n {index}")
#                         # logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length}, \n dataIndex:{data[index]}, {index}")

#                         index += 1
#                         result_list.append({
#                             "qr_id": qr_id_data,
#                             "material_no": material_no_data
#                         })
#                         # continue
#                         # return Response({

#                         #     "qr_id": qr_id_data,
#                         #     "material_no": data[index].get('material_no'),

#                         # })

#                     else:
#                         return Response({
#                             "nooooooooooooooooooooooooooooooooo visible_material_no"
#                         })
#                 # if data and data[0].get('visible_material_no') is not None:
#                 #     # Get the qr_id from the first record
#                 #     qr_id_data = data[0].get('qr_id')
#                 #     logging.warning(data[0].get('qr_id'),len(data))
#                 #     return Response({"qr_id": qr_id_data,
#                 #                      "material_no":data[0].get('material_no')})

#                 # return Response(serializer.data)
#                 return Response(result_list)

#             except master_data.DoesNotExist:
#                 error_msg = "Data not found."
#                 return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)

#             qr_id_data = data_model_instance.qr_id
#             return Response({"qr_id": qr_id_data})
#         else:
#             error_msg = "Condition not met. Data not available."
#             return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)

    #   ----------------------under this code is working-----------------------------------------------------------------------------

# QR Checking function
# class QRconditionView(APIView):
#     def get(self, request):
#         # Your condition to check against the database

#         if master_data.visible_material_no is not None:

#             try:
#                 queryset = master_data.objects.all()
#                 serializer = master_dataSerializer(queryset, many=True)
#                 data =serializer.data
#                 data_length = len(data)  # Get the length of the data array using len()
#                 index = 0
#                 result_list = []
#                 while index < data_length :
#                     if data[index].get('visible_material_no') is not None:
#                         # Get the qr_id from the current record
#                         qr_id_data = data[index].get('qr_id')
#                         material_no_data = data[index].get('material_no')
#                         # Log the qr_id and the length of the data array together
#                         logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length},\n {index}")
#                         # logging.warning(f"\n qr_id: {qr_id_data},\n data_length: {data_length}, \n dataIndex:{data[index]}, {index}")

#                         index += 1
#                         result_list.append({
#                             "qr_id": qr_id_data,
#                             "material_no": material_no_data
#                         })
#                         # continue
#                         # return Response({

#                         #     "qr_id": qr_id_data,
#                         #     "material_no": data[index].get('material_no'),

#                         # })

#                     else:
#                         return Response({
#                             "nooooooooooooooooooooooooooooooooo visible_material_no"
#                         })
#                 # if data and data[0].get('visible_material_no') is not None:
#                 #     # Get the qr_id from the first record
#                 #     qr_id_data = data[0].get('qr_id')
#                 #     logging.warning(data[0].get('qr_id'),len(data))
#                 #     return Response({"qr_id": qr_id_data,
#                 #                      "material_no":data[0].get('material_no')})

#                 # return Response(serializer.data)
#                 return Response(result_list)

#             except master_data.DoesNotExist:
#                 error_msg = "Data not found."
#                 return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)

#             qr_id_data = data_model_instance.qr_id
#             return Response({"qr_id": qr_id_data})
#         else:
#             error_msg = "Condition not met. Data not available."
#             return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)
    #   -----------------------------------------------------------------------------------------------------------------------------
# # QR Checking function
# class QRconditionView(APIView):
#     def get(self, request):
#         # Your condition to check against the database

#         if master_data.visible_material_no is not None:

#             try:
#                 queryset = master_data.objects.all()
#                 serializer = master_dataSerializer(queryset, many=True)
#                 data =serializer.data
#                 if data and data[0].get('visible_material_no') is not None:
#                     # Get the qr_id from the first record
#                     qr_id_data = data[0].get('qr_id')
#                     logging.warning(data[0].get('qr_id'))
#                     return Response({"qr_id": qr_id_data,
#                                      "material_no":data[0].get('material_no')})

#                 return Response(serializer.data)

#             except master_data.DoesNotExist:
#                 error_msg = "Data not found."
#                 return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)

#             qr_id_data = data_model_instance.qr_id
#             return Response({"qr_id": qr_id_data})
#         else:
#             error_msg = "Condition not met. Data not available."
#             return Response({"error": error_msg}, status=status.HTTP_404_NOT_FOUND)

# ==============================================================================================================================
# class CheckQRIdView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = MasterDataSerializer
#     lookup_field = 'visible_material_no'  # Use 'visible_material_no' as the lookup field

#     def get_queryset(self):
#         return master_data.objects.all()

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()

#         if instance.material_no:
#             if instance.active == 1:
#                 if not instance.qr_id:
#                     # Use the QRUpdateDetail view to update the qr_id
#                     qr_update_view = QRUpdateDetail.as_view()
#                     qr_update_response = qr_update_view(request._request, visible_material_no=instance.visible_material_no)

#                     if qr_update_response.status_code == status.HTTP_200_OK:
#                         return Response({'message': 'QR ID updated'}, status=status.HTTP_200_OK)
#                     else:
#                         return Response({'message': 'QR ID update failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#                 else:
#                     return Response({'message': 'QR ID is not empty', 'active': instance.active, 'material_no': instance.material_no}, status=status.HTTP_200_OK)

#             else:
#                 return Response({'message': ' Not active'}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({'message': 'material_no is empty'}, status=status.HTTP_204_NO_CONTENT)
