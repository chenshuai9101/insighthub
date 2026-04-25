#!/bin/bash
# InsightHub 打包脚本
cd "$(dirname "$0")/.."
PROJECT_ROOT=$(pwd)
BUILD_DIR="/tmp/insighthub-build"

echo "🏗️  Building InsightHub package..."

rm -rf "$BUILD_DIR"
mkdir -p "$BUILD_DIR"

cp -r \
    main.py config.py models.py utils.py \
    insightlens_client.py insightsee_client.py \
    requirements.txt README.md \
    routes/ templates/ static/ assets/ scripts/ data/ \
    "$BUILD_DIR/"

echo "✅ Build complete: $BUILD_DIR"
echo "📦 Contents:"
ls -la "$BUILD_DIR"
