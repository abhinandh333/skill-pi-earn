from rest_framework import serializers
from .models import CustomUser, WorkerProfile
from website.models import Profile  # ✅ Make sure it's imported

class RegisterTelegramSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    category = serializers.CharField()
    city = serializers.CharField()
    district = serializers.CharField()
    state = serializers.CharField()
    phone_number = serializers.CharField()
    telegram_user_id = serializers.IntegerField()
    email = serializers.EmailField(required=False, allow_null=True)

    def create(self, validated_data):
        telegram_id = validated_data['telegram_user_id']
        phone_number = validated_data['phone_number']
        email = validated_data.get('email') or f"{phone_number}@skillpi.com"

        # 🔍 Try to get existing user (based on telegram ID)
        user, user_created = CustomUser.objects.get_or_create(
            telegram_user_id=telegram_id,
            defaults={
                'full_name': validated_data['full_name'],
                'phone_number': phone_number,
                'email': email,
                'from_telegram': True,
            }
        )

        if not user_created:
            # If user exists, check if WorkerProfile exists
            if WorkerProfile.objects.filter(user=user).exists():
                raise serializers.ValidationError("User already registered with this Telegram ID.")

        # ✅ Create or update WorkerProfile
        WorkerProfile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': validated_data['full_name'],
                'category': validated_data['category'],
                'city': validated_data['city'],
                'district': validated_data['district'],
                'state': validated_data['state'],
                'phone_number' : validated_data['phone_number'],
            }
        )

        # ✅ Create or update main Profile (used in Django search)
        Profile.objects.update_or_create(
            user=user,
            defaults={
                'full_name': validated_data['full_name'],
                'phone_number': phone_number,
                'category': validated_data['category'],
                'city': validated_data['city'],
                'district': validated_data['district'],
                'state': validated_data['state']
            }
        )

        return user
