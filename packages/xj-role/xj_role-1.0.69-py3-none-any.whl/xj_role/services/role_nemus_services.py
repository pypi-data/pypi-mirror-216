# encoding: utf-8
"""
@project: djangoModel->role_nemus_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 菜单服务
@created_time: 2023/6/20 9:33
"""
from django.core.paginator import Paginator, EmptyPage
from django.db.models import F

from ..models import RoleMenu, RolePermission
from ..utils.custom_tool import format_params_handle, force_transform_type, filter_fields_handler
from ..utils.j_recur import JRecur


class RoleMenuServices:
    menu_fields = [i.name for i in RoleMenu._meta.fields]

    @staticmethod
    def get_menu(params: dict = None, only_first: int = None, pagination=True, get_tree=False, filter_fields: "str|list" = None, **kwargs):
        """
        查询菜单
        :param params: 查询参数
        :param only_first: 是否仅仅查询第一条
        :param pagination: 是否需要分页
        :param get_tree: 查询树结构数据
        :param filter_fields: 过滤的字段
        :param kwargs: 最缺省值
        :return: data,err
        """
        # 类型校验
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)
        page, err = force_transform_type(variable=params.pop("page", 1), var_type="int", default=1)
        size, err = force_transform_type(variable=params.pop("size", 10), var_type="int", default=10)
        pagination, err = force_transform_type(variable=pagination, var_type="bool", default=True)
        only_first, err = force_transform_type(variable=only_first, var_type="bool", default=False)
        get_tree, err = force_transform_type(variable=get_tree, var_type="bool", default=False)

        # 排序字段
        sort = params.get("sort", "-id")
        sort = sort if sort in ["menu_id", "-menu_id", "sort", "-sort"] else "-menu_id"
        # 查询字段
        all_fields = ["menu_id", "category_id", "parent_id", "name", "route", "icon", "link", "level", "config", "sort", "is_using", "menu_description"]
        filter_fields = filter_fields_handler(
            input_field_expression=filter_fields,
            default_field_list=all_fields,
            all_field_list=all_fields
        )
        # 查询字典
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id|int", "role_id|int", "category_id|int", "parent_id|int", "name", "route", "icon", "link", "level",
                "config|dict", "is_using|int", "role_id_list|list_int"
            ],
            alias_dict={"route": "route__contains", "name": "name__contains", "role_id_list": "role_id__in"}
        )
        # 构建ORM
        if not (params.get("role_id") or params.get("role_id__in")):
            query_set = RoleMenu.objects.annotate(
                menu_id=F("id"),
                menu_description=F("description")
            ).filter(**params).order_by(sort)
        else:
            query_set = RolePermission.objects.annotate(
                category_id=F("menu__category_id"),
                parent_id=F("menu__parent_id"),
                name=F("menu__name"),
                route=F("menu__route"),
                icon=F("menu__icon"),
                link=F("menu__link"),
                level=F("menu__level"),
                config=F("menu__config"),
                is_using=F("menu__is_using"),
                sort=F("menu__sort"),
                menu_description=F("menu__description"),
            ).filter(**params).order_by(sort)
            filter_fields += ["role_id"]

        # 查询字段
        query_set = query_set.values(*filter_fields)

        # 查询树形数据
        if get_tree:
            query_set = list(query_set.all())
            menu_tree = JRecur.create_forest(
                query_set,
                primary_key="id",
                parent_key="parent_id",
                children_key="children"
            )
            return menu_tree, None

        # 单条详情查询
        if only_first:
            return query_set.first(), None

        # 不分页查询
        count = query_set.count()
        if not pagination and count <= 500:
            return list(query_set), None

        # 分页查询
        paginator = Paginator(query_set, size)

        try:
            finish_set = list(paginator.page(page).object_list)
        except EmptyPage:
            return {"count": count, "page": int(page), "size": int(size), "list": []}, None
        return {"count": count, "page": int(page), "size": int(size), "list": finish_set}, None

    @staticmethod
    def del_menu(pk: int = None, search_params: dict = None, **kwargs):
        """删除系统API"""
        pk, err = force_transform_type(variable=pk, var_type="int")
        search_params, err = force_transform_type(variable=search_params, var_type="only_dict")
        # 构建ORM
        if pk:
            menu_obj = RoleMenu.objects.filter(pk=pk)
        elif search_params:
            menu_obj = RoleMenu.objects.filter(**search_params)
        else:
            return None, None
        # 删除
        total = menu_obj.count()
        if total < 1:
            return None, "没有可修改的数据"
        menu_obj.delete()

        return None, None

    @staticmethod
    def add_menu(params: dict = None, **kwargs):
        """
        新增系统菜单
        :param params: 添加参数
        :param kwargs: 最缺省值
        :return: data,err
        """
        # ------------------------- section 参数处理 start--------------------------------
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        try:
            params = format_params_handle(
                param_dict=params,
                is_validate_type=True,
                is_remove_empty=True,
                filter_filed_list=[
                    "category_id|int", "parent_id|int", "name|str", "route|str", "icon|str", "link|str", "level|int", "config|dict", "description", "is_using|int"
                ]
            )
        except ValueError as e:
            return None, str(e)

        # 参数校验
        for key in ["name", "route"]:
            if params.get(key):
                continue
            return None, key + "必须填写"

        # 层级处理，校验父级节点
        if params.get("level") == 1:
            params["parent_id"] = 0

        elif not params.get("level") == 1 and not params.get("parent_id"):
            return None, "请选择父节点"

        elif not params.get("level") == 1 and params.get("parent_id"):
            parent_menu = RoleMenu.objects.filter(id=params.get("parent_id")).values("id", "level").first()
            if not parent_menu:
                return None, "该父节点不存在"
            if not parent_menu.get("level") == params.get("level") - 1:
                return None, "父级菜单层级不正确"

        params.setdefault("is_using", 1)
        # ------------------------- section 参数处理 start--------------------------------

        # ------------------------- section 构建ORM start--------------------------------
        # 重复校验
        if RoleMenu.objects.filter(route=params["route"]).first():
            return None, "该路由已经创建，请勿重复创建"

        # 创建数据
        try:
            RoleMenu.objects.create(**params)
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", "  ") + ";tip:新增异常，请稍后再试"
        # ------------------------- section 构建ORM end  --------------------------------

        return None, None

    @staticmethod
    def edit_menu(pk: int, params: dict = None, **kwargs):
        """编辑系统API"""
        pk, err = force_transform_type(variable=pk, var_type="int")
        params, err = force_transform_type(variable=params, var_type="only_dict", default={})
        kwargs, err = force_transform_type(variable=kwargs, var_type="only_dict", default={})
        params.update(kwargs)

        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "category_id|int", "parent_id|int", "name|str", "route|str", "icon|str", "link|str", "level|int", "config|dict", "description", "is_using|int"
            ]
        )

        # 重复校验
        if not RoleMenu.objects.filter(id=pk).first():
            return None, "msg:数据不存在,无法修改;tip:数据不存在,无法修改"

        # 创建数据
        try:
            RoleMenu.objects.filter(id=pk).update(**params)
        except Exception as e:
            return None, "msg:" + str(e).replace(":", " ").replace(";", "  ") + ";tip:新增异常，请稍后再试"

        return None, None
