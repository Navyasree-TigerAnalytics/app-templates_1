from apps.common.views import (ItemDetail, ItemList, LanguageDetail,
                               LanguageList)
from django.urls import path

urlpatterns = [
    path("languages", LanguageList.as_view()),
    path(
        "languages/<int:language_id>/",
        LanguageDetail.as_view(),
    ),
    # path("status", StatusList.as_view()),
    # path("promoTypes", PromoTypesList.as_view()),
    # path("promoChannel", PromoChannelList.as_view()),
    # path("geos", OfferHierMasterList.as_view()),
    # path("fixedPromos", FixedPromos.as_view()),
    # path("competitionPromos", CompetitionPromosList.as_view()),
    path("items", ItemList.as_view()),
    path(
        "items/<int:item_id>/",
        ItemDetail.as_view(),
    )
]
