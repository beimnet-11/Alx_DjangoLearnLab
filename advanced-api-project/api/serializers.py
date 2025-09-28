from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate(self, data):
        if data['publication_year'] > datetime.now():
            raise serializers.ValidationError("Publication year cannot in the future.")
        return data


class AuthorSerializer(serializers.ModelSerializer):
    book = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = '__all__'