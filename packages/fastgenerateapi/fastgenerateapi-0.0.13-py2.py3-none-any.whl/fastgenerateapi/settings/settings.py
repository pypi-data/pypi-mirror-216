from typing import Optional

from pydantic import BaseSettings, Field, BaseModel


class AppSettings(BaseSettings):
    # 分页对应字段以及配置默认值
    CURRENT_PAGE_FIELD: Optional[str] = Field(default='page', description="当前页字段")
    PAGE_SIZE_FIELD: Optional[str] = Field(default='page_size', description="每页数量字段")
    TOTAL_SIZE_FIELD: Optional[str] = Field(default='total', description="统计数量字段")
    DETERMINE_WHETHER_PAGE_FIELD: Optional[str] = Field(default='no_page', description="判断是否分页字段")
    DETERMINE_PAGE_BOOL_VALUE: Optional[bool] = Field(default=True, description="分页对应的布尔值")
    DEFAULT_WHETHER_PAGE: Optional[bool] = Field(default=False, description="默认是否分页")
    DEFAULT_PAGE_SIZE: Optional[int] = Field(default=10, description="默认每页数量")
    DEFAULT_MAX_PAGE_SIZE: Optional[int] = Field(default=200, description="默认最大每页数量")

    # 路由后缀字段是否添加以及配置默认值
    ROUTER_WHETHER_ADD_SUFFIX: Optional[bool] = Field(default=True, description="增删改查路由是否添加后缀")
    ROUTER_CREATE_SUFFIX_FIELD: Optional[str] = Field(default='create', description="创建路由后缀字段")
    ROUTER_GET_ONE_SUFFIX_FIELD: Optional[str] = Field(default='get-one', description="获取一个路由后缀字段")
    ROUTER_GET_ALL_SUFFIX_FIELD: Optional[str] = Field(default='get-all', description="获取列表路由后缀字段")
    ROUTER_GET_TREE_SUFFIX_FIELD: Optional[str] = Field(default='get-tree', description="获取树状数据路由后缀字段")
    ROUTER_UPDATE_SUFFIX_FIELD: Optional[str] = Field(default='update', description="修改路由后缀字段")
    ROUTER_DELETE_SUFFIX_FIELD: Optional[str] = Field(default='delete', description="删除路由后缀字段")
    ROUTER_RECURSION_DELETE_SUFFIX_FIELD: Optional[str] = Field(default='delete-tree', description="递归删除路由后缀字段")

    # 数据库字段默认值
    WHETHER_DELETE_FIELD: Optional[str] = Field(default="is_active", description="是否删除字段")
    ACTIVE_DEFAULT_VALUE: Optional[bool] = Field(default=True, description="有效的默认值")
    GET_EXCLUDE_ACTIVE_VALUE: Optional[bool] = Field(default=True, description="查询结果是否排除有效字段")
    CREATE_EXCLUDE_ACTIVE_VALUE: Optional[bool] = Field(default=True, description="创建是否排除有效字段")
    UPDATE_EXCLUDE_ACTIVE_VALUE: Optional[bool] = Field(default=True, description="修改是否排除有效字段")
    DEFAULT_TREE_PARENT_FIELD: Optional[str] = Field(default="parent", description="默认递归父级字段")
    DEFAULT_TREE_CHILDREN_FIELD: Optional[str] = Field(default="children", description="默认递归子级字段")
    DEFAULT_TREE_FILTER_FIELD: Optional[str] = Field(default="node_id", description="默认递归筛选开始节点字段")

    # 返回格式字段配置默认值
    CODE_RESPONSE_FIELD: Optional[bool] = Field(default=True, description="code返回字段")
    SUCCESS_RESPONSE_FIELD: Optional[bool] = Field(default=True, description="success返回字段")
    MESSAGE_RESPONSE_FIELD: Optional[str] = Field(default="message", description="消息返回字段")
    DATA_RESPONSE_FIELD: Optional[str] = Field(default="data", description="数据返回字段")
    LIST_RESPONSE_FIELD: Optional[str] = Field(default='list', description="列表页返回字段")

    # GetAll 筛选是否双下划线转单下划线
    FILTER_UNDERLINE_WHETHER_DOUBLE_TO_SINGLE: Optional[bool] = Field(default=True, description="筛选是否双下划线转单下划线")
    SCHEMAS_UNDERLINE_WHETHER_DOUBLE_TO_SINGLE: Optional[bool] = Field(default=True, description="序列化字段是否双下划线转单下划线")

    class Config:
        env_prefix = 'APP_'
        env_file = "./.env"
        case_sensitive = True


class SettingsModel(BaseModel):
    # 系统配置
    app_settings: AppSettings = AppSettings()









