import random
import time
import uuid

from drf_spectacular.utils import extend_schema
from pulpcore.plugin.constants import TASK_FINAL_STATES
from pulpcore.plugin.models import Task, TaskGroup
from pulpcore.plugin.serializers import AsyncOperationResponseSerializer
from pulpcore.plugin.tasking import dispatch
from pulpcore.plugin.viewsets import OperationPostponedResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers, tasks


class TaskingBenchmarkView(APIView):
    @extend_schema(
        request=serializers.TaskingBenchmarkSerializer,
        description="Trigger an asynchronous task to benchmark the task queueing.",
        responses={
            200: serializers.TaskingBenchmarkResultSerializer,
            202: AsyncOperationResponseSerializer,
        },
    )
    def post(self, request):
        serializer = serializers.TaskingBenchmarkSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        background = serializer.validated_data["background"]
        truncate_tasks = serializer.validated_data["truncate_tasks"]
        count = serializer.validated_data["count"]
        resources = [str(uuid.uuid4()) for i in range(serializer.validated_data["resources_N"])]
        resources_K = serializer.validated_data["resources_K"]
        if background:
            task = dispatch(tasks.benchmark_tasking, ["benchmark_tasking"], kwargs={"count": count})
            return OperationPostponedResponse(task, request)
        else:
            if truncate_tasks:
                Task.objects.filter(state_in=TASK_FINAL_STATES).delete()
            prior_tasks = Task.objects.count()
            task_group = TaskGroup(description="Tasking system benchmark tasks")
            task_group.save()
            before = time.perf_counter_ns()
            for i in range(count):
                dispatch(tasks.noop, random.choices(resources, k=resources_K), task_group=task_group)
            after = time.perf_counter_ns()
            task_group.finish()

            benchmark_result = models.TaskingBenchmarkResult(
                count, after - before, prior_tasks, task_group
            )
            response_serializer = serializers.TaskingBenchmarkResultSerializer(
                benchmark_result, context={"request": request}
            )
            return Response(data=response_serializer.data, status=200)
