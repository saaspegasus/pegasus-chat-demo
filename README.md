Pegasus Chat Demo
-----------------

## Installation

First install this library:

```
pip install .
```

Add the app to `settings.INSTALLED_APPS`:

```
INSTALLED_APPS = [
   # other apps here
   "pegasus_chat_demo.apps.PegasusChatDemoConfig",
]
```

Add the URLs to `urls.py`:

```python
urlpatterns = [
    # other urls here
    path("chat-demo/", include("pegasus_chat_demo.urls")),
]
```

Then set up your URL routes. In `asgi.py`:

```
from pegasus_chat_demo.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    websocket_url_patterns,
                )
            )
        ),
    }
)
```

Finally, to call ChatGPT you need to set `OPENAI_API_KEY` in `settings.py`

```python
OPENAI_API_KEY = "sk-***"
```
