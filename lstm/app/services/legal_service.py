import re
import json
from app.utils.ollama_runner import ollama_generate
from fastapi import HTTPException

def get_legal_response(prompt: str) -> dict:
    """
    Génére une réponse juridique en utilisant le modèle Ollama.
    
    # [🇬🇧 Generates a legal response using the Ollama model.] 
    # [🇪🇸 Genera una respuesta legal utilizando el modelo Ollama.] 
    # [🇵🇹 Gera uma resposta legal usando o modelo Ollama.] 
    # [🇰🇷 Ollama モデルを使用して法的な回答を生成します。] 
    # [🇷🇺 Генерирует юридический ответ с использованием модели Ollama.] 
    # [🇦🇪 يُنشئ استجابة قانونية باستخدام نموذج Ollama.]
    """
    response = ollama_generate("gemma", prompt)

    # Vérifie si une erreur est survenue
    # [🇬🇧 Checks if an error occurred] | [🇪🇸 Comprueba si ha ocurrido un error] | [🇵🇹 Verifica se ocorreu um erro] | [🇰🇷 エラーが発生したかどうかを確認します] | [🇷🇺 Проверяет, произошла ли ошибка] | [🇦🇪 يتحقق مما إذا كان هناك خطأ]
    if "error" in response:
        raise HTTPException(status_code=404, detail="Ollama model not found or unreachable.")

    try:
        # Extraire et nettoyer la réponse attendue
        # [🇬🇧 Extract and clean the expected response] | [🇪🇸 Extraer y limpiar la respuesta esperada] | [🇵🇹 Extrair e limpar a resposta esperada] | [🇰🇷 予期される応答を抽出して清潔化します] | [🇷🇺 Извлекает и очищает ожидаемый ответ] | [🇦🇪 استخراج وتنظيف الاستجابة المتوقعة]
        response_data = json.loads(response.get("response", "{}"))
        return {
            "question": response_data.get("question", "Unknown question"),
            "answer": response_data.get("answer", "No answer available.")
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid response format from Ollama.")
