from rest_framework import serializers

from restaurant_management.users.models import User


class UserRetrievingSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class UserCreateSerializer(serializers.ModelSerializer[User]):
    password_confirmation = serializers.CharField(
        write_only=True,
        min_length=6,
        required=True,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "password_confirmation",
        )

    def validate(self, data):
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."},
            )
        return data

    def create(self, validated_data):
        del validated_data["password_confirmation"]

        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.is_staff = True
        user.save()
        return user
