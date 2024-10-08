from django.urls import path
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from zanhu.messager.consumers import MessagesConsumer
from zanhu.notifications.consumers import NotificationsConsumer

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/notifications/', NotificationsConsumer.as_asgi()),
                path('ws/<username>/', MessagesConsumer.as_asgi()),
            ])
        ),
    ),
})

"""
OriginValidator或AllowedHostsOriginValidator可以防止通过WebSocket进行CSRF攻击
OriginValidator需要手动添加允许访问的源站，如：

from channels.security.websocket import OriginValidator
application = ProtocolTypeRouter({

    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                ...
            ])
        ),
        [".imooc.com", "http://.imooc.com:80", "http://muke.site.com"],
    ),
})

而使用AllowedHostsOriginValidator，允许访问的源站与settings.py文件中的ALLOWED_HOSTS相同
AuthMiddleware用于WebSocket认证，集成了CookieMiddleware, SessionMiddleware, AuthMiddleware, 兼容Django的认证系统
"""
