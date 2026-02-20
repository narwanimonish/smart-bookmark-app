#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.database_stack import DatabaseStack
from stacks.backend_stack import BackendStack
from stacks.frontend_stack import FrontendStack

app = cdk.App()

# 1. Init Database
db_stack = DatabaseStack(app, "Curator-Database")

# 2. Init Backend (Pass the table object!)
backend_stack = BackendStack(app, "Curator-Backend", table=db_stack.table)

# 3. Init Frontend
# frontend_stack = FrontendStack(app, "Curator-Frontend")

app.synth()