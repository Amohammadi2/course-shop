'use client';

import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import useChat from '@/hooks/useChat';
import api from '@/services/api';

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [ticketId, setTicketId] = useState<string | null>(null);
  const { messages, sendMessage } = useChat(ticketId || '');
  const [newMessage, setNewMessage] = useState('');

  const createTicket = async () => {
    try {
      const response = await api.post('/chat/tickets/create/');
      setTicketId(response.data.id);
    } catch (error) {
      console.error('Failed to create ticket:', error);
    }
  };

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      sendMessage(newMessage);
      setNewMessage('');
    }
  };

  return (
    <>
      <div className="fixed bottom-4 right-4">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="rounded-full bg-indigo-600 p-4 text-white shadow-lg transition-transform hover:scale-110"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8"
            fill="none"
            viewBox="0 0 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
            />
          </svg>
        </button>
      </div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
            className="fixed bottom-20 right-4 h-[500px] w-96 rounded-lg bg-white shadow-xl"
          >
            <div className="flex h-full flex-col">
              <div className="rounded-t-lg bg-indigo-600 p-4 text-white">
                <h3 className="text-lg font-bold">Support Chat</h3>
              </div>
              <div className="flex-grow space-y-4 overflow-y-auto p-4">
                {ticketId ? (
                  messages.map((msg, index) => (
                    <div key={index} className="flex flex-col">
                      <span className="font-bold">{msg.sender}</span>
                      <span className="text-gray-600">{msg.message}</span>
                      <span className="text-xs text-gray-400">
                        {new Date(msg.timestamp).toLocaleTimeString()}
                      </span>
                    </div>
                  ))
                ) : (
                  <div className="flex h-full items-center justify-center">
                    <button
                      onClick={createTicket}
                      className="rounded-md bg-indigo-600 px-4 py-2 text-white"
                    >
                      Start a new chat
                    </button>
                  </div>
                )}
              </div>
              {ticketId && (
                <div className="flex border-t p-4">
                  <input
                    type="text"
                    placeholder="Type a message..."
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyPress={(e) =>
                      e.key === 'Enter' && handleSendMessage()
                    }
                    className="w-full rounded-md border p-2"
                  />
                  <button
                    onClick={handleSendMessage}
                    className="ml-2 rounded-md bg-indigo-600 px-4 py-2 text-white"
                  >
                    Send
                  </button>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default ChatWidget;
