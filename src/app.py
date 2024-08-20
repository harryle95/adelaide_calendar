


# We add the session security schema to the OpenAPI config.
openapi_config = OpenAPIConfig(
    title="My API",
    version="1.0.0",
)


app = Litestar(
    route_handlers=[
        authorise,
        oauth2callback,
    ],
    openapi_config=openapi_config,
)
