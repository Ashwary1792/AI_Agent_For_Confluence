# Confluence AI Agent

A Streamlit-powered AI assistant that answers your questions based on documentation from your Confluence space.

## Features
- Interactive chat UI with sidebar history and recent Q&A
- No code exposure—just run and use!

## How to Use
1. **Clone or copy the project files to your machine.**
2. **Get your Confluence API token and space info:**
   - Go to [Atlassian API tokens page](https://id.atlassian.com/manage-profile/security/api-tokens).
   - Click "Create API token" and give it a name.
   - Copy the generated token.
   - Your Confluence email is the email you use to log in.
   - Your Confluence base URL is usually like `https://yourdomain.atlassian.net/wiki`.
   - Your space key is found in the URL when you open your Confluence space (e.g., `spaces/SPACEKEY/overview`).
   - Create a `.env` file in the project folder with the following content:
     ```env
     CONFLUENCE_EMAIL=your_confluence_email
     CONFLUENCE_API_TOKEN=your_confluence_api_token
     CONFLUENCE_BASE_URL=https://yourdomain.atlassian.net/wiki
     CONFLUENCE_SPACE_KEY=your_space_key
     ```
   - Replace the values with your own credentials.
3. **Install dependencies:**
   - Run `pip install -r requirements.txt` in your virtual environment.

4. **Ask questions!**
   - The app will fetch your Confluence documentation and answer your queries using AI.

## Notes
- Your credentials are never shared; only you have access to your tokens.
- The sidebar shows previous questions; click to expand and view answers.
- The main area shows only the most recent Q&A.
- You only need to provide your Confluence API token and space info. The AI integration is handled automatically in the code.

## Requirements
- Python 3.8+
- Streamlit
- requests
- beautifulsoup4
- python-dotenv

## Logo
- Place your logo file (e.g., `ai_logo.png`) in the project folder for branding.

---

For any issues, contact your project admin or maintainer.
