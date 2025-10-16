# Frontend Integration with a Deployed Agent (Complete Implementation Guide)
Using the **Demo6-AlphaMind** project as an example, this guide explains how to connect a frontend application to a backend Agent service — covering interface contracts, streaming responses, UI handling, stop control, Markdown rendering, and error management.

## 1. Prerequisites
🕐 Have a working frontend project (React + Vite).

🕑 The backend Agent is deployed and supports standard HTTP or SSE (Server-Sent Events) streaming.

🕒 Confirm the backend streaming API endpoint to connect, e.g.:/api/v1/core-agent/chat/stream

## 2. Minimal Interface Contract (Recommended)
🕐 **Request body example:**
{
  "user_id": "string",
  "mode": "chat | agent",
  "message": "user input",
  "session_id": "optional",
  "conversation_id": "optional"
}

🕐 **Streaming response (SSE recommended):**
Push each line as data: {json}
Send data: [DONE] to indicate completion

🕐 **Normal message fields (one of the following recommended):**
data.content | data.text | data.message | content | text | message

🕒 **Error message example:**
{"type":"error","data":{"error":"..."}}

## 3. Frontend Service Wrapper (chatService)
**File: src/demos/Demo6-AlphaMind/service/chatService.ts**

Uses AbortController to support the Stop function:
stopCurrentRequest() — aborts the active request.
sendMessageStream(...) — sends the streaming request, parses each data: line, and calls onMessage to update the UI incrementally.

**Key points:**

--Use fetch(url, { method:'POST', body: JSON.stringify(payload), signal })

--Read stream with response.body.getReader() and decode using TextDecoder

--Split by \n, handle lines starting with data:

--Extract message content from any supported field name

--Handle AbortError to distinguish between user stop and network errors

## 4. Page State & Stream Control
**File: src/demos/Demo6-AlphaMind/index.tsx**

Manage page-level state:
tasks, isLoading, isStreaming, error

handleSendMessage:
--Insert an empty placeholder for the assistant message.

--Call chatService.sendMessageStream(...) and append message fragments via onMessage.

--Use throttled updates to minimize re-rendering.

--Finalize once stream completes with onComplete.

handleStopStreaming:
Calls chatService.stopCurrentRequest() and sets isStreaming=false.

## 5. Input Area & Stop Button
**File: src/demos/Demo6-AlphaMind/components/InputArea.tsx**

Add props: isStreaming, onStopStreaming

Conditional rendering:
--When not streaming → show “Send” button.

--When streaming → show red “Stop” button calling onStopStreaming.

--Adjust padding and height to prevent overlap with chat/agent switch buttons.

## 6. Markdown Rendering (Assistant Messages)
**Files:**

**🕐 Renderer: src/demos/Demo6-AlphaMind/components/MarkdownRenderer.tsx**

**🕐 Used in: src/demos/Demo6-AlphaMind/components/ChatInterface.tsx**

Implementation:

--Use react-markdown with remark-gfm.

--Customize rendering for headings, lists, code blocks, tables, and links.

--In ChatInterface, apply MarkdownRenderer only for assistant messages; keep user messages plain (or optionally Markdown too).

## 7. Component Integration (AlphaMindLayout)
**File: src/demos/Demo6-AlphaMind/components/AlphaMindLayout.tsx**

Pass isStreaming and onStopStreaming down to each InputArea.
Pass message array to ChatInterface for display.

## 8. Proxy / CORS Setup (Optional)
If frontend and backend are on different domains:
Configure proxy in Vite or use environment variables:.env
VITE_AGENT_BASE_URL=https://your-agent.example.com
Use this base URL in chatService.

## 9. Error & Edge Case Handling
When the backend returns an error fragment, trigger onError and stop streaming.

--In the UI, append a user-friendly “Error” message.

--Reset isStreaming and isLoading.

After user clicks “Stop”, no further content should be added — optionally display “Stopped by user.”

## 10. Validation Checklist

✅ Can send and receive streamed replies correctly

✅ Stop button appears during streaming and halts within 1 second

✅ Markdown (headings/lists/tables/code) renders properly

✅ Errors are clearly displayed and do not affect future messages

## 11. Quick Integration Steps (Checklist)
--Create or reuse a chatService to connect to your Agent’s streaming API.

--Manage isStreaming / isLoading and message list in your page state.

--Add a Stop button in the input area (toggle by isStreaming).

--Use MarkdownRenderer for assistant messages.

--Optionally configure .env and proxy for environment flexibility.

## 12. Debugging Tips
Use browser network panel to inspect raw data: lines.
If parsing fails, log the full raw data: line before JSON decoding.
Add scroll containers for long tables/code blocks to avoid layout issues.
If you want to render user messages as Markdown too, or add advanced features like syntax highlighting, copy buttons, or mind map visualization, extend the MarkdownRenderer (e.g., integrate rehype-highlight).





