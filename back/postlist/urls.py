from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (TechnologiesViewSet, BusinessesViewSet, CreativesViewSet, SearchViewSet, PortfolioViewSet, ImageViewSet,
                    TitleImageViewSet, WriteViewSet, CommentViewSet, ReplyViewSet, CategoryViewSet, GanreViewSet, LikeViewSet,
                    TagSearchViewSet,GanreSearchViewSet,TaglistViewSet,SoundsViewSet,VideosViewSet,DesignsViewSet, SendEmailView,
                    UserPortfolioViewSet,MyPortfolioViewSet,LikeListViewSet, like_count_sort_Viewset,FollowUserPostViewSet,Portfolio_New_ViewSet,
                    like_count_sort_all_Viewset,SchoolPostListViewSet,
                    Portfolio_Paginator_ViewSet,
                    DraftViewSet,
                    Portfolio_Draft_ViewSet,like_count_sort_Pagination_Viewset,LikeList_Pagination_ViewSet,
                    FollowUserPost_Pagination_ViewSet,topImage_Viewset, LikeUserShow_Pagination_ViewSet)
from django.views.decorators.cache import cache_page

router = DefaultRouter()
router.register('post', WriteViewSet)
router.register('draft', DraftViewSet)
router.register('index', PortfolioViewSet)
router.register('userindex',UserPortfolioViewSet)
router.register('myindex',MyPortfolioViewSet)
router.register('mydraft',Portfolio_Draft_ViewSet)
router.register('technology', TechnologiesViewSet)
router.register('business', BusinessesViewSet)
router.register('creative', CreativesViewSet)
router.register('sound', SoundsViewSet)
router.register('video', VideosViewSet)
router.register('design', DesignsViewSet)
router.register('search', SearchViewSet)
router.register('tagsearch', TagSearchViewSet)
router.register('ganresearch', GanreSearchViewSet)
router.register('image', ImageViewSet)
router.register('titleimage', TitleImageViewSet)
router.register('category', CategoryViewSet)
router.register('ganre', GanreViewSet)
router.register('taglist', TaglistViewSet)
router.register('like_count_sort', like_count_sort_Viewset)
router.register('like_count_sort_all', like_count_sort_all_Viewset)
router.register('new_portfolio', Portfolio_New_ViewSet),
router.register('post_pagination', Portfolio_Paginator_ViewSet),
router.register('like_count_sort_pagination',like_count_sort_Pagination_Viewset)
router.register('like_list_pagination',LikeList_Pagination_ViewSet)
router.register('followUserPost_Pagination', FollowUserPost_Pagination_ViewSet)
router.register('like_userShow_pagination',LikeUserShow_Pagination_ViewSet)

router.register('comment', CommentViewSet)
router.register('reply', ReplyViewSet)
router.register('like', LikeViewSet)
router.register('like_list',LikeListViewSet)
router.register('followUserPost',FollowUserPostViewSet)
router.register('schoolPostList', SchoolPostListViewSet)
router.register('top_image',topImage_Viewset)

urlpatterns = [
    path('', include(router.urls)),
    path('email/', SendEmailView.as_view(), name='send-email'),
    path('', cache_page(60*60*24)(SearchViewSet))
]
