# 数据质量分级标准与消息模板

> **参考文件** — 由 workflow 步骤引用，不可独立执行。
> **引用方**：`workflows/step1_research.md`、`workflows/step1/step1c_profiling.md` C6

## data_quality.json 格式

生成到 `output/{school_id}/{dept_id}/data_quality.json`：

```json
{
  "overall_quality": "high | medium | low",
  "scrape_success": true,
  "data_source": "jina_reader | direct_html | web_search_summary | manual_paste",
  "faculty_count": 6,
  "high_overlap_count": 2,
  "papers_downloaded": 3,
  "issues": []
}
```

## 质量分级标准

| 质量 | 条件 | 行为 |
|------|------|------|
| **high** | 直接爬取成功 + faculty 页面完整 + high overlap faculty 论文已下载 | 静默继续 Step 2 |
| **medium** | 爬取成功但部分信息缺失，或来自 WebSearch 摘要但确认了 faculty 主页 | **⚠ Warning**：询问用户是否继续 |
| **low** | 爬取完全失败 / faculty 数据未验证 / high overlap faculty = 0 | **❌ 暂停**：等用户手动补充 |

## Warning 消息模板

```
⚠ Step 1 数据质量警告：{school_name}

数据来源：{data_source}（非直接爬取）
问题：
  - {issue_1}

影响：
  - Faculty overlap 判断基于搜索摘要，可能不准确
  - 未下载高匹配 faculty 论文，fit_report 中的"具体研究结合点"将缺乏依据

选项：
A. 继续 Step 2（分析结果标注为 [低置信度]）
B. 手动补充数据（copy-paste 到此处）
C. 中止

请回复 A、B 或 C。
```
