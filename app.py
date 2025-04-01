from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__, template_folder="templates")

# Load the JSON data once at startup
with open("moddalar_baza.json", encoding='utf-8') as f:
    data = json.load(f)

def find_matches(query):
    query = query.lower()
    results = []
    for item in data:
        if (query in item['nomi'].lower() or
            query in item['lotincha_nomi'].lower() or
            query in item['inn_taxminiy'].lower()):
            results.append({
                'nomi': item['nomi'],
                'guruh': item['guruh']
            })
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify([])
    results = find_matches(query)
    return jsonify(results)

if __name__ == '__main__':
    os.makedirs("templates", exist_ok=True)
    with open("templates/index.html", "w", encoding='utf-8') as f:
        f.write("""<!DOCTYPE html>
<html lang=\"uz\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>Taqiqlangan Modda Qidiruvi</title>
    <style>
        body { font-family: sans-serif; padding: 20px; }
        input { padding: 10px; width: 300px; font-size: 16px; }
        .result { margin-top: 20px; }
        .item { margin-bottom: 10px; padding: 10px; border: 1px solid #ccc; border-radius: 8px; }
    </style>
</head>
<body>
    <h1>Taqiqlangan Moddalarni Qidirish</h1>
    <input type=\"text\" id=\"query\" placeholder=\"Modda nomini kiriting...\">
    <div class=\"result\" id=\"result\"></div>

    <script>
        const input = document.getElementById('query');
        const resultDiv = document.getElementById('result');

        input.addEventListener('input', async () => {
            const query = input.value.trim();
            if (!query) {
                resultDiv.innerHTML = '';
                return;
            }
            const res = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const data = await res.json();
            resultDiv.innerHTML = data.length
                ? data.map(item => `<div class='item'><strong>${item.nomi}</strong><br>${item.guruh}</div>`).join('')
                : '<p>Hech narsa topilmadi</p>';
        });
    </script>
</body>
</html>""")
    app.run(debug=True)
