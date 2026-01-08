'use client';

import { useState, useEffect } from 'react';
import io, { Socket } from 'socket.io-client';

interface Message {
  message: string;
  sender: string;
  timestamp: string;
}

const useChat = (ticketId: string) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [socket, setSocket] = useState<Socket | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && ticketId) {
      const newSocket = io(
        `${process.env.NEXT_PUBLIC_WEBSOCKET_URL}/chat/${ticketId}/?token=${token}`
      );

      newSocket.on('connect', () => {
        console.log('Connected to chat server');
      });

      newSocket.on('disconnect', () => {
        console.log('Disconnected from chat server');
      });

      newSocket.on('chat_message', (message: Message) => {
        setMessages((prevMessages) => [...prevMessages, message]);
      });

      setSocket(newSocket);

      return () => {
        newSocket.disconnect();
      };
    }
  }, [ticketId]);

  const sendMessage = (message: string) => {
    if (socket) {
      socket.emit('chat_message', { message });
    }
  };

  return { messages, sendMessage };
};

export default useChat;
