from rest_framework import serializers

from .models import Problems, Submission_results, Case, Judge_group
from django.contrib.auth import get_user_model
from login.models import User
from login.serializers import UserSerializer
from collections import defaultdict

class ProblemsSerializers(serializers.ModelSerializer):
    user_answer_count = serializers.SerializerMethodField()
    accuracy = serializers.SerializerMethodField()

    class Meta:
        model = Problems
        fields = ['id', 'title', 'problem','difficulty','target_time', 'is_public',
                  'user_answer_count', 'accuracy', 'sample_explanation']

    def get_user_answer_count(self, obj):
        return Submission_results.objects.filter(problem_id=obj.id).count()

    def get_accuracy(self, obj):
        problem_id = obj.id
        ac_count = Submission_results.objects.filter(problem_id=problem_id, status="AC").count()
        total_count = Submission_results.objects.filter(problem_id=problem_id).count()
        accuracy = ac_count / total_count * 100 if total_count > 0 else 0.0
        return "{:.1f}".format(accuracy)
    
class ProblemsdiffSerializers(serializers.ModelSerializer):
    class Meta:
        model = Problems
        fields = ['difficulty']

class RecommendUserSerializers(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model = Submission_results
        fields = ['user_id','language']
        
class SubmissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Submission_results
        fields = '__all__'

class GroupListSerializers(serializers.ModelSerializer):
    problems = ProblemsSerializers(many=True)
   
    admins=UserSerializer(many=True)
    member_rank = serializers.SerializerMethodField()
    class Meta:
        model = Judge_group
        fields = ['id','name','member','problems','admins','introduction','member_rank','starttime','endtime']
        
    def get_member_rank(self, obj):
        problems_list = obj.problems.all()
        problems_id = [problem.id for problem in problems_list]
        user_list = obj.member.all()
        user_id = [member.id for member in user_list]
        rank = Submission_results.objects.filter(problem_id__in=problems_id,user_id__in=user_id).values('user_id', 'score')
        user_scores = defaultdict(int)
        for entry in rank:
            user_id = entry["user_id"]
            score = entry["score"]
            user_scores[user_id] += score
        
        sorted_data = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        rank = 1
        prev_total_score = None
        equal_flag=0
        flag=False
        for user_id, total_score in sorted_data[:10]:
            user = User.objects.get(id=user_id)
            if prev_total_score is not None and total_score == prev_total_score:
                equal_flag+=1
                rank -= equal_flag
                flag=True
            else:
                equal_flag=0
            result.append({
                "user_id": user_id,
                "user_name": user.username,
                "icon": user.icon,
                "total_score": total_score,
                "rank": rank
            })
            prev_total_score = total_score
            if flag==True:
                rank+=equal_flag
                flag=False
            rank += 1
        return result

class GroupSerializers(serializers.ModelSerializer):
    member_rank = serializers.SerializerMethodField()
    class Meta:
        model = Judge_group 
        fields = ['id', 'name', 'admins', 'problems', 'member', 'introduction', 'starttime','endtime', 'is_public', 'finish', 'member_rank']

    def get_member_rank(self, obj):
        problems_list = obj.problems.all()
        problems_id = [problem.id for problem in problems_list]
        user_list = obj.member.all()
        user_id = [member.id for member in user_list]
        rank = Submission_results.objects.filter(problem_id__in=problems_id,user_id__in=user_id).values('user_id', 'score')
        user_scores = defaultdict(int)
        for entry in rank:
            user_id = entry["user_id"]
            score = entry["score"]
            user_scores[user_id] += score
        
        sorted_data = sorted(user_scores.items(), key=lambda x: x[1], reverse=True)
        
        result = []
        rank = 1
        prev_total_score = None
        equal_flag=0
        flag=False
        for user_id, total_score in sorted_data[:10]:
            user = User.objects.get(id=user_id)
            if prev_total_score is not None and total_score == prev_total_score:
                equal_flag+=1
                rank -= equal_flag
                flag=True
            else:
                equal_flag=0
            result.append({
                "user_id": user_id,
                "user_name": user.username,
                "icon": user.icon,
                "total_score": total_score,
                "rank": rank
            })
            prev_total_score = total_score
            if flag==True:
                rank+=equal_flag
                flag=False
            rank += 1
            
        #result = [{"user_id": user_id, "user_name":User.objects.get(id=user_id).username, "icon":User.objects.get(id=user_id).icon, "total_score": total_score} for user_id, total_score in sorted_data[:10]]
        return result
    
class GroupJoinSerializers(serializers.ModelSerializer):
    class Meta:
        model = Judge_group 
        fields = ['member']

    def update(self, instance, validated_data):
        users_id = validated_data
        print('user_id = ', users_id['member'])
        for user_id in users_id['member']:
            print('iiii', user_id)
            if  user_id not in instance.member.all():
                instance.member.add(user_id)
                print('iiii', user_id)
        return instance

class CaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'

class SubresultSerializers(serializers.ModelSerializer):

    class Meta:
        model = Submission_results
        fields = ['id', 'language', 'code']