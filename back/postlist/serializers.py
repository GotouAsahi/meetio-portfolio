from rest_framework import serializers

from .models import Portfolio, Tag, Category, Ganre, Image, TitleImage, Comment, Reply, Portfolio_Draft
from django.contrib.auth import get_user_model
import json
# from django.http import JsonResponse
from login.models import User
# from django.shortcuts import render
from school.serializers import SchoolSerializer
# from login.serializers import FollowListSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class GanreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ganre
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    school=SchoolSerializer(read_only=True)
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'icon', 'nickname', 'email', 'Profession', 'introduction', 'gender', 'school']
class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'icon', 'nickname', 'email', 'Profession', 'introduction', 'gender']

class PortfolioSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    category_id = CategorySerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class Portfolio_DraftSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    category_id = CategorySerializer()
    class Meta:
        model = Portfolio_Draft
        fields = '__all__'

class PortfolioDetailSerializer(serializers.ModelSerializer):
    user_id = UserDetailSerializer()
    ganre_id = GanreSerializer()
    category_id = CategorySerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'
        

class WriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id', 'title', 'title_image', 'sentence','movie', 'category_id', 'ganre_id', 'user_id', 'tag','is_public']

class DraftSerializers(serializers.ModelSerializer):
    class Meta:
        model = Portfolio_Draft
        fields = ['id', 'title', 'title_image', 'sentence','movie', 'category_id','tag','ganre_id', 'user_id',]


class TechnologiesSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class BusinessesSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class CreativesSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class SoundsSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class VideosSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class DesignsSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    ganre_id = GanreSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"

class TitleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TitleImage
        fields = "__all__"
class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["id", "user", "text"]
        context = None
    def create(self, validated_data):
        reply = Reply.objects.create(**validated_data)
        id = self.context['request'].query_params.get('id')
        comments = Comment.objects.filter(id=id)#変更
        if comments:
            for comment in comments:
                comment.reply.add(reply)
        return reply

class ReplyListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Reply
        fields = ["id", "user", "text", "created_at"]

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "text", "target", "reply"]
    

class CommentListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    reply = ReplyListSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "text", "target", "reply", "created_at"]
    

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["id", "like_count"]

    #返却時だけdrfの表示を変更できるやつ
    def to_representation(self, instance):
        convert_data = []
        #↓drfに表示されているデータを取得（ポートフォリオidとlike_list）
        drf_data = super().to_representation(instance)
        #いいねしているユーザーIDをUserテーブルから検索して、UserNameを抽出してdataに格納する
        for count in range(len(drf_data['like_count'])):
           #like_count内のユーザーをUserテーブルから抽出する（Usernameを抽出するため）
           like_count = User.objects.get(id=super().to_representation(instance)['like_count'][count])
           #json.dumpsしないとエラー吐く
           json.dumps(like_count,default=str)
           convert_data.append({'portfolio_id':drf_data['id'],'user_id':like_count.id,'username':like_count.username})
        #drf_dataにlike_listを作成してconvert_dataを格納する
        drf_data['like_count'] = convert_data
        #検索用のデータは削除する（ポートフォリオidとlike_list）
        del drf_data['id']
        return drf_data
   
    def update(self, instance, validated_data):
        like_count = validated_data.pop('like_count')
        instance.save()
        for user in like_count:
            if user in instance.like_count.all():
                #テーブル内にある場合は削除（いいね解除）
                instance.like_count.remove(user)
            else:
                #テーブルにない場合はテーブルに追加（いいね）
                instance.like_count.add(user)
        return instance
        
class EmailSerializer(serializers.Serializer):

    to_email = serializers.EmailField()

class MyLikeListSerializer(serializers.Serializer):
    user_id=UserSerializer()
    ganre_id=GanreSerializer()
    category_id=CategorySerializer()
    like_count = UserSerializer(many=True)
    
    class Meta:
        model = Portfolio
        fields = ['like_count']

class LikeListSerializer(serializers.ModelSerializer):
    user_id=UserSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'
    

class FollowUserPostSerializer(serializers.ModelSerializer):
    user_id=UserSerializer()
    ganre_id=GanreSerializer()
    category_id=CategorySerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'

class schoolPostListSerializer(serializers.ModelSerializer):
    user_id=UserSerializer()
    class Meta:
        model = Portfolio
        fields = '__all__'



    #返却時だけdrfの表示を変更できるやつ
    '''
    def to_representation(self, instance):
        convert_data = []
        #↓drfに表示されているデータを取得（ポートフォリオidとlike_list）
        drf_data = super().to_representation(instance)
        id = super().to_representation(instance)['user_id']['id']
        convert_data.append({id:drf_data})
        return convert_data
    '''