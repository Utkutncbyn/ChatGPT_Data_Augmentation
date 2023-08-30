from typing import List
import pandas as pd
import io
import re
from fastapi import Depends
from fastapi import UploadFile, File
import openai
from decouple import config

OPENAI_API_KEY = config("OPENAI_API_KEY")

class AugmentationGenerateService(metaclass=Singleton):

    def __init__(self):
        pass

    ##############################
    # FUNCTIONS USED BY CONTROLLER
    ##############################

    def generate(self, payload: AugmentationGenerateDTO):

        generated_items = self.paraphrase_with_gpt(payload.text, num= 10)

        return IResponse({"success": True, "message": "Augmentation generated successfully", "data": generated_items})


    ##############################
    # FUNCTIONS USED BY SERVICE
    ##############################

    def paraphrase_with_gpt(self, text: str, num: int):

        # Get GPT-3 Response
        openai.api_key = OPENAI_API_KEY
        gpt_responses= openai.ChatCompletion.create(
            model= "gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Paraphrase following sentences in Turkish and generate {num} sentences :\n- {text}" # TODO: this can be improved later
            }]
        )

        # Parse GPT-3 Response
        answer = gpt_responses["choices"][0]["message"]["content"]

        sentences = answer.split("\n")
        sentences = sentences[2:] # TODO: this can be removed later

        result = []
        for sentence in sentences:
            # "- Yardım ederek para gönderebilmeme yardımcı olur musunuz?"
            # remove "- " from the beginning of the sentence if exists
            sentence = re.sub(r"^\- ", "", sentence)

            # "1. Yardım ederek para gönderebilmeme yardımcı olur musunuz?"
            # "10. Yardım ederek para gönderebilmeme yardımcı olur musunuz?"
            # remove "1. " or "10. " from the beginning of the sentence if exists
            sentence = re.sub(r"^\d+\.\s", "", sentence)

            if len(sentence) > 1 and sentence not in ["Paraphrased in English:", "Translation:"]: # TODO: this can be improved later
                result.append(sentence)
            else:
                continue

        return result

    def keyword_with_gpt(self, text: str):

        # Get GPT-3 Response
        openai.api_key = OPENAI_API_KEY
        gpt_responses= openai.ChatCompletion.create(
            model= "gpt-3.5-turbo",
            messages=[{
                "role": "user",
                "content": f"Convert following sentences to shortest :\n- {text}" # TODO: this can be improved later
            }]
        )
        # TODO: "Extract key phrases from following sentences:" gibi bir aciklama daha iyi olabilir

        # Parse GPT-3 Response
        answer = gpt_responses["choices"][0]["message"]["content"]

        sentences = answer
        gpt_response = sentences[2:] # TODO: this can be removed later

        keyword_result = []
        unwanted_chars = ['?', '.', '!',":"] # TODO: more char can be added
        response = ""

        for char in gpt_response:
            if char not in unwanted_chars:
                response += char

        keyword_result.append(response)

        return keyword_result
