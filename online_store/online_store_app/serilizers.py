from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import UserCustom, Product


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserCustom
        fields = ('email', 'password')


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, required=True)
    name = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, required=True)
    password_confirmation = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = UserCustom
        fields = ('email', 'name', 'password', 'password_confirmation')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirmation']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = UserCustom.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
            password=make_password(validated_data['password']),
        )
        return user


class ProductViewSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(read_only=True)
    description = serializers.ReadOnlyField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    price = serializers.ReadOnlyField(read_only=True)
    quantity = serializers.ReadOnlyField(read_only=True)

    class Meta:
        model = Product
        fields = ('name', 'description', 'category_name', 'price', 'quantity')
