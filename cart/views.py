from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart,CartItems
from cart.serializers import CartItemSerializer,CartSerializer
from rest_framework.response import Response
from product.models import Product
from rest_framework import status
from user_authentication.views import get_success,get_error

# Create your views here.
class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        user=request.user
        cart = Cart.objects.filter(user=user,status=False).first()
        qs = CartItems.objects.filter(cart=cart)
        serializer = CartItemSerializer(qs,many=True)
        return Response(get_success(200,"Cart data",serializer.data), status=status.HTTP_200_OK) 

    
    def post(self,request):
        cart,_ = Cart.objects.get_or_create(user=request.user,status = False)
        product = Product.objects.get(id=request.data.get('product'))
        price = product.price
        quantity = request.data.get('quantity')
        cart_items = CartItems(cart=cart,user=request.user,product=product,price=price,quantity=quantity)
        cart_items.save()
        total_price = 0
        cart_items = CartItems.objects.filter(user=request.user,cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response(get_success(200,"Items added to the cart"), status=status.HTTP_200_OK) 
    
    def patch(self,request):
        cart_item = CartItems.objects.filter(id=request.data.get('id')).first()
        quantity = request.data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response(get_success(200,"Items updated"), status=status.HTTP_200_OK) 

    
    def delete(self,request):
        cart_item = CartItems.objects.get(id = request.data.get('id'))
        cart_item.delete()
        
        cart = Cart.objects.filter(user=request.user,status = False).first()
        qs = CartItems.objects.filter(cart = cart)
        serializer = CartItemSerializer(qs,many = True)
        return Response(get_success(200,"Items deleted",serializer.data), status=status.HTTP_200_OK) 


class Checkout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self,request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart,many=True) 
        return Response(get_success(200,"Checkout items",serializer.data), status=status.HTTP_200_OK) 



#after payment 
# cart.status = True
# cart.save()