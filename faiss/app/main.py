from fastapi import FastAPI, HTTPException
from app.services.general_service import get_general_response
from app.services.economic_service import get_economic_response
from app.services.legal_service import get_legal_response

app = FastAPI()

@app.get("/api/general")
def general_endpoint(prompt: str):
    try:
        response = get_general_response(prompt)
        return {"service": "general", "response": response}
    except HTTPException as e:
        # L'exception est propagée avec le bon code (404 ou autre)
        # [🇬🇧 The exception is propagated with the correct code (404 or other)] | [🇪🇸 La excepción se propaga con el código correcto (404 u otro)] | [🇵🇹 A exceção é propagada com o código correto (404 ou outro)] | [🇰🇷 例外は適切なコード (404 またはその他) で伝播されます] | [🇷🇺 Исключение передается с правильным кодом (404 или другим)] | [🇦🇪 يتم نشر الاستثناء برمز صحيح (404 أو غيره)]
        raise e
    except Exception as e:
        # Pour tout autre type d'erreur, renvoyer un statut 500
        # [🇬🇧 For any other type of error, return a 500 status] | [🇪🇸 Para cualquier otro tipo de error, devolver un estado 500] | [🇵🇹 Para qualquer outro tipo de erro, retornar um status 500] | [🇰🇷 その他のエラーに対しては、500 ステータスを返します] | [🇷🇺 Для любого другого типа ошибки вернуть статус 500] | [🇦🇪 لأي نوع آخر من الأخطاء، قم بإرجاع حالة 500]
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/economic")
async def economic_endpoint(prompt: str):
    try:
        response = get_economic_response(prompt)
        return {"service": "economic", "response": response}
    except HTTPException as e:
        # L'exception est propagée avec le bon code (404 ou autre)
        # [🇬🇧 The exception is propagated with the correct code (404 or other)] | [🇪🇸 La excepción se propaga con el código correcto (404 u otro)] | [🇵🇹 A exceção é propagada com o código correto (404 ou outro)] | [🇰🇷 例外は適切なコード (404 またはその他) で伝播されます] | [🇷🇺 Исключение передается с правильным кодом (404 или другим)] | [🇦🇪 يتم نشر الاستثناء برمز صحيح (404 أو غيره)]
        raise e
    except Exception as e:
        # Pour tout autre type d'erreur, renvoyer un statut 500
        # [🇬🇧 For any other type of error, return a 500 status] | [🇪🇸 Para cualquier otro tipo de error, devolver un estado 500] | [🇵🇹 Para qualquer outro tipo de erro, retornar um status 500] | [🇰🇷 その他のエラーに対しては、500 ステータスを返します] | [🇷🇺 Для любого другого типа ошибки вернуть статус 500] | [🇦🇪 لأي نوع آخر من الأخطاء، قم بإرجاع حالة 500]
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/legal")
async def legal_endpoint(prompt: str):
    try:
        response = get_legal_response(prompt)
        return {"service": "legal", "response": response}
    except HTTPException as e:
        # L'exception est propagée avec le bon code (404 ou autre)
        # [🇬🇧 The exception is propagated with the correct code (404 or other)] | [🇪🇸 La excepción se propaga con el código correcto (404 u otro)] | [🇵🇹 A exceção é propagada com o código correto (404 ou outro)] | [🇰🇷 例外は適切なコード (404 またはその他) で伝播されます] | [🇷🇺 Исключение передается с правильным кодом (404 или другим)] | [🇦🇪 يتم نشر الاستثناء برمز صحيح (404 أو غيره)]
        raise e
    except Exception as e:
        # Pour tout autre type d'erreur, renvoyer un statut 500
        # [🇬🇧 For any other type of error, return a 500 status] | [🇪🇸 Para cualquier otro tipo de error, devolver un estado 500] | [🇵🇹 Para qualquer outro tipo de erro, retornar um status 500] | [🇰🇷 その他のエラーに対しては、500 ステータスを返します] | [🇷🇺 Для любого другого типа ошибки вернуть статус 500] | [🇦🇪 لأي نوع آخر من الأخطاء، قم بإرجاع حالة 500]
        raise HTTPException(status_code=500, detail=str(e))
