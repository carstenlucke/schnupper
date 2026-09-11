#!/usr/bin/env bash
# dev-typen.sh — Typen für den Editor bereitstellen
#
# Aufruf: ./scripts/dev-typen.sh
#
# Für die Vorführung ist dieses Skript nicht nötig: pi bringt seinen eigenen
# TypeScript-Lader mit und löst die Importe in .pi/extensions/ selbst auf.
# Nur ein Editor kann das nicht — er sucht ein node_modules und findet keins,
# also unterringelt er jede Zeile rot.
#
# Statt die Pakete ein zweites Mal herunterzuladen, verweisen wir auf die
# Kopien, die in der global installierten pi-CLI ohnehin schon liegen — genau
# wie es scripts/test-tools.mjs beim Testen tut. Das entstehende node_modules
# besteht nur aus Verknüpfungen und ist gitignored.

set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if ! command -v pi >/dev/null 2>&1; then
  echo "Fehler: pi ist nicht installiert (which pi)." >&2
  exit 1
fi

# Vom Startskript zum Paketverzeichnis: bin/pi -> dist/ -> Paketwurzel.
PI_BIN="$(python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$(command -v pi)")"
PI_PACKAGE="$(cd "$(dirname "$PI_BIN")/../.." && pwd)"
PI_MODULES="$PI_PACKAGE/node_modules"

link() {
  local ziel="$1" name="$2"
  if [[ ! -e "$ziel" ]]; then
    echo "Fehler: $name nicht gefunden unter $ziel" >&2
    exit 1
  fi
  mkdir -p "$(dirname "$PROJECT/node_modules/$name")"
  rm -rf "$PROJECT/node_modules/$name"
  ln -s "$ziel" "$PROJECT/node_modules/$name"
  echo "  $name"
}

echo "Verknüpfe Typen aus $PI_PACKAGE:"
link "$PI_PACKAGE" "@earendil-works/pi-coding-agent"
link "$PI_MODULES/@earendil-works/pi-ai" "@earendil-works/pi-ai"
link "$PI_MODULES/typebox" "typebox"
link "$PI_MODULES/@types/node" "@types/node"
echo "Fertig. Der Editor braucht unter Umständen einen Neustart des TypeScript-Servers."
