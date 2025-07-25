// Diese Komponenete wurde zu einem großen Teil mit GPT erzeugt, wurde jedoch an unseren Bedarf angepasst (mit Icons und Text und Reaktion-Art)
// Diese Komponenete wird genutzt, ein Warte-Effekt beim Warten auf die Antwort zu erzeugen

import { useEffect, useState } from "react";

export default function ThinkingBlock() {
  const [dotCount, setDotCount] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setDotCount((prev) => (prev + 1) % 4); 
    }, 500); 

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-gray-100 text-gray-800 p-4 rounded-2xl w-fit max-w-[80%] ml-4 flex items-center">
      {/* Textbereich */}
      <p className="font-medium text-base mr-3 whitespace-nowrap">
        Bundesliga-ChatBot denkt
      </p>

      {/* Denk-Punkte mit Animation */}
      <div className="flex space-x-1.5 items-center h-6">
        {[1, 2, 3].map((i) => (
          <span
            key={i}
            className={`w-2 h-2 bg-orange-500 rounded-full transition-all duration-300 ${
              i <= dotCount ? "opacity-100" : "opacity-40 scale-90"
            }`}
          />
        ))}
      </div>
    </div>
  );
}