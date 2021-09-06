
from rest_framework import serializers
from .models import User, Friend_Request



# class UserSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     online = serializers.ReadOnlyField(source='userprofile.online')

#     class Meta:
#         model = User
#         fields = ['id','username', 'password', 'online']


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    to_user= serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())
    # from_user_id = serializers.IntegerField(source='from_user.id')
    from_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Friend_Request
        fields = ['from_user', 'to_user', 'from_user_id']

    def get_from_user_id(self, obj):
        return obj.from_user.id
        print('success')