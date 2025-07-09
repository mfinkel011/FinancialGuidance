# -*- coding: utf-8 -*-
"""
Created on Mon Jul  7 13:18:17 2025

@author: A6844
"""
import streamlit as st
import openai
from typing import Dict, List
import time

# Configuration
st.set_page_config(
    page_title="Michael's Consulting - Financial Guidance",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# TODO: Add your OpenAI API key here
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
if OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
    openai.api_key = OPENAI_API_KEY

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .quiz-container {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .question-section {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .question-title {
        color: #667eea;
        font-weight: bold;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        display: block;
    }
    .question-subtitle {
        color: #666;
        font-style: italic;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
    }
    .results-container {
        background: #e8f5e8;
        padding: 1.3rem;
        border-radius: 10px;
        border-left: 4px solid #28a745;
    }
    .debug-container {
        background: #f0f0f0;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
        border: 1px solid #ccc;
    }
    .website-link {
        color: #667eea;
        text-decoration: none;
        font-weight: bold;
    }
    .website-link:hover {
        color: #764ba2;
        text-decoration: underline;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'welcome'
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    if 'financial_guidance' not in st.session_state:
        st.session_state.financial_guidance = ""
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    # =============================================================================
    # DEBUG VARIABLES - REMOVE BEFORE PRODUCTION DEPLOYMENT
    # =============================================================================
   # if 'chatgpt_input' not in st.session_state:
    #    st.session_state.chatgpt_input = ""
    # =============================================================================
    # END DEBUG VARIABLES
    # =============================================================================

def format_quiz_answers(answers: Dict) -> str:
    """Format quiz answers into a clear text summary"""
    summary = "Quiz Response Summary:\n\n"
    
    questions = [
        "What country are you located in?",
        "What are your biggest money goals for the next 10 years?",
        "Do you have any debt with high interest (around 7% or more)?",
        "Are you currently financing or leasing a car?",
        "Are you investing right now?",
        "What types of insurance do you have?",
        "How do you feel about your monthly budget and spending?",
        "Do you have an emergency fund saved up?",
        "How do you feel about your credit cards and rewards?",
        "Are you looking for bonus tips to level up your money game?"
    ]
    
    answered_questions = []
    for i, question in enumerate(questions, 1):
        answer_key = f"q{i}"
        if answer_key in answers and answers[answer_key]:
            answered_questions.append(f"{i}. {question}\n")
            if isinstance(answers[answer_key], list):
                answered_questions.append(f"   Answer: {', '.join(answers[answer_key])}\n")
            else:
                answered_questions.append(f"   Answer: {answers[answer_key]}\n")
            answered_questions.append("\n")
    
    summary += "".join(answered_questions)
    return summary

def get_financial_guidance(quiz_summary: str) -> str:
    """Send quiz summary to OpenAI and get financial guidance"""
    try:
        if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            return """
            **Demo Mode - OpenAI API Key Required**
            
            To get personalized financial guidance, please add your OpenAI API key to the code.
            
            Once configured, GenAI tools will analyze your quiz responses and provide personalized recommendations based on your financial goals, debt management strategies, investment advice tailored to your situation, insurance and emergency fund guidance, and budget optimization tips.
            
            Based on your responses, here are some general recommendations. Emergency funds are crucial - aim to build 3-6 months of expenses in a high-yield savings account. For high-interest debt, prioritize paying off any debt above 7% interest before investing heavily. Consider maxing out Roth IRA and 401(k) contributions for retirement savings. Ensure you have adequate health, disability, and life insurance coverage. For investing, focus on diversified, low-cost index funds for long-term growth.
            
            Your responses are not saved or stored by Michael's Consulting. This assessment is for immediate guidance only.
            
            Reach out to Michael's Consulting for personalized guidance and support at michaels-consulting.com.
            """
        
        prompt = f"""ChatGPT, here is a list of quiz responses to help build a financial guidance summary. Please provide your recommendations in 3-4 cohesive paragraphs rather than bullet points. Use the guidance below as a reference for how to respond to each question, but feel free to add any additional advice you think is relevant. Summarize your recommendations clearly and helpfully. Be empathetic as to how the ideal isn't always doable because of financial constraints. 

IMPORTANT: The user's country is mentioned in the first question. Please provide advice that is relevant to their country's financial system, tax laws, and available investment accounts, while also including relevant USA information where applicable. If they're in the USA, focus primarily on USA advice. If they're in another country, provide country-specific advice first, then mention USA equivalents where relevant.

Always end your response with: 'Reach out to Michael's Consulting for personalized guidance and support at michaels-consulting.com.'

{quiz_summary}

Guidance per question:
1. What country are you located in?
→ Use this information to tailor all subsequent advice to their country's financial system, tax laws, investment accounts, and regulations.

2. What are your biggest money goals for the next 10 years?
If they say buying a house:
→ Start saving in a high-yield savings account (find them online) for your down payment. Set a goal (e.g., 20% down if that's feasible'), and research first-time homebuyer programs.
→ Balance house savings with retirement savings. Don't put all your eggs in the "home" basket.
If they say retirement:
→ Prioritize maxing out retirement accounts like a Roth IRA, 401(k), or HSA. Understand the difference of each.
→ Invest long-term in diversified index funds. Don't get caught up in stock picking.
If they say paying off student loans or other debt:
→ Focus on the highest-interest debt first, then invest more aggressively when it's paid off.
If they say travel, business, etc.:
→ Create a separate savings bucket (short-term savings or conservative investments) outside your retirement accounts.

3. Do you have any debt with high interest (7%+)?
If yes:
→ Focus on paying this down ASAP before heavy investing. Anything over ~6–7% interest likely beats average market returns.
→ Look into refinancing or consolidating options.
If no:
→ Awesome! Now you can build wealth faster through investing or savings goals.

4. Are you financing a car? What kind, what terms, new or used?
If they bought new, long loan (60+ months), high interest:
→ Recommend paying extra toward the loan if the interest rate is high. Consider refinancing. Next time, consider a reliable used car instead.
If they bought used, low interest (~0-4%), short term:
→ That's financially solid. Stick to the payment plan or pay it off early if desired.
If they're leasing:
→ Make sure they understand mileage limits and long-term costs vs. ownership.
Overall, always recommend buying a somewhat used reliable car that a mechanic signs off on.

5. Are you investing? What accounts? Long or short term?
If they say Roth IRA, 401(k), brokerage, long term:
→ Keep it up. Encourage diversified low-cost index funds.
If they only mention short-term trading (crypto, meme stocks, individual stocks):
→ Suggest balancing that with long-term, steady investments like index funds. Short-term plays are riskier. Most people lose money across the board.
If they're not investing yet:
→ Start with something simple like a Roth IRA or a workplace 401(k) if available. Emphasize time in the market and understanding investment tools. Most important thing is to get started.

6. What types of insurance do you have?
If they lack health insurance:
→ This is a priority. Medical debt can wreck finances. Recommend checking marketplace plans. Also consider an HSA for retirement savings which bundles with a HDHP.
If they have no renters/homeowners/car insurance:
→ Recommend basic coverage to protect assets. Also note that state minimums are often highly insufficient.
If they're missing disability or life insurance (especially if they have dependents):
→ Recommend term life insurance and considering disability insurance to protect income.

7. How do you feel about your budget/spending?
If they're on track:
→ Awesome — now optimize. Automate savings, boost investments, fine-tune categories like subscriptions and food spending.
If they're struggling:
→ Recommend tracking spending with an app or spreadsheet for a month. Focus on needs vs. wants. Start with small changes like cutting eating out, subscriptions, etc. People often underestimate their spending.

8. Do you have an emergency fund?
If they have less than 1 month of expenses:
→ Priority #1: Build 3–6 months of expenses in a high yield savings account. Start with a mini goal of $500–$1,000.
If they have 3+ months saved:
→ Good shape! Recommend balancing saving with investing.

9. How do you feel about your credit cards?
If they carry a balance:
→ Pay this off before investing heavily. Credit card interest is brutally high (15%–25%). Consider a balance transfer if needed.
If they pay in full and use for rewards:
→ Perfect. Recommend checking if they're maximizing cashback, travel rewards, or rotating categories.

10. Are you looking for bonus tips?
If yes:
→ Offer tips like:
• Best cashback/travel cards for their situation.
• Switching to a high-yield savings account.
• Automating savings and bill pay.
• Tracking credit scores for free.
• Refer to resources like doctor of credit
If no:
→ Respect that they're happy where they are. Maybe send a tip every now and then just for fun.

Some key recommendations to keep in mind no matter what: Roths are great if you can get one. If not use loopholes like backdoor Roths if you can. Roths have no RMDs and contributions can be taken out so it's a fine place for mid-term savings like 5-15 years, but ideally it's for long term.
If you're doing other things while investing, like buying a house, just remember every year matters, so make investing a priority no matter what.
Also insurance is an important risk management. And use tools that work for you- credit cards are great If you can get rewards but if you are going to overspend, don't get one.
Google sheets is a great tool for money tracking and planning. Or there are apps that can help with that. Always emphasize long term saving- include detailed advice like investing in VOO or FXAIX to track the S&P 500"""

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful financial advisor providing personalized guidance in paragraph form, not bullet points. Tailor your advice to the user's country while also providing relevant USA information where applicable."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"Error generating financial guidance: {str(e)}. Please check your OpenAI API key and try again."

def show_welcome_page():
    """Display the welcome page"""
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Michael's Consulting</h1>
        <h3>Your Partner in Financial Success</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## Welcome to Your Financial Journey! 👋
    
    At **Michael's Consulting**, we believe everyone deserves personalized financial guidance tailored to their unique situation. 
    
    Our quick and comprehensive quiz will help us understand your current financial landscape, goals, and challenges. 
    Based on your responses, you'll receive customized recommendations to help you:
    
    - 🎯 Achieve your biggest financial goals
    - 💳 Manage debt effectively
    - 📈 Optimize your investments
    - 🛡️ Protect yourself with proper insurance
    - 💰 Build a strong financial foundation
    
    The quiz takes just 5-10 minutes and covers the most important aspects of your financial life. 
    Ready to take control of your financial future?
    """)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Get Started", key="get_started", help="Begin your personalized financial assessment"):
            st.session_state.current_page = 'quiz'
            st.rerun()

def show_quiz_page():
    """Display the quiz page with all questions"""
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Michael's Consulting</h1>
        <h3>Financial Assessment Quiz</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="quiz-container">
        <p><strong>Please answer all questions honestly for the most accurate guidance.</strong></p>
        <p>Your responses will be used to generate personalized financial recommendations.</p>
        <p style="font-size: 0.9em; color: #666;">🔒 <em>Privacy Note: Your responses are not saved or stored by Michael's Consulting. This assessment is for immediate guidance only.</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize answers from session state
    answers = st.session_state.quiz_answers
    
    # Question 1 - Country
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">1. What country are you located in?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">This helps us provide relevant financial advice for your region.</div>', unsafe_allow_html=True)
    
    q1 = st.text_input(
        label="Enter your country",
        key="q1",
        placeholder="e.g., United States, Canada, United Kingdom, etc.",
        label_visibility="collapsed",
        value=answers.get('q1', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 2
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">2. What are your biggest money goals for the next 10 years?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Examples: buying a home, saving for retirement, traveling more, starting a business, paying off student loans, etc.</div>', unsafe_allow_html=True)
    q2 = st.text_area(
        label="Financial goals",
        key="q2", 
        height=100, 
        placeholder="Describe your financial goals...", 
        label_visibility="collapsed", 
        value=answers.get('q2', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 3
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">3. Do you have any debt with high interest (around 7% or more)?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Roughly how much do you owe, and what type of debt is it? (Examples: credit cards, personal loans, student loans)</div>', unsafe_allow_html=True)
    q3 = st.text_area(
        label="High interest debt",
        key="q3", 
        height=100, 
        placeholder="Describe your high-interest debt...", 
        label_visibility="collapsed", 
        value=answers.get('q3', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 4
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">4. Are you currently financing or leasing a car?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">If yes, what kind of car is it? Did you buy it new or used? What are your monthly payments and interest rate?</div>', unsafe_allow_html=True)
    q4 = st.text_area(
        label="Car financing",
        key="q4", 
        height=100, 
        placeholder="Describe your car financing situation...", 
        label_visibility="collapsed", 
        value=answers.get('q4', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 5
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">5. Are you investing right now?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">What kinds of accounts do you have? (Examples: Roth IRA, 401(k), brokerage account, crypto, etc.)<br>Are you investing long term (5+ years) or short term?</div>', unsafe_allow_html=True)
    q5 = st.text_area(
        label="Investment accounts",
        key="q5", 
        height=100, 
        placeholder="Describe your investment accounts and strategy...", 
        label_visibility="collapsed", 
        value=answers.get('q5', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 6
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">6. What types of insurance do you have?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Check all that apply or list what you have:</div>', unsafe_allow_html=True)
    
    insurance_options = [
        "Health", "Dental", "Vision", "Disability", 
        "Life", "Car", "Renters/Homeowners", "Other"
    ]
    
    q6 = st.multiselect(
        label="Insurance types",
        options=insurance_options, 
        key="q6", 
        label_visibility="collapsed", 
        default=answers.get('q6', [])
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 7
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">7. How do you feel about your monthly budget and spending?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Are you staying on track, struggling, or somewhere in between?</div>', unsafe_allow_html=True)
    q7 = st.text_area(
        label="Budget and spending",
        key="q7", 
        height=100, 
        placeholder="Describe your budgeting situation...", 
        label_visibility="collapsed", 
        value=answers.get('q7', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 8
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">8. Do you have an emergency fund saved up?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Roughly how many months of expenses could you cover if your income stopped?</div>', unsafe_allow_html=True)
    q8 = st.text_area(
        label="Emergency fund",
        key="q8", 
        height=100, 
        placeholder="Describe your emergency fund...", 
        label_visibility="collapsed", 
        value=answers.get('q8', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 9
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">9. How do you feel about your credit cards?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Are you paying them in full each month, carrying a balance, or using them for rewards?</div>', unsafe_allow_html=True)
    q9 = st.text_area(
        label="Credit cards",
        key="q9", 
        height=100, 
        placeholder="Describe your credit card usage...", 
        label_visibility="collapsed", 
        value=answers.get('q9', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Question 10
    #st.markdown('<div class="question-section">', unsafe_allow_html=True)
    st.markdown('<div class="question-title">10. Are you looking for bonus tips to level up your money game?</div>', unsafe_allow_html=True)
    st.markdown('<div class="question-subtitle">Example topics: Winning with credit card rewards, Optimizing savings accounts, Automating your finances, Smart ways to cut bills</div>', unsafe_allow_html=True)
    q10 = st.text_area(
        label="Bonus tips",
        key="q10", 
        height=100, 
        placeholder="What additional topics interest you?", 
        label_visibility="collapsed", 
        value=answers.get('q10', '')
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📋 Submit Quiz", key="submit_quiz", help="Generate your personalized financial guidance"):
            # Collect all answers
            current_answers = {
                'q1': q1, 'q2': q2, 'q3': q3, 'q4': q4, 'q5': q5,
                'q6': q6, 'q7': q7, 'q8': q8, 'q9': q9, 'q10': q10
            }
            
            # Store answers in session state
            st.session_state.quiz_answers = current_answers
            
            # Check if at least some questions are answered
            answered_questions = sum(1 for key, value in current_answers.items() if value)
            
            if answered_questions < 3:
                st.error("Please answer at least 3 questions to receive meaningful guidance.")
            else:
                with st.spinner("Generating your personalized financial guidance..."):
                    quiz_summary = format_quiz_answers(current_answers)
                    # =============================================================================
                    # DEBUG LINE - REMOVE BEFORE PRODUCTION DEPLOYMENT
                    # =============================================================================
                    #st.session_state.chatgpt_input = quiz_summary  # Store for debugging
                    # =============================================================================
                    # END DEBUG LINE
                    # =============================================================================
                    guidance = get_financial_guidance(quiz_summary)
                    st.session_state.financial_guidance = guidance
                    st.session_state.quiz_submitted = True
                    st.session_state.current_page = 'results'
                    st.rerun()
    
    # Back to welcome button
    if st.button("← Back to Welcome", key="back_to_welcome"):
        st.session_state.current_page = 'welcome'
        st.rerun()

def show_results_page():
    """Display the results page with financial guidance"""
    # Scroll to top of page when results load

    st.markdown("""
        <script>
            window.scrollTo({ top: 0, behavior: 'smooth' });
        </script>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
    <div class="main-header">
        <h1>🏦 Michael's Consulting</h1>
        <h3>Your Personalized Financial Guidance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="results-container">
        <h2>🎉 Thank you for completing the assessment!</h2>
        <p>Based on your responses, here's your personalized financial guidance:</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display the financial guidance
    st.markdown("") 
    st.markdown(st.session_state.financial_guidance)
    
    # =============================================================================
    # DEBUG SECTION - REMOVE THIS ENTIRE SECTION BEFORE PRODUCTION DEPLOYMENT
    # =============================================================================
    # Debug section for testing
    #st.markdown("---")
   # with st.expander("🔍 Debug: View ChatGPT Input (For Testing)"):
       # st.markdown('<div class="debug-container">', unsafe_allow_html=True)
      #  st.markdown("**Information sent to ChatGPT:**")
     #   st.text(st.session_state.chatgpt_input)
    #    st.markdown('</div>', unsafe_allow_html=True)
    # =============================================================================
    # END DEBUG SECTION
    # =============================================================================
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Back to Quiz", key="back_to_quiz"):
            st.session_state.current_page = 'quiz'
            st.rerun()
    
    with col2:
        if st.button("🏠 Back to Home", key="back_to_home"):
            st.session_state.current_page = 'welcome'
            st.rerun()
    
    # Contact information
    st.markdown("""
    ---
    
    <div style="text-align: center; font-size: 1em; font-weight: bold; margin: 20px 0;">
    Your personalized guidance is displayed above
    </div>
    
    ### 📞 Ready for More Personalized Support?
    
    This AI powered guidance is just the beginning. For comprehensive financial planning, 
    debt strategies, investment advice, and ongoing support, reach out to **Michael's Consulting** 
    at <a href="https://michaels-consulting.com" target="_blank" class="website-link">michaels-consulting.com</a>.
    
    Our team is ready to help you achieve your financial goals!
    
    *🔒 Privacy Note: Your quiz responses were not saved or stored by Michael's Consulting. This assessment was for immediate guidance only.*
    
    <div style="text-align: center; font-size: .8em; font-weight: bold; margin: 20px 0;">
    Your personalized guidance is displayed above
    </div>
    
    """, unsafe_allow_html=True)

def main():
    """Main application function"""
    initialize_session_state()
    
    # Navigation based on current page
    if st.session_state.current_page == 'welcome':
        show_welcome_page()
    elif st.session_state.current_page == 'quiz':
        show_quiz_page()
    elif st.session_state.current_page == 'results':
        show_results_page()
    
    # Footer
    st.markdown("""
    ---
    <div style="text-align: center; color: #666; font-size: 0.9em;">
        <p>© 2025 Michael's Consulting. All rights reserved.</p>
        <p>Visit us at <a href="https://michaels-consulting.com" target="_blank" class="website-link">michaels-consulting.com</a></p>
        <p style="font-size: 0.8em; margin-top: 10px;">🔒 Your quiz responses are not saved or stored by Michael's Consulting</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
