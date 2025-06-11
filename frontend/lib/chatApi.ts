import { Client, ThreadState } from "@langchain/langgraph-sdk";
import {
  LangChainMessage,
  LangGraphCommand,
} from "@assistant-ui/react-langgraph";

const createClient = () => {
  const apiUrl =
    process.env["NEXT_PUBLIC_LANGGRAPH_API_URL"] ||
    new URL("/api", window.location.href).href;
  return new Client({
    apiUrl,
  });
};

export const createThread = async () => {
  const client = createClient();
  try {
    return await client.threads.create();
  } catch (error) {
    console.error("Error creating thread:", error);
    throw error;
  }
};

export const getThreadState = async (
  threadId: string
): Promise<ThreadState<{ messages: LangChainMessage[] }>> => {
  const client = createClient();
  try {
    return await client.threads.getState(threadId);
  } catch (error) {
    console.error(`Error getting state for thread ${threadId}:`, error);
    throw error;
  }
};

export const sendMessage = async (params: {
  threadId: string;
  messages?: LangChainMessage[];
  command?: LangGraphCommand | undefined;
}) => {
  const client = createClient();
  const assistantId = process.env["NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID"];
  if (!assistantId) {
    throw new Error("NEXT_PUBLIC_LANGGRAPH_ASSISTANT_ID is not set.");
  }
  try {
    return await client.runs.stream(
      params.threadId,
      assistantId,
      {
        input: params.messages?.length
          ? {
              messages: params.messages,
            }
          : null,
        command: params.command,
        streamMode: ["messages", "updates"],
      }
    );
  } catch (error) {
    console.error(`Error sending message to thread ${params.threadId}:`, error);
    throw error;
  }
};
