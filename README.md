**DataLabeler Project Directory**
------------


*[data/](/data)* 
- 
- **[dataset/](/data/dataset)** 
    - a folder of 43 example images we intend to use as our dataset
- **[sample_io/](/data/sample_io)**
    - **[README.md](/data/sample_io/README.md)** : contains the sample aggregation inputs and outputs of our pipeline for 4 example images.
    - **[image1.jpeg](/data/sample_io/image1.jpeg)** : example input
    - **[image2.jpg](/data/sample_io/image2.jpg)** : example input
    - **[image3.jpg](/data/sample_io/image3.jpg)** : example input
    - **[image4.jpg](/data/sample_io/image4.jpg)** : example input

*[docs/](/docs)* 
-
- **[flowchart.png](/docs/flowdiagram.png)** : flow diagram for our application pipeline 
- **[mockup.pdf](/docs/mockup.pdf)** : example mockups for our 
- **[README.md](/docs/README.md)** : Markdown file explaining the major components of our project. 

*[src/](/src)* 
-
- **qc.py** : a simple working version of our quality control pipeline
    - The quality control module consists of two phases:
      - The first step involves processing the input image through a multimodal model. This model generates a set of keywords that are concrete nouns found within the image. These keywords represent the key objects or features present in the image and are crucial for verifying the transcription in the next phase.
      - In the second phase, the generated keywords from phase 1 are combined with the worker's transcription. This combination is then fed into a LLM, specifically OpenAI's ChatGPT API. The LLM checks if the transcription is of sufficient quality by verifying whether at least 2 out of 10 keywords are included in the transcription and the transcription contains a minimum of 80 words. If both criteria are satisfied, the transcription passes the QC checks; otherwise, it is flagged as low quality and gets removed.
    - To improve our final version, we may consider:
      - Using a cheaper, open-source model: we want to explore using more affordable open-source models for keyword extraction and quality verification, such as Hugging Face's transformers or other lightweight models. This would hopefully reduce the dependency on costly API calls while maintaining performance.
      - Keyword and word count fine-tuning: we may fine-tune the pipeline by adjusting the number of required keywords (e.g., increasing the threshold to 3 keywords) and maybe extending the minimum word count to 90 words to better capture the quality of transcriptions.
- **agg.py** : a simple working version of our aggregation pipeline
    - The aggergation module is designed to combine multiple image captions into a single, dense caption that encapsulates the core information from all inputs. The process involves taking three captions, processing them through a model, and creating a more concise and coherent summary using Cerebras.
    - To improve our final version, we may consider:
      - Model optimization: we can explore alternative models or more efficient versions, such as smaller or fine-tuned models, to balance quality and performance.
      - Additional inputs: We could incorporate metadata (e.g., keywords from QC or other relevant data) into the aggregation process, allowing the model to make more informed decisions about what to keep and what to not.
- **routes.py** : the coordinator file that calls previous pipelines and serves images to the user
    - Uses Whisper for Speech-to-Text
    - Chooses a random image from the raw data to serve to the user



