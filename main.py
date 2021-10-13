from flask import Flask, jsonify
from deep_translator import GoogleTranslator
from urllib.parse import urlencode

app = Flask(__name__)

# data class (
#   private val result: String,
#   private private val fromLanguage: String,
#   private val toLanguage,
#   private val srcWord,
#   private val translatorWord
# )

SUCCESS_MARK = "Success"
FAILURE_MARK = "Failure"

RU_LANGUAGE = "ru"
EN_LANGUAGE = "en"

@app.route('/')
def index():
    return "default page"


@app.route('/translate/<string:src_word>')
def translate(src_word):
    try:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", FAILURE_MARK, "", "", "", "")
        else:
            translator_word = GoogleTranslator(source='auto', target='en').translate(src_word)
            return responseAsJson("", SUCCESS_MARK, RU_LANGUAGE, EN_LANGUAGE, src_word, translator_word)
    except Exception as e:
        if isEmpty(src_word):
            return responseAsJson("Field not will be empty", FAILURE_MARK, "", "", "", "")
        else:
            errorMessage = e.message
            return responseByErrorMessage(errorMessage)

def isEmpty(src):
    if src == "\"\"":
        return True
    else:
        return False


def responseAsJson(message, mark, fromLanguage, toLanguage, srcWord, translatorWord):
    return jsonify({
        "message": message,
        "mark": mark,
        "fromLanguage": fromLanguage,
        "toLanguage": toLanguage,
        "srcWord": srcWord,
        "translatorWord": translatorWord
    })


def responseByErrorMessage(message):
    if message == "text must be a valid text with maximum 5000 character, otherwise it cannot be translated":
        return responseAsJson("Not correctly entered word", FAILURE_MARK, "", "", "", "")
    else:
        return responseAsJson("Cannot be translated", FAILURE_MARK, "", "", "", "")


if __name__ == "__main__":
    app.run()

