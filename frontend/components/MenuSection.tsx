import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { parse, differenceInCalendarDays, compareDesc } from 'date-fns';
import type {Conversation} from './AppController';

interface ConversationInfo {
  conversation_id: string;
  title: string;
  date: string;
  time: string;
}

interface MenuSectionProps {
  isNewChat: boolean;
  setIsNewChat: React.Dispatch<React.SetStateAction<boolean>>;
  userId: string;
  conversationId: string;
  setConversationId: React.Dispatch<React.SetStateAction<string>>;
  email_address: string;
  firstQuestionAsked: boolean;
  setFirstQuestionAsked: React.Dispatch<React.SetStateAction<boolean>>;
  setConversations: React.Dispatch<React.SetStateAction<Conversation[]>>;
  
}

interface GroupedConversations {
  [label: string]: ConversationInfo[];
}

const MenuSection: React.FC<MenuSectionProps> = ({
  isNewChat,
  setIsNewChat,
  userId,
  conversationId,
  setConversationId,
  email_address,
  firstQuestionAsked,
  setFirstQuestionAsked,
  setConversations,
  
}) => {
  const [notification, setNotification] = useState<{
    type: 'success' | 'error' | 'info';
    message: string;
  } | null>(null);

  const [conversationsInfo, setConversationsInfo] = useState<ConversationInfo[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const fetchConversationsInfos = async () => {
    setIsLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/conversations_info', {
        user_id: userId,
      });

      const data = Array.isArray(response.data?.conversations)
        ? response.data.conversations
        : [];

      const formattedConversations = data.map((conv: any) => ({
        conversation_id: String(conv.conversation_id || ''),
        title: String(conv.title || 'Ohne Namen'),
        date: String(conv.date || ''),
        time: String(conv.time || ''),
      }));

      setConversationsInfo(formattedConversations);
    } catch (error) {
      console.error('Gespräche konnten nicht geladen werden:', error);
      setNotification({
        type: 'error',
        message: 'Gespräche konnten nicht geladen werden',
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    
    fetchConversationsInfos();
    
  }, [firstQuestionAsked]);

  const handleConversationAction = async (
    action: 'download' | 'send' | 'delete',
    conversation_id: string,
    title: string = ''
  ) => {
    try {
      switch (action) {
        case 'download':
          const downloadRes = await axios.post(
            'http://localhost:8000/download_conversation',
            { conversation_id },
            { responseType: 'blob' }
          );
          const blob = new Blob([downloadRes.data], { type: 'application/pdf' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = title ? `${title}.pdf` : `conversation_${conversation_id}.pdf`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);

          setNotification({ type: 'success', message: 'Unterhaltung wurde als PDF-Datei heruntergeladen' });
          break;

        case 'send':
          await axios.post('http://localhost:8000/send_conversation', {
            email_address,
            conversation_id,
          });
          setNotification({ type: 'success', message: `Unterhaltung wurde als PDF-Datei an ${email_address} gesendet` });
          break;

        case 'delete':
          await axios.delete('http://localhost:8000/delete_conversation_by_conversation_id', {
            data: { conversation_id },
          });
          console.log('Current id: ',conversationId);
          console.log('delete id: ',conversation_id);
          if (conversationId === conversation_id){
            setFirstQuestionAsked(false);
            setConversationId('');
            setIsNewChat(true);
            setConversations([]);
          }
          setConversationsInfo((prev) =>
            prev.filter((c) => c.conversation_id !== conversation_id)
          );
          
           setNotification({ type: 'success', message: `Unterhaltung wurde gelöscht` });
          break;
      }
    } catch (error) {
      console.error(`Fehler bei der Aktion ${action}:`, error);
      setNotification({
        type: 'error',
        message: `Fehler beim ${action}`,
      });
    }
  };

  useEffect(() => {
    if (notification) {
      const timer = setTimeout(() => setNotification(null), 3000);
      return () => clearTimeout(timer);
    }
  }, [notification]);

  const groupConversationsByDate = (convs: ConversationInfo[]): GroupedConversations => {
    const now = new Date();
    const grouped: GroupedConversations = {};

    const sorted = [...convs].sort((a, b) => {
      const dateA = parse(`${a.date} ${a.time}`, 'dd-MM-yyyy HH:mm:ss', new Date());
      const dateB = parse(`${b.date} ${b.time}`, 'dd-MM-yyyy HH:mm:ss', new Date());
      return compareDesc(dateA, dateB); // neueste zuerst
    });

    sorted.forEach((conv) => {
      const parsedDate = parse(`${conv.date} ${conv.time}`, 'dd-MM-yyyy HH:mm:ss', new Date());
      const daysAgo = differenceInCalendarDays(now, parsedDate);

      let label = '';
      if (daysAgo === 0) label = 'Heute';
      else if (daysAgo === 1) label = 'Gestern';
      else if (daysAgo <= 6) label = `vor ${daysAgo} Tagen`;
      else if (daysAgo <= 13) label = 'vor 1 Woche';
      else if (daysAgo <= 20) label = 'vor 2 Wochen';
      else if (daysAgo <= 27) label = 'vor 3 Wochen';
      else if (daysAgo <= 34) label = 'vor 4 Wochen';
      else if (daysAgo <= 60) label = 'vor 1 Monat';
      else if (daysAgo <= 90) label = 'vor 2 Monaten';
      else if (daysAgo <= 120) label = 'vor 3 Monaten';
      else label = `vor ${Math.floor(daysAgo / 30)} Monaten`;

      if (!grouped[label]) grouped[label] = [];
      grouped[label].push(conv);
    });

    return grouped;
  };

  const filteredConversations = conversationsInfo.filter((conv) =>
    conv.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const groupedConvs = groupConversationsByDate(filteredConversations);

  return (
    <div className="w-full h-full bg-yellow-50 flex flex-col overflow-hidden">
      {/* Suchfeld */}
      <div className="p-4 border-b border-gray-200">
        <input
          type="text"
          placeholder="Gespräche durchsuchen..."
          className="block w-full pl-3 pr-3 py-2 border border-gray-300 rounded-lg bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Gesprächsliste */}
      <div className="flex-1 overflow-y-auto">
        {isLoading ? (
          <div className="flex justify-center items-center h-full">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-blue-500"></div>
          </div>
        ) : Object.keys(groupedConvs).length === 0 ? (
          <div className="flex justify-center items-center h-full text-gray-500">
            Keine Gespräche gefunden
          </div>
        ) : (
          Object.entries(groupedConvs).map(([groupLabel, items]) => (
            <div key={groupLabel}>
              <h3 className="px-4 pt-4 pb-2 text-sm font bg-blue-50 semibold text-gray-700">{groupLabel}</h3>
              <ul className="divide-y divide-gray-200">
                {items.map((conv) => (
                  <li
                    key={conv.conversation_id}
                    className="px-4 py-3 hover:bg-gray-100 transition-colors cursor-pointer group"
                    onClick={() => {
                      setConversationId(conv.conversation_id);
                      setIsNewChat(false);
                    }}
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {conv.title}
                      </p>
                      <div className="ml-2 flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        {/* Send */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleConversationAction('send', conv.conversation_id);
                          }}
                          title="Per E-Mail senden"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg"
                           fill="none" viewBox="0 0 24 24"
                            strokeWidth="1.5"
                             stroke="green"
                              className="size-6">
                                <path strokeLinecap="round"
                                 strokeLinejoin="round"
                                  d="M21.75 6.75v10.5a2.25 2.25 0 0 1-2.25 2.25h-15a2.25 2.25 0 0 1-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0 0 19.5 4.5h-15a2.25 2.25 0 0 0-2.25 2.25m19.5 0v.243a2.25 2.25 0 0 1-1.07 1.916l-7.5 4.615a2.25 2.25 0 0 1-2.36 0L3.32 8.91a2.25 2.25 0 0 1-1.07-1.916V6.75" />
                            </svg>
                        </button>
                        {/* Download */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleConversationAction('download', conv.conversation_id, conv.title);
                          }}
                          title="Herunterladen"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg"
                           fill="none" viewBox="0 0 24 24"
                            strokeWidth="1.5"
                             stroke="gray"
                              className="size-6">
                                <path strokeLinecap="round"
                                 strokeLinejoin="round"
                                  d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5M16.5 12 12 16.5m0 0L7.5 12m4.5 4.5V3" />
                            </svg>
                        </button>
                        {/* Delete */}
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            if (window.confirm('Gespräch wirklich löschen?')) {
                              handleConversationAction('delete', conv.conversation_id);
                            }
                          }}
                          title="Löschen"
                        >
                          <svg xmlns="http://www.w3.org/2000/svg"
                           fill="none" viewBox="0 0 24 24"
                            strokeWidth="1.5"
                             stroke="red"
                              className="size-6">
                                <path strokeLinecap="round"
                                 strokeLinejoin="round"
                                  d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
                            </svg>

                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          ))
        )}
      </div>

      {/* Notification */}
      {notification && (
        <div
          className={`p-3 m-4 rounded-lg text-sm ${
            notification.type === 'success'
              ? 'bg-green-100 text-green-800'
              : notification.type === 'error'
              ? 'bg-red-100 text-red-800'
              : 'bg-blue-100 text-blue-800'
          }`}
        >
          {notification.message}
        </div>
      )}
    </div>
  );
};

export default MenuSection;
