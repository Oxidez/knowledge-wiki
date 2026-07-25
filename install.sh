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
echo "[1/6] Checking for Hermes installation..."
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
echo "[2/6] Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "✅ Python $PYTHON_VERSION found"

# 3. Copy skill files
echo "[3/6] Installing skill to: $TARGET_DIR"
mkdir -p "$TARGET_DIR"
cp -r "$SOURCE_DIR"/* "$TARGET_DIR/"
echo "✅ Skill files copied"

# 4. Install Python dependencies
echo "[4/6] Installing Python dependencies..."
if [[ -f "$TARGET_DIR/scripts/requirements.txt" ]]; then
    pip install -q -r "$TARGET_DIR/scripts/requirements.txt" 2>/dev/null || {
        echo "⚠️  Some optional dependencies may have failed (PDF/DOCX/XLSX conversion)."
        echo "   Core functionality (indexing, validation) will still work."
    }
    echo "✅ Dependencies installed"
else
    echo "⚠️  requirements.txt not found, skipping"
fi

# 5. Copy workspace template
echo "[5/6] Setting up workspace..."
cd "$TARGET_DIR"
python3 scripts/setup.py --auto

# 6. Final verification
echo "[6/6] Verifying installation..."
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
echo "Skill installed to: $TARGET_DIR"
echo
echo "Next steps:"
echo "  1. Restart Hermes or reload skills"
echo "  2. The skill will be available as 'knowledge-wiki'"
echo "  3. Config file: ~/.config/knowledge-wiki/config.yaml"
echo "  4. Workspace created with AGENTS.md, instructions/, knowledge/, etc."
echo
echo "To verify installation:"
echo "  hermes skill list | grep knowledge-wiki"
echo