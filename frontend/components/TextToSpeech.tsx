// Diese Komponenete wurde zu einem großen Teil mit GPT erzeugt, wurde jedoch an unseren Bedarf angepasst (mit Icons und Text und Reaktion-Art)
// Diese Komponenete wird genutzt, um einen Antwort-Text vorzulesen
import React from 'react';
const TextToSpeech = ({ text }) => {
  const speak = () => {
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.lang = 'de-DE'; 
      speechSynthesis.speak(utterance);
    } else {
      alert('Der Browser unterstützt das nicht.');
    }
  };

  return (
    <div>
      
      <button onClick={speak}>
        <svg xmlns="http://www.w3.org/2000/svg"
         fill="none"
          viewBox="0 0 24 24"
          strokeWidth="1.5"
            stroke="currentColor"
             className="size-6">
                <path strokeLinecap="round"
                 strokeLinejoin="round"
                  d="M19.114 5.636a9 9 0 0 1 0 12.728M16.463 8.288a5.25 5.25 0 0 1 0 7.424M6.75 8.25l4.72-4.72a.75.75 0 0 1 1.28.53v15.88a.75.75 0 0 1-1.28.53l-4.72-4.72H4.51c-.88 0-1.704-.507-1.938-1.354A9.009 9.009 0 0 1 2.25 12c0-.83.112-1.633.322-2.396C2.806 8.756 3.63 8.25 4.51 8.25H6.75Z" />
        </svg></button>
    </div>
  );
};

export default TextToSpeech;