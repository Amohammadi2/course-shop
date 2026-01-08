'use client';

import { useState, useEffect } from 'react';
import api from '@/services/api';
import useChat from '@/hooks/useChat';

interface Ticket {
  id: number;
  user: string;
  category: string;
}

const AdminChatDashboard = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const { messages, sendMessage } = useChat(selectedTicket?.id.toString() || '');
  const [newMessage, setNewMessage] = useState('');

  useEffect(() => {
    const fetchTickets = async () => {
      try {
        const response = await api.get('/chat/tickets/');
        setTickets(response.data);
      } catch (error) {
        console.error('Failed to fetch tickets:', error);
      }
    };
    fetchTickets();
  }, []);

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      sendMessage(newMessage);
      setNewMessage('');
    }
  };

  return (
    <div className="flex h-screen">
      <div className="w-1/3 border-r">
        <h2 className="p-4 text-xl font-bold">Chat Tickets</h2>
        <ul>
          {tickets.map((ticket) => (
            <li
              key={ticket.id}
              onClick={() => setSelectedTicket(ticket)}
              className={`cursor-pointer p-4 hover:bg-gray-100 ${
                selectedTicket?.id === ticket.id ? 'bg-gray-200' : ''
              }`}
            >
              <p className="font-bold">{ticket.user}</p>
              <p className="text-sm text-gray-600">{ticket.category}</p>
            </li>
          ))}
        </ul>
      </div>
      <div className="flex w-2/3 flex-col">
        {selectedTicket ? (
          <>
            <div className="border-b p-4">
              <h3 className="text-lg font-bold">
                Chat with {selectedTicket.user}
              </h3>
            </div>
            <div className="flex-grow space-y-4 overflow-y-auto p-4">
              {messages.map((msg, index) => (
                <div key={index} className="flex flex-col">
                  <span className="font-bold">{msg.sender}</span>
                  <span className="text-gray-600">{msg.message}</span>
                  <span className="text-xs text-gray-400">
                    {new Date(msg.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
            <div className="flex border-t p-4">
              <input
                type="text"
                placeholder="Type a message..."
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                className="w-full rounded-md border p-2"
              />
              <button
                onClick={handleSendMessage}
                className="ml-2 rounded-md bg-indigo-600 px-4 py-2 text-white"
              >
                Send
              </button>
            </div>
          </>
        ) : (
          <div className="flex h-full items-center justify-center">
            <p>Select a ticket to start chatting</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminChatDashboard;
