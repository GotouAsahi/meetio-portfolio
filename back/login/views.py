from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,AllowAny

from .models import User,Icon,Banner
from .serializers import UserSerializer,UserWriteSerializers,AccountSerializer,IconSerializer,FollowSerializer,FollowListSerializer,ChangePasswordSerializer,SchoolSearchSerializer,SchoolSerializer,BannerSerializer
from rest_framework import status,generics
from django.db import transaction
from django.http import JsonResponse
from rest_framework.response import Response
import jwt
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from school.models import School
from django.db.models import Q
from .pagenations import SchoolCursorpagination
from postlist.models import Portfolio
from postlist.serializers import PortfolioSerializers
from django.db.models import F, Window
from django.db.models.functions import RowNumber
from collections import defaultdict
        
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )

    def destroy(self, request, *args,**kwrgs):
        instance = self.get_object()
        instance.is_active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserWriteViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserWriteSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )

class IconViewSet(viewsets.ModelViewSet):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    
class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    def get_queryset(self):
        queryset = Banner.objects.filter()
        image = self.request.GET.get('image')
        if image:
            print(queryset)
            queryset = queryset.filter(image=image)
            print(image)
        return queryset

class AuthRegister(generics.CreateAPIView):#user作成
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = (AllowAny,)

    @transaction.atomic
    def post(self, request, format=None):
        serializer = AccountSerializer(data=request.data)
                
        if serializer.is_valid():
            newuser=serializer.save()
            
            if newuser:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (AllowAny,)

'''
    def update(self, request, *args, **kwargs):

        print(self.request.data)
        follows = self.request.data['follows']
        instance = self.get_object()
        for user in follows:
            if  user in instance.follows.all():
                instance.follows.remove(user)

                data = User.objects.get(username=user)
                data.followers.remove(instance.id)
            else:
                instance.follows.add(user)
                data = User.objects.get(username=user)
                print(self.initial_data)
                print('aaaaaaaaaa',user)
                data.followers.add(instance.id)
        
        return super().update(request, *args, **kwargs)
    '''
    

class FollowListViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = FollowListSerializer
    permission_classes = (AllowAny,)

class ChangePasswordView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'パスワードが変更されました。'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated, )


class SchoolSerachViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = SchoolSearchSerializer
    permission_classes =(AllowAny,)#(IsAuthenticated,)
    pagination_class = SchoolCursorpagination
    
    def list(self, request, *args, **kwargs):

        language = self.request.GET.get('language')
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = serializer.data
        combined_data =[]
        portfolio = defaultdict(list)

        if language:
            #dataではなくserializer.dataに変更したらいけるかも
            data = [user for user in serializer.data if user['likelanguage'] == language]
            page = self.paginate_queryset(data)
            if page is not None:
                combined_data.append({'user':data})

                lst = [fds['id'] for fds in data]
                subquery = (
                    Portfolio.objects.values('user_id')
                    .annotate(rank=Window(expression=RowNumber(),partition_by=F('user_id'), order_by=F('created_date').desc()))
                    .filter(rank__lte=2, user_id__in=lst)
                )
    
                # 最終的なクエリ
                result = Portfolio.objects.filter(pk__in=subquery.values('pk')).order_by("-created_date")#ここで降順に並び替え（降順の場合は「-」がいるよ
                portfolioSerializer = PortfolioSerializers(result, many=True)
                for user_portfolio in portfolioSerializer.data:
                    portfolio[user_portfolio['user_id']['id']].append(user_portfolio)
                combined_data.append({'portfolios':portfolio})

                return self.get_paginated_response(combined_data)
        
        combined_data.append({'user':data})

        lst = [fds['id'] for fds in data]
        subquery = (
            Portfolio.objects.values('user_id')
            .annotate(rank=Window(expression=RowNumber(),partition_by=F('user_id'), order_by=F('created_date').desc()))
            .filter(rank__lte=2, user_id__in=lst)
        )
    
         # 最終的なクエリ
        result = Portfolio.objects.filter(pk__in=subquery.values('pk')).order_by("-created_date")#ここで降順に並び替え（降順の場合は「-」がいるよ
        portfolioSerializer = PortfolioSerializers(result, many=True)
        for user_portfolio in portfolioSerializer.data:
            portfolio[user_portfolio['user_id']['id']].append(user_portfolio)
        combined_data.append({'portfolios':portfolio})
        
        return self.get_paginated_response(combined_data)
    
    def get_queryset(self):
        queryset = User.objects.filter(Profession='学生')
        filters = {}

        grade = self.request.GET.get('grade')
        department = self.request.GET.get('department')
        name = self.request.GET.get('name')

        if grade:
            filters['school__grade__icontains'] = grade
        if department:
            filters['school__department__icontains'] = department
        if name:
            filters['school__name__icontains'] = name

        if filters:
            queryset = queryset.filter(Q(**filters))
        
        return queryset