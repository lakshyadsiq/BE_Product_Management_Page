from app import app
from database import db_manager
from seed_data import seed_sample_data

if __name__ == '__main__':
    try:
        seed_sample_data()
        print("Database initialized successfully")

        print("Starting Flask application...")
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)

    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        db_manager.close_connection()
    except Exception as e:
        print(f"Error starting application: {e}")
        db_manager.close_connection()
