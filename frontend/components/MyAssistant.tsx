"use client";

import { useRef, useMemo, type FC } from "react";
import { AssistantRuntimeProvider } from "@assistant-ui/react";
import { useLangGraphRuntime } from "@assistant-ui/react-langgraph";
import React from "react";

import { createThread, getThreadState, sendMessage } from "@/lib/chatApi";
import { Thread } from "@/components/assistant-ui/thread";
import { CompositeAttachmentAdapter, SimpleImageAttachmentAdapter } from "@assistant-ui/react";

type MyAssistantProps = {};

export const MyAssistant: FC<MyAssistantProps> = ({}) => {
  const threadIdRef = useRef<string | undefined>(undefined);
  const runtime = useLangGraphRuntime({
    threadId: threadIdRef.current,
    stream: async (messages, { command }) => {
      if (!threadIdRef.current) {
        const { thread_id } = await createThread();
        threadIdRef.current = thread_id;
      }
      const threadId = threadIdRef.current;
      return sendMessage({
        threadId,
        messages,
        command,
      });
    },
    onSwitchToNewThread: async () => {
      const { thread_id } = await createThread();
      threadIdRef.current = thread_id;
    },
    onSwitchToThread: async (threadId) => {
      threadIdRef.current = threadId;
      const state = await getThreadState(threadId);
      return { messages: state.values.messages };
    },
    adapters: useMemo(() => ({
      attachments: new CompositeAttachmentAdapter([
        new SimpleImageAttachmentAdapter(),
      ]),
    }), []),
  });

  // Log the runtime object to inspect its available methods and properties
  React.useEffect(() => {
    console.log("Runtime object:", runtime);
  }, [runtime]);

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <Thread />
    </AssistantRuntimeProvider>
  );
};
