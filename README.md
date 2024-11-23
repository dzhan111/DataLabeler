# **DataLabeler**
A service using crowdsourcing to create dense image captions

## Team

- Ahmed (ahmedOmuharram)
- Eric (ezou626)
- David (dzhan111)
- Akash (akashkau1224)

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

For a more detailed breakdown of the repo or hosting instructions, please check out [this document](/docs/README.md).