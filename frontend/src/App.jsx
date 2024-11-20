import React, { useState } from "react";
import CaptionPage from "./components/CaptionPage";
import ConfirmationPage from "./components/ConfirmationPage";
import InputPage from "./components/InputPage";
import InstructionPage from "./components/InstructionPage";

function App() {
  const [currentPage, setCurrentPage] = useState(0);

  const [mturkId, setMturkId] = useState('');
  const [confirmationCode, setConfirmationCode] = useState('');

  const nextPage = () => setCurrentPage((prev) => {
    if (prev == 3) {
      return 1; // start a new image captioning task
    }
    prev = prev + 1
    return prev;
  });

  const renderPage = () => {
    switch (currentPage) {
      case 0:
        return <InputPage onSubmit={(id) => { 
          setMturkId(id); 
          nextPage(); 
        }} />;
      case 1:
        return <InstructionPage startTask={nextPage}/>
      case 2:
        return <CaptionPage mturkId={mturkId} onReceive={(code) => { 
          setConfirmationCode(code); 
          nextPage(); 
        }} />;
      case 3:
        return <ConfirmationPage 
          confirmationCode={confirmationCode} 
          moreTasks={nextPage}
        />;
      default:
        return null;
    }
  };

  return <div>
    {renderPage()}
  </div>;
}

export default App;