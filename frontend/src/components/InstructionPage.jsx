function InstructionPage({ startTask, exit }) {
  return (
    <div className="max-w-2xl mx-auto mt-10 p-6 bg-white shadow-lg rounded-md text-gray-800">
      <h1 className="text-2xl font-bold text-center mb-6 text-blue-600">
        Welcome to the Task
      </h1>
      <p className="text-lg mb-4">
        Thank you for participating! In the next step, you will be presented
        with an image. Your task is to carefully observe the image and then 
        describe what you see. Please speak freely, but ensure your recording lasts 
        at least <span className="font-bold">60 seconds</span>.
      </p>
      <p className="text-lg mb-4">
        At the end of the task, provided your recording passes our 
        <span className="font-bold"> quality control standards</span>, 
        you will receive a confirmation code that you can use to claim your payment on MTurk.
      </p>
      <h2 className="text-xl font-semibold mb-3">Important Guidelines:</h2>
      <ul className="list-disc list-inside mb-6">
        <li>Do not muffle your microphone or stand too far away.</li>
        <li>Ensure your audio is clear and relevant to the task.</li>
        <li>Recording irrelevant audio or low-quality submissions may violate the terms and conditions and result in payment revocation.</li>
      </ul>
      <p className="font-bold py-5">By clicking 'Start Task', you are agreeing to our terms and conditions.</p>
      <div className="flex justify-center space-x-4">
        <button
          onClick={startTask}
          className="px-6 py-3 bg-green-600 text-white font-semibold rounded-md hover:bg-green-700 transition duration-200"
        >
          Start Task
        </button>
        <button
          onClick={exit}
          className="px-6 py-3 bg-red-600 text-white font-semibold rounded-md hover:bg-red-700 transition duration-200"
        >
          Exit
        </button>
      </div>
    </div>
  );
}

export default InstructionPage;
