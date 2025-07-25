// WIchtiger Hinweis: Das Stylen wurde mit GPT und DeepSeek verbessert
import React, { useCallback } from 'react';

interface TopSectionProps {
  isMenuOpening: boolean;
  setIsMenuOpening: React.Dispatch<React.SetStateAction<boolean>>;
  setIsNewChatOpened: React.Dispatch<React.SetStateAction<boolean>>;
}

const TopSection: React.FC<TopSectionProps> = ({  isMenuOpening, setIsMenuOpening,setIsNewChatOpened}) => {
  
  const openCloseMenu = () => {
    if (isMenuOpening) {
      setIsMenuOpening(false);
      
    } else {
      setIsMenuOpening(true);  
    }
   
  };
  
 
  const openNewConversation = useCallback(() => {
    setIsNewChatOpened(true);
  }, [setIsNewChatOpened]);

  return(

  <div className={' flex flex-row justify-between items-center bg-yellow-50 p-5 border-b-2 border-black'}>
      
      
      {/* Hier ist der Button, um die linke Leiste (Unterhaltungen) auf- und zuzumachen */}
      <div className="flex items-start p-5">
        <button
          onClick={openCloseMenu}
          className="transition-transform duration-200 ease-in-out hover:scale-110 active:scale-95 text-gray-700 hover:text-blue-500"
        >
        {isMenuOpening ? (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={0.5}
            stroke="currentColor"
            className="size-12"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M6 18 18 6M6 6l12 12"
            />
          </svg>
        ) : (
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            strokeWidth={0.5}
            stroke="currentColor"
            className="size-12"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12"
            />
          </svg>
        )}
      </button>
    </div>

       
    
    
    {/* Hier ist der Name der App */}
    <div className="flex flex-col justify-between items-start italic font-extrabold ">
      <img src='https://i.postimg.cc/8c0p84hL/Logo-without-BG.png' alt='Bundesliga-ChatBot' className='h-24'/>
    </div>
    
    
    {/* Hier ist der Button, um eine neue Unterhaltung zu starten*/}
    <div >
    <button onClick={()=>{openNewConversation()}} >
    <svg xmlns="http://www.w3.org/2000/svg"
     fill="none"
      viewBox="0 0 24 24"
       strokeWidth="1.5"
        stroke="currentColor"
         className="size-12">
     <path strokeLinecap="round"
      strokeLinejoin="round"
        d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z" />
    </svg>
    </button>
  </div>
  </div>
  
  );

}
export default TopSection;