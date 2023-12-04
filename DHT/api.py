import serial as serial
from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
import rest_framework
@api_view(["GET","POST"])
def dhtuser(request, serial=None):
    if request.method=="GET":
          all=Dht11.objects.all()
          dataSer=DHT11serialize(all,many=True) # les donnée se form fichier JSON
          return Response(dataSer.data)
    elif request.method=="POST":
        serial=DHT11serialize(data=request.data)
        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)
            if (int(derniere_temperature) > 10):
                # Alert Email
                subject = 'Alerte'
                message = 'Il y a une alerte importante sur votre Capteur latempérature dépasse le seuil'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = ['imane.madrane20@ump.ac.ma']
                send_mail(subject, message, email_from, recipient_list)
        return Response(serial.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serial.id, status=status.HTTP_400_CREATED)