import json
from contextlib import nullcontext
from datetime import datetime
from os import stat
from turtle import pos

import pandas as pd
import structlog
from apps.common.models import Category, Item, PromoTypes
from apps.common.serializers import (ItemSerializers, LanguageSerializers,
                                     PromoTypesSerializers)
from apps.common.services import (add_languages, delete_items,
                                  delete_languages, get_Items, get_languages,
                                  post_Items, update_items, update_languages)
from apps.common.unit_of_work import (ItemsUnitOfWork, LanguagesUnitOfWork,
                                      PromoTypesUnitOfWork)
from core.generics.exceptions import MissingRequestParamsError
from core.generics.resp_utils import handle_response
from django.db import transaction
from django.shortcuts import render
from drf_spectacular.utils import (OpenApiExample, OpenApiParameter,
                                   extend_schema)
from rest_framework import generics
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated

logger = structlog.get_logger(__name__)


class LanguageList(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = LanguageSerializers

    @handle_response
    @extend_schema(
        summary="Get the entire list of languages",
        description="API end point that serves the list of languages",
    )
 
    def get(self, request):
        uow = LanguagesUnitOfWork(transaction)
        logger.bind(method_name="get_languages", app_name="Common", params=str([-1]))
        resp = get_languages(uow, -1)
        serializer = LanguageSerializers(resp, many=True)
        return serializer.data

    @handle_response
    @extend_schema(
        summary="Add language to list of languages",
        description="API end point to add data to the list of languages",
    )
    def post(self, request):
        uow = LanguagesUnitOfWork(transaction)
        post_data = request.data
        serializer = LanguageSerializers(data=post_data)
        logger.bind(method_name="post_languages", app_name="Common", params=post_data)
        if serializer.is_valid():
            add_languages(uow, serializer)
            return {"status": "data added  succesfully"}
        else:
            raise (MissingRequestParamsError("status", serializer.data))


class LanguageDetail(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = LanguageSerializers

    @handle_response
    @extend_schema(
        summary="Get the details of a language based on id",
        description="API end point that serves the languages based on language id",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="Filter by language id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by language id",
                        description="should be a integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        if not language_id:
            raise MissingRequestParamsError("language id", language_id)
        uow = LanguagesUnitOfWork(transaction)
        logger.bind(
            method_name="get_languages", app_name="Common", params=str([language_id])
        )
        resp = get_languages(uow, language_id)
        serializer = LanguageSerializers(resp)
        return serializer.data

    @handle_response
    @extend_schema(
        summary="Update a language from list of languages",
        description="API end point that is used to update the list of languages",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="Update0 by language id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Update using language id",
                        description="needs language id in URL and update data params in request data",
                        value=1,
                    )
                ],
            )
        ],
    )
    def put(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        if language_id is None:
            raise MissingRequestParamsError("id", language_id)
        uow = LanguagesUnitOfWork(transaction)
        put_data = request.data
        item = get_languages(uow, language_id)
        serializer = LanguageSerializers(item, data=put_data, partial=True)
        logger.bind(method_name="put_languages", app_name="Common", params=put_data)
        if serializer.is_valid():
            update_languages(uow, language_id, serializer)
            return {"status": "data updated succesfully"}
        else:
            raise MissingRequestParamsError("status", "data")

    @handle_response
    @extend_schema(
        summary="Delete a language",
        description="API end point that is used to delete a language",
        parameters=[
            OpenApiParameter(
                name="language_id",
                description="delete using the language id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="delete using the language id",
                        description="language id is needed to delete a language",
                        value=1,
                    )
                ],
            )
        ],
    )
    def delete(self, request):
        language_id = request.parser_context["kwargs"].get("language_id")
        uow = LanguagesUnitOfWork(transaction)
        logger.bind(
            method_name="delete_languages", app_name="Common", params=str([language_id])
        )
        delete_languages(uow, language_id)
        return {"status": "data deleted succesfully"}

class ItemList(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = ItemSerializers
    queryset = Item.objects.all()

    @handle_response
    @extend_schema(
        summary="Get the entire list of Items",
        description="API end point that serves the list of Items",
    )
    def get(self, request):
 
        uow = ItemsUnitOfWork(transaction)
        logger.bind(method_name="get_Items", app_name="Common", params=str([-1]))
        resp = get_Items(uow, -1)
        serializer = ItemSerializers(resp, many=True)
        return serializer.data

    @handle_response
    @extend_schema(
        summary="Add Item to list of Items",
        description="API end point to add data to the list of Items",
    )
    def post(self, request):
        uow = ItemsUnitOfWork(transaction)
        post_data = request.data
        serializer = ItemSerializers(data=post_data)
        
        logger.bind(method_name="post_Items", app_name="Common", params=post_data)
        if serializer.is_valid():
            post_Items(uow, serializer)
            return {"status": "data added  succesfully"}
        else:
            raise (MissingRequestParamsError("status", serializer.data))

class ItemDetail(APIView):
    permission_classes = []  # [IsAuthenticated]
    serializer_class = ItemSerializers

    @handle_response
    @extend_schema(
        summary="Get the details of a item based on id",
        description="API end point that serves the items based on item id",
        parameters=[
            OpenApiParameter(
                name="item_id",
                description="Filter by item id",
                required=True,
                type=int,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Filter by item id",
                        description="should be a integer value",
                        value=1,
                    )
                ],
            )
        ],
    )
    def get(self, request):
        item_id = request.parser_context["kwargs"].get("item_id")
        if not item_id:
            raise MissingRequestParamsError("item id", item_id)
        uow = ItemsUnitOfWork(transaction)
        logger.bind(
            method_name="get_Items", app_name="Common", params=str([item_id])
        )
        resp = get_Items(uow, item_id)
        serializer = ItemSerializers(resp)
        return serializer.data

    @handle_response
    @extend_schema(
        summary="Update a item from list of items",
        description="API end point that is used to update the list of items",
        parameters=[
            OpenApiParameter(
                name="item_id",
                description="Update0 by item id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="Update using item id",
                        description="needs item id in URL and update data params in request data",
                        value=1,
                    )
                ],
            )
        ],
    )
    def put(self, request):
        item_id = request.parser_context["kwargs"].get("item_id")
        if item_id is None:
            raise MissingRequestParamsError("id", item_id)
        uow = ItemsUnitOfWork(transaction)
        put_data = request.data
        item = get_Items(uow, item_id)
        serializer = ItemSerializers(item, data=put_data, partial=True)
        logger.bind(method_name="update_items", app_name="Common", params=put_data)
        if serializer.is_valid():
            update_items(uow, item_id, serializer)
            return {"status": "data updated succesfully"}
        else:
            raise MissingRequestParamsError("status", "data")

    @handle_response
    @extend_schema(
        summary="Delete a item",
        description="API end point that is used to delete a item",
        parameters=[
            OpenApiParameter(
                name="item_id",
                description="delete using the item id",
                required=True,
                type=str,
                examples=[
                    OpenApiExample(
                        "Example 1",
                        summary="delete using the item id",
                        description="item id is needed to delete a item",
                        value=1,
                    )
                ],
            )
        ],
    )
    def delete(self, request):
        item_id = request.parser_context["kwargs"].get("item_id")
        uow = ItemsUnitOfWork(transaction)
        logger.bind(
            method_name="delete_items", app_name="Common", params=str([item_id])
        )
        delete_items(uow, item_id)
        return {"status": "data deleted succesfully"}
