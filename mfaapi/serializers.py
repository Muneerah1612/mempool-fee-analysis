from django.contrib.auth.models import User, Group
from rest_framework import serializers


class TxSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['rpc-user','rpc-pass','txid','rpc-port']