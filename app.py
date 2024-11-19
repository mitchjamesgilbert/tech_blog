from app import create_app

app = create_app()

if __name__ == "__main__":
    app.config['SECRET_KEY'] = '6c75e9b3c02469fecd9c0e1a69e6edc2d1a72f5f002e3b29'
    app.run(debug=True)
    
