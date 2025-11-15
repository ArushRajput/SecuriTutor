import google.generativeai as genai
import json
import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()

class SecurityStudyAgent:
    """AI Agent that helps students learn cybersecurity"""
    
    def __init__(self):
        # Load and configure API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file. Please create .env file with your API key.")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Flash - stable and reliable
        try:
            self.model = genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            raise ValueError(f"Failed to initialize model: {e}. Check your API key is valid.")
        
        self.progress_file = 'study_progress.json'
        self.load_progress()
    
    def load_progress(self):
        """Load or create progress tracking file"""
        try:
            with open(self.progress_file, 'r') as f:
                self.progress = json.load(f)
        except:
            self.progress = {
                'topics_studied': [],
                'quiz_scores': [],
                'total_questions': 0,
                'correct_answers': 0
            }
    
    def save_progress(self):
        """Save progress to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress, f, indent=2)
    
    def explain_concept(self, topic):
        """
        TOOL 1: Explain Security Concepts
        
        Uses Gemini to explain cybersecurity topics in simple terms.
        Tracks which topics the student has studied.
        """
        prompt = f'''
        You are a cybersecurity tutor for beginners.
        Explain {topic} in simple terms with:
        1. Simple definition (1 sentence)
        2. Real-world example
        3. Why it matters in cybersecurity
        
        Keep it under 200 words and use beginner-friendly language.
        '''
        
        try:
            response = self.model.generate_content(prompt)
            explanation = response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                return "⚠️ API rate limit reached. Please wait a minute and try again, or check your API quota at https://ai.dev/usage"
            elif "403" in error_msg or "permission" in error_msg.lower():
                return "⚠️ API access denied. Please check your API key is valid and has proper permissions."
            else:
                return f"⚠️ Error generating explanation: {error_msg[:100]}"
        
        # Track this topic in progress
        if topic not in [t['topic'] for t in self.progress['topics_studied']]:
            self.progress['topics_studied'].append({
                'topic': topic,
                'date': datetime.now().isoformat()
            })
            self.save_progress()
        
        return explanation
    
    def generate_quiz(self, topic, num_questions=5):
        """
        TOOL 2: Generate Practice Quiz
        
        Creates custom quiz questions on any security topic.
        Returns questions in structured format.
        """
        prompt = f'''
        Create {num_questions} multiple-choice quiz questions about {topic}.
        
        Format as JSON array:
        [
          {{
            "question": "What is the main purpose of...?",
            "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
            "correct": "A",
            "explanation": "Brief explanation why this is correct"
          }}
        ]
        
        Make questions appropriate for beginners learning cybersecurity.
        '''
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower() or "rate" in error_msg.lower():
                print("⚠️ API rate limit reached. Please wait a minute and try again.")
                return []
            elif "403" in error_msg or "permission" in error_msg.lower():
                print("⚠️ API access denied. Please check your API key.")
                return []
            else:
                print(f"⚠️ Error generating quiz: {error_msg[:100]}")
                return []
        
        # Extract JSON from response
        start = text.find('[')
        end = text.rfind(']') + 1
        
        if start != -1 and end != 0:
            try:
                quiz_data = json.loads(text[start:end])
                return quiz_data
            except json.JSONDecodeError:
                return []
        else:
            return []
    
    def take_quiz(self, quiz_data):
        """
        Interactive quiz interface
        
        Presents questions one by one, checks answers,
        provides feedback, and tracks score.
        """
        score = 0
        
        for i, q in enumerate(quiz_data, 1):
            print(f"\n{'='*60}")
            print(f"Question {i}: {q['question']}")
            print()
            for option in q['options']:
                print(f"  {option}")
            
            answer = input("\nYour answer (A/B/C/D): ").strip().upper()
            
            if answer == q['correct']:
                print("✓ Correct!")
                score += 1
            else:
                print(f"✗ Wrong. Correct answer: {q['correct']}")
            
            print(f"Explanation: {q['explanation']}")
        
        # Save quiz results to progress
        accuracy = (score / len(quiz_data)) * 100
        self.progress['quiz_scores'].append({
            'date': datetime.now().isoformat(),
            'score': score,
            'total': len(quiz_data),
            'accuracy': accuracy
        })
        self.progress['total_questions'] += len(quiz_data)
        self.progress['correct_answers'] += score
        self.save_progress()
        
        return score, len(quiz_data)
    
    def show_progress(self):
        """
        TOOL 3: Display Learning Progress
        
        Shows statistics about topics studied, quiz performance,
        and provides personalized recommendations.
        """
        print("\n" + "="*60)
        print("📊 YOUR LEARNING PROGRESS")
        print("="*60)
        
        # Topics studied
        print(f"\n📚 Topics Studied: {len(self.progress['topics_studied'])}")
        if self.progress['topics_studied']:
            print("\nRecent topics:")
            for item in self.progress['topics_studied'][-5:]:
                print(f"  - {item['topic']}")
        
        # Quiz statistics
        if self.progress['quiz_scores']:
            overall = (self.progress['correct_answers'] / 
                      self.progress['total_questions'] * 100)
            print(f"\n🎯 Quiz Performance:")
            print(f"  Total Questions Attempted: {self.progress['total_questions']}")
            print(f"  Correct Answers: {self.progress['correct_answers']}")
            print(f"  Overall Accuracy: {overall:.1f}%")
            
            # Recent quizzes
            print(f"\n  Recent Quiz Scores:")
            for quiz in self.progress['quiz_scores'][-3:]:
                print(f"    {quiz['score']}/{quiz['total']} ({quiz['accuracy']:.1f}%)")
        else:
            print("\n🎯 No quizzes taken yet!")
            print("  Try: 'quiz phishing' to get started")
        
        # Personalized recommendations
        print(f"\n💡 Recommendations:")
        if self.progress['quiz_scores']:
            avg_score = sum(q['accuracy'] for q in self.progress['quiz_scores']) / len(self.progress['quiz_scores'])
            if avg_score < 70:
                print("  - Review topics where you scored low")
                print("  - Take more practice quizzes")
                print("  - Ask for explanations: 'explain [topic]'")
            else:
                print("  - Great job! Try more advanced topics")
                print("  - Help others learn what you know")
        else:
            print("  - Start with basic topics: phishing, passwords, malware")
            print("  - Take quizzes to test your knowledge")
    
    def chat(self):
        """
        Main Conversation Loop
        
        Handles user input and routes to appropriate tools.
        Provides friendly interface for interaction.
        """
        print("\n" + "="*60)
        print("🔐 CYBERSECURITY STUDY ASSISTANT")
        print("="*60)
        print("\nI'm your AI tutor for learning cybersecurity!")
        print("\nWhat I can do:")
        print("  📖 Explain security concepts in simple terms")
        print("  📝 Generate practice quiz questions")
        print("  📊 Track your learning progress")
        print("\nCommands:")
        print("  'explain [topic]' - Learn about a security topic")
        print("  'quiz [topic]'    - Take a practice quiz")
        print("  'progress'        - See your study stats")
        print("  'help'            - Show this message")
        print("  'quit'            - Exit")
        
        # Suggest topics for beginners
        print("\n💡 Popular topics: phishing, passwords, malware, firewalls, encryption")
        
        while True:
            print("\n" + "-"*60)
            user_input = input("\nYou: ").strip().lower()
            
            if user_input == 'quit':
                print("\n👋 Happy studying! Keep learning cybersecurity!")
                break
            
            elif user_input == 'help':
                print("\nCommands:")
                print("  explain [topic] - Learn about any security topic")
                print("  quiz [topic]    - Test your knowledge with a quiz")
                print("  progress        - View your learning statistics")
            
            elif user_input.startswith('explain '):
                topic = user_input.replace('explain ', '').strip()
                print(f"\n🤖 Agent: Let me explain {topic}...\n")
                explanation = self.explain_concept(topic)
                print(explanation)
                print("\n💡 Want to test your knowledge? Try: quiz " + topic)
            
            elif user_input.startswith('quiz '):
                topic = user_input.replace('quiz ', '').strip()
                print(f"\n🤖 Agent: Generating quiz on {topic}...\n")
                quiz_data = self.generate_quiz(topic)
                
                if quiz_data:
                    score, total = self.take_quiz(quiz_data)
                    print(f"\n{'='*60}")
                    print(f"🎯 Final Score: {score}/{total} ({score/total*100:.1f}%)")
                    
                    if score == total:
                        print("🌟 Perfect score! You mastered this topic!")
                    elif score >= total * 0.8:
                        print("🎉 Great job! You understand this well!")
                    elif score >= total * 0.6:
                        print("👍 Good work! Review and try again for higher score.")
                    else:
                        print("📚 Keep studying! Try 'explain " + topic + "' to review.")
                else:
                    print("❌ Sorry, couldn't generate quiz. Try another topic!")
            
            elif user_input == 'progress':
                self.show_progress()
            
            else:
                print("\n❓ I didn't understand that command.")
                print("Try: 'explain phishing', 'quiz passwords', or 'progress'")

# Run the agent
if __name__ == "__main__":
    try:
        agent = SecurityStudyAgent()
        agent.chat()
    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease check:")
        print("  1. .env file exists in the same directory")
        print("  2. .env contains: GOOGLE_API_KEY=your_key_here")
        print("  3. API key is valid (get one at: https://aistudio.google.com/app/apikey)")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

