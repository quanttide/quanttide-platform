# ROADMAP

## 当前阶段：文档体系建立（v0.3.x）

三层文档链路（BRD→PRD→ADD）和 MyST 文档站基建已跑通，qtcloud-hr 有 Salary + Recruitment 两个完整模块作为模板。

### 已完成

- 逆向文档化方法论：代码 → ADD → PRD → BRD
- BRD/PRD 写作技能化（product-brd / product-prd）
- MyST 文档站模板 + GitHub Pages CI/CD
- qtcloud-hr 两层三模块文档全覆盖
- qtcloud-asset 产品简介 + 文档站基建

### 未完成

产品清单（README.md 完整产品边界）在当前阶段优先级已降低——体系未成熟前定义边界没有意义，先让两个方向验证体系完备性。

---

## 方向一：横向铺开

把 qtcloud-asset 中已有的 BRD/PRD/IXD/QA 文档按新格式统一对齐，验证体系的普适性和兼容性。

### 目标

- **资产云全量文档重写**：按 BRD→PRD→ADD 三层重新组织现有 graph、harness、pricing 等模块
- **IXD 层技能化**：将交互设计文档的叙事规范提炼为 `product-ixd` SKILL
- **QA 层技能化**：将质量保证文档的验证规范提炼为 `product-qa` SKILL
- **兼容性检验**：旧文档到新格式的迁移成本、信息损耗评估

### 产出

- qtcloud-asset 全模块 docset
- `product-ixd` / `product-qa` 两个 SKILL
- 迁移指南：旧文档 → 新格式的 checklist

### 风险

- 旧文档可能信息不全，逆向补充成本高
- 不同模块的叙事深度不一，模板需要容错

---

## 方向二：纵向补全

补全文档链路末端，让 QA 层能反过来验证 BRD 定义的问题是否解决，形成闭环。

### 目标

- **QA 层标准化**：QA 文档回答"BRD 的问题解决了吗"，验收标准可追溯到 PRD 的 Given-When-Then
- **闭环验证**：沿着 BRD→PRD→ADD→QA 正向走一遍，选一个模块（如 salary）从零写 QA
- **文档链路可追溯**：每层之间的引用关系显式化（BRD 场景 → PRD 故事 → ADD 组件 → QA 用例）

### 产出

- `product-qa` SKILL
- salary 模块 QA 示例
- 链路追溯矩阵模板

### 风险

- QA 需要开发验证，纯文档 QA 可能沦为形式
- 可能暴露 PRD/ADD 的模糊点，需要反复迭代

---

## 决策

两个方向不互斥，但建议先后顺序。选一个先走，另一个作为下一个阶段。

**建议优先级**：方向一（横向铺开）> 方向二（纵向补全）。理由：先验证体系可复用，再深入链路闭环。如果横向铺开发现模板本身不通用，补全链路就没有意义。
