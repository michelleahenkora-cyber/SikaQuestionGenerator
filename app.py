from flask import Flask, render_template, request
import requests


app = Flask(__name__)


OLLAMA_API_URL = "http://localhost:11434/api/generate"



@app.route("/", methods=["GET", "POST"])
def index():
   generated_questions = ""
   error_message = "" 
    
    
    if request.method == "POST":
        subject= request.form["subject"]
        topic = request.form["topic"]
        difficulty = request.form["difficulty"]
        amount = request.form["amount"]


        ai_prompt = f"""
        Generate exactly {amount} multiple choice quiz questions about subject {subject} and topic {topic}.
        Difficulty level: {difficulty}.

        VERY IMPORTANT RULES:
        - Generate COMPLETE questions only
        - Do NOT use placeholders like "..."
        - Do NOT skip any questions
        - Each question must contain:
        1 question
        4 answer choices
        1 correct answer

        FORMAT EXACTLY LIKE THIS:

        Question 1:
        What is photosynthesis?

        A. Process plants use to make food
        B. Type of animal
        C. A chemical reaction in rocks
        D. Process of evaporation

        Correct Answer: A

        Question 2:
        What is gravity?

        A. Force pulling objects together
        B. Type of energy drink
        C. Speed of light
        D. Plant growth process

        Correct Answer: A

        Now generate the quiz.
        """

        try:
            response = requests.post(
                OLLAMA_API_URL,
                json={"model": "llama3", "prompt": ai_prompt, "stream": False}
            )

            response_data = response.json()

            generated_questions = response_data["response"]
            generated_questions = generated_questions.replace("Generated quiz questions by Sika AI", "")


        except Exception as error:
            error_message = f"An error occurred while generating quiz questions: {error}"
            





            return render_template("index.html", questions=generated_questions, error=error_message)
        

if __name__ == "__main__":
    app.run(debug=True)        