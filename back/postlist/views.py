from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import viewsets, filters
from .models import Portfolio,Tag,Image,TitleImage,Comment,Reply,Ganre,Category,Portfolio_Draft
from .serializers import (TechnologiesSerializers, BusinessesSerializers, CreativesSerializers, SoundsSerializers,
                          VideosSerializers, DesignsSerializers, TagSerializer, WriteSerializers, PortfolioSerializers, ImageSerializer, TitleImageSerializer,
                          CommentSerializer, ReplySerializer, CommentListSerializer, GanreSerializer, CategorySerializer, LikeSerializers, EmailSerializer,
                          LikeListSerializer, FollowUserPostSerializer,PortfolioDetailSerializer,
                          schoolPostListSerializer,
                          Portfolio_DraftSerializers,
                          DraftSerializers,
                          UserSerializer)
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from login.models import User
from rest_framework import status, generics
from rest_framework.views import APIView
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.db.models import Count
import logging
from rest_framework.parsers import MultiPartParser, FormParser
from login.views import SchoolSerachViewSet
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from django.core.paginator import Paginator
from .pagenations import CustomCursorpagination ,SchoolCursorpagination, UserShowCursorpagination
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# 以下データ抽出
class SearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(sentence__icontains=keyword) | Q(ganre_id__name__icontains=keyword) | 
                Q(category_id__name__icontains=keyword) | Q(tag__name__icontains=keyword)).distinct()
        return queryset

class TagSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(tag__name__iexact=keyword)).distinct()
        return queryset

class GanreSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        keyword = self.request.GET.get('keyword')
        if keyword:
            queryset = queryset.filter(
                Q(ganre_id__name__icontains=keyword))
        return queryset

class WriteViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = WriteSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )

    def destroy(self, request, *args,**kwrgs):
        instance = self.get_object()
        instance.is_public = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WriteViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = WriteSerializers
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_public = False
        instance.save()
        # return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        print("Received request data:", request.data)
        movie_file = request.data.get('movie')

        # タグを取得して保存
        if 'tag' in request.data:
            tag_data = request.data.getlist('tag')  # 複数のタグを取得
            
            for i in tag_data:
                if not Tag.objects.filter(name=i).exists():
                    tag_serializer = TagSerializer(data={'name': i})
                    if tag_serializer.is_valid():
                        tag_serializer.save()

        serializer = WriteSerializers(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # ビデオファイルを含む場合のレスポンス
            if movie_file:
                # ビデオファイルへのURLをレスポンスに含める
                instance.movie_url = instance.movie.url
                serializer = WriteSerializers(instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
            print("Received request data:", request.data)
            if 'tag' in self.request.data:
                tag_data = self.request.data.getlist('tag')
                for i in tag_data:
                    if not Tag.objects.filter(name=i).exists():
                        tag_serializer = TagSerializer(data={'name':i})
                        if tag_serializer.is_valid():
                            tag_serializer.save()
            serializer = WriteSerializers(data=request.data)
            if serializer.is_valid():
                # オブジェクトの更新
                instance = self.get_object()
                serializer.update(instance, serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DraftViewSet(viewsets.ModelViewSet):
    queryset = Portfolio_Draft.objects.all()
    serializer_class = DraftSerializers
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        print("Received request data:", request.data)
        movie_file = request.data.get('movie')

        # タグを取得して保存
        if 'tag' in request.data:
            tag_data = request.data.getlist('tag')  # 複数のタグを取得
            
            for i in tag_data:
                if not Tag.objects.filter(name=i).exists():
                    tag_serializer = TagSerializer(data={'name': i})
                    if tag_serializer.is_valid():
                        tag_serializer.save()

        serializer = DraftSerializers(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()

            # ビデオファイルを含む場合のレスポンス
            if movie_file:
                # ビデオファイルへのURLをレスポンスに含める
                instance.movie_url = instance.movie.url
                serializer = DraftSerializers(instance)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, pk=None):
            print("Received request data:", request.data)
            if 'tag' in self.request.data:
                tag_data = self.request.data.getlist('tag')
                for i in tag_data:
                    if not Tag.objects.filter(name=i).exists():
                        tag_serializer = TagSerializer(data={'name':i})
                        if tag_serializer.is_valid():
                            tag_serializer.save()
            serializer = DraftSerializers(data=request.data)
            if serializer.is_valid():
                # オブジェクトの更新
                instance = self.get_object()
                serializer.update(instance, serializer.validated_data)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    # queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).order_by('-created_date')
    queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
    #serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PortfolioSerializers
        return PortfolioDetailSerializer
    
    def update(self, request, pk=None):
        instance = get_object_or_404(Portfolio, id=pk)
        instance.view_count += 1
        instance.save()
        return Response({'message': 'View count increased.'})
    
class Portfolio_New_ViewSet(viewsets.ReadOnlyModelViewSet):
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).order_by('-created_date')
    # queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
    #serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PortfolioSerializers
        return PortfolioDetailSerializer
    
    def update(self, request, pk=None):
        instance = get_object_or_404(Portfolio, id=pk)
        instance.view_count += 1
        instance.save()
        return Response({'message': 'View count increased.'})

class Portfolio_Draft_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio_Draft.objects.order_by('-created_date')
    serializer_class = Portfolio_DraftSerializers
    permission_classes =(IsAuthenticated, )
    pagination_class = CustomCursorpagination
    
    def get_queryset(self):
        user_id=self.request.user.id
        queryset = Portfolio_Draft.objects.filter(user_id=user_id).order_by('-created_date')
        return queryset
    
class Portfolio_Paginator_ViewSet(viewsets.ReadOnlyModelViewSet):
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).order_by('-created_date')
    #serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    #↓pagenations.pyからページネーション機能を呼び出している
    pagination_class= CustomCursorpagination
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PortfolioSerializers
        return PortfolioDetailSerializer
    
    def update(self, request, pk=None):
        instance = get_object_or_404(Portfolio, id=pk)
        instance.view_count += 1
        instance.save()
        return Response({'message': 'View count increased.'})

class MyPortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.order_by('-created_date')
    serializer_class = PortfolioSerializers
    permission_classes =(IsAuthenticated, )
    pagination_class = UserShowCursorpagination

    def get_queryset(self):
        user_id=self.request.user.id
        queryset = Portfolio.objects.filter(user_id=user_id).order_by('-created_date')
        return queryset

class UserPortfolioViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.order_by('-created_date')
    serializer_class = PortfolioSerializers
    pagination_class = UserShowCursorpagination
    permission_classes =(AllowAny,)

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(user_id=id)
        return queryset

class TaglistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )


class TechnologiesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=1).order_by('-created_date')
    serializer_class = TechnologiesSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination
    

class BusinessesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=2).order_by('-created_date')
    serializer_class = BusinessesSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination


class CreativesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=3).order_by('-created_date')
    serializer_class = CreativesSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

class SoundsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=4).order_by('-created_date')
    serializer_class = SoundsSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

class VideosViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=5).order_by('-created_date')
    serializer_class = VideosSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

class DesignsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.filter(category_id=6).order_by('-created_date')
    serializer_class = DesignsSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    pagination_class = CustomCursorpagination

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class TitleImageViewSet(viewsets.ModelViewSet):
    queryset = TitleImage.objects.all()
    serializer_class = TitleImageSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    create_serializer_class = CommentSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    def get_serializer_class(self):
        if self.action == 'create':
            return self.create_serializer_class
        return super().get_serializer_class()

    def destroy(self, request, *args,**kwrgs):
        instance = self.get_object()
        instance.is_public = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_queryset(self):
        queryset = Comment.objects.filter(is_public=True)
        target = self.request.query_params.get('target')
        if target:
            queryset = queryset.filter(target=target)
        return queryset

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )

    def destroy(self, request, *args,**kwrgs):
        instance = self.get_object()
        instance.is_public = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

class GanreViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ganre.objects.all()
    serializer_class = GanreSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = LikeSerializers
    filter_backends = (filters.SearchFilter,)
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    search_fields = ('like_count')

"""
class MyLikeListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all()
    serializer_class = MyLikeListSerializer
    permission_classes =(AllowAny,)
    filter_backends = (filters.SearchFilter,)
    
    def get_queryset(self):
        user = self.request.GET.get('user')
        queryset = Portfolio.objects.filter(like_count = user)
        return queryset
""" 

class LikeListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = LikeListSerializer
    permission_classes =(AllowAny,)
    
    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(like_count=id)
        return queryset

class LikeList_Pagination_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = LikeListSerializer
    permission_classes =(AllowAny,)
    pagination_class = CustomCursorpagination
    
    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(like_count=id)
        return queryset
    
class LikeUserShow_Pagination_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = LikeListSerializer
    permission_classes =(AllowAny,)
    pagination_class = UserShowCursorpagination
    
    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            queryset = queryset.filter(like_count=id)
        return queryset
    

      
class SendEmailView(generics.CreateAPIView):
    serializer_class = EmailSerializer
    permission_classes =(IsAuthenticated,)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        to_email = serializer.validated_data['to_email']
        title = f"{request.user.username}さんからスカウトが来ています！！"
        sentence = (
            f"{request.user.username}さんからスカウトが来ています！\n"
            f"ぜひ{request.user.username}さんの詳細を見てみましょう！！\n"
            f"{settings.BASE_URL}user/{request.user.id}\n\n"
            f"{request.user.username}さんのメールアドレス：{request.user.email}"
        )
        context={'username':f"{request.user.username}",'userURL': f"{settings.BASE_URL}user/{request.user.id}", 'mail': f"{request.user.email}"}
        html_message = render_to_string('mailer/template_mail.html', context)
        text_content = strip_tags(html_message)
        send_mail(title, text_content, 'pbl2pbl2a@gmail.com', [to_email], html_message=html_message, fail_silently=False)
        headers = self.get_success_headers(serializer.data)
        return Response({'message': 'Email sent successfully.'}, status=status.HTTP_201_CREATED, headers=headers)
    
class like_count_sort_Viewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)
    '''
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()
    '''

    def get_queryset(self):
        today = datetime.now().astimezone()
        next = today - timedelta(days=7)
        genre = self.request.query_params.get('Genre')
        category = self.request.query_params.get('Category')
        queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()
        if genre:
            queryset = queryset.filter(ganre_id=genre)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset
    
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()

class like_count_sort_Pagination_Viewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)
    pagination_class = CustomCursorpagination
    '''
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()
    '''

    def get_queryset(self):
        today = datetime.now().astimezone()
        next = today - timedelta(days=7)
        genre = self.request.query_params.get('Genre')
        category = self.request.query_params.get('Category')
        queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()
        if genre:
            queryset = queryset.filter(ganre_id=genre)
        if category:
            queryset = queryset.filter(category_id=category)
        return queryset
    
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()

class like_count_sort_all_Viewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)
    pagination_class = CustomCursorpagination
    '''
    today = datetime.now().astimezone()
    next = today - timedelta(days=7)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next).annotate(Count("like_count")).order_by('like_count__count').reverse()
    '''

    def get_queryset(self):
        genre = self.request.query_params.get('Genre')
        category = self.request.query_params.get('Category')
        tag = self.request.query_params.get('Tag')
        keyword = self.request.query_params.get('Keyword')
        queryset = Portfolio.objects.filter(is_public=True).annotate(Count("like_count")).order_by('like_count__count').reverse()
        if genre:
            queryset = queryset.filter(ganre_id__name=genre)
        if category:
            queryset = queryset.filter(category_id__name=category)
        if tag:
            queryset = queryset.filter(
                Q(tag__name__iexact=tag)).distinct()
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(sentence__icontains=keyword) | Q(ganre_id__name__icontains=keyword) | 
                Q(category_id__name__icontains=keyword) | Q(tag__name__icontains=keyword)).distinct()
        return queryset
    
    queryset = Portfolio.objects.filter(is_public=True).annotate(Count("like_count")).order_by('like_count__count').reverse()
class FollowUserPostViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = FollowUserPostSerializer
    permission_classes =(AllowAny,)

    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True ).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            user = User.objects.get(id=id)
            follows = user.follows.all()
            queryset = queryset.filter(user_id__in=follows)
        return queryset
    
class FollowUserPost_Pagination_ViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = FollowUserPostSerializer
    permission_classes =(AllowAny,)
    pagination_class = CustomCursorpagination
    
    def get_queryset(self):
        queryset = Portfolio.objects.filter(is_public=True ).order_by('-created_date')
        id = self.request.query_params.get('id')
        if id:
            user = User.objects.get(id=id)
            follows = user.follows.all()
            queryset = queryset.filter(user_id__in=follows)
        return queryset

class SchoolPostListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Portfolio.objects.all().order_by('-created_date')
    serializer_class = schoolPostListSerializer
    permission_classes =(AllowAny,)
    #pagination_class = SchoolCursorpagination

    def get_queryset(self):

        #queryset = Portfolio.objects.filter(user_id=1).order_by('-created_date')
        school = User.objects.filter(Profession='学生')#.order_by('-created_at')
        grade = self.request.GET.get('grade')
        department = self.request.GET.get('department')
        name = self.request.GET.get('name')
        if grade and department and name:
            school = school.filter(Q(school__grade__icontains=grade) & Q(school__department__icontains=department) & Q(school__name__icontains=name))
        elif grade and department:
            school = school.filter(Q(school__grade__icontains=grade) & Q(school__department__icontains=department))
        elif grade and name:
            school = school.filter(Q(school__grade__icontains=grade) & Q(school__name__icontains=name))
        elif department and name:
            school = school.filter(Q(school__department__icontains=department) & Q(school__name__icontains=name))
        elif grade:
            school = school.filter(Q(school__grade__icontains=grade))
        elif department:
            school = school.filter(Q(school__department__icontains=department))
        elif name:
            school = school.filter(Q(school__name__icontains=name))
        else :
            school = school.none()
        
        result_list =[]

        #queryset = Portfolio.objects.filter().order_by('-created_date')
        
        ''''
        for fds in school:
            queryset = Portfolio.objects.filter(user_id=fds.id).order_by('-created_date')[:3]
            result_list.extend(queryset)
        '''
    
        lst = [fds.id for fds in school]
        test = []
        #サブクエリでlst（学校や学科検索に合致したuserIDたち）をPortfolioから検索。またPortfolioも作成日を降順に並び替えている（昇順だと古い二件がくるため）
        #rank__lte=2が二件までに絞っている
        subquery = (
            Portfolio.objects.values('user_id')
            .annotate(rank=Window(expression=RowNumber(),partition_by=F('user_id'), order_by=F('created_date').desc()))
            .filter(rank__lte=2, user_id__in=lst)
        )
        '''
        for fds in school:
            subquery = Portfolio.objects.filter(user_id__id=fds.id).order_by('user_id__id')[:2]
            print("subquery",subquery)
            test.append(subquery)
            print('test = ',test)
        '''

        # 最終的なクエリ
        result = Portfolio.objects.filter(pk__in=subquery.values('pk')).order_by("-created_date")#ここで降順に並び替え（降順の場合は「-」がいるよ
        return result
    
class topImage_Viewset(viewsets.ReadOnlyModelViewSet):
    serializer_class = PortfolioSerializers
    permission_classes =(AllowAny,)
    today = datetime.now().astimezone()
    next = today - timedelta(days=30)
    queryset = Portfolio.objects.filter(is_public=True, created_date__gte = next, category_id__name='クリエイティブ').annotate(Count("like_count")).order_by('like_count__count').reverse()[:10]
