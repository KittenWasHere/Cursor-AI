#!/bin/bash

# Termux PATH Setup Script
# This script permanently adds common directories to your PATH
# Paste this entire script into your Termux terminal

echo "🚀 Setting up permanent PATH for Termux..."

# Create directories if they don't exist
mkdir -p $HOME/bin
mkdir -p $HOME/.local/bin
mkdir -p $PREFIX/bin

# Backup existing shell configuration
if [ -f "$HOME/.bashrc" ]; then
    cp "$HOME/.bashrc" "$HOME/.bashrc.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backed up existing .bashrc"
fi

# Function to add path if not already present
add_to_path() {
    local dir="$1"
    if [[ ":$PATH:" != *":$dir:"* ]]; then
        echo "export PATH=\"$dir:\$PATH\"" >> "$HOME/.bashrc"
        echo "✅ Added $dir to PATH"
    else
        echo "ℹ️  $dir already in PATH"
    fi
}

# Add common directories to PATH
echo "" >> "$HOME/.bashrc"
echo "# Added by Termux PATH setup script" >> "$HOME/.bashrc"

# Add user bin directories
add_to_path "$HOME/bin"
add_to_path "$HOME/.local/bin"

# Add Termux specific paths
add_to_path "$PREFIX/bin"
add_to_path "$PREFIX/sbin"

# Add Python user bin if it exists
if [ -d "$HOME/.local/lib/python*/site-packages" ]; then
    PYTHON_USER_BIN=$(python -m site --user-base)/bin
    add_to_path "$PYTHON_USER_BIN"
fi

# Add Node.js global bin if npm is installed
if command -v npm >/dev/null 2>&1; then
    NPM_GLOBAL_BIN=$(npm config get prefix)/bin
    add_to_path "$NPM_GLOBAL_BIN"
fi

# Add Rust cargo bin if it exists
if [ -d "$HOME/.cargo/bin" ]; then
    add_to_path "$HOME/.cargo/bin"
fi

# Add Go bin if it exists
if [ -d "$HOME/go/bin" ]; then
    add_to_path "$HOME/go/bin"
fi

echo "" >> "$HOME/.bashrc"

# Reload the shell configuration
echo "🔄 Reloading shell configuration..."
source "$HOME/.bashrc"

echo ""
echo "✅ PATH setup complete!"
echo ""
echo "📁 The following directories are now in your PATH:"
echo "   • $HOME/bin"
echo "   • $HOME/.local/bin"
echo "   • $PREFIX/bin"
echo "   • $PREFIX/sbin"

if [ -d "$HOME/.cargo/bin" ]; then
    echo "   • $HOME/.cargo/bin (Rust)"
fi

if [ -d "$HOME/go/bin" ]; then
    echo "   • $HOME/go/bin (Go)"
fi

if command -v python >/dev/null 2>&1; then
    PYTHON_USER_BIN=$(python -m site --user-base)/bin
    echo "   • $PYTHON_USER_BIN (Python user packages)"
fi

if command -v npm >/dev/null 2>&1; then
    NPM_GLOBAL_BIN=$(npm config get prefix)/bin
    echo "   • $NPM_GLOBAL_BIN (npm global packages)"
fi

echo ""
echo "💡 Usage:"
echo "   1. Place any executable file in one of the above directories"
echo "   2. Make it executable: chmod +x filename"
echo "   3. Run it from anywhere: filename"
echo ""
echo "🔧 To add a custom directory to PATH:"
echo "   echo 'export PATH=\"/your/custom/path:\$PATH\"' >> ~/.bashrc"
echo "   source ~/.bashrc"
echo ""
echo "📋 Current PATH:"
echo "$PATH" | tr ':' '\n' | sed 's/^/   • /'