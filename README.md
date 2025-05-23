# 🥘 Recipe Chatbot Assistant

This project is a Discord-integrated chatbot built with **Flask** and **Python** that allows users to search for recipes using either a local CSV dataset or the **Spoonacular API**. It includes a fully functional Flask backend, an ETL preprocessing step, and a Discord bot for interaction.

## 👥 Team Members
Jessica Xiong\
Lingyue Ji

## 💡 Features

- Search for recipes by ingredient or keyword
- Retrieves from a cleaned dataset (`cleaned_recipes.csv`)
- Falls back to Spoonacular API for real-time results
- Integrated Discord bot for interactive chat
- Deployed on Google Cloud App Engine
- Handles long responses and newline formatting issues

---

## 🗂️ Project Structure

📁 ds_project2/ │ ├── app.yaml # GCP deployment config ├── cleaned_recipes.csv # Cleaned dataset ├── etl_recipes.py # Script for cleaning the raw 13k recipe dataset ├── main.py # Flask backend ├── discord_basic.py # Discord bot logic ├── requirements.txt # All dependencies ├── README.md # This file └── .gcloudignore


---

## 🧪 Live Demo

You can try the deployed Flask chatbot at:  
🔗 [https://flask-chatbot-457918.ue.r.appspot.com](https://flask-chatbot-457918.ue.r.appspot.com)

## 💬 Try It on Discord (Optional)

Want to see the bot live in action?  
Join our test server here: [Join RecipeBot Discord](https://discord.gg/q9KwwWZx)

*Note: The bot must be running for the command `!recipe <ingredient>` to respond.*

### How to use:

Send a `POST` request to `/chat` with a JSON body like:

```json
{
  "message": "chicken"
}

You can test with:
curl -X POST https://flask-chatbot-457918.ue.r.appspot.com/chat \
-H "Content-Type: application/json" \
-d '{"message": "chicken"}'



