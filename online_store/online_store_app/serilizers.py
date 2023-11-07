from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers

from .models import UserCustom, Product, Category


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


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(max_length=30, required=True)
    description = serializers.CharField(max_length=500, required=False)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'description', 'total_amount')

    def get_total_amount(self, obj):
        return Category.objects.filter(pk=obj.id).aggregate(Sum('product__quantity'))['product__quantity__sum']
