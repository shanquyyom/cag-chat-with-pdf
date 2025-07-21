from fastapi import FastAPI
from src.routers import data_handler
from fastapi.responses import HTMLResponse


app = FastAPI(
    title = "CAG Project API Chat With Your PDF",
    description = "API for uploading PDFs, quering content via LLM, and managing data.",
    version = "0.1.0"
)


app.include_router(
    data_handler.router,
    prefix = "/api/v1",
    tags = ["Data Handling AND Chat With PDF"],
)


@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    """Provide a simple HTML Welcome page with a link to the Swagger (OpenAI)"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CAG Project API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                padding: 2rem;
                background: #f9f9f9;
            }
            .container {
                max-width: 600px;
                margin: auto;
                background: #fff;
                padding: 2rem;
                border: 1px solid #ddd;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }
            h1 { color: #333; }
            a {
                color: #007acc;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to the CAG Project API</h1>
            <p>👉 View the automatically generated API documentation here:</p>
            <p>
                <a href="/docs" target="_blank">Swagger UI (OpenAI Docs)</a>
            </p>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content, status_code=200)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)