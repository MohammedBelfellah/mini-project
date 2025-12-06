import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Railway sets PORT, default to 5000 locally
    app.run(host='0.0.0.0', port=port, debug=True)  # debug=True is fine locally





# from app import create_app

# app = create_app()

# if __name__ == '__main__':
#     app.run(debug=True)
