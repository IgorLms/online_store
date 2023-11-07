from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from rest_framework.viewsets import GenericViewSet

from .models import UserCustom, Product, Category
from .serilizers import UserLoginSerializer, UserRegisterSerializer, ProductViewSerializer, CategorySerializer, ProductSerializer, HistoryChangesSerializer


class UserLogIn(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                    "access_token": token.key
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserRegister(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            id_user = UserCustom.objects.get(email=request.data['email'])
            if id_user is not None:
                token = Token.objects.get(user=id_user)
                response = {
                    "access_token": token.key
                }
                return Response(response, status=status.HTTP_201_CREATED)
            res = {
                'status': status.HTTP_201_CREATED
            }
            return Response(res, status=status.HTTP_201_CREATED)
        response = {
            "status": status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIViewPagination(PageNumberPagination):
    page_size = 10


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer
    pagination_class = ProductAPIViewPagination


class CategoryAPI(mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticated,)

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except ProtectedError as protected_error:
            protected_elements = [
                {"id": protected_object.pk, "label": str(protected_object)}
                for protected_object in protected_error.protected_objects
            ]
            response_data = {"protected_elements": protected_elements}
            return Response(data=response_data, status=status.HTTP_400_BAD_REQUEST)


class ProductAPI(mixins.CreateModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        pk = self.kwargs['pk']
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        return get_object_or_404(Product, pk=pk)

    def update(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = Product.objects.get(pk=pk)
        except:
            return Response({"error": "Object does not exists"})

        serializer_history = HistoryChangesSerializer(
            data={
                'product_id': instance.pk,
                'quantity_old': instance.quantity,
                'quantity_now': request.data['quantity'],

            }
        )
        serializer_history.is_valid(raise_exception=True)
        serializer_history.save()

        serializer = ProductSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"update": serializer.data})

    def create(self, request, *args, **kwargs):
        try:
            Product.objects.get(pk=request.data['category_id'])
        except:
            return Response({"error": "Object does not exists"})

        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'post': serializer.data})
