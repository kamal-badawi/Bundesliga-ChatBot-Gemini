import React, { useState } from 'react';

interface BottomSectionProps {
  question: string;
  setQuestion: React.Dispatch<React.SetStateAction<string>>;
  isMenuOpening: boolean;
  isAsking:boolean;
  setIsAsking: React.Dispatch<React.SetStateAction<boolean>>;
}

const BottomSection: React.FC<BottomSectionProps> = ({
  question,
  setQuestion,
  isMenuOpening,
  isAsking,
  setIsAsking,
}) => {
  const [questionValue, setQuestionValue] = useState('');

  // Wenn diese Methode aufgerufen wird
  // Hier wird setAsking auf True gesetzt
  // Hier wird setQuestion auf den Frage-Inhalt gesetzt
  const handleSend = () => {
      const trimmed = questionValue.trim();
      if (!trimmed) return;
      if (trimmed === question) {
        setIsAsking(false); 
        setTimeout(() => setIsAsking(true), 0);
      } else {
        setQuestion(trimmed);
        setIsAsking(true);
      }

      setQuestionValue('');
    };
  

  // Wenn man Enter drückt, soll handleSend ausgeführt werden, sowie wenn man auf den Senden Button klickt
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSend();
    }
  };


  // Wichtiger Hinweis: Das Stylen wurde mit GPT und Deepseek verbessert
  return (
    <div
      className={`fixed bottom-0 z-50 px-4 py-3 border-t border-gray-300 bg-white transition-all duration-300 ${
        isMenuOpening ? 'w-[75%] left-[25%]' : 'w-full left-0'
      }`}
    >
      <div className="relative flex items-center">
        {/* Search Icon */}
        <span className="absolute inset-y-0 left-3 flex items-center text-gray-400">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="size-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"
            />
          </svg>
        </span>

        {/* Input Field */}
        <input
          type="text"
          placeholder="Stelle eine Frage an Bundesliga-ChatBot..."
          value={questionValue}
          onChange={(e) => setQuestionValue(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full pl-10 pr-12 py-2 rounded-lg bg-gray-100 text-black placeholder-gray-400 border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#5C67F2] transition"
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={!questionValue.trim() || isAsking}
          className={`absolute right-2 p-1 transition ${
            questionValue.trim()
              ? 'text-gray-600 hover:text-black'
              : 'text-gray-300 cursor-not-allowed'
          }`}
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth="1.5"
            stroke="currentColor"
            className="size-6"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 12 3.269 3.125A59.769 59.769 0 0 1 21.485 12 59.768 59.768 0 0 1 3.27 20.875L5.999 12Zm0 0h7.5"
            />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default BottomSection;
