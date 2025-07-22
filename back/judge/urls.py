from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (SubmissionViewSet, ProblemViewSet, GroupListViewSet, CaseViewSet,GroupViewSet,
                    ProblemSearchViewSet, RecommendUserViewSet, ProblemDifflistViewSet, Sample_SubmissionViewSet, GroupJoinViewSet)

router = DefaultRouter()
router.register('post', SubmissionViewSet)
router.register('list', ProblemViewSet)
router.register('grouplist', GroupListViewSet)
router.register('group', GroupViewSet)
router.register('case', CaseViewSet)
router.register('search', ProblemSearchViewSet)
router.register('recommend', RecommendUserViewSet)
router.register('diff', ProblemDifflistViewSet)
router.register('sample_test', Sample_SubmissionViewSet)
router.register('group_join', GroupJoinViewSet)


urlpatterns = [
    path('', include(router.urls)),
]