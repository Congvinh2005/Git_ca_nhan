from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

HOST = "0.0.0.0"
PORT = 10000000


def render_chart_page(nam=0, nu=0):
    nam = max(0, int(nam))
    nu = max(0, int(nu))
    max_value = max(nam, nu, 1)

    nam_height = int((nam / max_value) * 100)
    nu_height = int((nu / max_value) * 100)

    html = f"""
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Thống kê sinh viên</title>
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #f5f7ff, #e9f7ef);
                color: #1f2937;
            }}
            .container {{
                max-width: 800px;
                margin: 40px auto;
                background: rgba(255,255,255,0.9);
                padding: 30px 24px;
                border-radius: 18px;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
            }}
            h1 {{
                text-align: center;
                color: #111827;
                margin-bottom: 24px;
            }}
            form {{
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 16px;
                margin-bottom: 30px;
            }}
            .input-box {{
                display: flex;
                flex-direction: column;
                gap: 8px;
                min-width: 180px;
            }}
            label {{
                font-weight: 600;
                color: #374151;
            }}
            input {{
                padding: 12px 14px;
                font-size: 16px;
                border: 1px solid #cbd5e1;
                border-radius: 10px;
                outline: none;
            }}
            input:focus {{
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59,130,246,0.15);
            }}
            button {{
                align-self: end;
                padding: 12px 18px;
                font-size: 16px;
                font-weight: 700;
                border: none;
                border-radius: 10px;
                background: #2563eb;
                color: white;
                cursor: pointer;
            }}
            button:hover {{ background: #1d4ed8; }}

            .summary {{
                text-align: center;
                margin: 20px 0 30px;
                font-size: 1.1rem;
                color: #374151;
            }}
            .chart-wrap {{
                display: flex;
                justify-content: center;
                align-items: end;
                gap: 40px;
                height: 260px;
                padding: 20px 10px 0;
                border-radius: 16px;
                background: #f8fafc;
                border: 1px solid #e5e7eb;
            }}
            .bar-group {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: end;
                height: 100%;
                width: 150px;
            }}
            .bar {{
                width: 90px;
                border-radius: 12px 12px 0 0;
                display: flex;
                align-items: flex-start;
                justify-content: center;
                padding-top: 8px;
                color: white;
                font-weight: bold;
                min-height: 12px;
                transition: height 0.3s ease;
            }}
            .bar.nam {{ background: linear-gradient(180deg, #3b82f6, #1d4ed8); }}
            .bar.nu {{ background: linear-gradient(180deg, #f472b6, #db2777); }}
            .label {{
                margin-top: 12px;
                font-weight: 700;
                color: #374151;
            }}
            .value {{
                margin-top: 6px;
                font-size: 1rem;
                color: #111827;
            }}
            @media (max-width: 600px) {{
                .chart-wrap {{ gap: 20px; }}
                .bar {{ width: 70px; }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Thống kê số sinh viên nam nữ</h1>

            <form method="post" action="/">
                <div class="input-box">
                    <label for="nam">Số sinh viên nam</label>
                    <input id="nam" type="number" name="nam" min="0" value="{nam}" required>
                </div>
                <div class="input-box">
                    <label for="nu">Số sinh viên nữ</label>
                    <input id="nu" type="number" name="nu" min="0" value="{nu}" required>
                </div>
                <button type="submit">Hiển thị biểu đồ</button>
            </form>

            <div class="summary">
                Tổng số sinh viên: <strong>{nam + nu}</strong>
            </div>

            <div class="chart-wrap">
                <div class="bar-group">
                    <div class="bar nam" style="height: {nam_height}%">{nam}</div>
                    <div class="label">Nam</div>
                    <div class="value">{nam} sinh viên</div>
                </div>

                <div class="bar-group">
                    <div class="bar nu" style="height: {nu_height}%">{nu}</div>
                    <div class="label">Nữ</div>
                    <div class="value">{nu} sinh viên</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        nam = query.get("nam", ["0"])[0]
        nu = query.get("nu", ["0"])[0]
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(render_chart_page(nam, nu).encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        data = parse_qs(body)
        nam = data.get("nam", ["0"])[0]
        nu = data.get("nu", ["0"])[0]

        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(render_chart_page(nam, nu).encode("utf-8"))

    def log_message(self, format, *args):
        return


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), MyHandler)
    print(f"Server đang chạy tại http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDừng server...")
    finally:
        server.server_close()
