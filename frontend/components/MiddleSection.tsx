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
  userName: string;
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
  userName,
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

       {/*Begrüßungsnachricht */}
      {conversations.length === 0 && (
        <div className="flex flex-col items-center justify-center h-full text-center p-4 text-gray-500">
         <svg 
            className='animate-wiggle'
            xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="100" height="100" viewBox="0 0 100 100">
            <path d="M 50.201172 8.5605469 A 2.0002 2.0002 0 0 0 49.824219 8.5898438 C 35.692692 11.076736 26.602337 22.300213 23.951172 26.09375 C 22.831824 27.692448 22.758479 29.512025 22.785156 31.5 C 22.811846 33.488891 23.090846 35.660359 23.441406 37.705078 C 23.7815 39.688752 24.191995 41.540179 24.527344 42.939453 C 24.199024 42.912446 23.858677 42.904929 23.509766 42.921875 C 22.142755 42.988265 20.458386 43.646323 19.46875 45.148438 C 18.479114 46.650551 18.182063 48.647269 18.439453 51.3125 C 18.928639 56.43511 20.342906 60.033928 22.644531 62.085938 C 23.795508 63.112088 25.290419 63.720827 26.798828 63.560547 C 27.062112 63.532567 27.283446 63.372944 27.535156 63.302734 C 27.928367 65.450071 28.390584 67.466116 28.542969 69.980469 A 2.0002 2.0002 0 0 0 28.544922 69.986328 C 28.634672 71.407953 29.124619 73.124156 29.986328 75.175781 C 30.848038 77.227407 32.096626 79.533024 33.779297 81.728516 C 37.144639 86.119499 42.419079 90.145943 49.480469 90 A 2.0002 2.0002 0 0 0 49.482422 90 C 55.81991 89.864559 60.982402 86.346414 64.662109 82.394531 C 68.340392 78.444179 70.631142 74.134669 71.402344 71.238281 L 71.402344 71.234375 C 72.185414 68.314411 73.27701 65.469231 74.091797 63.439453 C 74.835688 63.803641 75.784605 64.105457 76.878906 64.029297 C 77.973941 63.953087 79.149272 63.441695 80.095703 62.53125 A 2.0002 2.0002 0 0 0 80.099609 62.529297 C 81.229705 61.438021 81.85052 60.0225 82.472656 58.330078 C 83.094793 56.637657 83.602435 54.694691 83.931641 52.773438 C 84.260846 50.852184 84.419435 48.97428 84.257812 47.310547 C 84.177003 46.478681 84.025652 45.693955 83.669922 44.929688 C 83.314192 44.165419 82.656763 43.344826 81.654297 42.986328 A 2.0002 2.0002 0 0 0 81.652344 42.986328 C 81.04205 42.768305 80.450335 42.65085 79.876953 42.591797 C 81.067921 36.911208 78.681226 32.517579 76.632812 29.810547 C 77.42232 29.613371 78.017049 29.56413 79.039062 29.158203 A 2.0002 2.0002 0 0 0 80.138672 26.515625 C 78.789296 23.354858 76.419912 21.5653 74.400391 20.408203 C 74.911392 19.933734 75.297912 19.663525 75.941406 18.943359 A 2.0002 2.0002 0 0 0 75.917969 16.251953 C 70.976994 10.916152 64.257583 10.367439 59.105469 11.123047 C 56.50084 11.505041 54.227307 12.204302 52.591797 12.810547 C 52.472814 11.965333 52.407481 11.216091 52.105469 10.056641 A 2.0002 2.0002 0 0 0 50.201172 8.5605469 z M 48.607422 13.03125 C 48.862009 14.554118 48.916016 15.544922 48.916016 15.544922 A 2.0002 2.0002 0 0 0 51.818359 17.470703 C 51.818359 17.470703 52.697857 17.026216 54.134766 16.503906 L 51.607422 20.294922 A 1.0001 1.0001 0 1 0 53.271484 21.404297 L 57.052734 15.734375 A 1.0001 1.0001 0 0 0 57.128906 15.597656 C 57.930905 15.397842 58.779855 15.21486 59.685547 15.082031 C 59.855354 15.057127 60.029813 15.044489 60.201172 15.023438 L 57.591797 18.611328 A 1.0002939 1.0002939 0 1 0 59.208984 19.789062 L 62.359375 15.458984 A 1.0001 1.0001 0 0 0 62.558594 14.865234 C 63.931765 14.860779 65.318875 15.025041 66.681641 15.388672 L 64.083984 17.832031 A 1.0003547 1.0003547 0 1 0 65.455078 19.289062 L 68.808594 16.134766 C 69.712851 16.548906 70.59318 17.074516 71.433594 17.736328 C 71.159283 17.979984 70.717875 18.46047 70.529297 18.603516 C 70.023017 18.987555 69.992188 18.976563 69.992188 18.976562 A 2.0002 2.0002 0 0 0 70.072266 22.677734 C 70.072266 22.677734 73.066022 24.045886 75.056641 26.132812 C 74.765601 26.191382 74.235983 26.39171 74.021484 26.417969 C 73.287678 26.507799 73.166016 26.46875 73.166016 26.46875 A 2.0002 2.0002 0 0 0 71.611328 29.988281 C 71.611328 29.988281 77.929303 35.207485 75.730469 42.697266 A 2.0002 2.0002 0 0 0 75.650391 43.492188 C 75.436495 43.618385 75.216249 43.741866 75.035156 43.880859 C 73.622 44.965496 72.964844 46.337891 72.964844 46.337891 A 2.0002 2.0002 0 1 0 76.554688 48.101562 C 76.554688 48.101562 76.85136 47.530051 77.470703 47.054688 C 78.048031 46.611573 78.719788 46.315296 80.066406 46.720703 C 80.133646 46.892331 80.229771 47.207559 80.277344 47.697266 C 80.382596 48.78072 80.276576 50.41516 79.988281 52.097656 C 79.699987 53.780153 79.237786 55.531953 78.716797 56.949219 C 78.195808 58.366485 77.500218 59.476666 77.320312 59.650391 C 76.9558 59.999562 76.785235 60.02628 76.601562 60.039062 C 76.416911 60.051913 76.152293 59.996892 75.847656 59.847656 C 75.238383 59.549192 74.710938 58.990234 74.710938 58.990234 A 2.0002 2.0002 0 0 0 71.363281 59.507812 C 71.363281 59.507812 70.436923 61.6946 69.419922 64.455078 L 66.625 62.21875 A 1.0001 1.0001 0 0 0 65.978516 61.990234 A 1.0001 1.0001 0 0 0 65.375 63.78125 L 68.697266 66.439453 C 68.498717 67.021801 68.306506 67.616235 68.121094 68.210938 L 66.554688 67.167969 A 1.0001 1.0001 0 0 0 65.990234 66.992188 A 1.0001 1.0001 0 0 0 65.445312 68.832031 L 67.53125 70.222656 C 67.043798 72.034628 64.94063 76.226512 61.734375 79.669922 C 59.169287 82.42474 55.957205 84.741698 52.279297 85.621094 L 52.189453 81.916016 A 1.0001 1.0001 0 0 0 51.150391 80.925781 A 1.0001 1.0001 0 0 0 50.189453 81.964844 L 50.287109 85.951172 C 49.993623 85.977005 49.696936 85.993577 49.398438 86 C 48.175906 86.025267 47.028834 85.888603 45.947266 85.628906 L 47.0625 82.740234 A 1.0001 1.0001 0 0 0 46.087891 81.367188 A 1.0001 1.0001 0 0 0 45.197266 82.019531 L 44.041016 85.013672 C 42.540767 84.40184 41.201372 83.525461 39.992188 82.498047 L 41.642578 80.669922 A 1.0001 1.0001 0 0 0 40.929688 78.990234 A 1.0001 1.0001 0 0 0 40.158203 79.330078 L 38.537109 81.125 C 37.978814 80.538906 37.442208 79.933061 36.953125 79.294922 C 36.564877 78.788349 36.205782 78.270517 35.867188 77.75 L 37.410156 76.142578 A 1.0001 1.0001 0 0 0 36.650391 74.441406 A 1.0001 1.0001 0 0 0 35.96875 74.755859 L 34.810547 75.962891 C 34.373857 75.159206 33.98474 74.367196 33.673828 73.626953 C 33.423229 73.030308 33.232249 72.476 33.066406 71.955078 L 36.341797 69.726562 A 1.0001 1.0001 0 0 0 35.75 67.892578 A 1.0001 1.0001 0 0 0 35.216797 68.072266 L 32.558594 69.882812 C 32.554006 69.841599 32.539288 69.77225 32.537109 69.738281 C 32.280579 65.505528 31.333375 63.403091 31.054688 59.873047 A 2.0002 2.0002 0 0 0 27.494141 58.787109 C 26.994005 59.41691 26.621357 59.556061 26.376953 59.582031 C 26.13255 59.608001 25.826914 59.563461 25.306641 59.099609 C 24.266094 58.171912 22.852884 55.445912 22.421875 50.929688 A 2.0002 2.0002 0 0 0 22.419922 50.927734 C 22.212312 48.777965 22.563543 47.719606 22.808594 47.347656 C 23.053645 46.975707 23.191385 46.940871 23.703125 46.916016 C 24.726605 46.866306 26.505859 47.6875 26.505859 47.6875 A 2.0002 2.0002 0 0 0 29.488281 45.732422 C 30.251509 44.791567 31.631464 43.035257 33.177734 40.478516 C 34.214865 38.76363 35.191739 36.872352 35.783203 35.007812 C 36.094488 34.026514 36.302359 33.041956 36.333984 32.087891 C 38.073844 33.19162 40.836955 34.841823 44.179688 36.355469 C 49.605267 38.812263 56.256662 40.873138 61.232422 38.351562 C 65.52434 36.178992 67.879521 36.274435 69.083984 36.707031 C 70.288448 37.139627 70.480469 37.806641 70.480469 37.806641 A 1.0001 1.0001 0 1 0 72.339844 37.074219 C 72.339844 37.074219 71.652802 35.504123 69.759766 34.824219 C 68.432908 34.347664 66.565144 34.277753 64 35.064453 L 64 33 A 1.0001 1.0001 0 0 0 62.984375 31.986328 A 1.0001 1.0001 0 0 0 62 33 L 62 35.789062 C 61.4679 36.015556 60.911643 36.272982 60.328125 36.568359 C 60.222493 36.621891 60.109011 36.662682 60 36.710938 L 60 35 A 1.0001 1.0001 0 0 0 58.984375 33.986328 A 1.0001 1.0001 0 0 0 58 35 L 58 37.298828 C 57.014351 37.459539 55.948453 37.476709 54.837891 37.384766 L 55.986328 35.074219 A 1.0001 1.0001 0 0 0 55.042969 33.619141 A 1.0001 1.0001 0 0 0 54.195312 34.185547 L 52.753906 37.085938 C 51.453998 36.839528 50.12619 36.48301 48.804688 36.035156 L 51.492188 32.664062 A 1.0001 1.0001 0 0 0 50.677734 31.029297 A 1.0001 1.0001 0 0 0 49.927734 31.416016 L 46.9375 35.166016 A 1.0006413 1.0006413 0 0 0 46.841797 35.3125 C 46.221134 35.064509 45.605479 34.804721 45.005859 34.533203 C 44.346216 34.234506 43.705258 33.926713 43.085938 33.617188 L 46.302734 31.0625 A 1.0001 1.0001 0 0 0 45.675781 29.271484 A 1.0001 1.0001 0 0 0 45.058594 29.496094 L 41.457031 32.357422 A 1.0001893 1.0001893 0 0 0 41.214844 32.638672 C 39.94874 31.95122 38.897423 31.329025 38.003906 30.777344 L 40.990234 28.597656 A 1.0001 1.0001 0 0 0 40.435547 26.78125 A 1.0001 1.0001 0 0 0 39.810547 26.982422 L 36.193359 29.625 C 35.994395 29.491468 35.870277 29.406869 35.804688 29.361328 C 34.693717 26.790066 33.436578 25.00809 32.425781 23.873047 C 32.179647 23.596658 31.948061 23.362011 31.732422 23.154297 C 33.397629 21.499934 35.438854 19.724252 37.804688 18.087891 A 1.0001 1.0001 0 0 0 37.837891 18.142578 L 39.636719 21.082031 A 1.0007268 1.0007268 0 0 0 41.34375 20.037109 L 39.542969 17.097656 A 1.0001 1.0001 0 0 0 39.474609 16.996094 C 40.303285 16.482852 41.167426 15.995156 42.0625 15.537109 L 43.736328 20.339844 A 1.0001 1.0001 0 1 0 45.625 19.681641 L 43.880859 14.677734 C 45.382561 14.019449 46.953561 13.448616 48.607422 13.03125 z M 30.349609 24.589844 C 30.523265 24.759971 30.715556 24.96048 30.931641 25.203125 C 31.83832 26.221252 33.026456 27.875199 34.078125 30.386719 C 34.482156 31.351597 34.392677 32.778523 33.876953 34.404297 C 33.361229 36.030071 32.451463 37.811995 31.464844 39.443359 C 30.53565 40.979771 29.559899 42.351463 28.771484 43.402344 C 28.497228 42.370071 27.904569 40.070603 27.382812 37.027344 C 27.053373 35.105813 26.807217 33.091187 26.785156 31.447266 C 26.763096 29.803345 27.119344 28.544441 27.228516 28.388672 A 2.0002 2.0002 0 0 0 27.228516 28.384766 C 27.829188 27.525265 28.896979 26.161021 30.349609 24.589844 z M 30.839844 30.039062 C 30.289844 30.039062 29.839844 30.489062 29.839844 31.039062 C 29.839844 31.589063 30.289844 32.039062 30.839844 32.039062 C 31.399844 32.039063 31.839844 31.589063 31.839844 31.039062 C 31.839844 30.489062 31.399844 30.039062 30.839844 30.039062 z M 51.175781 45.316406 A 1.0001 1.0001 0 0 0 50.242188 46.171875 C 48.838226 54.954102 47.61585 59.385063 46.443359 62.541016 A 1.0001 1.0001 0 0 0 47.130859 63.857422 L 52.859375 65.337891 A 1.0001 1.0001 0 1 0 53.359375 63.402344 L 48.634766 62.181641 C 49.764502 58.93815 50.919669 54.60223 52.216797 46.488281 A 1.0001 1.0001 0 0 0 51.275391 45.316406 A 1.0001 1.0001 0 0 0 51.175781 45.316406 z M 40.451172 46.148438 C 38.952863 46.173428 37.484726 46.553591 36.140625 47.193359 A 2.0006192 2.0006192 0 1 0 37.859375 50.806641 C 39.751172 49.906178 41.226164 49.785864 43.058594 50.763672 A 2.0002 2.0002 0 1 0 44.941406 47.236328 C 43.477621 46.455233 41.949481 46.123445 40.451172 46.148438 z M 62.396484 46.431641 C 61.012918 46.446011 59.666154 46.683934 58.384766 47.097656 A 2.0002 2.0002 0 1 0 59.615234 50.902344 C 61.512457 50.289788 63.309799 50.210728 65.367188 50.896484 A 2.0002 2.0002 0 1 0 66.632812 47.103516 C 65.201508 46.626414 63.780051 46.417268 62.396484 46.431641 z M 69.480469 56.359375 C 68.930469 56.359375 68.480469 56.809375 68.480469 57.359375 C 68.480469 57.909375 68.930469 58.359375 69.480469 58.359375 C 70.030469 58.359375 70.480469 57.909375 70.480469 57.359375 C 70.480469 56.809375 70.030469 56.359375 69.480469 56.359375 z M 35.669922 62.369141 C 35.119922 62.369141 34.669922 62.819141 34.669922 63.369141 C 34.669922 63.919141 35.119922 64.369141 35.669922 64.369141 C 36.219922 64.369141 36.669922 63.919141 36.669922 63.369141 C 36.669922 62.819141 36.219922 62.369141 35.669922 62.369141 z M 41.958984 69 A 1.0001 1.0001 0 0 0 41.224609 70.630859 C 45.357335 75.707154 50.182021 76.102429 53.720703 75.070312 C 57.259386 74.038197 59.685547 71.728516 59.685547 71.728516 A 1.0001 1.0001 0 0 0 59.058594 70.001953 L 42.058594 69.001953 A 1.0001 1.0001 0 0 0 41.958984 69 z M 44.650391 71.158203 L 55.943359 71.822266 C 55.124357 72.303674 54.287969 72.821445 53.160156 73.150391 C 50.668102 73.87724 47.7044 73.768437 44.650391 71.158203 z"></path>
            </svg>
          <h3 className="text-xl font-medium text-gray-600 mb-2">Hallo {userName.split(' ')[0]}!</h3>
          <h6 className="text-xl font-medium text-gray-600 mb-2">Ich bin dein Bundesliga-ChatBot 🤖</h6>
          <p className="max-w-xs">Wie kann ich Dir heute helfen?</p>
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
