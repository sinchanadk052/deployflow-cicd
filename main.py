from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import requests
from datetime import datetime

app = FastAPI(
    title="GitHub Profile Card API",
    description="Fetch and display beautiful GitHub profile cards",
    version="1.0.0"
)

GITHUB_API_BASE = "https://api.github.com"


# ============ HTML Page ============

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Profile Card</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            min-height: 100vh;
            background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #1f2937 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
            color: #e6edf3;
        }
        
        .container {
            width: 100%;
            max-width: 600px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .logo {
            font-size: 48px;
            margin-bottom: 10px;
        }
        
        h1 {
            font-size: 32px;
            font-weight: 700;
            background: linear-gradient(135deg, #58a6ff 0%, #a371f7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
        }
        
        .subtitle {
            color: #8b949e;
            font-size: 14px;
        }
        
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            background: #161b22;
            padding: 8px;
            border-radius: 12px;
            border: 1px solid #30363d;
        }
        
        .search-input {
            flex: 1;
            padding: 12px 16px;
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            color: #e6edf3;
            font-size: 16px;
            outline: none;
            transition: border 0.2s;
        }
        
        .search-input:focus {
            border-color: #58a6ff;
        }
        
        .search-btn {
            padding: 12px 24px;
            background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .search-btn:hover { transform: translateY(-1px); }
        .search-btn:active { transform: translateY(0); }
        .search-btn:disabled { opacity: 0.6; cursor: not-allowed; }
        
        .card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
            display: none;
            animation: fadeIn 0.4s ease-out;
        }
        
        .card.visible { display: block; }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .profile-top {
            display: flex;
            gap: 20px;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .avatar {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid #30363d;
        }
        
        .profile-info h2 {
            font-size: 24px;
            margin-bottom: 4px;
        }
        
        .username {
            color: #8b949e;
            font-size: 16px;
            margin-bottom: 8px;
        }
        
        .bio {
            color: #c9d1d9;
            font-size: 14px;
            line-height: 1.5;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 20px;
        }
        
        .stat {
            background: #0d1117;
            padding: 16px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #30363d;
        }
        
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            color: #58a6ff;
            margin-bottom: 4px;
        }
        
        .stat-label {
            font-size: 11px;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .meta-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 20px;
            padding: 16px;
            background: #0d1117;
            border-radius: 10px;
            border: 1px solid #30363d;
        }
        
        .meta-item {
            font-size: 13px;
            color: #c9d1d9;
        }
        
        .meta-icon {
            margin-right: 6px;
        }
        
        .meta-label {
            color: #8b949e;
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }
        
        .repos-section {
            margin-top: 20px;
        }
        
        .section-title {
            font-size: 14px;
            color: #8b949e;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            font-weight: 600;
        }
        
        .repo {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 10px;
            padding: 14px;
            margin-bottom: 10px;
            transition: border 0.2s;
        }
        
        .repo:hover { border-color: #58a6ff; }
        
        .repo-name {
            color: #58a6ff;
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 6px;
            text-decoration: none;
            display: inline-block;
        }
        
        .repo-name:hover { text-decoration: underline; }
        
        .repo-desc {
            color: #8b949e;
            font-size: 12px;
            margin-bottom: 8px;
            line-height: 1.4;
        }
        
        .repo-meta {
            display: flex;
            gap: 12px;
            font-size: 11px;
            color: #8b949e;
        }
        
        .repo-meta span {
            display: flex;
            align-items: center;
            gap: 4px;
        }
        
        .lang-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #58a6ff;
        }
        
        .profile-link {
            display: block;
            text-align: center;
            padding: 12px;
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 8px;
            color: #58a6ff;
            text-decoration: none;
            font-weight: 600;
            margin-top: 16px;
            transition: background 0.2s;
        }
        
        .profile-link:hover { background: #30363d; }
        
        .loader {
            text-align: center;
            padding: 40px;
            color: #8b949e;
            display: none;
        }
        
        .loader.visible { display: block; }
        
        .spinner {
            display: inline-block;
            width: 30px;
            height: 30px;
            border: 3px solid #30363d;
            border-top-color: #58a6ff;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 10px;
        }
        
        @keyframes spin { to { transform: rotate(360deg); } }
        
        .error {
            background: rgba(248, 81, 73, 0.1);
            border: 1px solid #f85149;
            color: #ffa198;
            padding: 16px;
            border-radius: 10px;
            display: none;
            text-align: center;
        }
        
        .error.visible { display: block; }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #6e7681;
            font-size: 12px;
        }
        
        .footer a {
            color: #58a6ff;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🐙</div>
            <h1>gitHub Profile Card</h1>
            <p class="subtitle">Discover any developer's GitHub profile</p>
        </div>
        
        <div class="search-box">
            <input 
                type="text" 
                id="usernameInput" 
                class="search-input" 
                placeholder="Enter GitHub username (e.g., torvalds)"
                value="torvalds"
            >
            <button id="searchBtn" class="search-btn" onclick="fetchProfile()">Search</button>
        </div>
        
        <div id="loader" class="loader">
            <div class="spinner"></div>
            <div>Fetching profile...</div>
        </div>
        
        <div id="error" class="error"></div>
        
        <div id="card" class="card">
            <div class="profile-top">
                <img id="avatar" class="avatar" src="" alt="avatar">
                <div class="profile-info">
                    <h2 id="name">Name</h2>
                    <div class="username" id="username">@username</div>
                    <div class="bio" id="bio"></div>
                </div>
            </div>
            
            <div class="stats-grid">
                <div class="stat">
                    <div class="stat-value" id="repos">0</div>
                    <div class="stat-label">Repos</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="followers">0</div>
                    <div class="stat-label">Followers</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="following">0</div>
                    <div class="stat-label">Following</div>
                </div>
            </div>
            
            <div class="meta-info">
                <div>
                    <div class="meta-label">Location</div>
                    <div class="meta-item" id="location">—</div>
                </div>
                <div>
                    <div class="meta-label">Joined</div>
                    <div class="meta-item" id="joined">—</div>
                </div>
                <div>
                    <div class="meta-label">Company</div>
                    <div class="meta-item" id="company">—</div>
                </div>
                <div>
                    <div class="meta-label">Blog</div>
                    <div class="meta-item" id="blog">—</div>
                </div>
            </div>
            
            <div class="repos-section">
                <div class="section-title">Top Repositories</div>
                <div id="reposList"></div>
            </div>
            
            <a id="profileLink" class="profile-link" target="_blank">View Full Profile on GitHub →</a>
        </div>
        
        <div class="footer">
            Built with FastAPI · <a href="/docs">API Docs</a> · Deployed on AWS EC2
        </div>
    </div>
    
    <script>
        const input = document.getElementById('usernameInput');
        const btn = document.getElementById('searchBtn');
        const loader = document.getElementById('loader');
        const card = document.getElementById('card');
        const errorEl = document.getElementById('error');
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') fetchProfile();
        });
        
        async function fetchProfile() {
            const username = input.value.trim();
            if (!username) return;
            
            btn.disabled = true;
            loader.classList.add('visible');
            card.classList.remove('visible');
            errorEl.classList.remove('visible');
            
            try {
                const res = await fetch(`/api/profile/${username}`);
                const data = await res.json();
                
                if (!res.ok) {
                    throw new Error(data.detail || 'User not found');
                }
                
                renderCard(data);
            } catch (err) {
                errorEl.textContent = '❌ ' + err.message;
                errorEl.classList.add('visible');
            } finally {
                btn.disabled = false;
                loader.classList.remove('visible');
            }
        }
        
        function renderCard(data) {
            document.getElementById('avatar').src = data.avatar_url;
            document.getElementById('name').textContent = data.name || data.username;
            document.getElementById('username').textContent = '@' + data.username;
            document.getElementById('bio').textContent = data.bio || 'No bio provided';
            document.getElementById('repos').textContent = data.public_repos;
            document.getElementById('followers').textContent = formatNum(data.followers);
            document.getElementById('following').textContent = formatNum(data.following);
            document.getElementById('location').textContent = data.location || '—';
            document.getElementById('joined').textContent = data.joined || '—';
            document.getElementById('company').textContent = data.company || '—';
            document.getElementById('blog').textContent = data.blog || '—';
            document.getElementById('profileLink').href = data.profile_url;
            
            const reposList = document.getElementById('reposList');
            reposList.innerHTML = '';
            
            if (data.top_repos && data.top_repos.length > 0) {
                data.top_repos.forEach(repo => {
                    const repoEl = document.createElement('div');
                    repoEl.className = 'repo';
                    repoEl.innerHTML = `
                        <a href="${repo.url}" target="_blank" class="repo-name">${repo.name}</a>
                        <div class="repo-desc">${repo.description || 'No description'}</div>
                        <div class="repo-meta">
                            ${repo.language ? `<span><span class="lang-dot"></span> ${repo.language}</span>` : ''}
                            <span>⭐ ${formatNum(repo.stars)}</span>
                            <span>🍴 ${formatNum(repo.forks)}</span>
                        </div>
                    `;
                    reposList.appendChild(repoEl);
                });
            } else {
                reposList.innerHTML = '<div style="color: #8b949e; text-align: center; padding: 20px;">No public repositories</div>';
            }
            
            card.classList.add('visible');
        }
        
        function formatNum(n) {
            if (n >= 1000000) return (n / 1000000).toFixed(1) + 'M';
            if (n >= 1000) return (n / 1000).toFixed(1) + 'K';
            return n.toString();
        }
        
        // Auto-load default user on page load
        window.addEventListener('DOMContentLoaded', () => fetchProfile());
    </script>
