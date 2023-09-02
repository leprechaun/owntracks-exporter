#!/usr/bin/env bash

CHART_FILENAME="${1}"
FOLDER_NAME="$(echo $CHART_FILENAME | rev | cut -d'-' -f2- | rev)"

CONTENT="$(cat $CHART_FILENAME | base64)"

echo '{"committer":{"name":"GoCD Automaton","email":"gocd-automaton@example.com"}}' | \
    jq ".message|=\"Update the chart to $CHART_FILENAME\"" | \
    jq ".content|=\"${CONTENT}\"" > payload.json

curl -L \
  -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/leprechaun/leprechaun.github.io/contents/${FOLDER_NAME}/${CHART_FILENAME} \
  -d @payload.json
