// Diese Komponenete wurde zu einem großen Teil mit GPT erzeugt, wurde jedoch an unseren Bedarf angepasst (mit Icons und Text und Reaktion-Art)
// Diese Komponenete wird genutzt, um einen Antwort-Text zu kopieren
import React, { useState } from 'react';
const CopyText = ({ text }) => {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      console.error('Kopieren ist nicht möglich!');
    }
  };

  return (
    <button className='pl-2' onClick={copyToClipboard} title="Antwort kopieren" style={{ position: 'relative' }}>
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
          d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75"
        />
      </svg>
            {copied && (
              <span className="absolute -top-6 right-0 text-black font-bold text-sm select-none">
                <svg xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth="1.5"
                  stroke="currentColor" 
                  className="size-6">
                <path strokeLinecap="round" 
                  strokeLinejoin="round" 
                 d="m4.5 12.75 6 6 9-13.5" />
              </svg>
        </span>
      )}
    </button>
  );
};

export default CopyText;
