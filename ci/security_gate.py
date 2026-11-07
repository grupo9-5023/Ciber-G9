#!/usr/bin/env python3
"""Puerta de seguridad del pipeline.

Lee los informes JSON de Semgrep o de ZAP, imprime un resumen y termina con
código 1 si hay hallazgos bloqueantes (así Jenkins para el pipeline).

  python3 ci/security_gate.py semgrep reports/semgrep.json
  python3 ci/security_gate.py zap reports/zap/*.json

Bloqueante:
  - Semgrep: hallazgos de severidad ERROR.
  - ZAP: alertas de riesgo High (riskcode 3).
"""
import json
import sys


def gate_semgrep(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    results = data.get("results", [])
    blocking = [r for r in results if r.get("extra", {}).get("severity") == "ERROR"]
    print(f"[SAST] Semgrep: {len(results)} hallazgos, {len(blocking)} de severidad ERROR")
    for r in results:
        sev = r.get("extra", {}).get("severity", "?")
        print(f"  {sev:8} {r.get('path')}:{r.get('start', {}).get('line')}  {r.get('check_id')}")
    for e in data.get("errors", []):
        print(f"  [aviso semgrep] {e.get('message', e)}")
    return len(blocking)


RISK = {"0": "Info", "1": "Low", "2": "Medium", "3": "High"}


def gate_zap(paths):
    blocking = 0
    for path in paths:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for site in data.get("site", []):
            alerts = site.get("alerts", [])
            high = [a for a in alerts if str(a.get("riskcode")) == "3"]
            blocking += len(high)
            print(f"[DAST] {site.get('@name')}: {len(alerts)} alertas, {len(high)} de riesgo High")
            for a in sorted(alerts, key=lambda a: -int(a.get("riskcode", 0))):
                risk = RISK.get(str(a.get("riskcode")), "?")
                print(f"  {risk:6} {a.get('name') or a.get('alert')} ({a.get('count', '?')} instancias)")
    return blocking


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("semgrep", "zap"):
        print(__doc__)
        return 2
    tool, files = sys.argv[1], sys.argv[2:]
    blocking = gate_semgrep(files[0]) if tool == "semgrep" else gate_zap(files)
    if blocking:
        print(f"PUERTA DE SEGURIDAD: FALLA ({blocking} hallazgos bloqueantes)")
        return 1
    print("PUERTA DE SEGURIDAD: OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
