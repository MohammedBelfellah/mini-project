import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Get the PORT Railway assigns, default to 8000 if not set
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)
