#!/bin/bash

PROJECT_DIR="/Users/miseioikawa/Projects/todofuken-crawler"
LOG_FILE="$PROJECT_DIR/data/logs/crawler.log"

echo "===== RUN START: $(date) =====" >> "$LOG_FILE"

cd "$PROJECT_DIR"
python3 -m src.main >> "$LOG_FILE" 2>&1

echo "===== RUN FINISHED: $(date) =====" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"