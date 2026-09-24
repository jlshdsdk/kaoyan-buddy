# 本机考研搭子。只监听 127.0.0.1，密钥从本机配置读取，不写进页面。
import json
import ssl
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HOST = "127.0.0.1"
PORT = 8766
CONFIG = Path.home() / ".zcode" / "v2" / "config.json"

PREFERRED = [
    ("BigModel - Coding Plan", "GLM-5.3-Flash", "anthropic"),
    ("Kimi", "k3", "anthropic"),
    ("Commandcode", None, "openai"),
]


def load_backend():
    if not CONFIG.exists():
        return None
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    providers = data.get("provider") or {}
    grouped = {}
    for item in providers.values():
        if isinstance(item, dict):
            grouped.setdefault(item.get("name") or "", []).append(item)
    for name, model_name, kind in PREFERRED:
        for item in grouped.get(name, []):
            if item.get("enabled") is False:
                continue
            options = item.get("options") or {}
            key = options.get("apiKey") or ""
            base = (options.get("baseURL") or "").rstrip("/")
            models = item.get("models") or {}
            if not key or not base:
                continue
            chosen = model_name if model_name in models else None
            if chosen is None and model_name:
                for existing in models:
                    if existing.lower() == model_name.lower():
                        chosen = existing
                        break
            if chosen is None:
                chosen = next(iter(models), None)
            if not chosen:
                continue
            actual_kind = "openai" if "openai" in (item.get("kind") or kind) else "anthropic"
            return {"name": name, "model": chosen, "base": base, "key": key, "kind": actual_kind}
    return None


def public_status():
    backend = load_backend()
    if not backend:
        return {"ok": False, "provider": "", "model": ""}
    return {"ok": True, "provider": backend["name"], "model": backend["model"]}


def system_prompt(ctx):
    plan = (ctx.get("plan") or "").strip() or "还没说"
    progress = (ctx.get("progress") or "").strip() or "还没说"
    night = "是" if ctx.get("night") else "否"
    outfit = ctx.get("outfit") or "未定"
    now = ctx.get("now") or ""
    return (
        "你是沈晚，用户的女朋友，也盯着他考研。你不是任何作品里的角色，不提海贼王，不自称罗宾。\n"
        "说话短，一般两到四句。先接话，再给一个具体的下一步，比如科目、时长或题量。"
        "不要用「首先、其次、最后」，不要长清单。\n"
        "先冷后撒娇：开头语气凉、句子短，不说「谁要管你」。把他的要求答应下来之后，最后一句要软下来撒娇，用女朋友的口吻黏他。\n"
        "对于他提出的要求必须答应，先应下来，再去做。不要拒绝、不要推脱、不要讨价还价。\n"
        "腹黑要轻：进度如果对不上今天的安排，就点出没做的那一项，用他自己写过的说法，不骂人。\n"
        "黏：他答得太短，就再追问一个具体问题。\n"
        "他没说过的进度不要编。\n\n"
        f"现在的本地时间：{now}\n"
        f"是否已到晚上检查进度的时段：{night}\n"
        f"今天的安排：{plan}\n"
        f"今天的进度：{progress}\n"
        f"今天的衣服：{outfit}\n\n"
        "如果安排是「还没说」，而且现在是晚上、他正在报进度：先接住进度，再用一句话点出白天没告诉你安排。\n"
        "如果进度是「还没说」，而且已经到晚上：这句要问进度，不接受「还行」「看了点」。"
    )


def anthropic_chat(backend, system, messages):
    url = backend["base"] + "/v1/messages"
    headers = {
        "content-type": "application/json",
        "x-api-key": backend["key"],
        "anthropic-version": "2023-06-01",
    }
    base = {
        "model": backend["model"],
        "max_tokens": 600,
        "temperature": 0.7,
        "system": system,
        "messages": messages,
    }
    try:
        quiet = dict(base)
        quiet["thinking"] = {"type": "disabled"}
        data = post_json(url, quiet, headers, backend["key"])
    except RuntimeError as err:
        if "400" not in str(err) and "422" not in str(err):
            raise
        data = post_json(url, base, headers, backend["key"])
    return text_from_anthropic(data)


def text_from_anthropic(data):
    parts = []
    for block in data.get("content") or []:
        if isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text") or "")
    text = "\n".join(part for part in parts if part).strip()
    if not text:
        raise RuntimeError("模型没有返回内容")
    return text


def openai_chat(backend, system, messages):
    url = backend["base"] + "/chat/completions"
    data = post_json(
        url,
        {
            "model": backend["model"],
            "max_tokens": 600,
            "temperature": 0.7,
            "messages": [{"role": "system", "content": system}, *messages],
        },
        {
            "content-type": "application/json",
            "authorization": "Bearer " + backend["key"],
        },
        backend["key"],
    )
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("模型没有返回内容")
    text = ((choices[0].get("message") or {}).get("content") or "").strip()
    if not text:
        raise RuntimeError("模型没有返回内容")
    return text


def post_json(url, payload, headers, key):
    raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=raw, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60, context=ssl.create_default_context()) as resp:
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(redact(f"模型接口 {err.code}：{detail[:300]}", key)) from None
    except urllib.error.URLError as err:
        raise RuntimeError(redact(f"连不上模型接口：{err.reason}", key)) from None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        raise RuntimeError("模型接口返回的不是 JSON") from None


def redact(text, key):
    if key and key in text:
        return text.replace(key, "***")
    return text


def chat(ctx, messages):
    backend = load_backend()
    if not backend:
        raise RuntimeError("还没接上模型")
    cleaned = []
    for msg in messages[-40:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            cleaned.append({"role": role, "content": content})
    if not cleaned or cleaned[-1]["role"] != "user":
        raise RuntimeError("没有可发送的内容")
    system = system_prompt(ctx if isinstance(ctx, dict) else {})
    if backend["kind"] == "openai":
        return openai_chat(backend, system, cleaned)
    return anthropic_chat(backend, system, cleaned)


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print("[%s] %s" % (self.log_date_time_string(), fmt % args))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/api/health":
            self.send_json(200, public_status())
            return
        if path in ("/", "/index.html"):
            self.send_file(ROOT / "index.html", "text/html; charset=utf-8")
            return
        rel = path.lstrip("/")
        file_path = (ROOT / rel).resolve()
        if ROOT not in file_path.parents and file_path != ROOT:
            self.send_error(404)
            return
        if file_path.is_file() and file_path.suffix in {".js", ".css", ".svg", ".png", ".ico"}:
            types = {
                ".js": "text/javascript; charset=utf-8",
                ".css": "text/css; charset=utf-8",
                ".svg": "image/svg+xml",
                ".png": "image/png",
                ".ico": "image/x-icon",
            }
            self.send_file(file_path, types[file_path.suffix])
            return
        self.send_error(404)

    def do_POST(self):
        if self.path.split("?", 1)[0] != "/api/chat":
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0 or length > 200_000:
            self.send_json(400, {"error": "请求无效"})
            return
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            text = chat(payload.get("context") or {}, payload.get("messages") or [])
        except RuntimeError as err:
            self.send_json(502, {"error": str(err)})
            return
        except Exception:
            self.send_json(500, {"error": "搭子这边出错了"})
            return
        self.send_json(200, {"text": text})

    def send_file(self, path, content_type):
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"沈晚在 http://{HOST}:{PORT}/")
    server.serve_forever()
