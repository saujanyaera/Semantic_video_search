from flask import Flask, request, jsonify, render_template
from pipeline import final_video_processed
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    print("=== /search called ===")
    print("Files:", request.files)
    print("Form:", request.form)

    video = request.files.get("video")
    query = request.form.get("query")

    if not video:
        return jsonify({"success": False, "message": "Missing video file"}), 400
    if not query:
        return jsonify({"success": False, "message": "Missing query"}), 400

    # Use a unique filename to avoid collisions/spaces in filenames
    ext = os.path.splitext(video.filename)[1] or ".mp4"
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    video_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    video.save(video_path)
    print(f"Video saved to: {video_path}")

    try:
        results = final_video_processed(query, video_path)
        print(f"Pipeline results: {results}")
    except Exception as e:
        print(f"Pipeline error: {e}")
        return jsonify({"success": False, "message": f"Pipeline error: {str(e)}"}), 500
    finally:
        # Clean up uploaded file after processing
        if os.path.exists(video_path):
            os.remove(video_path)

    if not results:
        return jsonify({"success": False, "message": "No match found"})

    best_result = results[0] if isinstance(results, list) else results

    return jsonify({
        "success": True,
        "start_time": best_result["start_time"],
        "end_time": best_result["end_time"]
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)