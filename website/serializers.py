from rest_framework import serializers
from .models import CustomUser, WorkerProfile

class RegisterTelegramSerializer(serializers.Serializer):
    telegram_user_id = serializers.IntegerField()
    full_name = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    category = serializers.CharField()
    email = serializers.EmailField(required=False)

    def create(self, validated_data):
        telegram_id = validated_data['telegram_user_id']
        email = validated_data.get('email') or f"{telegram_id}@dummy.com"

        if CustomUser.objects.filter(telegram_user_id=telegram_id).exists():
            raise serializers.ValidationError("User already registered with this Telegram ID.")

        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")

        user = CustomUser.objects.create(
            email=email,
            full_name=validated_data['full_name'],
            telegram_user_id=telegram_id,
            from_telegram=True,
            
        )

        WorkerProfile.objects.create(
            user=user,
            full_name=validated_data['full_name'],
            city=validated_data['city'],
            district=validated_data['district'],
            state=validated_data['state'],
            category=validated_data['category']
        )

        return user
