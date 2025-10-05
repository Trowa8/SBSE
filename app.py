from flask import Flask, request, render_template, redirect, url_for
import csv
from math import ceil

app = Flask(__name__)


experiments = []
with open("SB_publication_PMC.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    headers = [h.strip().lower() for h in reader.fieldnames]

    title_key = None
    link_key = None
    for h in headers:
        if "title" in h or "назв" in h:
            title_key = h
        if "link" in h or "ссыл" in h or "url" in h:
            link_key = h

    for row in reader:
        experiments.append({
            "title": row[title_key].strip(),
            "link": row[link_key].strip()
        })


@app.route("/", methods=["GET", "POST"])
def search():
    query = request.form.get("query", request.args.get("query", "")).lower().strip()
    page = int(request.args.get('page', 1))

    results = [exp for exp in experiments if query in exp["title"].lower()]

    if len(results) == 1 and request.method == "POST":
        return redirect(results[0]["link"])

    per_page = 20
    total_results = len(results)
    total_pages = ceil(total_results / per_page) if total_results > 0 else 1
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    return render_template("index.html", results=paginated_results, query=query, page=page, total_pages=total_pages, total_results=total_results)


@app.route("/open/<int:item_id>")
def open_link(item_id):

    return redirect(experiments[item_id]["link"])


if __name__ == "__main__":
    app.run(debug=True)
