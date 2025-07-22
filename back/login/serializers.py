from .models import User,Icon,Banner
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer #追加
from school.models import School
from school.serializers import SchoolSerializer
from postlist.models import Portfolio
from judge.models import Submission_results
import json
from django.db.models import Count
from django.http import QueryDict
class UserSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(read_only=True)
    difficulty_level_count = serializers.SerializerMethodField()
    language_answer_count = serializers.SerializerMethodField()
    likelanguage = serializers.SerializerMethodField()
    """ A serializer class for the User model """
    class Meta:
        model = User
        fields = ('id','username','nickname','icon','banner','email','Profession','introduction',
                  'gender','github','twitter','instagram','facebook','pixiv','follows','followers','school','difficulty_level_count','rank','language_answer_count','likelanguage','scout_receive')
    def get_difficulty_level_count(self, obj):
        difficulty_counts = []
        for i in range(1,6):
            count=Submission_results.objects.filter(problem_id__difficulty=i,user_id=obj.id,status="AC").count()
            difficulty_counts.append(count)
        difficulty_counts=difficulty_counts[::-1]
        
        return difficulty_counts
    def get_language_answer_count(self, obj):
        language_counts = Submission_results.objects.filter(user_id=obj.id,status="AC").values('language').annotate(count=Count('language')).order_by('-count')
        converted_data = {entry["language"]: entry["count"] for entry in language_counts}
        return converted_data
    def get_likelanguage(self, obj):
        language_counts = Submission_results.objects.filter(user_id=obj.id,status="AC").values('language').annotate(count=Count('language')).order_by('-count')
        print("データベース接続")
        converted_data = {entry["language"]: entry["count"] for entry in language_counts}
        return sorted(converted_data.items(), key=lambda x: x[1], reverse=True)[0][0] if converted_data else None
    def create(self, validated_data):
        school = School.objects.create()
        validated_data['school'] = school
        return super().create(validated_data)
    
class UserWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','nickname','icon','banner','email','Profession','introduction','gender','github','twitter','instagram','facebook','pixiv','followers','school','scout_receive']

class IconSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = Icon
        fields = "__all__"
        
class BannerSerializer(serializers.ModelSerializer):
    """ A serializer class for the User model """
    class Meta:
        model = Banner
        fields = "__all__"
    

class AccountSerializer(serializers.ModelSerializer):
    #確認用のパスワードを作成
    confirm_password = serializers.CharField(write_only=True, required=True) 
    class Meta: #　表示したり、create時のrequiredのキー
        model = User
        fields = ('email', 'username', 'password', 'confirm_password',)#required?? 
        extra_kwargs = {'password': {'write_only': True}}#write_onlyなのでpasswordはkeyに入らない

    def create(self, validated_data): #validated_dataはviews.pyから入ってくるデータ
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def validate(self, data):#パスワードと確認用が一致しているかのvalidation
        password = data.get('password')
        confirm_password = data.pop('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError('パスワードが一致していません')
        return data


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('follows','followers')
    
    def update(self, instance, validated_data):
        
        follows = validated_data['follows']
        for user in follows:
            if  user in instance.follows.all():
                instance.follows.remove(user)
                data = User.objects.get(id=self.initial_data['follows'][0])
                print('data = ',data)
                print('instance = ', instance.id)
                data.followers.remove(instance.id)
            else:
                instance.follows.add(user)
                data = User.objects.get(id=self.initial_data['follows'][0])
                print(self.initial_data)
                print('aaaaaaaaaa',user)
                data.followers.add(instance.id)
        return instance
    
# class FollowListSerializer(serializers.ModelSerializer):
#     follows = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")
#     followers = serializers.SlugRelatedField(queryset=User.objects.all(), many=True, slug_field="username")
#     class Meta:
#         model = User
#         fields = ('follows','followers')

class FollowListSerializer(serializers.ModelSerializer):
    follows = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

    def get_follows(self, obj):
        follows = obj.follows.all()
        return [{'id': user.id, 'username': user.username,'usericon':user.icon  } for user in follows]

    def get_followers(self, obj):
        followers = obj.followers.all()
        return [{'id': user.id, 'username': user.username,'usericon':user.icon } for user in followers]

    class Meta:
        model = User
        fields = ('follows', 'followers')


class ChangePasswordSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('current_password', 'new_password', 'confirm_password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = self.context['request'].user
        current_password = validated_data.pop('current_password', None)
        new_password = validated_data.pop('new_password', None)
        if user.check_password(current_password):
            user.set_password(new_password)
            user.save()
        else:
            raise serializers.ValidationError('現在のパスワードが正しくありません。')
        return validated_data

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError('パスワードが一致していません')
        return data


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class SchoolSearchSerializer(serializers.ModelSerializer):
    school = SchoolSerializer()
    likelanguage = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id','username','nickname','icon','introduction','school','likelanguage')

    '''
    def to_representation(self, instance):
        convert_data = []
        drf_data = super().to_representation(instance)
        hoge = Portfolio.objects.filter(user_id__id=drf_data['id']).order_by('-created_date').values()[:2]
        print("データベース接続")
        drf_data['portfolio'] = hoge
        #print('portfolio = ', hoge)
        return drf_data
    '''

    def get_likelanguage(self, obj):
        language_counts = Submission_results.objects.filter(user_id=obj.id,status="AC").values('language').annotate(count=Count('language')).order_by('-count')
        print("データベース接続")
        converted_data = {entry["language"]: entry["count"] for entry in language_counts}
        return sorted(converted_data.items(), key=lambda x: x[1], reverse=True)[0][0] if converted_data else None
    