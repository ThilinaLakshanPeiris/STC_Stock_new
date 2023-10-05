from rest_framework import serializers
from rest_flex_fields import FlexFieldsModelSerializer
from stc.models import depot, document, master_data, movement, region, region_auth, user_details, user_level
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User

class userSuperSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')

# class usersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = users
#         fields = ('__all__')
        
class user_levelSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_level
        fields = ('__all__')
        
class regionSerializer(serializers.ModelSerializer):
    class Meta:
        model = region
        fields = ('__all__')
        
class depotSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = depot
        fields = ('__all__')
        expandable_fields = {'reg': (regionSerializer, {'source': 'region_id', 'fields': ['region_id', 'region_txt','region_code','priority']})}

class region_authSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = region_auth
        fields = ('__all__')
        # expandable_fields = {'users': (usersSerializer, {'source': 'user_id', 'fields': ['user_id', 'username','status','password']})}

class user_detailsSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = user_details
        fields = ('__all__')
        # expandable_fields = {'users': (usersSerializer, {'source': 'user_id', 'fields': ['user_id', 'username','status','password']})}

class master_dataSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data
        fields = ('__all__')  

class documentSerializer(serializers.ModelSerializer):
    class Meta:
        model = document
        fields = ('__all__')  

class movementSerializer(serializers.ModelSerializer):
    class Meta:
        model = movement
        fields = ('__all__')  
        

class testqrSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data
# this will show only below mentioned fields
        fields = '__all__'
        
# by using the below code we can show the relevent table's column names through the django restframework.
class QRUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data
        fields = ( "visible_material_no", "qr_id")
        # inside the brackets we can give column names that we want to show in the restframework
        
# ===============================================================================================

    
class MasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = master_data
        fields = ("visible_material_no", "qr_id")
        
        
""" 
Extend user and autohnticatons

"""
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        # Add custom claims
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    password  = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()

        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance
    
# =========================get data through api and check================================================
class QrDataSerializer(serializers.Serializer):
    depot = serializers.CharField()
    visible_material_no = serializers.CharField()
    # visible_material_no = serializers.IntegerField()
    # email = serializers.EmailField()
    
# ===============================================================================================
# class qrSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = master_data
# # this will show only below mentioned fields
#         fields = ("material_no", "visible_material_no", "qr_id")  

# ===============================================================================================