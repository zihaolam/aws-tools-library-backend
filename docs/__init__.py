import json

from docs.openapi import get_openapi_schema

swagger_ui_params = {
    "dom_id": "#swagger-ui",
    "layout": "BaseLayout",
    "deepLinking": True,
    "showExtensions": True,
    "showCommonExtensions": True,
}


def get_redoc_html() -> str:
    return """
    <!DOCTYPE html>
    <html>
    <head>
    <title>API Docs</title>
    <!-- needed for adaptive design -->
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <!--
    ReDoc doesn't change outer page styles
    -->
    <style>
      body {
        margin: 0;
        padding: 0;
      }
    </style>
    </head>
    <body>
    <noscript>
        ReDoc requires Javascript to function. Please enable it to browse the documentation.
    </noscript>
    <redoc spec-url="/openapi.json"></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
    </body>
    </html>
    """


def get_swagger_ui_html(
    *,
    openapi_url: str = "/openapi.json",
    swagger_js_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
    swagger_css_url: str = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
) -> str:
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link type="text/css" rel="stylesheet" href="{swagger_css_url}">
    <title>Lean API Docs</title>
    </head>
    <body>
    <div id="swagger-ui">
    </div>
    <script src="{swagger_js_url}"></script>
    <!-- `SwaggerUIBundle` is now available on the page -->
    <script>
    const ui = SwaggerUIBundle({{
        url: '{openapi_url}',
        presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
        ],
    """

    for key, value in swagger_ui_params.items():
        html += f"{json.dumps(key)}: {json.dumps(value)},\n"

    html += "})"
    html += """
    </script>
    </body>
    </html>
    """
    return html


def swagger_ui_handler(event, context):
    return dict(
        statusCode=200,
        body=get_swagger_ui_html(),
        headers={
            "Content-Type": "text/html",
        },
    )


open_api_schema = get_openapi_schema()


def openapi_handler(event, context):
    return dict(statusCode=200, body=json.dumps(open_api_schema))