from dataclasses import fields

from apps.common.constants import STATUS_MASTER_NAMES
from apps.common.models import Category, Item, Language, PromoTypes
from rest_framework import serializers


class LanguageSerializers(serializers.ModelSerializer):
    language_id = serializers.IntegerField()
    language_code = serializers.CharField(max_length=200)
    language_description = serializers.CharField(max_length=1000)
    currency_symbol = serializers.CharField(max_length=200)
    default_language = serializers.CharField(max_length=1000)

    class Meta:
        model = Language
        fields = "__all__"


class PromoTypesSerializers(serializers.ModelSerializer):
    promo_type_id = serializers.IntegerField()
    promo_type_name = serializers.CharField(max_length=200)
    promo_type_code = serializers.CharField(max_length=200)
    active = serializers.BooleanField()

    class Meta:
        model = PromoTypes
        fields = "__all__"

class ItemSerializers(serializers.ModelSerializer):
    item_id = serializers.IntegerField()
    item_code = serializers.IntegerField()
    item_name = serializers.CharField(max_length=1000)
    recommender_flag = serializers.BooleanField(default=True)
    scenario_planner_flag = serializers.BooleanField()
    # promo_type_id = PromoTypesSerializers(read_only = True)
    category_id = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all())
    promo_type_id = serializers.PrimaryKeyRelatedField(queryset = PromoTypes.objects.all())
    # promo_type_code = serializers.CharField(max_length=10)
    n_store = serializers.IntegerField()
    active = serializers.BooleanField(default=True)

    class Meta:
        model = Item
        fields = "__all__"
