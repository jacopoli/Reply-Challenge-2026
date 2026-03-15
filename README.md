# Reply-Challenge-2026

## 📋 Project Description

A financial life simulation game built with **Streamlit** and powered by **Google Gemini AI**. This interactive RPG lets players experience real-world financial decisions including job changes, apartment hunting, investments, banking products, and major life events. The game combines AI-driven narrative storytelling with realistic financial mechanics to create an engaging educational experience.

### Key Features

- **AI-Powered Narrative**: Dynamic storytelling using Google Gemini AI
- **Financial Simulation**: Manage balance, savings, investments, and debt
- **Life Decisions**: Change jobs, find apartments, make major financial choices
- **Banking Products**: Access savings accounts and credit options
- **Investments**: Invest in various financial products (Livret A, Assurance-Vie, etc.)
- **Random Events**: Unexpected life events that impact your finances
- **Multi-Player Profiles**: Manage multiple player profiles with persistent game state

---

## 🚀 Prerequisites & Setup

### System Requirements

- Python 3.8 or higher
- Windows, macOS, or Linux

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd Reply-Challenge-2026
```

### Step 2: Create a Python Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure API Keys

1. Create a `config.py` file in the root directory (if it doesn't exist)
2. Add your Google Gemini API key:

```python
import os

# Google Generative AI Configuration
GOOGLE_API_KEY = "your-api-key-here"

# Game Configuration
STARTING_BALANCE = 1000
STARTING_SAVINGS = 5000
MONTHLY_RENT = 600
MONTHLY_EXPENSES = 400
SALARY = 1800

# Bank Partner Settings
SAVINGS_RATE = 0.03
LOAN_RATE = 0.05

# ... (rest of configuration)
```

3. To get your Google Gemini API key:
   - Visit [Google AI Studio](https://aistudio.google.com)
   - Click "Get API Key"
   - Create a new API key
   - Copy and paste it in `config.py`

### ⚠️ Important: Protecting Sensitive Data

The `config.py` file is already added to `.gitignore` to prevent accidentally pushing API keys to the repository. **Never commit your API keys to version control.**

### Step 5: Run the Application

```bash
streamlit run main.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📁 Project Structure

```
Reply-Challenge-2026/
├── main.py                  # Main Streamlit application entry point
├── game_engine.py          # Core game state and logic
├── ai_agents.py            # AI narrator and advisor using Gemini
├── config.py               # Configuration & API keys (NOT in git)
├── data_manager.py         # User data persistence
├── banking_products.py     # Banking products and offers
├── investments.py          # Investment mechanics
├── major_decisions.py      # Job and apartment decisions
├── random_events.py        # Random event generation
├── pending_requests.py     # Pending request handling
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Files to exclude from git
└── user_data/              # User save files directory
    ├── user.json
    └── test_1.json
```

---

## 🎮 How to Play

1. **Start the game**: Run `streamlit run main.py`
2. **Create or select a profile**: Choose an existing player or create a new one
3. **Make decisions**:
   - Interact with the narrative
   - Manage your finances
   - Make job and housing decisions
   - Invest money
   - Respond to random events
4. **Track your progress**: Monitor your stress, fun level, and financial status
5. **Save automatically**: Your progress is saved after each action

---

## 📦 Dependencies

- `streamlit` - Web application framework
- `google-generativeai` - Google Gemini AI integration
- `python-dotenv` - Environment variable management
- `pandas` - Data manipulation and analysis

All dependencies are listed in `requirements.txt`

---

## 🔒 Security Best Practices

- ✅ Never commit `config.py` to version control (protected by `.gitignore`)
- ✅ Use environment variables for sensitive data when possible
- ✅ Keep your API keys confidential
- ✅ Regularly rotate API keys if exposed

---

## 📝 Configuration

Key game configuration parameters in `config.py`:

- `STARTING_BALANCE`: Initial cash balance
- `STARTING_SAVINGS`: Initial savings account balance
- `MONTHLY_RENT`: Monthly housing cost
- `MONTHLY_EXPENSES`: Other monthly expenses
- `SALARY`: Base salary
- `SAVINGS_RATE`: Bank savings interest rate
- `LOAN_RATE`: Loan interest rate

---

## 🛠️ Development

To modify game parameters or add new features:

1. Edit `config.py` for game constants
2. Edit `game_engine.py` for core mechanics
3. Edit `ai_agents.py` for AI behavior
4. Run tests and verify changes before pushing

---

## 📞 Support & Troubleshooting

**Issue: "ModuleNotFoundError: No module named 'streamlit'"**

- Solution: Run `pip install -r requirements.txt` again

**Issue: "Invalid API key"**

- Solution: Verify your Google API key in `config.py` is correct

**Issue: "Port 8501 already in use"**

- Solution: Run `streamlit run main.py --server.port 8502` to use a different port

---

## 📄 License

This project is part of the Reply Challenge 2026
