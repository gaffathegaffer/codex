import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

const response = await openai.responses.create({
  prompt: {
    id: "pmpt_XXXXXXXX",
    version: "2",
  },
  input: [],
  text: {
    format: {
      type: "text",
    },
  },
  reasoning: {},
  tools: [
    {
      type: "function",
      name: "text_to_speech",
      description: "Converts input text to speech audio",
      parameters: {
        type: "object",
        properties: {
          text: {
            type: "string",
            description: "The text to be converted to speech",
          },
          language: {
            type: "string",
            description: "The language code for speech synthesis, such as 'en', 'es', 'fr'",
          },
          voice: {
            type: "string",
            description: "Preferred voice for speech synthesis, if available",
          },
          speed: {
            type: "number",
            description: "Speech speed as a multiplier, where 1 is normal speed",
          },
        },
        required: ["text", "language", "voice", "speed"],
        additionalProperties: false,
      },
      strict: true,
    },
    {
      type: "code_interpreter",
      container: {
        type: "auto",
      },
    },
    {
      type: "image_generation",
      size: "1024x1536",
      quality: "high",
      output_format: "jpeg",
      background: "transparent",
      moderation: "low",
      partial_images: 3,
    },
    {
      type: "mcp",
      server_label: "cloudflare",
      server_url: "https://browser.mcp.cloudflare.com/sse",
      server_description: "Example Cloudflare MCP server",
      headers: {
        Authorization: "Bearer <token>",
      },
      allowed_tools: [],
      require_approval: "always",
    },
    {
      type: "mcp",
      server_label: "deepwiki",
      server_url: "https://mcp.deepwiki.com/mcp",
      allowed_tools: ["read_wiki_structure", "read_wiki_contents", "ask_question"],
      require_approval: "always",
    },
  ],
  max_output_tokens: 2048,
  store: true,
});

console.log(response);
