import json
import re


# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        return json.load(bot_responses)


# Store JSON data
response_data = load_json("bot.json")


def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    curse_words = ("fuck","shit","stupid","idiot")
    for x in curse_words:
        if x in input_string:
            return "Behave!"

    if "say " in input_string:
        say = input_string.replace("say ", '')
        return say.capitalize()

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response["required_words"]

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # print(required_score == len(required_words))
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response["user_input"]:
                    response_score += 1

        # Add score to list
        score_list.append(response_score)
        # Debugging: Find the best phrase
        # print(response_score, response["user_input"])

    # Find the best response and return it if they're not all 0
    best_response = max(score_list)
    response_index = score_list.index(best_response)

    # Check if input is empty
    if input_string == "":
        return "Please type something so we can chat :("

    # If there is no good response, return a random one.
    if best_response != 0:
        return response_data[response_index]["bot_response"]

    if best_response == 0:
        bot_res = input("I don't understand, what should I say?\nYou: ")
        bot_res_list = list(bot_res.split(" "))
        if ["you","should","say"] in bot_res_list:
            bot_res_list.remove("you")
            bot_res_list.remove("should")
            bot_res_list.remove("say")
            bot_res_list = print(" ".join(bot_res_list))

        for x in curse_words:
            if x in bot_res.lower():
                return "Behave! I won't learn from a person like you."
            else:
                filename = "bot.json"
                user = list(input_string.split(" "))
                add = {
                    "user_input": user,
                    "bot_response": bot_res.capitalize(),
                    "required_words": user
                }
                response_data.append(add)
                with open(filename, 'w') as file:
                    json.dump(response_data, file)
                return "Thanks For Teaching Me!"


while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input.lower()))