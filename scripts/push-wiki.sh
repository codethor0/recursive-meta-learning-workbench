#!/usr/bin/env bash
# Push docs/wiki content to the GitHub Wiki.
# Prerequisite: Enable Wiki in repo Settings, then create the first page via
# https://github.com/codethor0/recursive-meta-learning-workbench/wiki
# (click "Create the first page", add any title, save). After that, run this script.

set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
WIKI_URL="https://github.com/codethor0/recursive-meta-learning-workbench.wiki.git"
TMP_WIKI="/tmp/rmlw-wiki-$$"

cd "$REPO_ROOT"
rm -rf "$TMP_WIKI"
git clone "$WIKI_URL" "$TMP_WIKI"
cp docs/wiki/Home.md "$TMP_WIKI/Home.md"
cp docs/wiki/Getting-Started.md "$TMP_WIKI/Getting-Started.md"
cp docs/wiki/Architecture.md "$TMP_WIKI/Architecture.md"
cp docs/wiki/Contributing.md "$TMP_WIKI/Contributing.md"
cp docs/wiki/Security-and-Scope.md "$TMP_WIKI/Security-and-Scope.md"
cd "$TMP_WIKI"
git add .
if git diff --staged --quiet; then
  echo "No changes to push."
else
  git commit -m "Sync wiki from docs/wiki"
  git push origin main
fi
rm -rf "$TMP_WIKI"
echo "Wiki updated."
