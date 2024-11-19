import React, { useState } from "react";
import CaptionPage from "./components/CaptionPage";
import InputPage from "./components/InputPage";

function App() {

  const [currentPage, setCurrentPage] = useState(0);
  const [mturkId, setMturkId] = useState('');
  const [confirmationCode, setConfirmationCode] = useState('');

  const nextPage = () => setCurrentPage((prev) => {
    if (prev == 3) {
      return 2; // start a new image captioning task
    } else {
      return prev + 1;
    }
  });

  const renderPage = () => {
    switch (currentPage) {
      case 0:
        return <InputPage onSubmit={(id) => { setMturkId(id); nextPage(); }} />;
      case 1:
        return <CaptionPage mturkId={mturkId} onReceive={(code) => { setConfirmationCode(code); nextPage(); }} />;
      case 2:
        return <ConfirmationPage confirmationCode={confirmationCode} whenFinished={nextPage()} />;
      default:
        return null;
    }
  };

  return <div>
    {renderPage()}
  </div>;
}

export default App;