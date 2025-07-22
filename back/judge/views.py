from rest_framework.response import Response
from threading import Timer
from judge.models import *
from django.contrib.auth import authenticate, login as django_login
from . import views
from django.contrib.auth import logout
from pathlib import Path
from .serializers import (ProblemsSerializers, SubmissionSerializers, SubresultSerializers, GroupSerializers,
                          CaseSerializers, GroupListSerializers, RecommendUserSerializers, ProblemsdiffSerializers,GroupJoinSerializers)
from rest_framework.permissions import IsAuthenticated, AllowAny
import docker
from rest_framework import viewsets, filters,status
from docker.errors import ContainerError
import tarfile
from typing import Dict
import time
from math import floor
import multiprocessing
from django.db.models import Max
from django.db.models import Count
from os import remove
from collections import Counter
from django.db.models import Q
import hashlib
from django.utils import timezone
from datetime import datetime

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problems.objects.filter(is_public=True)
    serializer_class = ProblemsSerializers
    permission_classes =(AllowAny,)
    
    
 
class RecommendUserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Submission_results.objects.all()
    serializer_class = RecommendUserSerializers
    permission_classes =(IsAuthenticated,)
    
    def get_queryset(self):
        user_id = self.request.user.id 
        language_counts = Submission_results.objects.filter(user_id=user_id,status="AC").values('language').annotate(count=Count('language')).order_by('-count')
        if language_counts:
            converted_data = {entry["language"]: entry["count"] for entry in language_counts}
            language=sorted(converted_data.items(), key=lambda x: x[1], reverse=True)[0][0] if converted_data else None
        else:
            language=""
        time = timezone.now() - timezone.timedelta(days=90)
        if language:
            subquery = Submission_results.objects.filter(created_at__gte=time,language=language).values('user_id').annotate(max_id=Max('id')).values('max_id')
        else:
            subquery = Submission_results.objects.filter(created_at__gte=time).values('user_id').annotate(max_id=Max('id')).values('max_id')
        
        exclude_id=User.objects.filter(id=user_id).values('follows')
        exclude_id = [item['follows'] for item in exclude_id if item['follows'] is not None]
        exclude_id.append(user_id)
        
        queryset = Submission_results.objects.exclude(user_id__in=exclude_id).filter(id__in=subquery).order_by('?')[:5]
        
        return queryset


class ProblemSearchViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problems.objects.filter(is_public=True,group_only=False)
    serializer_class = ProblemsSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )

    def get_queryset(self):
        queryset = Problems.objects.filter(is_public=True,group_only=False)
        diff = self.request.GET.get('diff')
        if diff:
            queryset = queryset.filter(Q(difficulty__icontains=diff)).distinct()
        return queryset
    
class ProblemDifflistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Problems.objects.filter(is_public=True,group_only=False)
    serializer_class = ProblemsdiffSerializers
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        data = [user for user in serializer.data]
        
        difficulty_count = Counter(item["difficulty"] for item in data)
        data = [difficulty_count.get(difficulty, 0) for difficulty in range(1, 6)]
        return Response({'diff': data})

    
class CaseViewSet(viewsets.ModelViewSet):
    queryset = Case.objects.all()
    serializer_class = CaseSerializers
    permission_classes =(AllowAny,)

class GroupListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Judge_group.objects.filter(is_public=True)
    serializer_class = GroupListSerializers
    permission_classes =(AllowAny,)
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Judge_group.objects.filter(is_public=True) 
    serializer_class = GroupSerializers
    permission_classes =(AllowAny,)
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        original_datetime = datetime.strptime(data[0]['endtime'], "%Y-%m-%dT%H:%M:%S%z")
        new_date_string = original_datetime.strftime("%Y-%m-%d %H:%M")
        data[0]['endtime'] = new_date_string
        return Response(data)
    
class GroupJoinViewSet(viewsets.ModelViewSet):
    queryset = Judge_group.objects.filter(is_public=True) 
    serializer_class = GroupJoinSerializers
    permission_classes =(AllowAny,)

   
