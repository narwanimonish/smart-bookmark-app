from aws_cdk import (
    Stack,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class DatabaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Define the DynamoDB Table
        self.table = dynamodb.Table(
            self, "BookmarksTable",
            partition_key=dynamodb.Attribute(
                name="bookmark_id", 
                type=dynamodb.AttributeType.STRING
            ),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST, # Serverless pricing
            removal_policy=RemovalPolicy.DESTROY, # For dev only; use RETAIN for prod
        )