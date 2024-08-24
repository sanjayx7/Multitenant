from rest_framework import generics
from customer.models import Customer  # Assuming you have a Customer model
from .serializers import CustomerSerializer  # Assuming you have a CustomerSerializer

class CustomerListView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
