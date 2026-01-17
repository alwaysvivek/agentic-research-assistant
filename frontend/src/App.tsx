import React, { useState } from 'react';
import { api } from './api';
import { Send, Upload, BookOpen, CheckCircle, AlertCircle, Loader2, Link, FileText, Type } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import clsx from 'clsx';

function App() {
  const [ingestMode, setIngestMode] = useState<'url' | 'file' | 'text'>('url');

  const [urlSource, setUrlSource] = useState('');
  const [textSource, setTextSource] = useState('');
  const [fileSource, setFileSource] = useState<File | null>(null);

  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant', content: string, confidence?: number, sources?: string[] }[]>([]);
  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<'idle' | 'success' | 'error'>('idle');

  const handleIngest = async () => {
    setIngesting(true);
    setIngestStatus('idle');
    try {
      if (ingestMode === 'url' && urlSource) {
        await api.ingest(urlSource);
      } else if (ingestMode === 'text' && textSource) {
        await api.ingestText(textSource);
      } else if (ingestMode === 'file' && fileSource) {
        await api.ingestFile(fileSource);
      } else {
        return; // nothing to ingest
      }
      setIngestStatus('success');
      setTimeout(() => setIngestStatus('idle'), 3000);

      // Clear inputs
      if (ingestMode === 'url') setUrlSource('');
      if (ingestMode === 'text') setTextSource('');
      if (ingestMode === 'file') setFileSource(null);

    } catch (error) {
      console.error(error);
      setIngestStatus('error');
    } finally {
      setIngesting(false);
    }
  };

  const isIngestDisabled = () => {
    if (ingesting) return true;
    if (ingestMode === 'url') return !urlSource;
    if (ingestMode === 'text') return !textSource;
    if (ingestMode === 'file') return !fileSource;
    return true;
  }

  const handleResearch = async () => {
    if (!query) return;
    setLoading(true);
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    const currentQuery = query;
    setQuery('');

    try {
      const result = await api.research(currentQuery);
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: result.answer,
        confidence: result.confidence_score,
        sources: result.source_chunk_ids
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error while researching." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex items-center gap-3">
          <BookOpen className="w-6 h-6 text-blue-600" />
          <h1 className="text-xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Reliable Researcher
          </h1>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-4 py-8 grid grid-cols-1 lg:grid-cols-4 gap-8">

        {/* Sidebar: Ingestion */}
        <aside className="lg:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-100">
            <h2 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Knowledge Base</h2>

            {/* Tabs */}
            <div className="flex bg-gray-100 p-1 rounded-lg mb-4">
              <button onClick={() => setIngestMode('url')} className={clsx("flex-1 py-1.5 rounded-md text-xs font-medium transition-all flex justify-center", ingestMode === 'url' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700')}>
                <Link className="w-4 h-4" />
              </button>
              <button onClick={() => setIngestMode('file')} className={clsx("flex-1 py-1.5 rounded-md text-xs font-medium transition-all flex justify-center", ingestMode === 'file' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700')}>
                <FileText className="w-4 h-4" />
              </button>
              <button onClick={() => setIngestMode('text')} className={clsx("flex-1 py-1.5 rounded-md text-xs font-medium transition-all flex justify-center", ingestMode === 'text' ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500 hover:text-gray-700')}>
                <Type className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3">
              {ingestMode === 'url' && (
                <input
                  type="text"
                  value={urlSource}
                  onChange={(e) => setUrlSource(e.target.value)}
                  placeholder="https://example.com"
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm transition-all"
                />
              )}

              {ingestMode === 'text' && (
                <textarea
                  value={textSource}
                  onChange={(e) => setTextSource(e.target.value)}
                  placeholder="Paste raw text here..."
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-200 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm transition-all resize-none"
                />
              )}

              {ingestMode === 'file' && (
                <div className="relative border-2 border-dashed border-gray-200 rounded-lg px-4 py-8 text-center hover:bg-gray-50 transition-colors cursor-pointer"
                  onClick={() => document.getElementById('file-upload')?.click()}>
                  <input
                    id="file-upload"
                    type="file"
                    accept=".pdf"
                    className="hidden"
                    onChange={(e) => setFileSource(e.target.files?.[0] || null)}
                  />
                  <Upload className="w-6 h-6 mx-auto text-gray-400 mb-2" />
                  <p className="text-xs text-gray-500 truncate px-2">{fileSource ? fileSource.name : "Click to upload PDF"}</p>
                </div>
              )}

              <button
                onClick={handleIngest}
                disabled={isIngestDisabled()}
                className="w-full flex items-center justify-center gap-2 bg-gray-900 text-white py-2 rounded-lg hover:bg-black transition-colors disabled:opacity-50 text-sm font-medium"
              >
                {ingesting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
                {ingesting ? 'Ingesting...' : 'Ingest'}
              </button>

              {ingestStatus === 'success' && (
                <div className="flex items-center gap-2 text-green-600 text-xs font-medium animate-in fade-in slide-in-from-top-1">
                  <CheckCircle className="w-3 h-3" /> Successfully Added
                </div>
              )}
              {ingestStatus === 'error' && (
                <div className="flex items-center gap-2 text-red-600 text-xs font-medium animate-in fade-in slide-in-from-top-1">
                  <AlertCircle className="w-3 h-3" /> Failed to ingest
                </div>
              )}
            </div>
          </div>
        </aside>

        {/* Main Chat Area */}
        <section className="lg:col-span-3 flex flex-col h-[calc(100vh-10rem)] bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 scroll-smooth">
            {messages.length === 0 && (
              <div className="flex flex-col items-center justify-center h-full text-center text-gray-400 space-y-4">
                <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center">
                  <BookOpen className="w-8 h-8 text-blue-500" />
                </div>
                <div>
                  <h3 className="text-lg font-medium text-gray-900">Ready to Research</h3>
                  <p className="text-sm mt-1">Ingest a URL, PDF, or Text to get started.</p>
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[85%] rounded-2xl p-4 ${msg.role === 'user'
                    ? 'bg-blue-600 text-white rounded-br-none'
                    : 'bg-gray-100 text-gray-800 rounded-bl-none'
                  }`}>
                  <div className="prose prose-sm max-w-none">
                    {msg.role === 'assistant' ? <ReactMarkdown>{msg.content}</ReactMarkdown> : msg.content}
                  </div>

                  {msg.confidence !== undefined && (
                    <div className="mt-3 pt-3 border-t border-black/10 flex items-center justify-between text-xs opacity-70">
                      <span>Confidence: {(msg.confidence * 100).toFixed(0)}%</span>
                      {msg.sources && msg.sources.length > 0 && <span>{msg.sources.length} Sources</span>}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="flex justify-start">
                <div className="bg-gray-50 text-gray-500 rounded-2xl rounded-bl-none p-4 flex items-center gap-2">
                  <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                  <span className="text-sm font-medium">Researching...</span>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-4 border-t border-gray-100 bg-white">
            <div className="relative flex items-center gap-2">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleResearch()}
                placeholder="Ask a question based on your documents..."
                className="w-full pl-4 pr-12 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 outline-none transition-all shadow-sm"
              />
              <button
                onClick={handleResearch}
                disabled={loading || !query}
                className="absolute right-2 p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </section>

      </main>
    </div>
  );
}

export default App;
