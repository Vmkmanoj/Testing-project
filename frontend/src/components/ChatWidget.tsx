import { useState, useRef, useEffect } from 'react';
import { MessageSquare, X, Send, Bot, User, Loader2, Maximize2, Minimize2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';

interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Dragging state
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const dragRef = useRef<{ startX: number, startY: number, startPosX: number, startPosY: number } | null>(null);

  const [messages, setMessages] = useState<ChatMessage[]>([
    { role: 'assistant', content: "Hi! I'm your AI assistant. How can I help you today?" }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  // Mode is permanently set to 'sql'
  const mode = 'sql';
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isOpen]);

  useEffect(() => {
    if (!isDragging) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (!dragRef.current) return;
      const dx = e.clientX - dragRef.current.startX;
      const dy = e.clientY - dragRef.current.startY;
      setPosition({
        x: dragRef.current.startPosX + dx,
        y: dragRef.current.startPosY + dy
      });
    };

    const handleMouseUp = () => {
      setIsDragging(false);
      dragRef.current = null;
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
    };
  }, [isDragging]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: ChatMessage = { role: 'user', content: input.trim() };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInput('');
    setIsLoading(true);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/api/v1/agent/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          message: userMessage.content,
          history: messages.map(m => ({ role: m.role, content: m.content })),
          mode: mode,
        })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      let latestAssistantResponse = 'Thinking...';

      // Add a temporary assistant message that we will update
      setMessages([...newMessages, { role: 'assistant', content: latestAssistantResponse }]);

      if (reader) {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n');

          for (const line of lines) {
            if (line.startsWith('data: ')) {
              const dataStr = line.slice(6).trim();
              if (dataStr) {
                try {
                  const data = JSON.parse(dataStr);
                  // Since LangGraph yields the full state with each update,
                  // we can check if it has updated the final_response or just show progress.

                  // If it's a node update, LangGraph returns an object where keys are node names
                  // e.g. {"apply_leave": {"final_response": "..."}} or just the state if stream_mode="values"
                  // Let's try to extract final_response depending on how it's structured.

                  let newContent = latestAssistantResponse;

                  if (data && data.token) {
                    if (newContent === 'Thinking...') {
                      newContent = data.token;
                    } else {
                      newContent += data.token;
                    }
                  } else if (data && data.final_state) {
                    if (data.final_state.final_answer) {
                      newContent = data.final_state.final_answer;
                    } else if (data.final_state.final_response) {
                      newContent = data.final_state.final_response;
                    }
                  } else if (data && data.final_response) {
                    newContent = data.final_response;
                  } else if (data && data.final_answer) {
                    newContent = data.final_answer;
                  } else if (data && typeof data === 'object') {
                    for (const key in data) {
                      if (data[key] && data[key].final_response) {
                        newContent = data[key].final_response;
                      }
                      if (data[key] && data[key].final_answer) {
                        newContent = data[key].final_answer;
                      }
                    }
                  }

                  // Only update if newContent is a valid string and different
                  if (typeof newContent === 'string' && newContent !== latestAssistantResponse) {
                    latestAssistantResponse = newContent;
                    setMessages((prev) => {
                      const updated = [...prev];
                      updated[updated.length - 1] = { role: 'assistant', content: latestAssistantResponse };
                      return updated;
                    });
                  }
                } catch (err) {
                  console.error('Error parsing SSE data', err);
                }
              }
            }
          }
        }
      }
    } catch (error) {
      console.error('Failed to send message:', error);
      setMessages((prev) => {
        const updated = [...prev];
        updated[updated.length - 1] = { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' };
        return updated;
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <>
      {/* Floating Button */}
      <button
        onClick={() => setIsOpen(true)}
        style={{
          position: 'fixed',
          bottom: '24px',
          right: '24px',
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          backgroundColor: 'var(--primary)',
          color: 'white',
          border: 'none',
          boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
          cursor: 'pointer',
          display: isOpen ? 'none' : 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1000,
          transition: 'transform 0.2s',
        }}
        onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.05)')}
        onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
      >
        <MessageSquare size={24} />
      </button>

      {/* Chat Window */}
      {isOpen && (
        <div
          style={{
            position: 'fixed',
            bottom: '24px',
            right: '24px',
            width: isExpanded ? '100%' : '380px',
            height: isExpanded ? '100%' : '600px',
            maxHeight: 'calc(100vh - 48px)',
            maxWidth: 'calc(100vw - 48px)',
            backgroundColor: 'var(--bg-card)',
            borderRadius: '16px',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.2)',
            display: 'flex',
            flexDirection: 'column',
            zIndex: 1000,
            overflow: 'hidden',
            border: '1px solid var(--border)',
            transition: isDragging ? 'none' : 'all 0.3s ease-in-out',
            transform: `translate(${position.x}px, ${position.y}px)`,
          }}
        >
          {/* Header */}
          <div
            onMouseDown={(e) => {
              if (e.target instanceof HTMLButtonElement || (e.target as HTMLElement).closest('button')) return;
              setIsDragging(true);
              dragRef.current = {
                startX: e.clientX,
                startY: e.clientY,
                startPosX: position.x,
                startPosY: position.y
              };
            }}
            style={{
              padding: '16px 20px',
              backgroundColor: 'var(--primary)',
              color: 'white',
              display: 'flex',
              flexDirection: 'column',
              gap: '12px',
              cursor: isDragging ? 'grabbing' : 'grab',
              userSelect: 'none'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Bot size={20} />
                <h3 style={{ margin: 0, fontSize: '16px', fontWeight: 600 }}>AI Assistant</h3>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '4px',
                    opacity: 0.8,
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.opacity = '1')}
                  onMouseLeave={(e) => (e.currentTarget.style.opacity = '0.8')}
                  title={isExpanded ? "Collapse" : "Expand"}
                >
                  {isExpanded ? <Minimize2 size={18} /> : <Maximize2 size={18} />}
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  style={{
                    background: 'transparent',
                    border: 'none',
                    color: 'white',
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '4px',
                    opacity: 0.8,
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.opacity = '1')}
                  onMouseLeave={(e) => (e.currentTarget.style.opacity = '0.8')}
                  title="Close"
                >
                  <X size={20} />
                </button>
              </div>
            </div>
          </div>

          {/* Messages Area */}
          <div
            style={{
              flex: 1,
              overflowY: 'auto',
              padding: '20px',
              display: 'flex',
              flexDirection: 'column',
              gap: '16px',
              backgroundColor: 'var(--bg-body)',
            }}
          >
            {messages.map((msg, index) => (
              <div
                key={index}
                style={{
                  display: 'flex',
                  gap: '12px',
                  flexDirection: msg.role === 'user' ? 'row-reverse' : 'row',
                }}
              >
                <div
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    backgroundColor: msg.role === 'user' ? 'var(--primary)' : 'var(--indigo)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    flexShrink: 0,
                  }}
                >
                  {msg.role === 'user' ? <User size={16} /> : <Bot size={16} />}
                </div>
                <div
                  style={{
                    backgroundColor: msg.role === 'user' ? 'var(--primary)' : 'var(--bg-card)',
                    color: msg.role === 'user' ? 'white' : 'var(--text-main)',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    borderTopRightRadius: msg.role === 'user' ? '4px' : '12px',
                    borderTopLeftRadius: msg.role === 'assistant' ? '4px' : '12px',
                    fontSize: '14px',
                    lineHeight: '1.5',
                    maxWidth: '80%',
                    border: msg.role === 'assistant' ? '1px solid var(--border)' : 'none',
                  }}
                >
                  {msg.role === 'user' ? (
                    msg.content
                  ) : (
                    <div className="markdown-body">
                      <ReactMarkdown>{msg.content}</ReactMarkdown>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {isLoading && (
              <div style={{ display: 'flex', gap: '12px' }}>
                <div
                  style={{
                    width: '32px',
                    height: '32px',
                    borderRadius: '50%',
                    backgroundColor: 'var(--indigo)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                  }}
                >
                  <Bot size={16} />
                </div>
                <div
                  style={{
                    backgroundColor: 'var(--bg-card)',
                    padding: '12px 16px',
                    borderRadius: '12px',
                    borderTopLeftRadius: '4px',
                    border: '1px solid var(--border)',
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  <Loader2 size={16} className="spin" style={{ color: 'var(--text-muted)' }} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div
            style={{
              padding: '16px',
              borderTop: '1px solid var(--border)',
              backgroundColor: 'var(--bg-card)',
            }}
          >
            <div
              style={{
                display: 'flex',
                gap: '8px',
                alignItems: 'flex-end',
              }}
            >
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Type your message..."
                disabled={isLoading}
                style={{
                  flex: 1,
                  backgroundColor: 'var(--bg-body)',
                  border: '1px solid var(--border)',
                  borderRadius: '12px',
                  padding: '12px',
                  color: 'var(--text-main)',
                  resize: 'none',
                  height: '44px',
                  maxHeight: '120px',
                  fontFamily: 'inherit',
                  fontSize: '14px',
                  outline: 'none',
                }}
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || isLoading}
                style={{
                  width: '44px',
                  height: '44px',
                  borderRadius: '12px',
                  backgroundColor: input.trim() && !isLoading ? 'var(--primary)' : 'var(--bg-body)',
                  color: input.trim() && !isLoading ? 'white' : 'var(--text-muted)',
                  border: '1px solid',
                  borderColor: input.trim() && !isLoading ? 'var(--primary)' : 'var(--border)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: input.trim() && !isLoading ? 'pointer' : 'not-allowed',
                  transition: 'all 0.2s',
                  flexShrink: 0,
                }}
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
