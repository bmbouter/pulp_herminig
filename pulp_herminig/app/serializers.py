from gettext import gettext as _
from rest_framework.serializers import Serializer, IntegerField, BooleanField

from pulpcore.plugin.serializers import RelatedField


class TaskingBenchmarkSerializer(Serializer):
    background = BooleanField(default=False)
    count = IntegerField(default=4)


class TaskingBenchmarkResultSerializer(Serializer):
    count = IntegerField(read_only=True)
    dispatch_time = IntegerField(read_only=True)
    prior_tasks = IntegerField(read_only=True)
    task_group = RelatedField(
        help_text=_("The task group that contains the dispatched tasks."),
        read_only=True,
        view_name="task-groups-detail",
    )
