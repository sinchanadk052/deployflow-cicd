from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="DeployFlow CI/CD Demo")

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>DeployFlow</title>
        <style>
            body { font-family: Arial; background: #1e1e2e; color: #cdd6f4; 
                   display: flex; justify-content: center; align-items: center; 
                   height: 100vh; margin: 0; text-align: center; }
            .container { padding: 40px; background: #313244; border-radius: 12px; 
                        box-shadow: 0 4px 12px rgba(0,0,0,0.4); }
            h1 { color: #89b4fa; }
            p { color: #a6adc8; }
            .badge { background: #a6e3a1; color: #1e1e2e; padding: 6px 12px; 
                    border-radius: 20px; font-weight: bold; display: inline-block; 
                    margin-top: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 DeployFlow</h1>
            <p>Automated CI/CD Pipeline on AWS</p>
            <div class="badge">✅ Deployment Successful</div>
            <p style="margin-top: 20px; font-size: 12px;">Built with FastAPI · Docker · GitHub Actions · AWS EC2</p>
        </div>
    </body>
    </html>
    """

@app.get("/health")
def health():
    return {"status": "healthy", "service": "deployflow"}

@app.get("/api/info")
def info():
    return {
        "app": "DeployFlow",
        "version": "1.0.0",
        "stack": ["FastAPI", "Docker", "GitHub Actions", "AWS EC2"]
    }