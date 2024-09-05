from flask import Flask, render_template_string, request, jsonify
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
    <!DOCTYPE html>
<html>
  <head>
    <title>YouTube Video Downloader</title>
    <link rel="icon" href="./download.jpeg">
    <style>
      body {
        font-family: Arial, Sans-Serif, Comic Sans MS;
        margin: 0;
        height: 100vh;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
      }
      button {
        padding: 15px;
        border: none;
        color: #fff;
        border-radius: 4px;
        cursor: pointer;
        background-color: #076c;
      }
      #form {
        width: 100%;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
      }
      #app {
        text-align: center;
      }
      input {
        width: 300px;
        border-radius: 3px;
        outline: none;
        border: none;
        padding: 15px;
      }
      progress {
        width: 100%;
        height: 35px;
        display: none;
      }
    </style>
  </head>
  <body>
    <div id="app">
      <h1>YouTube Video Downloader</h1>
      <p>Welcome to YouTube video downloader for free</p>
      <div id="form">
        <input type="url" id="url" placeholder="Put YouTube URL" required>
        <button id="download">Download</button>
      </div>
      <progress value="0" id="progress"></progress>
    </div>
    <script>
      document.getElementById('download').addEventListener('click', function () {
        const url = document.getElementById('url').value;
        if (!url) {
          alert('Please enter a YouTube URL');
          return;
        }
        fetch('/download', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            alert('Download started');
          } else {
            alert('Error: ' + data.error);
            console.log(data);
          }
        })
        .catch(error => {
          alert('Error: ' + error.message);
        });
      });
    </script>
  </body>
</html>''')

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json()
    print("Received data:", data)  # Add this line for debugging
    url = data.get('url')
    
    if not url:
        return jsonify({'success': False, 'error': 'No URL provided'})
    
    try:
        yt = YouTube(url)
        video = yt.streams.get_highest_resolution()
        video.download()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
