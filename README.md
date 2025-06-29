---
title: Anvesana
emoji: 🐢
colorFrom: pink
colorTo: purple
sdk: docker
pinned: false
---
# Anveṣaṇā 🐢

>**_/ənʋeːʂəɳɑː/ · Sanskrit: अन्वेषणा_**  
search after, seek for, or inquiry into.  

Derived from the root verb "anveṣ" (अन्वेष), which means "to search for" or "to seek out".  
In the context of Vedic texts, Anveṣaṇā refers to the process of searching for
knowledge, wisdom, and understanding within these ancient scriptures.

Anvesana is tool that allows you to search through Vedic texts using natural language queries, using retrieval-augmented-generation to provide accurate and relevant answers.  
It is designed to help you find information quickly and efficiently, making it easier to explore the vast knowledge contained within Vedic literature.


## Available Texts
The following texts are currently supported:
- **Charaka Samhita**: A foundational text of Ayurveda, detailing various aspects of medicine, including diagnosis, treatment, and pharmacology. [1]

More texts coming soon.

## Usage
The Anvesana demo app is available [here](https://anvesana-285115912145.europe-west2.run.app/).  

### Local Setup
Anvesana uses a local database to store the text data. This needs to be set up once before running the app for the first time.  
1. Set the text source API URL in the `API_URL` environment variable.
   ```bash
    export API_URL=https://www.carakasamhitaonline.com/api.php
    ```

2. Run the following command to set up the database:
   ```bash
   python data/main.py
   ```
   This will create a SQLite database file `./data/` directory.

\
Anvesana requires a Google AI Studio API key to function (free tier). Set the Google AI Studio API key in the `GOOGLE_API_KEY` environment variable:
   ```bash
   export GOOGLE_API_KEY=your_api_key_here
   ```

### Docker Setup
You can also run Anvesana locally using Docker. This does not require cloning the repo or setup of the local database. The app runs on port 7860.
1. Pull the Docker image:
   ```bash
   docker pull docker.io/dvmht/anvesana:latest
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 7860:7860 --gpus all \
   -e GOOGLE_API_KEY=your_api_key_here \
   dvmht/anvesana:latest
   ```
Make sure to provide your Google AI Studio API key to the container in the `GOOGLE_API_KEY` environment variable.


### Example Queries
Unsure what to ask? Why not start with:
- What is Ayurveda?
- What is the difference between Ayurveda and modern medicine?
- How does Ayurveda define health?
- What are the principles of Ayurveda?


## Acknowledgements
This project would not be possible without the extensive resources at [Caraka Samhita Online][1].


[1]: https://www.carakasamhitaonline.com/index.php?title=Main_Page
