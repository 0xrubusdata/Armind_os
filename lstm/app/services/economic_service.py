import re
import json
from app.utils.ollama_runner import ollama_generate
from fastapi import HTTPException

def get_economic_response(prompt: str) -> dict:
    """
    Generates an economic response using the Ollama model.
    
    # [🇬🇧 Generates an economic response using the Ollama model.] 
    # [🇪🇸 Genera una respuesta económica utilizando el modelo Ollama.] 
    # [🇵🇹 Gera uma resposta econômica usando o modelo Ollama.] 
    # [🇯🇵 Ollama モデルを使用して経済的な応答を生成します。] 
    # [🇷🇺 Генерирует экономический ответ с использованием модели Ollama.] 
    # [🇸🇦 يُنشئ استجابة اقتصادية باستخدام نموذج Ollama.]
    """
    response = ollama_generate("deepseek-r1:8b", prompt)

    # Check if an error occurred
    # [🇬🇧 Check if an error occurred] | [🇪🇸 Verificar si ocurrió un error] | [🇵🇹 Verificar se ocorreu um erro] | [🇯🇵 エラーが発生したかどうかを確認] | [🇷🇺 Проверить, произошла ли ошибка] | [🇸🇦 التحقق مما إذا كان هناك خطأ]
    if "error" in response:
        raise HTTPException(status_code=404, detail="Ollama model not found or unreachable.")

    try:
        # Extract and clean the expected response
        # [🇬🇧 Extract and clean the expected response] | [🇪🇸 Extraer y limpiar la respuesta esperada] | [🇵🇹 Extrair e limpar a resposta esperada] | [🇯🇵 期待される応答を抽出してクリーンにする] | [🇷🇺 Извлечь и очистить ожидаемый ответ] | [🇸🇦 استخراج وتنظيف الاستجابة المتوقعة]
        response_data = json.loads(response.get("response", "{}"))
        return {
            "question": response_data.get("question", "Unknown question"),
            "answer": response_data.get("answer", "No answer available.")
        }
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid response format from Ollama.")
