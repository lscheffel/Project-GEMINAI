import google.generativeai as genai
import requests
import os
import logging
from utils.config import GOOGLE_API_KEY, DEEPAI_API_KEY

# Configurar logging
logging.basicConfig(level=logging.DEBUG, filename='debug.log', filemode='a', 
                    format='%(asctime)s - %(levelname)s - %(message)s')

genai.configure(api_key=GOOGLE_API_KEY)

def generate_text(prompt):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        logging.info(f"Texto gerado para prompt: {prompt}")
        return response.text
    except Exception as e:
        logging.error(f"Erro Gemini: {str(e)}")
        return f"Erro Gemini: {str(e)}. Verifique a cota da API."

def generate_image(prompt):
    try:
        logging.info(f"Enviando requisição DeepAI para prompt: {prompt}")
        response = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': prompt,
                'image_generator_version': 'standard',
                'width': '512',
                'height': '512'
            },
            headers={'api-key': DEEPAI_API_KEY}
        )
        logging.debug(f"Resposta bruta DeepAI: {response.text}")
        
        if response.status_code != 200:
            logging.error(f"Erro DeepAI: Status {response.status_code} - {response.text}")
            return f"Erro DeepAI: Status {response.status_code} - {response.text}"
        
        result = response.json()
        if 'output_url' in result:
            img_url = result['output_url']
            logging.info(f"URL da imagem: {img_url}")
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                os.makedirs("static/images", exist_ok=True)
                img_path = f"static/images/{prompt[:20].replace(' ', '_')}.png"
                with open(img_path, 'wb') as f:
                    f.write(img_response.content)
                logging.info(f"Imagem salva em: {img_path}")
                return img_path
            else:
                logging.error(f"Erro ao baixar imagem: Status {img_response.status_code}")
                return f"Erro DeepAI: Falha ao baixar imagem (Status {img_response.status_code})"
        else:
            logging.error(f"Erro DeepAI: {result}")
            return f"Erro DeepAI: {result.get('error', 'Resposta inválida da API')}"
    except Exception as e:
        logging.error(f"Exceção DeepAI: {str(e)}")
        return f"Erro DeepAI: {str(e)}"