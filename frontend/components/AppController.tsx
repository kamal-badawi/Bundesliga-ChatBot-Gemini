// Diese Komponente Kontrolliert die ganze APP
import React, { useState } from 'react';
import TopSection from './TopSection';
import MiddleSection from './MiddleSection';
import BottomSection from './BottomSection';
import ChatHistorySection from './ChatHistorySection';

 export interface Conversation {
    question: string;
    answer: string;
    date: string;
    time: string;
  }



// Da wir keine Register und Login Maske haben, nutzen wir die Daten vom folgenden Nutzer
const AppController = () => {
  const currentUser = {
    userId :'fan_1',
    emailAddress :'kamal.badawi@gmx.de',

  }

 
   // Unterhaltungen.
  const [conversations, setConversations] = useState<Conversation[]>([]);

  
  // conversationId wird genutzt um eine Unterhaltung zu löschen, per Mail zu schicken, lokal herunterzuladen
  // Bei neuen Unterhaltungen wird automatisch eine conversationId erstellt 
  const [conversationId, setConversationId] = useState("");

  // isMenuOpening wird genutzt um die Side-BAr zu öffnen oder zu schließen
  const [isMenuOpening, setIsMenuOpening] = useState(false);

  // isNewChat wird genutzt um eine bestehende Unterhaltung zuzugreifen oder ggf. eine neue Unterhaltung zu erstellen
  const [isNewChat, setIsNewChat] = useState(true);

  // isAsking wird genutzt, um zu wissen, ob man gerade auf eine Antwort von Gemini wartet
  const [isAsking, setIsAsking] = useState(false);

  // lastQuestionAndAnswer speichert die letzte Frage und Antwort
  const [lastQuestionAndAnswer, setLastQuestionAndAnswer] = useState<{question: string, answer: string} | null>(null);
  
  // question speichert die aktuelle Frage
  const [question, setQuestion] = useState("");

  // gibt an, ob die erste Frage gefragt wurde.
  const [firstQuestionAsked, setFirstQuestionAsked] = useState(false);

  // gibt an, ob den Button (New Chat) geklickt wurde.
  const [isNewChatOpened, setIsNewChatOpened] = useState(false);

 

  // Wichtiger Hinweis: Das Stylen wurde mit GPT und Deepseek verbessert
  return (
  <div className="flex h-screen">
    {/* Sidebar */}
    <div
      className={`transition-all duration-300 ${
        isMenuOpening ? 'w-1/4 p-4' : 'w-0 p-0'
      } bg-yellow-50 border-r-2 border-black overflow-y-auto`}
    >
      {isMenuOpening && (
        <ChatHistorySection
          isNewChat={isNewChat}
          setIsNewChat={setIsNewChat} 
          userId={currentUser.userId}
          conversationId={conversationId}
          setConversationId={setConversationId}
          firstQuestionAsked={firstQuestionAsked}
          email_address={currentUser.emailAddress}
          setFirstQuestionAsked={setFirstQuestionAsked}
          setConversations={setConversations}
          setLastQuestionAndAnswer={setLastQuestionAndAnswer}
          
        />
      )}
    </div>

    {/* Hauptbereich */}
    <div className="flex-1 flex flex-col overflow-hidden relative">
      {/* Der obere Bereich */}
      <div className="w-full bg-yellow-50 border-b-2 border-black">
        <TopSection
          isMenuOpening={isMenuOpening}
          setIsMenuOpening={setIsMenuOpening}
          setIsNewChatOpened={setIsNewChatOpened}
        />
      </div>

      {/* Der Unterhaltungs- und Sendebereich*/}
      <div className="flex-1 overflow-y-auto">
        <MiddleSection 
        isNewChat={isNewChat}
        setIsNewChat={setIsNewChat}
        userId={currentUser.userId}
        conversationId={conversationId}
        setConversationId={setConversationId}
        question={question} 
        setQuestion ={setQuestion}
        lastQuestionAndAnswer={lastQuestionAndAnswer}
        setLastQuestionAndAnswer={setLastQuestionAndAnswer}
        isAsking={isAsking}
        setIsAsking={setIsAsking}
        setFirstQuestionAsked={setFirstQuestionAsked}
        isNewChatOpened={isNewChatOpened}
        setIsNewChatOpened={setIsNewChatOpened}
        conversations={conversations}
        setConversations={setConversations} />

        <BottomSection
          question={question} 
          setQuestion={setQuestion} 
          isMenuOpening={isMenuOpening} 
          isAsking={isAsking} 
          setIsAsking={setIsAsking} />
      </div>

     
    </div>
  </div>
);

};

export default AppController;