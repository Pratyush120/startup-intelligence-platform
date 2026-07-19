"use client";

import { useState } from "react";
import { X, Sparkles, Send, BookOpen, ShieldAlert, ArrowRight, ExternalLink } from "lucide-react";
import { useUIStore } from "@/store/ui.store";
import { Badge } from "@/components/ui/badge";
import { IntelligenceService } from "@/services/intelligence.service";

export function AICopilot() {
  const { isCopilotOpen, closeCopilot } = useUIStore();
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<any[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  if (!isCopilotOpen) return null;

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Add user message
    setMessages(prev => [...prev, { role: "user", content: query }]);
    const currentQuery = query;
    setQuery("");
    setIsTyping(true);

    try {
      const response = await IntelligenceService.askCopilot(currentQuery);
      setMessages(prev => [...prev, response]);
    } catch (e) {
      setMessages(prev => [...prev, { role: "assistant", content: "Failed to fetch response." }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <>
      {/* Backdrop */}
      <div 
        className="fixed inset-0 bg-base/50 backdrop-blur-sm z-[110]" 
        onClick={closeCopilot}
      />
      
      {/* Panel */}
      <div className="fixed top-0 right-0 h-screen w-full sm:w-[450px] bg-surface-1 border-l border-border-default shadow-2xl z-[120] flex flex-col animate-in slide-in-from-right duration-300">
        
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-border-default bg-surface-1">
          <div className="flex items-center gap-2 text-primary font-medium">
            <Sparkles className="w-5 h-5 text-signal-positive" />
            Strategic AI Copilot
          </div>
          <button 
            onClick={closeCopilot}
            className="p-2 text-secondary hover:text-primary rounded-md hover:bg-surface-2 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Chat Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center space-y-6">
              <div className="w-16 h-16 rounded-2xl bg-surface-2 flex items-center justify-center border border-border-default">
                <Sparkles className="w-8 h-8 text-signal-positive" />
              </div>
              <div>
                <h3 className="text-lg font-medium text-primary">How can I assist your strategy?</h3>
                <p className="text-sm text-secondary mt-2 max-w-[280px]">
                  I can analyze markets, compare competitors, or summarize the latest intelligence.
                </p>
              </div>
              <div className="w-full space-y-2 mt-8">
                {["Summarize today's market", "Which startups deserve attention?", "Compare OpenAI and Anthropic"].map((prompt, i) => (
                  <button
                    key={i}
                    onClick={() => setQuery(prompt)}
                    className="w-full text-left p-3 rounded-lg border border-border-default hover:border-border-strong bg-surface-2 hover:bg-surface-3 transition-colors text-sm text-primary flex items-center justify-between group"
                  >
                    {prompt}
                    <ArrowRight className="w-4 h-4 opacity-0 group-hover:opacity-100 transition-opacity" />
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.role === 'user' ? (
                    <div className="bg-primary text-primary-foreground px-4 py-3 rounded-2xl rounded-tr-sm max-w-[85%] text-sm">
                      {msg.content}
                    </div>
                  ) : (
                    <div className="bg-surface-2 border border-border-default px-5 py-4 rounded-2xl rounded-tl-sm w-full max-w-[95%] space-y-4">
                      <p className="text-sm text-primary leading-relaxed">{msg.content}</p>
                      
                      {/* CERSR Formatting block */}
                      {msg.cersr && (
                        <div className="space-y-3 mt-4 pt-4 border-t border-border-default">
                          
                          <div className="flex items-center justify-between">
                             <div className="text-xs font-mono uppercase tracking-wider text-secondary flex items-center gap-1.5">
                                <Sparkles className="w-3.5 h-3.5" /> AI Confidence
                             </div>
                             <Badge variant="outline" className="font-mono bg-transparent border-signal-positive/30 text-signal-positive">
                               {msg.cersr.confidence}%
                             </Badge>
                          </div>

                          <div className="space-y-1.5">
                             <div className="text-xs font-mono uppercase tracking-wider text-secondary flex items-center gap-1.5">
                                <BookOpen className="w-3.5 h-3.5" /> Evidence & Sources
                             </div>
                             <p className="text-sm text-primary leading-relaxed">{msg.cersr.evidence}</p>
                             <div className="flex flex-wrap gap-2 pt-1">
                               {msg.cersr.sources.map((s: string, j: number) => (
                                 <span key={j} className="text-[10px] font-mono text-secondary bg-surface-3 px-2 py-1 rounded flex items-center gap-1 border border-border-default">
                                   <ExternalLink className="w-2.5 h-2.5" /> {s}
                                 </span>
                               ))}
                             </div>
                          </div>

                          <div className="space-y-1.5">
                             <div className="text-xs font-mono uppercase tracking-wider text-secondary flex items-center gap-1.5">
                                <ShieldAlert className="w-3.5 h-3.5" /> Strategic Recommendation
                             </div>
                             <p className="text-sm text-primary leading-relaxed bg-selection-bg p-3 rounded-lg border border-primary/20">
                               {msg.cersr.strategy}
                             </p>
                          </div>

                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
              {isTyping && (
                <div className="flex justify-start">
                  <div className="bg-surface-2 border border-border-default px-4 py-3 rounded-2xl rounded-tl-sm text-sm text-secondary flex items-center gap-2">
                    <Sparkles className="w-4 h-4 animate-pulse text-signal-positive" />
                    Analyzing intelligence...
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="p-4 bg-surface-1 border-t border-border-default">
          <form onSubmit={handleSend} className="relative flex items-center">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Ask anything..."
              className="w-full bg-surface-2 border border-border-default rounded-xl pl-4 pr-12 py-3 text-sm text-primary focus:outline-none focus:border-border-strong focus:ring-1 focus:ring-focus transition-all"
            />
            <button
              type="submit"
              disabled={!query.trim() || isTyping}
              className="absolute right-2 p-2 bg-primary text-primary-foreground rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-opacity"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
          <div className="text-center mt-2">
            <span className="text-[10px] text-tertiary font-mono uppercase tracking-widest">
              AI Copilot can make mistakes. Verify important metrics.
            </span>
          </div>
        </div>

      </div>
    </>
  );
}
