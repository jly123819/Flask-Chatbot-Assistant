from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)
recipes_df = pd.read_csv("cleaned_recipes.csv")

@app.route("/", methods=["GET"])
def home():
    return """
    <h1>🍽️ Welcome to the Recipe Chatbot!</h1>
    <p>To use the chatbot, send a POST request to <code>/chat</code> with a JSON body like:</p>
    <pre>
    {
      "message": "chicken"
    }
    </pre>
    <p>You can use <a href="https://www.postman.com/" target="_blank">Postman</a> or <code>curl</code> to try it out!</p>
    """

def find_recipe(query):
    query = query.lower()
    for _, row in recipes_df.iterrows():
        try:
            ingredients = eval(row['Parsed_Ingredients'])
            if any(query in ingredient.lower() for ingredient in ingredients):
                return {
                    "title": row['Title'],
                    "ingredients": ingredients,
                    "instructions": row['Instructions']
                }
        except:
            continue
    matches = recipes_df[recipes_df['Title'].str.contains(query, case=False, na=False)]
    if not matches.empty:
        recipe = matches.iloc[0]
        return {
            "title": recipe['Title'],
            "ingredients": eval(recipe['Parsed_Ingredients']),
            "instructions": recipe['Instructions']
        }
    return None

SPOONACULAR_API_KEY = "f7e624ecb5e9494b95e31d9b368b1665"

def fetch_from_spoonacular(query):
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "query": query,
        "number": 1,
        "addRecipeInformation": True,
        "apiKey": SPOONACULAR_API_KEY
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            recipe = data["results"][0]
            return {
                "title": recipe["title"],
                "ingredients": [ing["original"] for ing in recipe["extendedIngredients"]],
                "instructions": recipe.get("instructions", "Instructions not available.")
            }
    return None

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    result = find_recipe(user_message)
    if not result:
        result = fetch_from_spoonacular(user_message)
        if not result:
            return jsonify({"response": "Sorry, I couldn't find a recipe for that."})
        response_string = (
        f"Here's a recipe for **{result['title']}**:\n\n"  
        f"**Ingredients:**\n" + "\n".join(result['ingredients']) + "\n\n" 
        f"**Instructions:**\n{result['instructions']}"
    )

    final_response_string = response_string.replace('\\n', '\n')
    
    print(f"Flask repr before jsonify: {repr(final_response_string)}")

    return jsonify({"response": final_response_string})

if __name__ == "__main__":
    app.run(debug=True)
