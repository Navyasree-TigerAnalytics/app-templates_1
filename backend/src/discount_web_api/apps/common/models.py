from apps.common.constants import STATUS_MASTER_NAMES
from core.generics.models import TimeStampModel
from django.db import models
from django.utils import timezone


class Market(TimeStampModel):
    market_id = models.AutoField(primary_key=True, unique=True)
    market_name = models.CharField(max_length=200, null=True)
    market_code = models.CharField(max_length=1000, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.market_name.upper()

    class Meta:
        db_table = "market"


class Language(TimeStampModel):
    language_id = models.AutoField(primary_key=True, unique=True)
    language_code = models.CharField(max_length=200, null=True)
    language_description = models.CharField(
        max_length=1000, null=True, blank=True
    )
    currency_symbol = models.CharField(max_length=200, null=True)
    active = models.BooleanField(default=True)
    default_language = models.CharField(max_length=1000, null=True, blank=True)
    region_id = models.ForeignKey(
        Market,
        default=None,
        on_delete=models.CASCADE,
        db_column="region_id",
        related_name="LanguageRegion",
    )

    class Meta:
        db_table = "language"


class PromoTypes(TimeStampModel):
    id = models.AutoField(
        "promo_type_id", primary_key=True, unique=True
    )
    promo_type_name = models.CharField(
        "promo_type_name", max_length=200, null=True
    )
    promo_type_code = models.CharField(
        "promo_type_code", max_length=200, null=True
    )
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "promo_types"

    def __int__(self):
        return self.promo_type_id


class Category(TimeStampModel):
    id = models.AutoField(primary_key=True,unique=True)
    category = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    class Meta:
        db_table = "product_category"



class Item(TimeStampModel):
    item_id = models.AutoField(primary_key=True, unique=True)
    item_code = models.IntegerField()
    item_name = models.CharField(
        max_length=1000, null=True, blank=True
    )
    recommender_flag = models.BooleanField(default=True)
    scenario_planner_flag = models.BooleanField(default=True)
    category_id = models.ForeignKey(
        Category,
        default=1,
        on_delete=models.CASCADE,
        db_column="category_id",
        related_name="Productcategory",
        )
    promo_type_id = models.ForeignKey(
        PromoTypes,
        default=1,
        on_delete=models.CASCADE,
        db_column="promo_type_id",
        related_name="Promotypes",
    )
    n_store = models.IntegerField()
    active = models.BooleanField(default=True)
    class Meta:
        db_table = "item_master"
       