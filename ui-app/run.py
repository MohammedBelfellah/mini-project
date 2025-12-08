import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()  # load local .env

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)



# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
