import { ChatInput } from "@/components/custom/chatinput";
import { PreviewMessage, ThinkingMessage } from "../../components/custom/message";
import { useScrollToBottom } from '@/components/custom/use-scroll-to-bottom';
import { useState, useEffect, useRef } from "react";
import { message } from "../../interfaces/interfaces";
import { Overview } from "@/components/custom/overview";
import { Header } from "@/components/custom/header";
import { v4 as uuidv4 } from 'uuid';

export function Chat() {
  const [messagesContainerRef, messagesEndRef] = useScrollToBottom<HTMLDivElement>();
  const [messages, setMessages] = useState<message[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [displayedResponses, setDisplayedResponses] = useState<{ [key: string]: string }>({});
  const processedMessagesRef = useRef<Set<string>>(new Set()); // Track processed message IDs
  const timersRef = useRef<NodeJS.Timeout[]>([]); // Store timers

  async function handleSubmit(text?: string) {
    if (isLoading) return;

    const messageText = text || question;
    if (!messageText) return;

    const traceId = uuidv4();
    setMessages(prev => [...prev, { content: messageText, role: "user", id: traceId }]);
    setIsLoading(true);
    setQuestion("");

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: messageText }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Response data:", data);
      const botResponse = data.response || "Error: No response";
      setMessages(prev => [...prev, { content: botResponse, role: "assistant", id: traceId }]);
      setIsLoading(false);
    } catch (error: unknown) {
      const errorMessage = error instanceof Error ? error.message : "Unknown error occurred";
      console.error("Error fetching response:", error);
      setMessages(prev => [
        ...prev,
        { content: `Error: ${errorMessage}`, role: "assistant", id: traceId },
      ]);
      setIsLoading(false);
    }
  }

  // Handle word-by-word display for new assistant messages
  useEffect(() => {
    // Clear previous timers
    timersRef.current.forEach(clearTimeout);
    timersRef.current = [];

    // Process only the latest assistant message that hasn't been processed
    const latestMessage = messages.filter(m => m.role === "assistant").slice(-1)[0];
    if (
      latestMessage &&
      !processedMessagesRef.current.has(latestMessage.id) &&
      latestMessage.content
    ) {
      console.log(`Processing message ID: ${latestMessage.id}, Content: ${latestMessage.content}`);
      processedMessagesRef.current.add(latestMessage.id); // Mark as processed
      const words = latestMessage.content.trim().split(/\s+/);
      let currentText = "";
      words.forEach((word, index) => {
        const timer = setTimeout(() => {
          currentText = currentText ? `${currentText} ${word}`.trim() : word;
          setDisplayedResponses(prev => ({
            ...prev,
            [latestMessage.id]: currentText,
          }));
          console.log(`Displaying: ${currentText}`);
        }, index * 100); // 100ms delay per word
        timersRef.current.push(timer);
      });
    }

    // Cleanup on unmount
    return () => {
      timersRef.current.forEach(clearTimeout);
      timersRef.current = [];
    };
  }, [messages]); // Depend only on messages

  return (
    <div className="flex flex-col min-w-0 h-dvh bg-background">
      <Header />
      <div className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4" ref={messagesContainerRef}>
        {messages.length === 0 && <Overview />}
        {messages.map((message, index) => (
          <PreviewMessage
            key={index}
            message={{
              ...message,
              content: message.role === "assistant" ? displayedResponses[message.id] || "" : message.content,
            }}
          />
        ))}
        {isLoading && <ThinkingMessage />}
        <div ref={messagesEndRef} className="shrink-0 min-w-[24px] min-h-[24px]" />
      </div>
      <div className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <ChatInput
          question={question}
          setQuestion={setQuestion}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
}