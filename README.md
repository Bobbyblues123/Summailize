# Summailize

Summailize is a smart email assistant that automatically fetches unread Gmail messages, summarizes them using Google Gemini AI, categorizes them into types (like Job Opportunity, Event, Promotion, etc.), applies labels inside Gmail, and shows you desktop notifications. Built for users who find it inconvenient to navigate through thousands of unread emails.


---

## Features

- OAuth2-based Gmail Authentication
- Reads your **latest unread email**
- Summarizes content using **Gemini AI**
- Automatically classifies as: `Job Opportunity`, `Promotion`, `Event`, `Newsletter`, etc. or `Other`
- Applies Gmail labels using **Gmail API**
- Sends native macOS desktop notifications
- Unit tested (mocked API responses)
- Flask backend ready for frontend integration

---

## Folder Structure

```
Summailize/
├── src/
│   ├── main.py                 # Core script to run auto-summarizer
│   ├── gmail_service.py        # Handles Gmail login, email fetching & labeling
│   ├── summarizer.py           # Gemini AI logic for summarization & classification
│   ├── notifier.py             # Sends Mac notifications using pync
│   ├── config.py               # Stores config paths, scopes, env handling
│   ├── app.py                  # Flask backend server for web/CLI interface
├── tests/
│   ├── test_summarizer.py      # Unit tests for summarizer logic
├── credentials.json            # Gmail API credentials
├── token.json                  # Auto-generated token file
├── tests/
│   ├── gmailsummarizerlogo.png # Icon for notifications

├── requirements.txt            # All pip dependencies
├── .env                        # Contains Gemini API key
├── .gitignore                  # Ignore token, env, and cache files
├── README.md                   
└──                
```

---

## Setup Instructions

### 1. Clone the project

```bash
git clone https://github.com/Bobbyblues123/Summailize.git
cd Summailize
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Add `.env` file

Create `.env` in the root:

```
GEMINI_API_KEY=your_actual_gemini_api_key(you can create this in Google AI Studio)
```

### 4. Add Gmail OAuth credentials

- Go to https://console.cloud.google.com/
- Create project > Enable Gmail API
- Download `credentials.json` and place it in the root of the project

---

## How It Works

1. The app logs into Gmail via OAuth
2. Fetches the **latest unread message**
3. Extracts the subject, sender, and plaintext or HTML content
4. Sends the text to **Gemini AI** to get:
   - A summary
   - A category
5. Creates a Gmail label (if needed)
6. Labels the email
7. Notifies the user via desktop notification

---

## Testing

This project uses `unittest` with mocked APIs:

```bash
python -m unittest discover tests
```

---

## API Endpoints (If using Flask)

Once you run `python src/app.py`, you’ll have:

| Endpoint          | Method | Description                             |
|-------------------|--------|-----------------------------------------|
| `/summarize`      | POST   | Summarizes and categorizes email text   |
| `/latest-email`   | GET    | Fetches the latest unread Gmail email   |
| `/label`          | POST   | Labels an email with a category         |

Example `POST /summarize` JSON:

```json
{
  "email_text": "Big Summer Sale! 70% off everything at Walmart..."
}
```

Response:

```json
{
  "summary": "Massive discounts storewide at Walmart.",
  "category": "Promotion"
}
```

---

## Roadmap

- [ ] One-by-one email summarization
- [ ] Frontend dashboard (React or Next.js)
- [ ] Multi-email batch summarization
- [ ] Email archiving & download
- [ ] Admin panel to reclassify/correct labels

---

## Technologies Used

- Python
- Flask
- Google Gmail API
- Google AI (Gemini)
- Pync (macOS notifications)
- BeautifulSoup
- `unittest` and `unittest.mock`

---

## Acknowledgements

- Google for Gmail + Gemini APIs
- OpenAI for guidance on prompt engineering
- BeautifulSoup and Pync developers

---

## License

MIT License © 2025 Shaheen Bhattacharya
