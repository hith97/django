from rest_framework import serializers

class DashboardOverviewSerializer(serializers.Serializer):
    user = serializers.EmailField()
    total_items = serializers.IntegerField()
    recent_activities = serializers.ListField(child=serializers.DictField())

class DashboardStatsSerializer(serializers.Serializer):
    stats = serializers.DictField(
        child=serializers.DictField()
    ) 