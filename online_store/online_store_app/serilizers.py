from django.contrib.auth.hashers import make_password
from django.db.models import Sum
from rest_framework import serializers

from .models import UserCustom, Product, Category, HistoryChanges


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


class HistoryChangesSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(write_only=True, required=False)
    date_changes = serializers.DateTimeField(read_only=True)
    quantity_old = serializers.IntegerField(min_value=0, required=True)
    quantity_now = serializers.IntegerField(min_value=0, required=True)

    class Meta:
        model = HistoryChanges
        fields = ('product_id', 'date_changes', 'quantity_old', 'quantity_now')

    def create(self, validated_data):
        history = HistoryChanges.objects.create(
            product_id=validated_data['product_id'],
            quantity_old=validated_data['quantity_old'],
            quantity_now=validated_data['quantity_now']
        )
        return history


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    name = serializers.CharField(min_length=5, max_length=50, required=True)
    description = serializers.CharField(max_length=500, required=False)
    price = serializers.DecimalField(max_digits=19, decimal_places=2, min_value=0, required=True)
    quantity = serializers.IntegerField(min_value=0, required=True)
    category_id = serializers.IntegerField(write_only=True, required=True)
    history = HistoryChangesSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'quantity', 'category_id', 'history')

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        instance.price = validated_data.get("price", instance.price)
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.category_id = validated_data.get("category_id", instance.category_id)
        instance.save()
        return instance

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
