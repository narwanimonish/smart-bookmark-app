import os
from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class FrontendStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "FrontendBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        dist = cloudfront.Distribution(
            self, "FrontendDistribution",
            default_root_object="index.html",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            error_responses=[cloudfront.ErrorResponse(
                http_status=404,
                response_http_status=200,
                response_page_path="/index.html"
            )]
        )

        # Deploys the local 'dist' folder to S3
        s3deploy.BucketDeployment(
            self, "DeployWebsite",
            sources=[s3deploy.Source.asset(os.path.join("..", "frontend", "dist"))],
            destination_bucket=bucket,
            distribution=dist
        )

        CfnOutput(self, "FrontendUrl", value=f"https://{dist.distribution_domain_name}")