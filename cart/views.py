from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart,CartItems
from cart.serializers import CartItemSerializer,CartSerializer
from rest_framework.response import Response
from product.models import Product
from rest_framework import status
# Create your views here.

class CartView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user=request.user
        cart = Cart.objects.filter(user=user,status=False).first()
        qs = CartItems.objects.filter(cart=cart)
        serializer = CartItemSerializer(qs,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        data = request.data
        user = request.user
        cart,_ = Cart.objects.get_or_create(user=user,status = False)
        product = Product.objects.get(id=data.get('product'))
        price = product.price
        quantity = data.get('quantity')
        cart_items = CartItems(cart=cart,user=user,product=product,price=price,quantity=quantity)
        cart_items.save()
        total_price=0
        cart_items = CartItems.objects.filter(user=user,cart=cart.id)
        for items in cart_items:
            total_price += items.price
        cart.total_price = total_price
        cart.save()
        return Response({'success':"Items added to the cart"})
    
    def patch(self,request):
        data = request.data
        cart_item = CartItems.objects.filter(id=data.get('id')).first()
        quantity = data.get('quantity')
        cart_item.quantity += quantity
        cart_item.save()
        return Response({"success":"Items added"})
    
    def delete(self,request):
        user=request.user
        data = request.data
        cart_item = CartItems.objects.get(id = data.get('id'))
        cart_item.delete()
        
        cart = Cart.objects.filter(user=user,status = False).first()
        qs = CartItems.objects.filter(cart = cart)
        serializer = CartItemSerializer(qs,many = True)
        return Response(serializer.data)

class Checkout(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        cart = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(cart,many=True) 
        return Response(serializer.data)


#after payment 
# cart.status = True
# cart.save()