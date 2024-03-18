import {
  BedrockRuntimeClient,
  InvokeModelCommand,
  InvokeModelCommandInput,
} from "@aws-sdk/client-bedrock-runtime";
import { Handler } from "aws-lambda";

function openaiToClaudeParams(messages) {
  // 使用 filter 方法过滤掉 role 为 'system' 的消息对象
  messages = messages.filter((message) => message.role !== "system");
  // 遍历消息对象数组
  messages.forEach((message) => {
    if (message.content && typeof message.content !== "string") {
      message.content.forEach((item) => {
        if (item.type === "image_url") {
          const imageUrl = item.image_url.url;
          const base64Image = imageUrl.substring(
            imageUrl.indexOf("{") + 1,
            imageUrl.indexOf("}")
          );
          item.type = "image";
          item.source = {
            type: "base64",
            media_type: "image/jpeg",
            data: base64Image,
          };
          delete item.image_url;
        }
      });
    }
  });

  return messages;
}

// {
//   "choices": [
//     {
//       "finish_reason": "stop",
//       "index": 0,
//       "message": {
//         "content": "The 2020 World Series was played in Texas at Globe Life Field in Arlington.",
//         "role": "assistant"
//       },
//       "logprobs": null
//     }
//   ],
//   "created": 1677664795,
//   "id": "chatcmpl-7QyqpwdfhqwajicIEznoc6Q47XAyW",
//   "model": "gpt-3.5-turbo-0613",
//   "object": "chat.completion",
//   "usage": {
//     "completion_tokens": 17,
//     "prompt_tokens": 57,
//     "total_tokens": 74
//   }
// }

function claudeToChatgptResponseStream(claudeFormat) {
  const obj2Data = {
    choices: [
      {
        finish_reason: "stop",
        index: 0,
        message: {
          content: claudeFormat.content[0].text,
          role: claudeFormat.role,
        },
        logprobs: null,
      },
    ],
    created: Math.floor(Date.now() / 1000), // 使用当前时间作为创建时间，单位为秒
    id: claudeFormat.id,
    model: claudeFormat.model,
    object: "chat.completion",
    usage: {
      completion_tokens: claudeFormat.usage.output_tokens,
      prompt_tokens: claudeFormat.usage.input_tokens,
      total_tokens:
        claudeFormat.usage.input_tokens + claudeFormat.usage.output_tokens,
    },
  };
  return obj2Data;
}

export const handler: Handler = async (event, context) => {
  const path = event.path;
  const isClaude = path === "/v1/messages" ? true : false;
  const badResponse = {
    statusCode: 400,
    body: JSON.stringify("Invalid request!"),
  };

  if (event.body && event.body !== "") {
    let body = JSON.parse(event.body);
    if (body.model && body.messages && body.messages.length > 0) {
      let system = body.system;
      if (body.messages[0].role === "system") system = body.messages[0].content;
      let convertedMessages = isClaude
        ? body.messages
        : openaiToClaudeParams(body.messages);
      console.log("begin invoke message", convertedMessages);
      if (convertedMessages.length <= 0) return badResponse;
      let max_tokens = body.max_tokens || 1000;
      let top_p = body.top_p || 1;
      let top_k = body.top_k || 250;
      let modelId = "anthropic.claude-3-sonnet-20240229-v1:0";
      if (body.model.startsWith("anthropic")) modelId = body.model;
      let temperature = body.temperature || 0.5;
      const contentType = "application/json";
      const rockerRuntimeClient = new BedrockRuntimeClient({
        region: process.env.REGION,
      });

      const inputCommand: InvokeModelCommandInput = {
        modelId,
        contentType,
        accept: contentType,
        body: system
          ? JSON.stringify({
              anthropic_version: "bedrock-2023-05-31",
              max_tokens: max_tokens,
              temperature: temperature,
              top_k: top_k,
              top_p: top_p,
              system: system,
              messages: convertedMessages,
            })
          : JSON.stringify({
              anthropic_version: "bedrock-2023-05-31",
              max_tokens: max_tokens,
              temperature: temperature,
              top_k: top_k,
              top_p: top_p,
              messages: convertedMessages,
            }),
      };

      const command = new InvokeModelCommand(inputCommand);
      const response = await rockerRuntimeClient.send(command);
      const result = {
        statusCode: 200,
        headers: {
          "Content-Type": `${contentType}`,
        },
        body: isClaude
          ? JSON.stringify(JSON.parse(new TextDecoder().decode(response.body)))
          : JSON.stringify(
              claudeToChatgptResponseStream(
                JSON.parse(new TextDecoder().decode(response.body))
              ),
              null,
              2
            ),
      };
      console.log("invoke success response", result);
      return result;
    } else {
      return badResponse;
    }
  } else {
    return badResponse;
  }
};
