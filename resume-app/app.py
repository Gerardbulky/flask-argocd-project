from flask import Flask, render_template,request, abort
import os
import markdown

app = Flask(__name__)

# Define the static path for the README files
static_dir = os.path.join(app.root_path, "static", "readme-folder")

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/readme/<filename>")
def readme(filename):
    # Sanitize the filename to prevent directory traversal attacks
    safe_filename = os.path.basename(filename)
    readme_path = os.path.join(static_dir, safe_filename)

    try:
        # Read the specified README file
        with open(readme_path, "r") as file:
            content = file.read()
        
        # Convert Markdown to HTML
        html_content = markdown.markdown(content, extensions=["fenced_code", "codehilite"])

        # Replace relative image paths with static paths for different markdown files
        if filename == "from-code-to-k8s.md":
            html_content = html_content.replace('src="images/from-code-to-k8s-images/images/', 'src="/static/from-code-to-k8s-images/images/')
        else:
            html_content = html_content.replace('src="images/', 'src="/static/readme-images/images/')
        
        # Render the HTML in a template
        return render_template("readme.html", content=html_content)
    except FileNotFoundError:
        return abort(404, description="README file not found")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)