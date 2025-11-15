![Uploading Cybersecurity_Study_Assistant_AI_Agent_Professional_Logo.png…]()


# 🔐 Cybersecurity Study Assistant Agent

AI agent that helps students learn cybersecurity through:
- **Clear explanations** of security concepts
- **Auto-generated practice quizzes**  
- **Progress tracking** and personalized recommendations

**Google AI Agents Intensive Course - Capstone Project**

## 🎯 Project Overview

This AI agent serves as a personalized cybersecurity tutor, making security education accessible to beginners. Built with Google's Gemini 2.0 Flash model, it provides interactive learning experiences through three main tools:

1. **Explain Tool**: Breaks down complex security concepts into simple, beginner-friendly explanations
2. **Quiz Tool**: Generates custom practice quizzes on any security topic
3. **Progress Tool**: Tracks learning progress and provides personalized study recommendations

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- Google Gemini API key (free at [Google AI Studio](https://aistudio.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/security-study-agent.git
   cd security-study-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   - Get your free API key from: https://aistudio.google.com/app/apikey
   - Copy `.env.example` to `.env`
   - Add your API key to `.env`:
     ```
     GOOGLE_API_KEY=your_actual_api_key_here
     ```

4. **Run the agent**
   ```bash
   python agent.py
   ```

## 📖 Usage

### Commands

- `explain [topic]` - Learn about any security topic (e.g., `explain phishing`)
- `quiz [topic]` - Take a practice quiz (e.g., `quiz passwords`)
- `progress` - View your learning statistics
- `help` - Show available commands
- `quit` - Exit the agent

### Example Session

```
🔐 CYBERSECURITY STUDY ASSISTANT
============================================================

I'm your AI tutor for learning cybersecurity!

You: explain phishing

🤖 Agent: Let me explain phishing...

Phishing is a cyber attack where criminals send fake emails or messages 
pretending to be from legitimate companies to trick you into revealing 
personal information like passwords or credit card numbers...

💡 Want to test your knowledge? Try: quiz phishing

You: quiz phishing

🤖 Agent: Generating quiz on phishing...

============================================================
Question 1: What is the main purpose of phishing attacks?
  A) To encrypt your files
  B) To steal personal information
  C) To speed up your computer
  D) To update your software

Your answer (A/B/C/D): B
✓ Correct!
```

## 🛠️ Features

### Three Core Tools

1. **Explain Concept Tool**
   - Provides simple, beginner-friendly explanations
   - Includes real-world examples
   - Tracks which topics you've studied

2. **Generate Quiz Tool**
   - Creates custom multiple-choice questions
   - Provides immediate feedback
   - Tracks quiz scores and accuracy

3. **Progress Tracking Tool**
   - Shows topics studied
   - Displays quiz performance statistics
   - Provides personalized study recommendations

### Technical Details

- **Model**: Gemini 1.5 Flash (stable and reliable)
- **Language**: Python 3.11+
- **Storage**: JSON-based progress tracking
- **Track**: Agents for Good

## 📊 Project Structure

```
security-study-agent/
├── agent.py              # Main agent code
├── requirements.txt      # Python dependencies
├── .env.example         # API key template
├── .gitignore           # Git ignore rules
├── README.md            # This file
└── study_progress.json  # Progress data (auto-generated)
```

## 🎯 Competition Details

**Competition**: [Google AI Agents Intensive - Capstone Project](https://www.kaggle.com/competitions/agents-intensive-capstone-project)

**Track**: Agents for Good

**Submission**: GitHub repository + demo video

## 🎥 Demo Video

[Link to demo video will be added here]

## 🏆 Why This Project

- ✅ **Simple to Build** - Clean, well-documented code (~200 lines)
- ✅ **Actually Useful** - Helps real students learn cybersecurity
- ✅ **Easy to Demo** - Judges can test it immediately
- ✅ **Clear Impact** - Educational value for "Agents for Good" track
- ✅ **Well-Documented** - Complete README and code comments

## 🔧 Troubleshooting

### Import Error
```bash
pip install --upgrade google-generativeai python-dotenv
```

### API Key Error
- Ensure `.env` file exists in the project root
- Verify API key is correct (no quotes needed)
- Check API key is active at Google AI Studio

### Quiz Generation Issues
- Try a different topic if JSON parsing fails
- Ensure stable internet connection
- API may be rate-limited (wait a moment and retry)

## 📝 License

This project is created for the Google AI Agents Intensive Course capstone project.

## 🙏 Acknowledgments

- Google AI Studio for providing Gemini API
- Google AI Agents Intensive Course
- Cybersecurity education community

---

**Built with ❤️ for cybersecurity education**


