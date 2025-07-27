import React, { useEffect, useRef, useState, useCallback } from 'react';
import axios from 'axios';
import TextToSpeech from './TextToSpeech';
import ThinkingBlock from './ThinkingBlock';
import CopyText from './CopyText';
import type {Conversation} from './AppController';



interface MiddleSectionProps {
  isNewChat: boolean;
  setIsNewChat: React.Dispatch<React.SetStateAction<boolean>>;
  userId: string;
  conversationId: string;
  setConversationId: React.Dispatch<React.SetStateAction<string>>;
  question: string;
  setQuestion: React.Dispatch<React.SetStateAction<string>>;
  lastQuestionAndAnswer: {question: string, answer: string} | null;
  setLastQuestionAndAnswer: React.Dispatch<React.SetStateAction<{question: string, answer: string} | null>>;
  isAsking: boolean;
  setIsAsking: React.Dispatch<React.SetStateAction<boolean>>;
  setFirstQuestionAsked: React.Dispatch<React.SetStateAction<boolean>>;
  isNewChatOpened: boolean;
  setIsNewChatOpened: React.Dispatch<React.SetStateAction<boolean>>;
  conversations: Conversation[];
  setConversations: React.Dispatch<React.SetStateAction<Conversation[]>>;
}


const MiddleSection: React.FC<MiddleSectionProps> = ({
  isNewChat,
  setIsNewChat,
  userId,
  conversationId,
  setConversationId,
  question,
  setQuestion,
  lastQuestionAndAnswer,
  setLastQuestionAndAnswer,
  isAsking,
  setIsAsking,
  setFirstQuestionAsked,
  isNewChatOpened,
  setIsNewChatOpened,
  conversations,
  setConversations,
}) => {
  
  const [error, setError] = useState<string | null>(null);
  
  const lastQuestion = lastQuestionAndAnswer?.question || ''
  const lastAnswer = lastQuestionAndAnswer?.answer || ''
  const bottomRef = useRef<HTMLDivElement>(null);
  const isProcessingRef = useRef(false);

  
  

  // Hilfsfunktionen
  const pad = useCallback((num: number): string => num.toString().padStart(2, '0'), []);
  const getCurrentDate = useCallback((): string => {
    const now = new Date();
    return `${pad(now.getDate())}-${pad(now.getMonth() + 1)}-${now.getFullYear()}`;
  }, [pad]);

  const getCurrentTime = useCallback((): string => {
    const now = new Date();
    return `${pad(now.getHours())}:${pad(now.getMinutes())}:00`;
  }, [pad]);

  const formatDate = (date: string) =>
    new Date(date.split('-').reverse().join('-')).toLocaleDateString('de-DE', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
    });

  const formatTime = (time: string) => {
    const [hours, minutes] = time.split(':');
    return `${hours}:${minutes} Uhr`;
  };

  const scrollToBottom = () => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const createConversation = async (userId: string): Promise<string> => {
    try {
      const response = await axios.post('http://localhost:8000/create_conversation', { user_id: userId });
      return response.data.conversation_id;
    } catch (err) {
      console.error('Fehler beim Erstellen der Konversation:', err);
      setError('Konversation konnte nicht erstellt werden');
      throw err;
    }
  };

  const createConversationTitle = async (
    userId: string,
    conversationId: string,
    qaPairs: { question: string; answer: string }[]
  ) => {
    try {
      const response = await axios.post('http://localhost:8000/add_dialog_title', {
        user_id: userId,
        conversation_id: conversationId,
        questions_and_answers: qaPairs,
      });
      if (response.status === 200) {
        setFirstQuestionAsked(true);
      }
    } catch (err) {
      console.error('Fehler beim Erstellen des Titels:', err);
      setError('Konversationstitel konnte nicht erstellt werden');
    }
  };

  const addDialogItem = async (
    userId: string,
    conversationId: string,
    question: string,
    answer: string
  ) => {
    try {
      await axios.post('http://localhost:8000/add_dialog_item', {
        user_id: userId,
        conversation_id: conversationId,
        question,
        answer,
        date: getCurrentDate(),
        time: getCurrentTime(),
      });
    } catch (err) {
      console.error('Fehler beim Hinzufügen des Dialogs:', err);
    }
  };

  const fetchConversationDialog = async () => {
    if (isNewChat || !conversationId) return;
    try {
      const response = await axios.post(`http://localhost:8000/conversations_dialogs/${conversationId}`);
      const dialogs = response.data?.conversations_dialogs ?? [];

      const formatted = dialogs.map((d: any) => ({
        question: d.question || '',
        answer: d.answer || '',
        date: d.date || '',
        time: d.time || '',
      }));

      setConversations(prev => (JSON.stringify(prev) !== JSON.stringify(formatted) ? formatted : prev));
    } catch (err) {
      console.error('Fehler beim Laden der Konversation:', err);
      setError('Gespräch konnte nicht geladen werden');
    }
  };

  const getAnswer = async (question: string, lastQuestion: string, lastAnswer: string): Promise<string> => {
    try {
      const response = await axios.post('http://localhost:8000/question', { question: question, last_question: lastQuestion, last_answer:lastAnswer});
      return response.data.answer;
    } catch (err) {
      console.error('Fehler beim Abrufen der Antwort:', err);
      setError('Antwort konnte nicht geladen werden');
      return 'Entschuldigung, ein Fehler ist aufgetreten.';
    }
  };

  useEffect(() => {
      setFirstQuestionAsked(false);
      setConversations([]);
      setConversationId('');
      setIsNewChat(true);
      setIsNewChatOpened(false);
      setLastQuestionAndAnswer(null)
    
  }, [isNewChatOpened]);

  useEffect(() => {
    if (!isNewChat && conversationId) {
      fetchConversationDialog();
    }
  }, [conversationId, isNewChat]);

  useEffect(() => {
    scrollToBottom();
  }, [conversations]);

  useEffect(() => {
    if (!isAsking || !question || isProcessingRef.current) return;

    const processQuestion = async () => {
      isProcessingRef.current = true;
      let currentConversationId = conversationId;

      try {
        if (isNewChat && !currentConversationId) {
          currentConversationId = await createConversation(userId);
          setConversationId(currentConversationId);
        }

        const newEntry: Conversation = {
          question,
          answer: '',
          date: getCurrentDate(),
          time: getCurrentTime(),
        };

        setConversations(prev => [...prev, newEntry]);

        const answer = await getAnswer(question=question, lastQuestion , lastAnswer);

        if (currentConversationId) {
          await addDialogItem(userId, currentConversationId, question, answer);

          if (isNewChat) {
            await createConversationTitle(userId, currentConversationId, [{ question, answer }]);
            setIsNewChat(false);
          }
        }

        setConversations(prev =>
          prev.map((item, index) =>
            index === prev.length - 1 ? { ...item, answer } : item
          )
        );
      } catch (err) {
        console.error('Fehler bei der Frageverarbeitung:', err);
        setConversations(prev =>
          prev.map((item, index) =>
            index === prev.length - 1 ? { ...item, answer: 'Fehler beim Antworten' } : item
          )
        );
      } finally {
        setIsAsking(false);
        setQuestion('');
        isProcessingRef.current = false;
      }
    };

    processQuestion();
  }, [isAsking, question]);

  // Letzte Frage und Antwort
  useEffect(() => {
  if (conversations.length > 0) {
    const last = conversations[conversations.length - 1];
    setLastQuestionAndAnswer({
      question: last.question,
      answer: last.answer
    });
  }
}, [conversations]);

  return (
    <div className="flex flex-col h-full overflow-y-auto px-4 pb-32 space-y-6">
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative">
          <span className="block sm:inline">{error}</span>
          <button
            onClick={() => setError(null)}
            className="absolute top-0 bottom-0 right-0 px-4 py-3"
          >
            <svg className="h-6 w-6 text-red-500" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      )}

      {conversations.map((item, index) => (
        <div key={index} className="space-y-4">
          {/* Frage */}
          <div className="flex justify-end">
            <div className="bg-emerald-100 text-gray-800 p-4 rounded-2xl max-w-[80%] lg:max-w-[60%]">
              <div className="flex items-start gap-3">
                <div className="flex-1">
                  <p className="text-left whitespace-pre-wrap">{item.question}</p>
                  <div className="text-xs text-gray-500 mt-2 text-right">
                    {formatDate(item.date)} um {formatTime(item.time)}
                  </div>
                </div>
                <div className="flex-shrink-0">
                  {/* Frage-Avatar */}
                  <svg width="40" height="40" viewBox="0 0 64 64" className="text-emerald-500">
                    <path
                      fill="currentColor"
                      d="M10.92,40.33h0c-.5,0-2.11-1.33-3-4.47s-.09-5.28.31-5.38c0,0,.73-1.47,3.1-1.15.88.12.14-1.78.29-2.63a9.83,9.83,0,0,0-.13-2.79,36.18,36.18,0,0,1-.21-8.79c.54-5.45,3.74-8.7,8.57-8.7a1.7,1.7,0,0,0,1-.34C23.24,4.32,27.92,3,31.79,3h1.71c10.35,0,17.83,5.29,20.9,14.64-1.18-.13-.78.69-1.62,1.5-.65.63-2.88,1.13-2.1,3.24a20.67,20.67,0,0,1,1.54,6.95c0,.61,3.06-.47,3.09-.47.41.14,1.16,3.83.31,7s-2.45,4.47-3,4.47A1.76,1.76,0,0,0,51,41.55C48.15,51.21,40.62,61,31.79,61S15.43,51.21,12.56,41.55A1.71,1.71,0,0,0,10.92,40.33Z"
                    />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* Antwort */}
          {item.answer ? (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 p-4 rounded-2xl max-w-[80%] lg:max-w-[60%]">
                <div className="flex items-start gap-3">
                  <div className="flex-shrink-0">
                    {/* Bot-Avatar */}
                    <svg width="40" height="40" viewBox="0 0 100 100" className="text-gray-500">
                      <path
                        fill="currentColor"
                        d="M50.2,8.56c-14.53,2.52-23.58,13.74-26.23,17.56c-1.12,1.6-1.19,3.37-1.16,5.38
                          c0.03,2.01,0.31,4.18,0.67,6.21c0.34,1.98,0.72,3.64,1.01,4.8c-0.31-0.02-0.63-0.03-0.94-0.02c-2.7,0.13-4.71,2.05-5.11,5.63
                          c-0.47,4.53,1.14,8.64,3.35,10.65c1.17,1.06,2.8,1.56,4.27,1.41c0.27-0.03,0.52-0.18,0.78-0.25c0.39,2.2,0.83,4.2,0.93,6.63
                          c0.09,1.43,0.57,3.24,1.4,5.26c0.83,2.02,2.11,4.28,3.74,6.39c3.3,4.34,8.51,8.28,15.5,8.13c6.34-0.14,11.51-3.65,15.16-7.59
                          c3.65-3.94,5.96-8.24,6.76-11.15c0.77-2.85,1.89-5.7,2.7-7.73c0.75,0.37,1.71,0.62,2.79,0.55c1.11-0.07,2.28-0.57,3.23-1.49
                          c1.16-1.12,1.8-2.54,2.44-4.41c0.64-1.87,1.16-4.03,1.48-6.03c0.31-2.01,0.49-3.94,0.31-5.72c-0.07-0.87-0.2-1.66-0.47-2.36
                          c-0.27-0.7-0.76-1.4-1.57-1.7c-0.78-0.29-1.5-0.45-2.17-0.52c1.17-5.8-1.25-10.18-3.31-12.88c0.79-0.2,1.45-0.26,2.42-0.65
                          c0.71-0.28,1.12-1.09,0.71-1.95c-1.39-2.9-3.84-4.64-5.88-5.79c0.49-0.45,0.9-0.73,1.48-1.42c0.62-0.75,0.32-1.89-0.35-2.65
                          C70.98,10.92,64.26,10.37,59.11,11.12c-2.61,0.38-4.92,1.06-6.52,1.64C52.47,11.97,52.4,11.22,52.1,10.06
                          C51.78,8.83,50.91,8.43,50.2,8.56z"
                      />
                    </svg>
                  </div>
                  <div className="flex-1">
                    <p className="whitespace-pre-wrap">{item.answer}</p>
                    <div className="flex justify-end gap-2 mt-2">
                      <TextToSpeech text={item.answer} />
                      <CopyText text={item.answer} />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <ThinkingBlock />
          )}
        </div>
      ))}

      <div ref={bottomRef} />
    </div>
  );
};

export default MiddleSection;
