import os
from aws_cdk import (
    Stack,
    aws_apigateway as apigw,
    aws_lambda_python_alpha as lambda_python, # Handles pip install automatically
    aws_lambda as _lambda,
    Duration,
    CfnOutput
)
from constructs import Construct

class BackendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, table, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Common Lambda Config
        LAMBDA_CONFIG = {
            "runtime": _lambda.Runtime.PYTHON_3_14,
            "entry": os.path.join("..", "backend", "src"), # Points to backend/src
            "timeout": Duration.seconds(15),
            "environment": {"TABLE_NAME": table.table_name}
        }

        # 1. Create Bookmark Lambda (Scraper)
        create_fn = lambda_python.PythonFunction(
            self, "CreateBookmarkFn",
            index="handlers/create_bookmark.py",
            handler="handler",
            **LAMBDA_CONFIG
        )

        # 2. Get Bookmarks Lambda
        get_fn = lambda_python.PythonFunction(
            self, "GetBookmarksFn",
            index="handlers/get_bookmarks.py",
            handler="handler",
            **LAMBDA_CONFIG
        )

        # 3. Grant Permissions
        table.grant_write_data(create_fn)
        table.grant_read_data(get_fn)

        # 4. API Gateway
        api = apigw.LambdaRestApi(
            self, "SmartCuratorApi",
            handler=create_fn,
            proxy=False,
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS
            )
        )

        # 5. Define Routes
        bookmarks = api.root.add_resource("bookmarks")
        bookmarks.add_method("POST", apigw.LambdaIntegration(create_fn)) # Create
        bookmarks.add_method("GET", apigw.LambdaIntegration(get_fn))     # List

        CfnOutput(self, "ApiUrl", value=api.url)