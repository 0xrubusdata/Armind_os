import re
import json
from app.utils.ollama_runner import ollama_generate
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.DEBUG)  # Configure logging level

def get_general_response(prompt: str) -> dict:
    try:
        logging.debug("DEBUG: Sending prompt to Ollama...")
        # [🇬🇧 DEBUG: Sending prompt to Ollama...] | [🇪🇸 DEPURACIÓN: Enviando prompt a Ollama...] | [🇵🇹 DEPURAÇÃO: Enviando prompt para Ollama...] | [🇯🇵 デバッグ: Ollama にプロンプトを送信中...] | [🇷🇺 ОТЛАДКА: Отправка запроса в Ollama...] | [🇸🇦 تصحيح الأخطاء: إرسال الموجه إلى Ollama...]
        response = ollama_generate("llama3.2", prompt)  # Call to Ollama
        # [🇬🇧 Call to Ollama] | [🇪🇸 Llamada a Ollama] | [🇵🇹 Chamada para Ollama] | [🇯🇵 Ollama への呼び出し] | [🇷🇺 Вызов Ollama] | [🇸🇦 استدعاء Ollama]
        logging.debug("DEBUG: Raw response from Ollama: %s", response)
        # [🇬🇧 DEBUG: Raw response from Ollama: %s] | [🇪🇸 DEPURACIÓN: Respuesta bruta de Ollama: %s] | [🇵🇹 DEPURAÇÃO: Resposta bruta de Ollama: %s] | [🇯🇵 デバッグ: Ollama からの生の応答: %s] | [🇷🇺 ОТЛАДКА: Сырой ответ от Ollama: %s] | [🇸🇦 تصحيح الأخطاء: الاستجابة الأولية من Ollama: %s]
    except Exception as e:
        logging.error("Error during call to Ollama: %s", str(e))
        # [🇬🇧 Error during call to Ollama: %s] | [🇪🇸 Error durante la llamada a Ollama: %s] | [🇵🇹 Erro durante a chamada para Ollama: %s] | [🇯🇵 Ollama への呼び出し中のエラー: %s] | [🇷🇺 Ошибка при вызове Ollama: %s] | [🇸🇦 خطأ أثناء استدعاء Ollama: %s]
        raise HTTPException(status_code=500, detail="Internal error during call to Ollama.")
        # [🇬🇧 Internal error during call to Ollama] | [🇪🇸 Error interno durante la llamada a Ollama] | [🇵🇹 Erro interno durante a chamada para Ollama] | [🇯🇵 Ollama への呼び出し中の内部エラー] | [🇷🇺 Внутренняя ошибка при вызове Ollama] | [🇸🇦 خطأ داخلي أثناء استدعاء Ollama]

    # Check if the response contains an error
    # [🇬🇧 Check if the response contains an error] | [🇪🇸 Verificar si la respuesta contiene un error] | [🇵🇹 Verificar se a resposta contém um erro] | [🇯🇵 応答にエラーが含まれているか確認] | [🇷🇺 Проверить, содержит ли ответ ошибку] | [🇸🇦 التحقق مما إذا كانت الاستجابة تحتوي على خطأ]
    if "error" in response:
        logging.error("Error returned by Ollama: %s", response["error"])
        # [🇬🇧 Error returned by Ollama: %s] | [🇪🇸 Error devuelto por Ollama: %s] | [🇵🇹 Erro retornado por Ollama: %s] | [🇯🇵 Ollama から返されたエラー: %s] | [🇷🇺 Ошибка, возвращенная Ollama: %s] | [🇸🇦 خطأ تم إرجاعه بواسطة Ollama: %s]
        raise HTTPException(status_code=404, detail="Ollama model not found or unreachable.")
        # [🇬🇧 Ollama model not found or unreachable] | [🇪🇸 Modelo de Ollama no encontrado o inalcanzable] | [🇵🇹 Modelo Ollama não encontrado ou inacessível] | [🇯🇵 Ollama モデルが見つからないか、到達不能です] | [🇷🇺 Модель Ollama не найдена или недоступна] | [🇸🇦 لم يتم العثور على نموذج Ollama أو لا يمكن الوصول إليه]

    # Return the cleaned response
    # [🇬🇧 Return the cleaned response] | [🇪🇸 Devolver la respuesta limpia] | [🇵🇹 Retornar a resposta limpa] | [🇯🇵 クリーンな応答を返す] | [🇷🇺 Вернуть очищенный ответ] | [🇸🇦 إرجاع الاستجابة المنظفة]
    return response
