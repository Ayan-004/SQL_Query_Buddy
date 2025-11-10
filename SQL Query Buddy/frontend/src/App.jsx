import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { vscDarkPlus } from "react-syntax-highlighter/dist/esm/styles/prism";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const API_URL = "http://localhost:8000/chat";

  const handleEnhancePrompt = async () => {
    if (!input.trim()) return;

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/enhance-prompt", {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          prompt: input,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to enhance prompt");
      }

      const data = await response.json();
      setInput(data.enhanced_prompt);
    } catch (error) {
      console.error("Error enhancing prompt:", error);
    }
    setLoading(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const sanitizedInput = input.replace(/[\u2018\u2019\u201C\u201D]/g, "'");

    const userMessage = { sender: "user", text: sanitizedInput };

    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    const simpleHistory = messages
      .filter((m) => m.sender === "ai")
      .map((m, i) => {
        const userMsg = messages.filter((m) => m.sender === "user")[i];
        return [userMsg ? userMsg.text : "", m.text];
      })
      .slice(-5);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-type": "application/json" },
        body: JSON.stringify({
          question: sanitizedInput,
          chat_history: simpleHistory,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Server error:", errorData);
        throw new Error(`Server error: ${response.status}`);
      }

      const data = await response.json();
      const aiMessage = { sender: "ai", text: data.answer };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error fetching from API:", error);
      const errorMessage = {
        sender: "ai",
        text: "Sorry, I ran into an error. Please check the console.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  return (
    // {Main Component}
    <div className="flex flex-col min-h-screen bg-neutral-900 text-white">
      {/* {Header} */}
      <header className="sticky top-0 z-10 p-4 border-b border-neutral-800 bg-neutral-900/75 backdrop-blur-xl">
        <h1 className="text-2xl font-sans">SQL Query Buddy</h1>
        <p className="text-sm text-gray-400">
          Ask me anything about your retail database!
        </p>

        <button
          onClick={() => setMessages([])}
          className="absolute top-7 right-4 bg-gray-700 hover:bg-gray-600 text-white text-sm font-semibold hover:cursor-pointer py-1 px-3 rounded-full"
        >
          New Chat
        </button>
      </header>

      {/* {Chat Window} */}
      <div className="flex flex-col items-center px-4 pt-6 pb-16 space-y-4">
        <div className="w-full max-w-2xl space-y-4">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "user" ? "justify-end" : "justify-center"
              }`}
            >
              <div
                className={`p-3 rounded-3xl max-w-2xl ${
                  msg.sender === "user"
                    ? "bg-blue-700 text-white"
                    : "text-white text-left"
                }`}
              >
                {msg.sender === "user" ? (
                  <p>{msg.text}</p>
                ) : (
                  <AIMessage content={msg.text} />
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* {Input form} */}
      <form
        className="sticky bottom-6 flex justify-center w-full px-4 z-10"
        onSubmit={handleSubmit}
      >
        <div className="flex items-center w-full max-w-3xl sm:max-w-3xl bg-neutral-800/80 backdrop-blur-xl border border-neutral-700 rounded-full px-2 py-2 transition-all duration-300 focus-within:scale-[1.02] focus-within:shadow-[0_0_15px_rgba(255,255,255,0.15)]">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask SQL Buddy..."
            disabled={loading}
            className="flex-1 bg-transparent text-white placeholder-gray-400 focus:outline-none text-base px-3"
          />

          <button
            type="button"
            onClick={handleEnhancePrompt}
            disabled={loading || !input}
            className="text-gray-400 hover:text-white mr-5 disabled:opacity-50 transition  cursor-pointer"
            title="Enhance Prompt"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#ffffff"
              stroke-width="1.75"
              stroke-linecap="round"
              stroke-linejoin="round"
              class="lucide lucide-wand-sparkles-icon lucide-wand-sparkles"
            >
              <path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72" />
              <path d="m14 7 3 3" />
              <path d="M5 6v4" />
              <path d="M19 14v4" />
              <path d="M10 2v2" />
              <path d="M7 8H3" />
              <path d="M21 16h-4" />
              <path d="M11 3H9" />
            </svg>
          </button>
          <button
            type="submit"
            disabled={loading}
            className="bg-blue-700 hover:bg-blur-800 text-white font-semibold py-2 px-2 rounded-full disabled:bg-gray-600 disabled:cursor-not-allowed transition hover:bg-blue-800 cursor-pointer"
          >
            {loading ? (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#ffffff"
                strokeWidth="1.75"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="lucide lucide-loader animate-spin"
              >
                <path d="M12 2v4" />
                <path d="m16.2 7.8 2.9-2.9" />
                <path d="M18 12h4" />
                <path d="m16.2 16.2 2.9 2.9" />
                <path d="M12 18v4" />
                <path d="m4.9 19.1 2.9-2.9" />
                <path d="M2 12h4" />
                <path d="m4.9 4.9 2.9 2.9" />
              </svg>
            ) : (
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="20"
                height="20"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
                stroke-linecap="round"
                stroke-linejoin="round"
                class="lucide lucide-arrow-up-icon lucide-arrow-up"
              >
                <path d="m5 12 7-7 7 7" />
                <path d="M12 19V5" />
                <path d="m5 12 7-7 7 7" />
                <path d="M12 19V5" />
              </svg>
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

const AIMessage = ({ content }) => {
  return (
    <ReactMarkdown
      children={content}
      components={{
        code({ node, inline, className, children, ...props }) {
          const match = /language-(\w+)/.exec(className || "");
          if (match && match[1] === "sql") {
            return (
              <SyntaxHighlighter
                style={vscDarkPlus}
                language="sql"
                PreTag="div"
                {...props}
              >
                {String(children).replace(/\n$/, "")}
              </SyntaxHighlighter>
            );
          }
          if (className === "language-") {
            return (
              <pre
                className="bg-gray-900 p-2 rounded-md overflow-x-auto text-sm"
                {...props}
              >
                <code>{children}</code>
              </pre>
            );
          }
          return (
            <code className="bg-gray-800 px-1 rounded-sm">{children}</code>
          );
        },
        h2({ children }) {
          return <strong className="text-lg text-blue-300">{children}</strong>;
        },
        blockquote({ children }) {
          return (
            <blockquote className="border-l-4 border-gray-500 pl-2 italic">
              {children}
            </blockquote>
          );
        },
      }}
    />
  );
};

export default App;
