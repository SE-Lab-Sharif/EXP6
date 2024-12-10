from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Database connection
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        database=os.getenv("DB_NAME", "postgres"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
        cursor_factory=RealDictCursor,
    )


# CRUD Operations
@app.route("/items", methods=["POST"])
def create_item():
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s) RETURNING id, name, description",
            (data["name"], data["description"]),
        )
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(item), 201
    except Exception as e:
        logger.error(f"Error creating item: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/items", methods=["GET"])
def get_items():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(items), 200
    except Exception as e:
        logger.error(f"Error fetching items: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/items/<int:id>", methods=["GET"])
def get_item(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM items WHERE id = %s", (id,))
        item = cur.fetchone()
        cur.close()
        conn.close()
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item), 200
    except Exception as e:
        logger.error(f"Error fetching item: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/items/<int:id>", methods=["PUT"])
def update_item(id):
    try:
        data = request.get_json()
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE items SET name = %s, description = %s WHERE id = %s RETURNING id, name, description",
            (data["name"], data["description"], id),
        )
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify(item), 200
    except Exception as e:
        logger.error(f"Error updating item: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/items/<int:id>", methods=["DELETE"])
def delete_item(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM items WHERE id = %s RETURNING id", (id,))
        item = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if item is None:
            return jsonify({"error": "Item not found"}), 404
        return jsonify({"message": "Item deleted"}), 200
    except Exception as e:
        logger.error(f"Error deleting item: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
