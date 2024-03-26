from rest_framework import serializers
from product.models import Category,Product,Review,KhaltiInfo
from user_authentication.serializers import UserAccount
from product.validators import name_validator

class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length = 50,validators=[name_validator])
    
    def create(self,validated_data):
        return Category.objects.create(name=validated_data['name'])
    
    def update(self,instance,validated_data):
        instance.name = validated_data.get('name',instance.name) 
        instance.save()
        return instance

class ProductSerializer(serializers.Serializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_name = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=250)
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    description = serializers.CharField(max_length=250, default='')    
    product_image = serializers.ImageField()
    is_available = serializers.BooleanField(default=True)
    
    class Meta:
        model = Product
        fields = [
            'category',
            'name',
            'price',
            'description',
            'product_image',
            'is_available'
        ]
    
    def get_category_name(self, obj):
        return obj.category.name if obj.category else None
    
    def create(self,validated_data):
        fields={
            "category" : validated_data['category'],
            "name":validated_data['name'],
            "price" : validated_data['price'],
            "description" : validated_data['description'],
            "product_image" : validated_data['product_image'],
            "is_available":validated_data['is_available']
        }
        return Product.objects.create(**fields)
    
    def update(self, instance, validated_data):
        instance.category=validated_data.get('category',instance.category)
        instance.name=validated_data.get('name',instance.name)
        instance.price=validated_data.get('price',instance.price)
        instance.description=validated_data.get('description',instance.description)
        instance.product_image=validated_data.get('product_image',instance.product_image)
        instance.is_available = validated_data.get('is_available',instance.is_available)
        instance.save()
        return instance

class ReviewSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product_name = serializers.SerializerMethodField()
    date_created = serializers.DateTimeField(read_only=True)
    description = serializers.CharField(default="description")
    user_id= serializers.PrimaryKeyRelatedField(queryset=UserAccount.objects.all())
    user_name = serializers.SerializerMethodField()
    
    def get_product_name(self, obj):
        return obj.product.name if obj.product else None

    def get_user_name(self, obj):
        return obj.user.first_name if obj.user else None
    
    def create(self, validated_data):
        fields = {
            'product' : validated_data['product_id'],
            'description' : validated_data['description'],
            'user' :validated_data['user_id']
        }
        return Review.objects.create(**fields)


class KhaltiSerializer(serializers.Serializer):
    pixd = serializers.CharField(max_length = 250)
    transaction_id= serializers.CharField(max_length = 250)
    tidx= serializers.CharField(max_length = 250)
    amount= serializers.IntegerField()
    total_amount=serializers.IntegerField()
    mobile=serializers.CharField(max_length = 50)
    status=serializers.CharField(max_length = 250)
    purchase_order_id=serializers.CharField(max_length = 250)
    purchase_order_name=serializers.CharField(max_length = 250)
    
    class Meta:
        model = KhaltiInfo
        fields={
            "pixd",
            "transaction_id",
            "tixd",
            "amount",
            "total_amount",
            "mobile",
            "status",
            "purchase_order_id",
            "purchase_order_name"
        }
        
    def create(self,validated_data):
        data={
            'pixd' : validated_data["pixd"],
            'transaction_id' : validated_data["transaction_id"],
            'tixd' : validated_data["tixd"],
            'amount' : validated_data["amount"],
            'total_amount' :validated_data["total_amount"],
            'mobile' : validated_data["mobile"],
            'status' : validated_data["status"],
            'purchase_order_id' : validated_data["purchase_order_id"],
            'purchase_order_name' :validated_data["purchase_order_name"],
        }
        
        return KhaltiInfo.objects.create(**data)
        
        
