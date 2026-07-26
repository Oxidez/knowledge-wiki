#!/bin/bash
# knowledge-wiki Skill Installer
# Installs the skill to ~/.hermes/skills/knowledge-management/knowledge-wiki/
# and runs setup for path configuration.

set -e

SKILL_NAME="knowledge-wiki"
SKILL_CATEGORY="knowledge-management"
TARGET_DIR="$HOME/.hermes/skills/$SKILL_CATEGORY/$SKILL_NAME"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================================"
echo "  knowledge-wiki Skill Installer"
echo "============================================================"
echo

# 1. Check for Hermes installation
echo "[1/7] Checking for Hermes installation..."
HERMES_CONFIG="$HOME/.hermes/config.yaml"
if [[ ! -f "$HERMES_CONFIG" ]]; then
    echo "❌ Hermes configuration not found at: $HERMES_CONFIG"
    echo "   Please install Hermes first: https://hermes-agent.nousresearch.com"
    echo
    echo "   If Hermes is installed at a different location, please specify:"
    read -p "   Hermes config path (or Enter to abort): " CUSTOM_HERMES
    if [[ -z "$CUSTOM_HERMES" ]]; then
        exit 1
    fi
    HERMES_CONFIG="$CUSTOM_HERMES"
    if [[ ! -f "$HERMES_CONFIG" ]]; then
        echo "   ❌ Not found: $HERMES_CONFIG"
        exit 1
    fi
fi
echo "✅ Hermes config found: $HERMES_CONFIG"

# 2. Check Python
echo "[2/7] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# 3. Copy main skill files
echo "[3/7] Installing knowledge-wiki skill to: $TARGET_DIR"
mkdir -p "$TARGET_DIR"
# Copy all files except knowledge-subcategory-classifier (separate skill)
for item in "$SOURCE_DIR"/*; do
    if [[ "$(basename "$item")" != "knowledge-subcategory-classifier" ]]; then
        cp -r "$item" "$TARGET_DIR/"
    fi
done
echo "✅ Skill files copied"

# 4. Install knowledge-subcategory-classifier skill
CLASSIFIER_NAME="knowledge-subcategory-classifier"
CLASSIFIER_TARGET="$HOME/.hermes/skills/$SKILL_CATEGORY/$CLASSIFIER_NAME"
echo "[4/7] Installing $CLASSIFIER_NAME skill to: $CLASSIFIER_TARGET"
mkdir -p "$CLASSIFIER_TARGET"
cp -r "$SOURCE_DIR/knowledge-subcategory-classifier"/* "$CLASSIFIER_TARGET/"
echo "✅ Classifier skill copied"

# 5. Install Python dependencies
echo "[5/7] Installing Python dependencies..."
if [[ -f "$TARGET_DIR/scripts/requirements.txt" ]]; then
    pip install -q -r "$TARGET_DIR/scripts/requirements.txt" 2>/dev/null || {
        echo "⚠️  Some optional dependencies may have failed (PDF/DOCX/XLSX conversion)."
        echo "   Core functionality (indexing, validation) will still work."
    }
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping"
fi

# 6. Copy workspace template
echo "[6/7] Setting up workspace..."
cd "$TARGET_DIR"
python3 scripts/setup.py --auto

# 7. Final verification
echo "[7/7] Verifying installation..."
if [[ -f "$HOME/.config/knowledge-wiki/config.yaml" ]]; then
    echo "✅ Config created: $HOME/.config/knowledge-wiki/config.yaml"
else
    echo "⚠️  Config not found - run setup.py manually if needed"
fi

echo
echo "============================================================"
echo "  ✅ Installation Complete!"
echo "============================================================"
echo
echo "Skills installed:"
echo "  - $TARGET_DIR"
echo "  - $CLASSIFIER_TARGET"
echo
echo "Next steps:"
echo "  1. Restart Hermes or reload skills"
echo "  2. The skills will be available as 'knowledge-wiki' and 'knowledge-subcategory-classifier'"
echo "  3. Config file: ~/.config/knowledge-wiki/config.yaml"
echo "  4. Workspace created with AGENTS.md, instructions/, knowledge/, etc."
echo
echo "To verify installation:"
echo "  hermes skill list | grep -E 'knowledge-wiki|knowledge-subcategory-classifier'"
echo