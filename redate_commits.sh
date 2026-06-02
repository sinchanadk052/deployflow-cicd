#!/bin/bash
set -e

START_DATE="$1"
END_DATE="$2"

if [ -z "$START_DATE" ] || [ -z "$END_DATE" ]; then
  echo "Usage: $0 <start-date YYYY-MM-DD> <end-date YYYY-MM-DD>"
  exit 1
fi

if [ ! -d ".git" ]; then
  echo "Error: run this from inside the root of a git repo (where .git lives)."
  exit 1
fi

START_EPOCH=$(date -d "$START_DATE" +%s)
END_EPOCH=$(date -d "$END_DATE 23:59:59" +%s)

COMMITS=($(git log --reverse --pretty=format:"%H"))
COUNT=${#COMMITS[@]}

if [ "$COUNT" -eq 0 ]; then
  echo "No commits found."
  exit 1
fi

echo "Found $COUNT commits. Spreading across $START_DATE -> $END_DATE ..."

RANGE=$((END_EPOCH - START_EPOCH))
DATES=()
for ((i=0; i<COUNT; i++)); do
  OFFSET=$((RANDOM * RANDOM % RANGE))
  EPOCH=$((START_EPOCH + OFFSET))
  HOUR_ROLL=$((RANDOM % 100))
  if [ "$HOUR_ROLL" -lt 55 ]; then
    HOUR=$((18 + RANDOM % 6))
  elif [ "$HOUR_ROLL" -lt 85 ]; then
    HOUR=$((13 + RANDOM % 5))
  else
    HOUR=$((9 + RANDOM % 4))
  fi
  MIN=$((RANDOM % 60))
  SEC=$((RANDOM % 60))
  DAY=$(date -d "@$EPOCH" +%Y-%m-%d)
  DATES+=("${DAY}T$(printf "%02d:%02d:%02d" $HOUR $MIN $SEC)")
done

IFS=$'\n' SORTED_DATES=($(sort <<<"${DATES[*]}"))
unset IFS

FILTER_SCRIPT="/tmp/redate_filter_$$.sh"
echo "#!/bin/bash" > "$FILTER_SCRIPT"
for ((i=0; i<COUNT; i++)); do
  HASH="${COMMITS[$i]}"
  NEWDATE="${SORTED_DATES[$i]}"
  echo "if [ \$GIT_COMMIT = $HASH ]; then" >> "$FILTER_SCRIPT"
  echo "  export GIT_AUTHOR_DATE=\"$NEWDATE\"" >> "$FILTER_SCRIPT"
  echo "  export GIT_COMMITTER_DATE=\"$NEWDATE\"" >> "$FILTER_SCRIPT"
  echo "fi" >> "$FILTER_SCRIPT"
  echo "  -> commit ${HASH:0:8} => $NEWDATE"
done
chmod +x "$FILTER_SCRIPT"

echo "Rewriting history..."
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter "$(cat "$FILTER_SCRIPT")" -- --all
rm -f "$FILTER_SCRIPT"

echo "Done. Review with: git log --pretty=fuller"
echo "Then push with:    git push --force"
