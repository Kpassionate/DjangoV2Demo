from django.apps import AppConfig
from suit.apps import DjangoSuitConfig
from suit.menu import ParentItem, ChildItem


class DemoConfig(AppConfig):
    name = 'demo'
    verbose_name = '示例'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'

    menu = (
        ParentItem('第三方登录', children=[
            ChildItem('association', url='/admin/social_django/association/'),
            ChildItem('nonce', url='/admin/social_django/nonce/'),
            ChildItem('user social auth', url='/admin/social_django/usersocialauth/'),
        ], icon='fa fa-leaf'),

        ParentItem('订单管理', children=[
            ChildItem('订单', model='demo.order'),
        ], icon='fa fa-leaf'),

        ParentItem('用户管理', children=[
            ChildItem(label='用户', model='auth.user'),
            ChildItem('用户组', 'auth.group'),
        ], icon='fa fa-users'),

        ParentItem('设置', children=[
            ChildItem('修改密码', url='admin:password_change'),
            ChildItem('百度一下', url='https://www.baidu.com', target_blank=True),
        ], align_right=True, icon='fa fa-cog'),
    )

    def ready(self):
        super(SuitConfig, self).ready()

        # DO NOT COPY FOLLOWING LINE
        # It is only to prevent updating last_login in DB for demo app
        self.prevent_user_last_login()

    def prevent_user_last_login(self):
        """
        Disconnect last login signal
        """
        from django.contrib.auth import user_logged_in
        from django.contrib.auth.models import update_last_login
        user_logged_in.disconnect(update_last_login)
