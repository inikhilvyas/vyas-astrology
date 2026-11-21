"""
MCP Server exposing Deep Diagnostic & Secret-Revelation tools for Acharya Vyas (v10.0).
"""

import sys
import json

sys.path.append("..")
from goodh_diagnostic_engine import (
    inspect_gandanta_and_tara,
    analyze_inner_psychology_and_karaka_dynamics,
)


def handle_rpc(req: dict) -> dict:
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "acharya-vyas-goodh-engine", "version": "10.0.0"},
                "capabilities": {"tools": {}},
            },
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "inspect_gandanta_and_tara",
                        "description": "Detect Gandanta junctions, transit Nakshatra Tara hits (1..9), and Dagdha rashis.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "planets_lon": {"type": "object"},
                                "moon_lon": {"type": "number"},
                                "transit_planets_lon": {"type": "object"},
                                "tithi": {"type": "integer"},
                            },
                            "required": ["planets_lon", "moon_lon"],
                        },
                    },
                    {
                        "name": "analyze_inner_psychology_and_karaka_dynamics",
                        "description": "Analyze Jaimini AK/AmK/Karakansha/Swamsa/UL/AL inner turmoil and karmic tension.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "ak_planet": {"type": "string"},
                                "amk_planet": {"type": "string"},
                                "karakansha_sign_idx": {"type": "integer"},
                                "swamsa_sign_idx": {"type": "integer"},
                                "ul_sign_idx": {"type": "integer"},
                                "al_sign_idx": {"type": "integer"},
                            },
                            "required": [
                                "ak_planet", "amk_planet",
                                "karakansha_sign_idx", "swamsa_sign_idx",
                                "ul_sign_idx", "al_sign_idx"
                            ],
                        },
                    },
                ]
            },
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "inspect_gandanta_and_tara":
            out = inspect_gandanta_and_tara(**args)
        elif name == "analyze_inner_psychology_and_karaka_dynamics":
            out = analyze_inner_psychology_and_karaka_dynamics(**args)
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown tool: {name}"}}
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}]},
        }
    return {"jsonrpc": "2.0", "id": req_id, "result": {}}


if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            reply = handle_rpc(msg)
            sys.stdout.write(json.dumps(reply, ensure_ascii=False) + "\n")
            sys.stdout.flush()
        except Exception as exc:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32603, "message": str(exc)}}) + "\n")
            sys.stdout.flush()
