"""Stock engine: fetch quotes, compute simple signals."""
from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

CACHE_TTL_SECONDS = 15


def _cache_path(data_dir: Path) -> Path:
    return data_dir / "stock_cache.json"


def _read_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            return data
    except Exception:
        pass
    return {}


def _write_cache(path: Path, data: dict[str, Any]) -> None:
    try:
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception:
        pass


def _now_ts() -> int:
    return int(datetime.now().timestamp())


def _mini_signal(change_pct: float | None) -> tuple[str, str]:
    if change_pct is None:
        return "Neutral", "gray"
    if change_pct >= 2.0:
        return "Long", "green"
    if change_pct >= 0.0:
        return "Hold", "lightgreen"
    if change_pct > -2.0:
        return "Hold", "orange"
    return "Short", "red"


def fetch_quotes(symbols: list[str], data_dir: Path) -> dict[str, Any]:
    try:
        import yfinance as yf
    except Exception as e:
        return {"error": f"yfinance unavailable: {e}", "quotes": {}}

    cache_path = _cache_path(data_dir)
    cache = _read_cache(cache_path)
    now = _now_ts()
    quotes: dict[str, Any] = {}

    valid_symbols = [s.upper().strip() for s in symbols if isinstance(s, str) and s.strip()]
    for sym in valid_symbols:
        cached = cache.get(sym)
        if isinstance(cached, dict) and now - int(cached.get("ts", 0)) < CACHE_TTL_SECONDS:
            quotes[sym] = cached
            continue

        info = {
            "symbol": sym,
            "price": None,
            "change": None,
            "change_pct": None,
            "volume": None,
            "source": "yfinance",
        }
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="5d", auto_adjust=False)
            if not hist.empty and len(hist) >= 2:
                last = float(hist["Close"].iloc[-1])
                prev = float(hist["Close"].iloc[-2])
                info["price"] = round(last, 4)
                info["change"] = round(last - prev, 4)
                info["change_pct"] = round((last - prev) / prev * 100, 4) if prev else 0.0
                if "Volume" in hist.columns and len(hist["Volume"]) >= 1:
                    info["volume"] = int(hist["Volume"].iloc[-1])
            elif not hist.empty:
                last = float(hist["Close"].iloc[-1])
                info["price"] = round(last, 4)
                info["change"] = 0.0
                info["change_pct"] = 0.0
        except Exception as e:
            info["error"] = str(e)

        if "error" not in info:
            signal, _color = _mini_signal(info.get("change_pct"))
            info["signal"] = signal
        else:
            info["signal"] = "Error"

        quotes[sym] = info
        cache[sym] = info | {"ts": now}

    try:
        _write_cache(cache_path, cache)
    except Exception:
        pass
    return {"error": None, "quotes": quotes}


def recommended_additions(watchlist: list[str], limit: int = 5) -> list[dict[str, Any]]:
    base = ["SPY", "QQQ", "AAPL", "MSFT", "NVDA", "AMZN", "META", "BTC-USD"]
    existing = {s.upper().strip() for s in watchlist if isinstance(s, str) and s.strip()}
    picks = []
    for sym in base:
        if sym in existing:
            continue
        picks.append({"symbol": sym, "reason": "common watchlist candidate"})
        if len(picks) >= limit:
            break
    return picks
