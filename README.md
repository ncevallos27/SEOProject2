# GenAI Calendar Assistant

This project is an intelligent, command-line-based assistant that uses **Google Calendar API** and **Gemini AI (Google GenAI)** to interact with your calendar via natural language. It supports listing and inserting events through conversational prompts.

---

## Features

- Authenticates and manages access to your Google Calendar
- Uses Google's Gemini AI to interpret natural language commands
- Lists upcoming calendar events
- Inserts custom calendar events
- Maintains an interactive, context-aware conversation with the user

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/seoProject2.git
cd seoProject2
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Your `.env` File

Create a `.env` file in the root directory with:

```env
GEMINI_API_KEY=<Insert Gemini Key Here>
```

### 5. Add Google Credentials

- Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Enable the **Google Calendar API**
- Download the `credentials.json` file
- Place it in the root directory

---

## Usage

Start the assistant:

```bash
python main.py
```

You’ll be prompted to enter commands like:

- `"Show me my events this week"`
- `"Add a call with Dr. Smith on Friday at 10 AM"`
- `"Schedule a team meeting for next Tuesday at 2 PM"`

The AI will process your input, decide on the proper function to call, and act accordingly.

---

## Future Features

- Delete or update existing events
- Detect time conflicts and suggest alternatives
- Web or GUI frontend for broader usability

---

## Authors

Created by [Nico Cevallos](https://github.com/ncevallos27) and [Edson Petry](https://github.com/EdsonPetry)
SEO Tech Developer 2025