</body>
</html>
"""


# ============ Routes ============

@app.get("/", response_class=HTMLResponse, tags=["UI"])
def home():
    """Renders the GitHub profile card UI."""
    return HTML_PAGE


@app.get("/api/profile/{username}", tags=["API"])
def get_profile(username: str):
    """
    Fetches a GitHub user profile and their top repositories.
    
    - **username**: GitHub username (e.g., 'torvalds')
    
    Returns user info, stats, and top 5 repositories sorted by stars.
    """
    try:
        # Fetch user profile
        user_res = requests.get(f"{GITHUB_API_BASE}/users/{username}", timeout=10)
        
        if user_res.status_code == 404:
            raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found")
        
        if user_res.status_code == 403:
            raise HTTPException(status_code=429, detail="GitHub API rate limit reached. Try again in an hour.")
        
        user_res.raise_for_status()
        user = user_res.json()
        
        # Fetch top repos
        repos_res = requests.get(
            f"{GITHUB_API_BASE}/users/{username}/repos",
            params={"sort": "updated", "per_page": 100},
            timeout=10
        )
        repos_res.raise_for_status()
        repos = repos_res.json()
        
        # Sort by stars and take top 5
        top_repos = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:5]
        
        # Format joined date nicely
        joined_str = "—"
        if user.get("created_at"):
            try:
                dt = datetime.fromisoformat(user["created_at"].replace("Z", "+00:00"))
                joined_str = dt.strftime("%b %Y")
            except:
                pass
        
        return {
            "username": user.get("login"),
            "name": user.get("name"),
            "bio": user.get("bio"),
            "avatar_url": user.get("avatar_url"),
            "profile_url": user.get("html_url"),
            "location": user.get("location"),
            "company": user.get("company"),
            "blog": user.get("blog"),
            "public_repos": user.get("public_repos", 0),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "joined": joined_str,
            "top_repos": [
                {
                    "name": r.get("name"),
                    "description": r.get("description"),
                    "url": r.get("html_url"),
                    "stars": r.get("stargazers_count", 0),
                    "forks": r.get("forks_count", 0),
                    "language": r.get("language"),
                }
                for r in top_repos
            ]
        }
    
    except HTTPException:
        raise
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"GitHub API unavailable: {str(e)}")


@app.get("/health", tags=["Monitoring"])
def health():
    """Health check endpoint."""
    return {"status": "healthy", "service": "github-profile-card"}


@app.get("/api/info", tags=["API"])
def info():
    """Returns API metadata."""
    return {
        "app": "GitHub Profile Card",
        "version": "1.0.0",
        "description": "Fetch and display GitHub profile information",
        "endpoints": {
            "/": "Web UI",
            "/api/profile/{username}": "Get profile data as JSON",
            "/health": "Health check",
            "/docs": "Auto-generated API docs"
        },
        "tech_stack": ["FastAPI", "Docker", "AWS EC2", "GitHub Actions"]
    }