def judge(language, code,cases,user_id):
    try:
        EXECUTION_LANGUAGE: Dict[str, str] = {"Java": f"/Main{user_id}.java", "Python3": f"/main{user_id}.py", "Cpp": f"/Main{user_id}.cpp", "C": f"/Main{user_id}.c",
                                    "Ruby": f"/main{user_id}.rb", "Go": f"/main{user_id}.go", "Php": f"/main{user_id}.php", "Javascript": f"/main{user_id}.js",
                                    "R": f"/main{user_id}.r", "Perl": f"/main{user_id}.pl", "Typescript": f"/main{user_id}.ts", "Crystal": f"/main{user_id}.cr",
                                    "Dart": f"/main{user_id}.dart", "Swift": f"/Main{user_id}.swift"}
        if language in EXECUTION_LANGUAGE:
            with open(f"judge/{language}{EXECUTION_LANGUAGE[language]}", "w") as text_file:
                text_file.write(code)
            judge_status=[]
            match language:
                case "Java":
                    client = docker.from_env()
                    name: str = f"java-judge{user_id}"
                    container_config = {
                        'image': "java-judge",
                        'name': name,
                        'stdin_open': True,
                        'tty': True,
                        }
                    if not client.images.list("java-judge"):
                        client.images.build(path='judge/Java', tag="java-judge")
                    container = client.containers.create(**container_config)
                    container.start()
                    
                    with tarfile.open(f'/usr/src/judge/Java/Java_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Java/Main{user_id}.java', arcname='Main.java')
                    with open(f"/usr/src/judge/Java/Java_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = f"javac /app/Main.java"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case
                        answer_case = case.answer
                        exec_command_java = ["sh", "-c", f'echo "{input_case}" | java -cp /app Main']
                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_java, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                                                
                        judge_status.append(que.get())
                    
                    container.stop()
                    container.remove()

                case "Python3":
                    client = docker.from_env()
                    name: str = "python-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'command': "/bin/bash",
                        'volumes': {
                            #'/var/run/docker.sock': {'bind': '/var/run/docker.sock', 'mode': 'rw'},
                        },
                        'stdin_open': True,
                        'tty': True,
                        'detach':True, 
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Python3', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                    
                    with tarfile.open(f'/usr/src/judge/Python3/Python3_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Python3/main{user_id}.py', arcname='main.py')
                    with open(f"/usr/src/judge/Python3/Python3_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          

                        exec_command = ["sh", "-c", f'echo "{input_case}" | python /app/main.py']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command, stdout=True, stderr=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck, args=(que, ))
                        process2 = multiprocessing.Process(target=run, args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                case 'C':
                    client = docker.from_env()
                    name: str = "c-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/C', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                        
                    with tarfile.open(f'/usr/src/judge/C/C_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/C/Main{user_id}.c', arcname='Main.c')
                    with open(f"/usr/src/judge/C/C_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = f"gcc -o myapp Main.c"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_c = ["sh", "-c", f'echo "{input_case}" | ./myapp']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_c, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()

                case 'Cpp':
                    client = docker.from_env()
                    name: str = "cpp-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Cpp', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                            
                    with tarfile.open(f'/usr/src/judge/Cpp/Cpp_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Cpp/Main{user_id}.cpp', arcname='Main.cpp')
                    with open(f"/usr/src/judge/Cpp/Cpp_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = "g++ -o myapp Main.cpp"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_cpp = ["sh", "-c", f'echo "{input_case}" | ./myapp']  
                        
                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_cpp, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()
                    
                case 'Ruby':
                    client = docker.from_env()
                    name: str = "ruby-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Ruby', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/Ruby/Ruby_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Ruby/main{user_id}.rb', arcname=f'main.rb')
                    with open(f"/usr/src/judge/Ruby/Ruby_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | ruby /app/main.rb']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                        
                case 'Go':
                    client = docker.from_env()
                    name: str = "go-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Go', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                    with tarfile.open(f'/usr/src/judge/Go/Go_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Go/main{user_id}.go', arcname='main.go')
                    with open(f"/usr/src/judge/Go/Go_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    exec_command = "go build -o main main.go"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_go = ["sh", "-c", f'echo "{input_case}" | /app/main']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_go, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()
                        
                case 'Javascript':
                    client = docker.from_env()
                    name: str = "javascript-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Javascript', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/Javascript/Javascript_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Javascript/main{user_id}.js', arcname=f'main.js')
                    with open(f"/usr/src/judge/Javascript/Javascript_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | node /app/main.js']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                    
                case 'Php':
                    client = docker.from_env()
                    name: str = "php-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Php', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/Php/Php_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Php/main{user_id}.php', arcname=f'main.php')
                    with open(f"/usr/src/judge/Php/Php_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | php /app/main.php']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'R':
                    client = docker.from_env()
                    name: str = "r-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/R', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/R/R_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/R/main{user_id}.r', arcname=f'main.r')
                    with open(f"/usr/src/judge/R/R_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | r /app/main.r']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'Perl':
                    client = docker.from_env()
                    name: str = "perl-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Perl', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/Perl/Perl_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Perl/main{user_id}.pl', arcname=f'main.pl')
                    with open(f"/usr/src/judge/Perl/Perl_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | perl /app/main.pl']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'Typescript':
                    client = docker.from_env()
                    name: str = "typescript-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Typescript', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()

                    with tarfile.open(f'/usr/src/judge/Typescript/Typescript_main_{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Typescript/main{user_id}.ts', arcname=f'main.ts')
                    with open(f"/usr/src/judge/Typescript/Typescript_main_{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)
                    for case in cases:
                        que = multiprocessing.Queue()
                        print("forの中", judge_status)
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')    
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')          
                        exec_command_ruby = ["sh", "-c", f'echo "{input_case}" | node /app/main.ts']

                        def timecheck():
                            try:
                                start_time = time.perf_counter()
                                end_time = 0
                                while (end_time - start_time) < 2.0000:
                                    end_time = time.perf_counter()
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")

                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_ruby, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                # print("EEEXXX", exec_response)
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                if answer_case == result:
                                    print("result:",repr(result))
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("result:",repr(result))
                                    print("NG")
                                    judge_status.append("NG")
                                    que.put("NG")
                                que.put("TLE")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")

                        process1 = multiprocessing.Process(target=timecheck)
                        process2 = multiprocessing.Process(target=run,  args=(que, ))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        if que.qsize() == 0:
                            print("きっとTLEだ")
                            judge_status.append('TLE')
                        else:
                            judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'Crystal':
                    client = docker.from_env()
                    name: str = "crystal-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Crystal', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                        
                    with tarfile.open(f'/usr/src/judge/Crystal/Crystal_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Crystal/main{user_id}.cr', arcname='Main.cr')
                    with open(f"/usr/src/judge/Crystal/Crystal_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = f"crystal run -o myapp Main.cr"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_c = ["sh", "-c", f'echo "{input_case}" | ./myapp']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_c, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'Dart':
                    client = docker.from_env()
                    name: str = "dart-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Dart', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                        
                    with tarfile.open(f'/usr/src/judge/Dart/Dart_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Dart/main{user_id}.dart', arcname='main.dart')
                    with open(f"/usr/src/judge/Dart/Dart_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = f"dart compile exe -o myapp main.dart"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_c = ["sh", "-c", f'echo "{input_case}" | ./myapp']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_c, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()
                
                case 'Swift':
                    client = docker.from_env()
                    name: str = "swift-judge"
                    container_config = {
                        'image': name,
                        'name': name + str(user_id),
                        'stdin_open': True,
                        'tty': True,
                    }
                    if not client.images.list(name):
                        client.images.build(path='judge/Swift', tag=name)
                    container = client.containers.create(**container_config)
                    container.start()
                        
                    with tarfile.open(f'/usr/src/judge/Swift/Swift_main{user_id}.tar', 'w') as tar:
                        tar.add(f'/usr/src/judge/Swift/Main{user_id}.swift', arcname='Main.swift')
                    with open(f"/usr/src/judge/Swift/Swift_main{user_id}.tar", "rb") as archive_file:
                        data = archive_file.read()
                    container.put_archive("/app",data)          
                    exec_command = f"swiftc -o myapp Main.swift"
                    container.exec_run(exec_command, stdout=True, stderr=True, stdin=True)
                    for case in cases:
                        print("case:",repr(case.case))
                        input_case = case.case.replace('\r\n', '\n')
                        answer_case = case.answer.replace('\r\n', '\n')
                        input_case = input_case.rstrip('\n')
                        answer_case = answer_case.rstrip('\n')
                        exec_command_c = ["sh", "-c", f'echo "{input_case}" | ./myapp']

                        def timecheck(que):
                            try:
                                start_time = time.perf_counter()
                                while (time.perf_counter() - start_time) < 2.0:
                                    pass
                                print("タイムアウト")
                                que.put("TLE")
                            except Exception as e:
                                print(f"時間計測時のエラー: {e}")
                                que.put("ERR")
                        def run(que):
                            try:
                                exec_response = container.exec_run(exec_command_c, stdout=True, stderr=True, stdin=True)
                                print("実行中")
                                result = exec_response.output.decode('utf-8')
                                print("answer",repr(answer_case))
                                result = result.rstrip('\n')
                                print("result:",repr(result))
                                if answer_case == result:
                                    print("AC")
                                    judge_status.append("AC")
                                    que.put("AC")
                                else:
                                    
                                    print("NG")
                                    que.put("NG")
                            except Exception as e:
                                print(f"実行時のエラー: {e}")
                                que.put("ERR")
                                
                        que = multiprocessing.Queue()
                        process1 = multiprocessing.Process(target=timecheck, args=(que,))
                        process2 = multiprocessing.Process(target=run,  args=(que,))

                        process1.start()
                        process2.start()
                        
                        print("処理開始")
                        process1.join()
                        
                        print("計測終わり")
                        process2.terminate()
                        process2.join()
                        print("実行終わり")
                        
                        
                        judge_status.append(que.get())
                    container.stop()
                    container.remove()

            file_path = f"judge/{language}{EXECUTION_LANGUAGE[language]}"
            file_path1 = f"judge/{language}/{language}_main{user_id}.tar"
            try:
                remove(file_path)
                remove(file_path1)
                print(f"File {file_path} deleted successfully.")
            except FileNotFoundError:
                print(f"File {file_path} not found.")
            except Exception as e:
                print(f"An error occurred: {e}")
            return judge_status
        else:
            return None
        return None
    except Exception as e:
            container.stop()
            container.remove()
            print(f"An error occurred: {e}")
from django.http import QueryDict

# テストケース実行
class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission_results.objects.all()
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    serializer_class = SubmissionSerializers
    def extract_id(obj):
        if hasattr(obj, 'id'):
            return obj.id
        return str(obj) 

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        try:
            if data['group_id']=="1":
                data['group_id'] = "11111111-1111-1111-1111-111111111111"
            if data['group_id']=="2":
                data['group_id'] = "22222222-2222-2222-2222-222222222222"
            times=Judge_group.objects.filter(id = data['group_id']).values('starttime','endtime')
            start_time=times[0]['starttime']
            end_time=times[0]['endtime']
            
            if start_time is not None:
                current_time = timezone.now()

                if current_time < start_time:
                    return Response({"error": "開始時間外です。"}, status=status.HTTP_400_BAD_REQUEST)
            if end_time is not None:
                current_time = timezone.now()

                if current_time > end_time:
                    return Response({"error": "回答可能時間外です。"}, status=status.HTTP_400_BAD_REQUEST)
            
            
            if Submission_results.objects.filter(group_id = data['group_id'],user_id = data['user_id'], problem_id = data['problem_id']).exists():
                
                return Response({"error": "コード提出済みです。"}, status=status.HTTP_400_BAD_REQUEST)
            else:

                cases = Case.objects.filter(problem_id=data['problem_id'])
                score_number = judge(data['language'], data['code'], cases,data['user_id'])
                if score_number.count("AC") == cases.count():
                    data['status'] = "AC"
                else:
                    data['status'] = "NG"

                diff = Problems.objects.get(id=data['problem_id']).difficulty
                try:
                    data['score'] = floor(diff * 10 / len(cases) * score_number.count("AC"))      #judge_statusがnullの時エラーが出るので。  
                except:
                    pass
                
                serializer = self.get_serializer(data=data)
                serializer.is_valid(raise_exception=True)
                
                # チュートリアル問題の場合、保存せず返却。
                if data['group_id'] == "22222222-2222-2222-2222-222222222222":
                    ordered_dict =serializer.validated_data
                    def extract_id(obj):
                        if hasattr(obj, 'id'):
                            return obj.id
                        return str(obj)                 
                    tutorial_data = {
                        'language': ordered_dict['language'],
                        'code': ordered_dict['code'],
                        'status': ordered_dict['status'],
                        'score': ordered_dict['score'],
                        'user_id': extract_id(ordered_dict['user_id']),
                        'problem_id': extract_id(ordered_dict['problem_id']),
                        'group_id': extract_id(ordered_dict['group_id']),
                    }
                    tutorial_data['judge_status']=score_number
                    return Response(tutorial_data, status=status.HTTP_201_CREATED)  
                serializer.save()
                
                response_data =serializer.data
                response_data['judge_status']=score_number    
                print(response_data)          
                return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"An error occurred: {e}")
            
            
# サンプルケース実行
class Sample_SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission_results.objects.all()
    permission_classes =(AllowAny,)#(IsAuthenticated, )
    serializer_class = SubmissionSerializers

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        try:
            print(data)
            if data['group_id']=="1":
                data['group_id'] = "11111111-1111-1111-1111-111111111111"
            if data['group_id']=="2":
                data['group_id'] = "22222222-2222-2222-2222-222222222222"
            cases = Sample_case.objects.filter(problem_id=data['problem_id'])
            sample_results = judge(data['language'], data['code'], cases,data['user_id'])
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            response_data = serializer.data
            response_data['sample_status'] = sample_results
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"An error occurred: {e}")