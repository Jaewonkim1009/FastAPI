from fastapi import FastAPI, HTTPException
from analysis import get_customer_analysis, get_sales_analysis, get_marketing_analysis
from fastapi.responses import JSONResponse


# FastAPI 앱 생성
app = FastAPI()

@app.get("/analysis/customer")
def analysis_customer():
    try:
        analysis_results = get_customer_analysis()
        return JSONResponse(content=analysis_results)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code = 500, detail= f"An error occurred: {str(e)}")
    

@app.post("/analysis/sales")
def analysis_sales():
    try:
        analysis_results = get_sales_analysis()
        return JSONResponse(content=analysis_results)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code = 500, detail= f"An error occurred: {str(e)}")

@app.post("/analysis/marketing")
def analysis_marketing():
    try:
        analysis_results = get_marketing_analysis()
        return JSONResponse(content=analysis_results)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code = 500, detail= f"An error occurred: {str(e)}")