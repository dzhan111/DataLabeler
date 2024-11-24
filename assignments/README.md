# DataLabeler
NETS 2130 Final Project

# Data Labeler: Dense Captioning Crowdsourcing Platform

**Data Labeler** is a platform designed for dense image captioning using crowdsourced audio descriptions. Users are presented with an image and asked to record an audio description for 60-90 seconds. The recorded audio is processed through Whisper for transcription, and the resulting caption undergoes quality evaluation using GPT. High-quality captions are aggregated and stored in a database for further use.

Upon successful submission of the audio description, the worker receives a unique completion code. This code can then be used by the worker to claim their reward on Amazon Mechanical Turk (MTurk), ensuring fair compensation for their efforts.

## Project Flow Diagram

![Flow Diagram](../docs/flowchart.png)

UI mockup can be found [here](../docs/mockup.pdf)

## Major Components and Milestones

Below is a detailed explanation of the major components of the project, following the schematic in the flow diagram. Each component is assigned a point value (1-4) based on its complexity and the amount of work required.

### 1. **User Interface (UI) [2 points]**
   - Design a simple and intuitive interface where users can view an image and record their audio description.
   - Milestones:
     - Create a basic web UI for image display and audio recording.
     - Integrate a recording feature with a countdown timer (60-90 seconds).

### 2. **Image to Describe [1 point]**
   - Load and present the image to the user for description.
   - Milestones:
     - Set up an image retrieval system to fetch images from the dataset.
     - Ensure each image is only shown once per worker to avoid duplicates.

### 3. **Audio File Upload [2 points]**
   - Allow the user to upload their recorded audio file/re-record
   - Milestones:
     - Implement audio file handling and storage.
     - Validate the audio file format and length.

### 4. **Speech-to-Text (Whisper) [3 points]**
   - Use Whisper for converting the recorded audio into a text caption.
   - Milestones:
     - Integrate Whisper API for transcription.
     - Process and clean the transcribed text.

### 5. **Quality Control and Evaluation [4 points]**
   - Compare the transcribed caption against a gold standard for quality control using GPT.
   - Milestones:
     - Set up a quality control mechanism using test batches.
     - Integrate GPT for evaluating the caption’s accuracy and relevance.
     - Implement a feedback loop for workers who fail quality checks.

### 6. **Aggregation of High-Quality Responses [3 points]**
   - Aggregate three high-quality captions into a single final caption using GPT.
   - Milestones:
     - Collect responses and filter out low-quality submissions.
     - Use GPT to merge the responses into a coherent and accurate final caption.

### 7. **Database Storage [2 points]**
   - Store the aggregated caption and metadata in a database for future use.
   - Milestones:
     - Design the database schema for efficient storage and retrieval.
     - Implement the saving of captions and associated metadata (e.g., worker ID, image ID).

### 8. **Payment Code Generation and MTurk Integration [2 points]**
   - Generate a unique completion code for each worker upon successful submission.
   - Milestones:
     - Implement a code generation system and display the code to the user.
     - Integrate with Amazon Mechanical Turk (MTurk) for payment processing using the completion code.

## Total Point Value: **19 Points**

## **DataLabeler Project Directory**

## _[data/](/data)_

-
- **[dataset/](/data/dataset)**
  - a folder of 43 example images we intend to use as our dataset
- **[sample_io/](/data/sample_io)**
  - **[README.md](/data/sample_io/README.md)** : contains the sample aggregation inputs and outputs of our pipeline for 4 example images.
  - **[image1.jpeg](/data/sample_io/image1.jpeg)** : example input
  - **[image2.jpg](/data/sample_io/image2.jpg)** : example input
  - **[image3.jpg](/data/sample_io/image3.jpg)** : example input
  - **[image4.jpg](/data/sample_io/image4.jpg)** : example input

## _[docs/](/docs)_

- **[flowchart.png](/docs/flowdiagram.png)** : flow diagram for our application pipeline
- **[mockup.pdf](/docs/mockup.pdf)** : example mockups for our
- **[README.md](/docs/README.md)** : Markdown file explaining the major components of our project.

## _[src/](/src)_

- **[qc.py](/src/qc.py)** : a simple working version of our quality control pipeline
  - The quality control module consists of two phases:
    - The first step involves processing the input image through a multimodal model. This model generates a set of keywords that are concrete nouns found within the image. These keywords represent the key objects or features present in the image and are crucial for verifying the transcription in the next phase.
    - In the second phase, the generated keywords from phase 1 are combined with the worker's transcription. This combination is then fed into a LLM, specifically OpenAI's ChatGPT API. The LLM checks if the transcription is of sufficient quality by verifying whether at least 2 out of 10 keywords are included in the transcription and the transcription contains a minimum of 80 words. If both criteria are satisfied, the transcription passes the QC checks; otherwise, it is flagged as low quality and gets removed.
  - To improve our final version, we may consider:
    - Using a cheaper, open-source model: we want to explore using more affordable open-source models for keyword extraction and quality verification, such as Hugging Face's transformers or other lightweight models. This would hopefully reduce the dependency on costly API calls while maintaining performance.
    - Keyword and word count fine-tuning: we may fine-tune the pipeline by adjusting the number of required keywords (e.g., increasing the threshold to 3 keywords) and maybe extending the minimum word count to 80 words to better capture the quality of transcriptions.
- **[agg.py](/src/agg.py)** : a simple working version of our aggregation pipeline
  - The aggergation module is designed to combine multiple image captions into a single, dense caption that encapsulates the core information from all inputs. The process involves taking three captions, processing them through a model, and creating a more concise and coherent summary using Cerebras.
  - To improve our final version, we may consider:
    - Model optimization: we can explore alternative models or more efficient versions, such as smaller or fine-tuned models, to balance quality and performance.
    - Additional inputs: We could incorporate metadata (e.g., keywords from QC or other relevant data) into the aggregation process, allowing the model to make more informed decisions about what to keep and what to not.
- **[routes.py](/src/routes.py)** : the coordinator file that calls previous pipelines and serves images to the user
  - Uses LemonFox.AI for Speech-to-Text
  - Chooses a random image from the raw data to serve to the user
  - Connects to the frontend with FastAPI
- **[alock.py](/src/alock.py)** : custom locking for background processes
- **[clients.py](/src/clients.py)**: contains all of the clients we use for the backend, from the databases to the LLM clients to mturk's client
- **[image_utils.py](/src/image_utils.py)**: helper function to convert all images to uniform format
- **[mturk.py](/src/mturk.py)**: background process that asynchronously polls for submitted tasks
  - Utilizes the mturk API and a custom user to access our account
  - Accepts or rejects based on if the worker ID confirmation code combo is in our DB

## _[frontend/](/frontend)_

-
- **[App.jsx](/frontend/src/App.jsx)**: main front-end page switching between all of the types of pages in our app
- **[InputPage.jsx](/frontend/src/components/InputPage.jsx)**: page to submit worker-id
  - Saves ID for later to confirm confirmation code
- **[InstructionsPage.jsx](/frontend/src/components/InstructionPage.jsx)**: displays instructions to user
- **[CaptionPage.jsx](/frontend/src/components/CaptionPage.jsx)**: main page to record audio
  - Loads the image using backend API call
  - Has a built in audio recorder and timer to see how long you record
  - Feature to upload audio
  - Has audio playback feature
  - Responds to QC result from backend
- **[ConfirmationPage.jsx](/frontend/src/components/ConfirmationPage.jsx)**: confirms the completion of the tast
  - Shows the confirmation code to submit back into turk
  - Uses uuid4 as code template