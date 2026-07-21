# 输出格式:台账、报告、HTML

## 1. 台账 ledger.json

跨次运行累积的核心资产。数组,每个元素是一个机会:

```json
{
  "id": "gm-2026-07-21-001",
  "created": "2026-07-21",
  "updated": "2026-07-21",
  "domain": "播客转文字",
  "repo": "owner/name",
  "repo_url": "https://github.com/owner/name",
  "license": "MIT",
  "license_note": "商用友好,保留版权声明",
  "score": {"readme": 4, "releases": 2, "maintenance": 5, "issues": 3, "total": 14},
  "verdict": "需要技术基础",
  "opportunity": "帮 Windows 用户一键装好 X 并配好中文界面",
  "service_type": "代装部署",
  "evidence": [
    {"desc": "12 条 Windows 安装求助,维护者只回复 'use docker'", "url": "https://github.com/owner/name/issues?q=windows"}
  ],
  "competition": {"tier": 2, "saturation": "有内容无服务", "note": "教程 3 篇,无人卖交付"},
  "pricing_hint": "49-99 一次性代装,+30/月 维护",
  "status": "待验证",
  "status_note": ""
}
```

**状态机**:`待验证` →(人工闲鱼核查通过)→ `已验证` →(实际上架)→ `已上架`;任何阶段可转 `已放弃`(写明原因)或 `已失效`(上游归档/需求被官方满足)。

**运行时的台账操作**:
1. 开始:读 ledger.json。对已有条目做轻量健康检查——机会对应的 repo 若已归档或需求已被官方修复,状态改 `已失效` 并写 status_note。
2. 去重:新发现的机会若与已有条目 repo+service_type 相同,不新增,只更新 updated 和 evidence。
3. 结束:追加新机会(状态 `待验证`),重写 opportunities.md。

## 2. opportunities.md(台账人类可读版,每次全量重新生成)

```markdown
# 机会台账
> 最后更新:YYYY-MM-DD | 待验证 N · 已验证 N · 已上架 N · 已放弃 N · 已失效 N

## 🟡 待验证
| ID | 机会 | 项目 | 服务形态 | 定价参考 | 发现日期 |
|---|---|---|---|---|---|
...
## 🟢 已验证 / 🔵 已上架 / ⚪ 已放弃 / ⚫ 已失效
(同样表格,已放弃/已失效附一句原因)
```

## 3. Markdown 报告 reports/YYYY-MM-DD-<领域>.md

固定结构:

```markdown
# <领域> GitHub 变现机会报告
> 日期 | 扫描方式(API/gh/MCP/WebFetch)| 候选 N 个 → 入选 N 个 → 机会 N 个

## 一、结论速览
(3-5 句话:最值得跟进的 1-2 个机会 + 一句为什么)

## 二、候选项目全景
| 项目 | Stars | 最近更新 | License | 成品 | 四查总分 | 结论 |

## 三、机会详情(每个机会一节)
### 机会 1:<一句话交付描述>
- 依托项目 / License 及含义
- 用户卡点证据(带链接)
- 服务形态与交付物
- 竞争:层级/饱和度/证据/进入建议
- 定价参考及理由
- 风险(上游更新依赖、售后成本、许可证约束)
- 机会四问自答

## 四、人工验证清单
(每个机会一张 10 分钟核查卡,格式见 competition.md 层 3)

## 五、本次运行局限
(访问方式降级情况、覆盖缺口、待人工确认项)
```

## 4. HTML 可视化报告

1. 读 `assets/report_template.html`
2. 构造数据对象(结构见模板顶部注释),序列化为 JSON,替换文件中的 `__GOLDMINE_DATA__` 占位符
3. 写到 `reports/YYYY-MM-DD-<领域>.html`
4. 有 Artifact 工具 → 同时发布为 artifact;有 SendUserFile → 发送文件;都没有 → 告知路径

注意:JSON 里的字符串要经过正规 JSON 序列化(用脚本注入,不要手拼),避免引号破坏页面。
