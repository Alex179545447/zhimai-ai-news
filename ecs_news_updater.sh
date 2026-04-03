#!/bin/bash
# 智脉AI每日晚报 - ECS服务器定时更新脚本
# 设置: 每天北京时间17:00自动运行
# 配合crontab: 0 17 * * * /opt/news_update/run_update.sh

WORK_DIR="/opt/news_update"
LOG_FILE="$WORK_DIR/update.log"
HTML_FILE="$WORK_DIR/index.html"
API_KEY="28133690e57f4ba9902b4015f21404bb.L3eQw0LRHCFM7N9f"

# 创建日志
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 主更新函数
run_update() {
    log "=========================================="
    log "智脉AI每日晚报更新任务开始"
    log "=========================================="
    
    # 拉取最新代码
    log "📥 拉取最新代码..."
    cd $WORK_DIR
    git pull origin main >> $LOG_FILE 2>&1
    
    # 运行Python脚本
    log "📡 调用智谱API获取新闻..."
    python3 $WORK_DIR/generate_news.py >> $LOG_FILE 2>&1
    
    if [ $? -eq 0 ]; then
        log "✅ 新闻生成成功"
        
        # 推送到GitHub
        log "📤 推送到GitHub..."
        cd $WORK_DIR
        git add index.html
        git commit -m "Auto update $(date +'%Y-%m-%d %H:%M') - powered by 智脉AI" >> $LOG_FILE 2>&1
        git push origin main >> $LOG_FILE 2>&1
        
        if [ $? -eq 0 ]; then
            log "✅ 推送成功!"
        else
            log "❌ 推送失败"
        fi
    else
        log "❌ 新闻生成失败，查看日志: $LOG_FILE"
    fi
    
    log "=========================================="
    log "任务完成"
    log "=========================================="
}

# 执行更新
run_update
