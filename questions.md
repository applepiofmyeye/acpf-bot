# ACPF Bot Question Flow

## 1. Language Selection
**Prompt:** 
"欢迎来到 ACPF。请选择您的语言：

Welcome to ACPF.
Please select your language:
"

| Option | Action |
|--------|--------|
| 中文 | Set language to Chinese |
| English | Set language to English |

---

## 2. Positioning Message
**中文:**
> ACPF 专注于协助美业高阶经营者突破瓶颈、建立系统。
> 在推荐任何方案之前，我们会先了解你目前的阶段与需求。
> 请回答以下问题，让我们为你提供最适合的方向。

**English:**
> ACPF focuses on helping high-level beauty industry operators break through bottlenecks and build systems.
> Before recommending any program, we first understand your current stage and needs.
> Please answer the following questions so we can provide the most suitable direction for you.

| Button | Action |
|--------|--------|
| 开始诊断 / Start Diagnosis | Proceed to Q1 |

---

## 3. Pain-Point Question 1 (Q1)
**中文:** 以下哪一个最接近你目前的状态？
**English:** Which one best describes your current situation?

| Option | 中文 | English | Score |
|--------|------|---------|-------|
| A | 技术很强，但生意始终卡在某个规模 | Strong technical skills, but business is stuck at a certain scale | Starter |
| B | 门店 / 团队有了，但无法复制与放大 | Have a shop / team, but unable to replicate and scale | Core |
| C | 有名气，但缺乏系统与长期布局 | Have reputation, but lack systems and long-term structure | Core |
| D | 我已经在高位，但下一步方向不清楚 | Already at a high level, but unclear on the next direction | Core |

---

## 4. Pain-Point Question 2 (Q2)
**中文:** 你目前最困扰你的「不是技术」的问题是？
**English:** What is the biggest non-technical problem troubling you right now?

| Option | 中文 | English | Score |
|--------|------|---------|-------|
| A | 客源不稳定，靠运气 | Inconsistent client flow, relying on luck | Starter |
| B | 团队无法独立运作 | Team cannot operate independently | Core |
| C | 收入有上限，时间被锁死 | Income has a ceiling, time is locked | Core |
| D | 有资源，但不会整合成体系 | Have resources, but cannot integrate them into a system | Core |

---

## 5. Pain-Point Question 3 (Q3)
**中文:** 如果这种状态再持续 2 年，你最担心什么？
If this situation continues for another 2 years, what concerns you most?

| Option | 中文 | English | Score |
|--------|------|---------|-------|
| A | 生意停滞，被后来者超越 | Business stagnates, overtaken by newcomers | Starter |
| B | 永远只是老板，而不是平台 | Forever just a boss, never a platform | Core |
| C | 影响力无法变现 | Influence cannot be monetized | Core |
| D | 精力耗尽，却没有累积 | Energy depleted, with no accumulation | Core |

---

## 6. Readiness Question
**中文:** 你目前对于解决这个问题的状态是？
What is your current readiness to solve this problem?

| Option | 中文 | English | Score |
|--------|------|---------|-------|
| A | 我只是想先了解，还没准备好投入 | I just want to understand first, not ready to commit | Starter |
| B | 如果方向对，我愿意投入时间学习 | If the direction is right, I am willing to invest time to learn | Starter |
| C | 我已经在找方法，准备好采取行动 | I am already looking for solutions, ready to take action | Core |
| D | 我很清楚问题所在，需要系统化的方案 | I am very clear about the problem, need a systematic solution | Core |

---

## 7. Scoring Logic

**Calculation:**
- Count total Starter scores
- Count total Core scores
- If Core > Starter → Recommend Core
- If Starter >= Core → Recommend Starter (tie-breaker favors Starter)

(Do not send any message to users yet)
---

## 8A. Starter Recommendation (if Starter wins)

**中文:**
"根据你的情况，我们建议你从 ACPF Starter 开始。
Starter 每两个月开班一次，帮助你建立系统思维的基础。"

**English:**
"Based on your situation, we recommend you start with ACPF Starter.
Starter runs every two months, helping you build a foundation for systematic thinking."

| Button (中文) | Button (English) | Action |
|--------|--------|---------|
| 报名 Starter（RM588） | Register Start (588RM) | Proceed to registration form |
| 申请 Core 评估 | Apply for Core Review | Proceed to upsell flow |

---

## 8B. Core Recommendation (if Core wins)

**中文:**
"根据你的经营阶段，你更适合进入 ACPF Core。
Core 每年两次（7月与12月），专为准备突破瓶颈的高阶经营者设计"

| Button | Action |
|--------|--------|
| 报名 Core（RM5,997） | Proceed to gate question |

---

## 9. Gate Question (Core path only)
**中文:** 你是否曾参加过 ACPF Starter？

| Option | Action |
|--------|--------|
| 是 | Proceed to registration form (Program=Core) |
| 否 | Show rejection message, offer Starter registration |

**Rejection Message (中文):**
> Core 课程需要先完成 Starter 作为基础。
> Starter 每两个月开班一次，费用为 RM588。
> 如果你准备好了，可以先报名 Starter。

---

## 10. Upsell Flow (Starter path only)

### Upsell Question 1
**中文:** 你目前是否有团队或门店？

| Option | Action |
|--------|--------|
| 有 | hasTeam = true, proceed to Q2 |
| 没有 | hasTeam = false, proceed to Q2 |

### Upsell Question 2
**中文:** 你目前更接近哪一种？

| Option | Action |
|--------|--------|
| 想复制放大（开分店/带团队） | intent = scale |
| 想建立系统（先打基础） | intent = foundation |

### Upsell Outcome

**If hasTeam=true AND intent=scale:**
- Track = CoreReview
- Program = Core
- Message: "我们将为你安排 Core 人工确认，请留下资料。"
- Proceed to registration form

**Otherwise:**
- Message: "从你目前阶段，Starter 会更稳。建议先从 Starter 开始。"
- Button: 报名 Starter（RM588）

---

## 11. Registration Form

Collected sequentially:
1. **Full Name** (required) - "请输入你的全名："
2. **Phone** (required) - "请输入你的电话号码（WhatsApp）："
3. **Email** (optional) - "请输入你的电子邮箱（输入 skip 跳过）："
4. **Business Type** (required) - "你目前从事什么类型的美业？"

---

## 12. Confirmation Summary

**中文:**
> 请确认你的资料：
> 
> 姓名：{name}
> 电话：{phone}
> 邮箱：{email}
> 业务类型：{businessType}
> 课程：{program}
> 核心痛点：{painPoint}

| Button | Action |
|--------|--------|
| 确认提交 | Submit to Google Sheet |
| 重新填写 | Restart form |

---

## 13. Payment Instructions (Final Step)

**中文:**
> 【付款资料】
> 公司名称： ACPF GROUP SDN. BHD.
> ACC NO： 3211951736
> BANK： PUBLIC BANK
> Swift Code: PBBEMYKL
> 
> 请完成转账后，将付款截图发送给负责人确认。
> 工作人员将协助你完成后续报名流程。

---

## Google Sheet Columns

| Column | Field |
|--------|-------|
| A | Timestamp |
| B | Language (中文 / English) |
| C | Telegram User ID |
| D | Telegram Username |
| E | Full Name |
| F | Phone (WhatsApp) |
| G | Email |
| H | Beauty Business Type |
| I | Track (Starter / Core / CoreReview) |
| J | Program Selected (Starter / Core) |
| K | Key Pain Point |
| L | Source (Telegram Bot) |
