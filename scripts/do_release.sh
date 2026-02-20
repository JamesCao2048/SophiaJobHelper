#!/bin/bash
# do_release.sh — 将 main 分支的指定路径同步到 release 分支
#
# 用法：
#   bash scripts/do_release.sh                  # 同步默认路径
#   bash scripts/do_release.sh --dry-run        # 预览变更，不实际提交
#   bash scripts/do_release.sh --push           # 同步后自动 push 到 origin/release
#
# 可扩展：在 SYNC_PATHS 数组中添加新的子模块路径即可

set -e

# ============================================================
# 配置：需要同步到 release 分支的路径
# ============================================================
SYNC_PATHS=(
    "general"
    "overseas_pipeline"
    "job_filling"
    "region_knowledge"
    "CLAUDE.md"
    "README.md"
    ".gitignore"
)

RELEASE_BRANCH="release"
MAIN_BRANCH="main"

# ============================================================
# 解析参数
# ============================================================
DRY_RUN=0
AUTO_PUSH=0
for arg in "$@"; do
    case $arg in
        --dry-run) DRY_RUN=1 ;;
        --push)    AUTO_PUSH=1 ;;
        *)
            echo "Unknown argument: $arg"
            echo "Usage: bash scripts/do_release.sh [--dry-run] [--push]"
            exit 1
            ;;
    esac
done

# ============================================================
# 找到 git 根目录（脚本从任意目录均可调用）
# ============================================================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GIT_ROOT=$(git -C "$SCRIPT_DIR" rev-parse --show-toplevel)
cd "$GIT_ROOT"

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║         SophiaJobHelper Release          ║"
echo "╚══════════════════════════════════════════╝"
echo "  Git root:  $GIT_ROOT"
echo "  Sync paths: ${SYNC_PATHS[*]}"
[ "$DRY_RUN" -eq 1 ] && echo "  ⚠️  DRY RUN mode — no commits will be made"
echo ""

# ============================================================
# 前置检查
# ============================================================
CURRENT_BRANCH=$(git branch --show-current)
if [ "$CURRENT_BRANCH" != "$MAIN_BRANCH" ]; then
    echo "❌ Error: 请从 $MAIN_BRANCH 分支运行（当前分支：$CURRENT_BRANCH）"
    exit 1
fi

if ! git rev-parse --verify "$RELEASE_BRANCH" > /dev/null 2>&1; then
    echo "❌ Error: release 分支不存在，请先运行初始化脚本"
    exit 1
fi

# ============================================================
# 自动提交 main 上的未提交修改
# ============================================================
if ! git diff --quiet || ! git diff --staged --quiet; then
    echo "📝 检测到未提交的修改，自动提交到 main..."
    git add -A
    AUTO_COMMIT_MSG="chore: auto-commit before release ($(date +%Y-%m-%d))"
    if [ "$DRY_RUN" -eq 1 ]; then
        echo "  [DRY RUN] 将自动提交：$AUTO_COMMIT_MSG"
        echo "  变更文件："
        git diff --staged --name-only | sed 's/^/    /'
    else
        git commit -m "$AUTO_COMMIT_MSG"
        echo "  ✓ 已提交：$AUTO_COMMIT_MSG"
    fi
    echo ""
fi

# ============================================================
# 切换到 release 分支并同步
# ============================================================
MAIN_COMMIT=$(git rev-parse --short HEAD)
RELEASE_DATE=$(date +%Y-%m-%d)

echo "🔀 切换到 $RELEASE_BRANCH 分支..."
git checkout "$RELEASE_BRANCH"

echo "🗑️  清除旧内容..."
for path in "${SYNC_PATHS[@]}"; do
    git rm -rf --ignore-unmatch "$path" > /dev/null 2>&1 || true
done

echo "📥 从 main@${MAIN_COMMIT} 同步..."
git checkout "$MAIN_BRANCH" -- "${SYNC_PATHS[@]}"

# ============================================================
# 提交
# ============================================================
if git diff --staged --quiet; then
    echo ""
    echo "✅ 无变更 — release 分支已是最新"
else
    if [ "$DRY_RUN" -eq 1 ]; then
        echo ""
        echo "📋 [DRY RUN] 以下变更将被提交："
        git diff --staged --stat
        git restore --staged . > /dev/null 2>&1 || true  # unstage
    else
        COMMIT_MSG="release: sync from main@${MAIN_COMMIT} (${RELEASE_DATE})"
        git commit -m "$COMMIT_MSG"
        echo ""
        echo "✅ 已提交: $COMMIT_MSG"
    fi
fi

# ============================================================
# 返回 main
# ============================================================
git checkout "$MAIN_BRANCH"


# ============================================================
# 自动 push
# ============================================================
if [ "$AUTO_PUSH" -eq 1 ] && [ "$DRY_RUN" -eq 0 ]; then
    echo "🚀 推送到 origin/$RELEASE_BRANCH..."
    git push origin "$RELEASE_BRANCH"
    echo "✅ 已推送"
fi

echo ""
echo "🎉 完成！如需推送到远端："
echo "   git push origin release"
echo ""
