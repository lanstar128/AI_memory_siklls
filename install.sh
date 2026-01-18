#!/bin/bash
# Memory Skills 安装脚本
# 支持: Claude Code, Gemini CLI, OpenAI Codex, iFlow CLI
# 项目地址: https://github.com/lanstar128/memory_siklls

set -e

REPO_URL="https://github.com/lanstar128/memory_siklls.git"
TMP_DIR="/tmp/memory_skills_install"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  Memory Skills 安装脚本${NC}"
echo -e "${GREEN}  跨平台 AI 记忆技能包${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# 检测 AI 终端环境
detect_platform() {
    echo -e "${YELLOW}正在检测 AI 终端环境...${NC}"
    
    # 按优先级检测
    if [ -d "$HOME/.claude" ]; then
        PLATFORM="claude"
        SKILL_DIR="$HOME/.claude/skills"
        MEMORY_DIR="$HOME/.claude/memory"
        CONFIG_FILE="$HOME/.claude/CLAUDE.md"
        echo -e "${GREEN}✓ 检测到 Claude Code${NC}"
    elif [ -d "$HOME/.gemini" ]; then
        PLATFORM="gemini"
        SKILL_DIR="$HOME/.gemini/skills"
        MEMORY_DIR="$HOME/.gemini/memory"
        CONFIG_FILE="$HOME/.gemini/GEMINI.md"
        echo -e "${GREEN}✓ 检测到 Gemini CLI${NC}"
    elif [ -d "$HOME/.codex" ]; then
        PLATFORM="codex"
        SKILL_DIR="$HOME/.codex/skills"
        MEMORY_DIR="$HOME/.codex/memory"
        CONFIG_FILE="$HOME/.codex/AGENTS.md"
        echo -e "${GREEN}✓ 检测到 OpenAI Codex${NC}"
    else
        # 默认使用 Gemini 目录结构
        PLATFORM="gemini"
        SKILL_DIR="$HOME/.gemini/skills"
        MEMORY_DIR="$HOME/.gemini/memory"
        CONFIG_FILE="$HOME/.gemini/GEMINI.md"
        echo -e "${YELLOW}未检测到已知平台，使用默认 Gemini 目录结构${NC}"
    fi
    
    echo "  技能目录: $SKILL_DIR"
    echo "  记忆目录: $MEMORY_DIR"
    echo ""
}

# 检查依赖
check_dependencies() {
    echo -e "${YELLOW}检查依赖...${NC}"
    
    # 检查 Git
    if ! command -v git &> /dev/null; then
        echo -e "${RED}✗ Git 未安装${NC}"
        echo "  请先安装 Git: brew install git"
        exit 1
    fi
    echo -e "${GREEN}✓ Git 已安装${NC}"
    
    # 检查 Python3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}✗ Python3 未安装${NC}"
        echo "  请先安装 Python3: brew install python3"
        exit 1
    fi
    echo -e "${GREEN}✓ Python3 已安装${NC}"
    echo ""
}

# 下载技能包
download_skills() {
    echo -e "${YELLOW}下载技能包...${NC}"
    
    # 清理临时目录
    rm -rf "$TMP_DIR"
    
    # 克隆仓库
    git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null
    echo -e "${GREEN}✓ 下载完成${NC}"
    echo ""
}

# 安装技能
install_skills() {
    echo -e "${YELLOW}安装技能到 $SKILL_DIR ...${NC}"
    
    # 创建目录
    mkdir -p "$SKILL_DIR"
    mkdir -p "$MEMORY_DIR/conversations"
    
    # 复制技能文件
    cp -r "$TMP_DIR/skills/"* "$SKILL_DIR/"
    
    echo -e "${GREEN}✓ 已安装 4 个技能:${NC}"
    echo "  - conversation-archive (对话归档)"
    echo "  - memory-recall (记忆检索)"
    echo "  - memory-sync (记忆同步)"
    echo "  - knowledge-deposit (经验沉淀)"
    echo ""
}

# 清理
cleanup() {
    rm -rf "$TMP_DIR"
}

# 完成提示
show_complete() {
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✅ 安装完成！${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo "已安装到: $SKILL_DIR"
    echo ""
    echo -e "${YELLOW}快速开始:${NC}"
    echo "  1. 在任务完成时说 \"帮我保存对话\" → 触发对话归档"
    echo "  2. 说 \"我们之前讨论过 XXX\" → 触发记忆检索"
    echo "  3. 说 \"同步记忆\" → 备份到远程 Git"
    echo ""
    echo -e "${YELLOW}可选 - 语义搜索依赖:${NC}"
    echo "  pip3 install sentence-transformers"
    echo ""
    echo -e "GitHub: ${GREEN}https://github.com/lanstar128/memory_siklls${NC}"
}

# 主流程
main() {
    detect_platform
    check_dependencies
    download_skills
    install_skills
    cleanup
    show_complete
}

main
