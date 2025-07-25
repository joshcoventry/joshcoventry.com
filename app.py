from flask import Flask, render_template

app = Flask(__name__)

app_data = {
    'asset_url': '/static/jc.css',
}

@app.route('/')
def home():
    home_seo = {
        'title': 'Josh Coventry | Software Engineering Manager',
        'description': 'Welcome to my personal website where I share my projects and thoughts.',
        'keywords': 'home, personal, website',
    }
    return render_template('index.html',seo=home_seo)

if __name__ == '__main__':
    app.run(debug=True)