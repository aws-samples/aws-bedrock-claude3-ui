import * as cdk from "aws-cdk-lib";
import { LambdaRestApi } from "aws-cdk-lib/aws-apigateway";
import { PolicyStatement } from "aws-cdk-lib/aws-iam";
import { Runtime, Tracing } from "aws-cdk-lib/aws-lambda";
import { NodejsFunction } from "aws-cdk-lib/aws-lambda-nodejs";
import { RetentionDays } from "aws-cdk-lib/aws-logs";

import { Construct } from "constructs";
import path = require("path");

export class AwsClaude3UiStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const modelId = "anthropic.claude-3-sonnet-20240229-v1:0";

    const model_runner = new NodejsFunction(this, "model-runner", {
      handler: "handler",
      runtime: Runtime.NODEJS_20_X,
      entry: path.join(__dirname, "/../lambda/model_invoker.ts"),
      environment: {
        MODEL_ID: modelId,
      },
      logRetention: RetentionDays.ONE_DAY,
      tracing: Tracing.ACTIVE,
      timeout: cdk.Duration.minutes(1),
    });

    model_runner.addToRolePolicy(
      new PolicyStatement({
        actions: ["bedrock:InvokeModel"],
        resources: [`arn:aws:bedrock:${cdk.Aws.REGION}::foundation-model/*`],
      })
    );

    const api = new LambdaRestApi(this, "claude-api", {
      handler: model_runner,
      defaultCorsPreflightOptions: {
        allowOrigins: ["*"],
        allowMethods: ["*"],
        allowHeaders: ["*"],
      },
      proxy: false,
    });

    const version = api.root.addResource("v1");
    const chat = version.addResource("chat");
    const messages = version.addResource("messages");
    const completions = chat.addResource("completions");
    messages.addMethod("ANY"); // GET /items/{item}
    completions.addMethod("ANY");
  }
}
