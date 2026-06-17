import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "users.csv"
HTML_PATH = ROOT / "index.html"


def load_users():
    with CSV_PATH.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def build_rows(users):
    return "\n".join(
        f"""      <tr>
        <td>{u["이름"]}</td>
        <td>{u["지역"]}</td>
        <td>{u["성별"]}</td>
        <td>{u["나이"]}</td>
      </tr>"""
        for u in users
    )


def generate_html(users):
  rows = build_rows(users)
  return f"""<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>사용자 정보 테이블</title>
  <style>
    body {{
      font-family: "Malgun Gothic", sans-serif;
      max-width: 800px;
      margin: 40px auto;
      padding: 0 20px;
      color: #333;
    }}
    h1 {{
      text-align: center;
      margin-bottom: 8px;
    }}
    .actions {{
      text-align: center;
      margin-bottom: 24px;
    }}
    .actions a {{
      color: #4a90d9;
      text-decoration: none;
      font-weight: bold;
    }}
    .actions a:hover {{
      text-decoration: underline;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}
    th, td {{
      border: 1px solid #ddd;
      padding: 12px 16px;
      text-align: center;
    }}
    th {{
      background-color: #4a90d9;
      color: #fff;
    }}
    tr:nth-child(even) {{
      background-color: #f9f9f9;
    }}
    tr:hover {{
      background-color: #f0f4ff;
    }}
  </style>
</head>
<body>
  <h1>사용자 정보</h1>
  <p class="actions"><a href="form.html">+ 새 사용자 추가</a></p>
  <table>
    <thead>
      <tr>
        <th>이름</th>
        <th>지역</th>
        <th>성별</th>
        <th>나이</th>
      </tr>
    </thead>
    <tbody>
{rows}
    </tbody>
  </table>
</body>
</html>
"""


def main():
    users = load_users()
    HTML_PATH.write_text(generate_html(users), encoding="utf-8")
    print(f"Generated {HTML_PATH} with {len(users)} users.")


if __name__ == "__main__":
    main()
