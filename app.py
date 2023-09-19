from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# Endpoint to fetch user data
API_ENDPOINT = "http://127.0.0.1:5000/users"

# Function to fetch user data from the API
def fetch_user_data():
    response = requests.get(API_ENDPOINT)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to add a new user
def add_user(name):
    payload = {"username": name}
    response = requests.post(API_ENDPOINT, json=payload)
    return response.status_code

# Function to update a user
def update_user(user_id, new_name):
    update_endpoint = f"{API_ENDPOINT}/{user_id}"
    payload = {"username": new_name}
    response = requests.put(update_endpoint, json=payload)
    return response.status_code

# Function to delete a user
def delete_user(user_id):
    delete_endpoint = f"{API_ENDPOINT}/{user_id}"
    response = requests.delete(delete_endpoint)
    return response.status_code

# Function to fetch posts for a user
def fetch_user_posts(user_id):
    post_endpoint = f"{API_ENDPOINT}/{user_id}/posts"
    response = requests.get(post_endpoint)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to add a new post for a user
def add_post(user_id, content):
    payload = {"content": content}
    post_endpoint = f"{API_ENDPOINT}/{user_id}/posts"
    response = requests.post(post_endpoint, json=payload)
    return response.status_code

# Function to update a post
def update_post(post_id, new_content):
    update_endpoint = f"{API_ENDPOINT}/posts/{post_id}"
    payload = {"content": new_content}
    response = requests.put(update_endpoint, json=payload)
    return response.status_code

# Function to delete a post
def delete_post(post_id):
    delete_endpoint = f"{API_ENDPOINT}/posts/{post_id}"
    response = requests.delete(delete_endpoint)
    return response.status_code

@app.route('/')
def index():
    # Fetch user data from the API
    user_data = fetch_user_data()
    
    if user_data:
        # Display the data in a table on the webpage
        return render_template('index.html', user_data=user_data)
    else:
        return "Failed to fetch user data from the API."

@app.route('/users', methods=['POST'])
def add_user_route():
    name = request.form['name']

    # Add the user using the API
    status_code = add_user(name)

    if status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Failed to add user."

@app.route('/users/<int:user_id>', methods=['POST'])
def update_user_route(user_id):
    new_name = request.form['new_name']

    # Update the user using the API
    status_code = update_user(user_id, new_name)

    if status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Failed to update user."

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user_route(user_id):

    # Delete the user using the API
    status_code = delete_user(user_id)

    if status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Failed to delete user."

@app.route('/users/<int:user_id>/posts', methods=['GET'])
def view_posts(user_id):
    posts = fetch_user_posts(user_id)
    if posts:
        return render_template('post.html', user_id=user_id, posts=posts)
    else:
        return "Failed to fetch posts for the user."

@app.route('/users/<int:user_id>/posts', methods=['POST'])
def add_post_route(user_id):
    content = request.form['content']

    # Add a post for the user using the API
    status_code = add_post(user_id, content)

    if status_code == 200:
        return render_template('success.html')
    else:
        return "Failed to add post."

@app.route('/posts/<int:post_id>', methods=['POST'])
def update_post_route(post_id):
    new_content = request.form['new_content']

    # Update the post using the API
    status_code = update_post(post_id, new_content)

    if status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Failed to update post."

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post_route(post_id):

    # Delete the post using the API
    status_code = delete_post(post_id)

    if status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Failed to delete post."

if __name__ == '__main__':
    app.run(debug=True, port=5555)
