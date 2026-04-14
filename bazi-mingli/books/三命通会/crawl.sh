#!/bin/bash
# 三命通会抓取脚本
# 存储位置: /root/.openclaw/workspace/knowledge/命理/三命通会/

OUTPUT_DIR="/root/.openclaw/workspace/knowledge/命理/三命通会"
BASE_URL="https://www.8bei8.com/book"

# 章节数量（根据目录页显示）
START=1
END=227

echo "开始抓取《三命通会》..."
echo "目标: $START - $END 章"
echo "输出目录: $OUTPUT_DIR"

# 先创建 index 文件
echo "#《三命通会》目录" > "$OUTPUT_DIR/README.md"
echo "" >> "$OUTPUT_DIR/README.md"

for i in $(seq -f "%03g" $START $END); do
    echo "抓取: sanmingtonghui_$i.html..."
    
    # 抓取内容
    content=$(curl -s -A "Mozilla/5.0" "https://www.8bei8.com/book/sanmingtonghui_$i.html" | grep -oP '(?<=<article class="article-content">)[\s\S]*?(?=</article>)' | head -1)
    
    if [ -n "$content" ]; then
        # 清理HTML标签，保留纯文本
        clean_content=$(echo "$content" | sed 's/<[^>]*>//g' | sed 's/&nbsp;/ /g' | sed 's/[[:space:]]\+/ /g' | tr -d '\n')
        
        echo "$clean_content" > "$OUTPUT_DIR/chapter_$i.md"
        echo "  ✓ 保存成功: chapter_$i.md"
    else
        echo "  ✗ 内容为空或抓取失败"
    fi
    
    # 间隔 2 秒，防止被限流
    sleep 2
done

echo ""
echo "抓取完成！"
echo "共 $(ls -1 $OUTPUT_DIR/chapter_*.md | wc -l) 章"
