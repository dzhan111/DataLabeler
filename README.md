# **DataLabeler**
A service created for our NETS 2130 final project using crowdsourcing to create dense image captions

## Team

- Ahmed (ahmedOmuharram)
- Eric (ezou626)
- David (dzhan111)
- Akash (akashkau1224)

## Premise

Users are presented with an image and asked to record an audio description for 60-90 seconds. The recorded audio is transcribed, and the resulting caption undergoes quality evaluation. High-quality captions are aggregated and stored in a database for further use.

Upon successful submission of the audio description, the worker receives a confirmation code. This code can then be used to claim their reward on Amazon Mechanical Turk, ensuring fair compensation.

## How To Contribute

### Submission Instructions
1. Create a Worker account on [Amazon Mechanical Turk Sandbox](https://workersandbox.mturk.com/).
2. Accept any of the following HITs [here](https://workersandbox.mturk.com/requesters/A1T9HCL62TFS2Q/projects).
3. Follow the embedded link to [our data collection website](https://data-labeler-ten.vercel.app/).
4. Complete the task, get the confirmation code, and submit it in the HIT.
5. Done! Thanks for your contribution.

### Instructional Video
Please watch the video [here](https://youtu.be/n4kLEWFMmuE) for a visual guide.

### View Completed Captions
Hit our API for viewing completed aggregations [here](https://datalabeler.onrender.com/get_captioned_images).

### Contact
Please contact ezou626@seas.upenn.edu for any questions/concerns/errors, or [submit an issue to our GitHub repo](https://github.com/dzhan111/DataLabeler/issues).

## Tech Stack

### Frontend
- [**React**](https://react.dev/)
- [**Tailwind CSS**](https://tailwindcss.com/)
- [**Vite**](https://vite.dev/)
### Backend
- [**FastAPI**](https://fastapi.tiangolo.com/)

### Third-Party Services
- [**Amazon Mechanical Turk:**](https://www.mturk.com/) Task verification and (theoretically) payment
- [**Lemonfox.ai:**](https://www.lemonfox.ai/) Model hosting and API for automatic speech recognition
- [**OpenAI GPT-4o:**](https://openai.com/api/) GPT-4o hosting and API for quality control keyword generation
- [**Cerebras:**](https://mega.io/) Llama-3.1b hosting and API for caption aggregation
- [**Mega:**]() Image store
- [**Supabase:**](https://supabase.com/) Postgres database hosting
- [**Vercel:**](https://vercel.com/) Frontend hosting
- [**Render:**](https://render.com/) Backend hosting


## Documentation

For hosting instructions, please check out [this document](/docs/README.md). For NETS 2130 milestones, please check out [this document](/assignments/README.md).

## Files and Directories
### [assignments/](./assignments)
- For README.mds and content used in past milestones and assignments
### [data/](data/)
- **[dataset/](/data/dataset)** 
    - 43 images used in the dataset
- **[sample_io/](/data/sample_io)**
    - **[README.md](/data/sample_io/README.md)** : contains the sample aggregation inputs and outputs of our pipeline for 4 example images.
    - **[image1.jpeg](/data/sample_io/image1.jpeg)** : example input
    - **[image2.jpg](/data/sample_io/image2.jpg)** : example input
    - **[image3.jpg](/data/sample_io/image3.jpg)** : example input
    - **[image4.jpg](/data/sample_io/image4.jpg)** : example input
### [docs/](docs/)
- **[flowchart.png](/docs/flowdiagram.png)** : flow diagram for our application pipeline 
- **[mockup.pdf](/docs/mockup.pdf)** : draft mockups for our frontend
- **[README.md](/docs/README.md)** : Markdown file to organize deployment/development information. 
### [frontend/](frontend/)
Contains React frontend code. A detailed listing can be found [here](frontend/README.md)
### [src/](src/)
Contains FastAPI backend code. A detailed listing can be found [here](src/README.md).
### [.env.example](.env.example)
Template .env file
### [.gitignore](.gitignore)
Excludes \_\_pycache\_\_, venv, .env, and node_modules
### [requirements.txt](requirements.txt)
### [run.py](./run.py)