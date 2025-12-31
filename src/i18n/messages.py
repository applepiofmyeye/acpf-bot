"""Bilingual messages for ACPF Bot."""

from typing import Any

# Welcome message (shown with image before language selection)
WELCOME_MESSAGE = {
    "zh": "ACPF 官方助理，用于美业老板的报名、资格筛选与后续对接。",
    "en": "Official ACPF assistant for beauty business owners. Registration, qualification, and program coordination.",
}

# All prompts organized by language
PROMPTS = {
    "zh": {
        "welcome": "欢迎来到 ACPF。\n请选择您的语言：",
        "languageChanged": "语言已更改为中文。",
        "positioning": "ACPF 专注于协助美业高阶经营者突破瓶颈、建立系统。\n\n在推荐任何方案之前，我们会先了解你目前的阶段与需求。\n\n请回答以下问题，让我们为你提供最适合的方向。",
        "startDiagnosis": "🚀 开始诊断",
        "painQuestions": {
            "q1": {
                "question": "📊 以下哪一个最接近你目前的状态？",
                "options": {
                    "a": "我技术很强，但规模一直卡住",
                    "b": "我有团队，但无法复制放大",
                    "c": "我有名气/规模，但缺乏系统",
                    "d": "我在高位，但下一步不清楚",
                },
            },
            "q2": {
                "question": "🔍 你目前最困扰的「非技术」问题是？",
                "options": {
                    "a": "我的客源不稳定，靠运气",
                    "b": "我的团队无法独立运作",
                    "c": "我的收入有上限，时间被锁",
                    "d": "我有资源，但无法整合成体系",
                },
            },
            "q3": {
                "question": "⏰ 如果这状态再持续2年，你最担心什么？",
                "options": {
                    "a": "我担心生意停滞，被超越",
                    "b": "我担心永远只是老板",
                    "c": "我担心影响力无法变现",
                    "d": "我担心精力耗尽，没有累积",
                },
            },
        },
        "readinessQuestion": {
            "question": "💡 你目前解决这个问题的状态是？",
            "options": {
                "a": "我想先了解，还没准备投入",
                "b": "方向对的话，我愿意学习",
                "c": "我正在找方法，准备行动",
                "d": "我很清楚问题，需要方案",
            },
        },
        "recommendStarter": {
            "message": "根据你的情况，我们建议你从 ACPF Starter 开始。\n\nStarter 每两个月开班一次，帮助你建立系统思维的基础。",
            "cta": "📝 报名 Starter（RM588）",
            "upsell": "🔎 申请 Core 评估",
        },
        "recommendCore": {
            "message": "根据你的经营阶段，你更适合进入 ACPF Core。\n\nCore 每年两次（7月与12月），专为准备突破瓶颈的高阶经营者设计。",
            "cta": "📝 报名 Core（RM5,997）",
        },
        "upsellQuestions": {
            "q1": {
                "question": "你目前是否有团队或门店？",
                "yes": "✅ 有",
                "no": "❌ 没有",
            },
            "q2": {
                "question": "你目前更接近哪一种？",
                "scale": "📈 想复制放大",
                "foundation": "🏗️ 想建立系统",
            },
        },
        "upsellApproved": "我们将为你安排 Core 人工确认，请留下资料。",
        "upsellRejected": "从你目前阶段，Starter 会更稳。建议先从 Starter 开始。",
        "backToStarter": "📝 报名 Starter（RM588）",
        "gateQuestion": "你是否曾参加过 ACPF Starter？",
        "gateYes": "✅ 是",
        "gateNo": "❌ 否",
        "gateNoResponse": "Core 课程需要先完成 Starter 作为基础。\n\nStarter 每两个月开班一次，费用为 RM588。\n\n如果你准备好了，可以先报名 Starter。",
        "registerStarter": "📝 报名 Starter",
        "form": {
            "askName": "请输入你的全名：",
            "askPhone": "请输入你的电话号码（WhatsApp）：",
            "askEmail": "请输入你的电子邮箱（输入 skip 跳过）：",
            "askBusinessType": "你目前从事什么类型的美业？",
            "invalidName": "请输入有效的姓名（至少2个字符）。",
            "invalidPhone": "请输入有效的电话号码（至少8位数字）。\n例如：+60123456789",
            "invalidEmail": "请输入有效的电子邮箱地址。\n例如：example@email.com",
            "invalidBusinessType": "请输入有效的业务类型。",
        },
        "summary": "请确认你的资料：\n\n姓名：{name}\n电话：{phone}\n邮箱：{email}\n业务类型：{businessType}\n课程：{program}\n核心痛点：{painPoint}",
        "confirm": "✅ 确认提交",
        "edit": "✏️ 重新填写",
        "success": """你的报名已收到。

我们的团队将尽快与你联系，协助你完成后续流程。

【付款资料】
公司名称： ACPF GROUP SDN. BHD.
ACC NO： 3211951736
BANK： PUBLIC BANK
Swift Code: PBBEMYKL
金额: RM{amount}

请完成转账后，将付款截图发送给负责人确认。
工作人员将协助你完成后续报名流程。""",
        "error": "提交成功，但系统出现错误。管理员将会跟进处理。",
        "sessionCleared": "你的会话已重置。输入 /start 重新开始。",
        "languagePrompt": "请选择您的语言：",
        "btnChinese": "🇨🇳 中文",
        "btnEnglish": "🇬🇧 English",
    },
    "en": {
        "welcome": "Welcome to ACPF.\nPlease select your language:",
        "languageChanged": "Language changed to English.",
        "positioning": "ACPF focuses on helping high-level beauty industry operators break through bottlenecks and build systems.\n\nBefore recommending any program, we first understand your current stage and needs.\n\nPlease answer the following questions so we can provide the most suitable direction for you.",
        "startDiagnosis": "🚀 Start Diagnosis",
        "painQuestions": {
            "q1": {
                "question": "📊 Which one best describes your current situation?",
                "options": {
                    "a": "I have strong skills but I'm stuck at scale",
                    "b": "I have a team but can't replicate or scale",
                    "c": "I have reputation/scale but lack systems",
                    "d": "I'm at a high level but unclear on next step",
                },
            },
            "q2": {
                "question": "🔍 What is your biggest non-technical problem?",
                "options": {
                    "a": "My client flow is unstable, relying on luck",
                    "b": "My team can't operate independently",
                    "c": "My income has a ceiling, time is locked",
                    "d": "I have resources but can't integrate them",
                },
            },
            "q3": {
                "question": "⏰ If this continues for 2 years, what concerns you most?",
                "options": {
                    "a": "I worry about being overtaken by newcomers",
                    "b": "I worry about being just a boss, not a platform",
                    "c": "I worry my influence can't be monetized",
                    "d": "I worry about burnout with no accumulation",
                },
            },
        },
        "readinessQuestion": {
            "question": "💡 What is your readiness to solve this problem?",
            "options": {
                "a": "I just want to understand first",
                "b": "I'm willing to learn if the direction is right",
                "c": "I'm actively looking for solutions",
                "d": "I'm clear on the problem, I need a plan",
            },
        },
        "recommendStarter": {
            "message": "Based on your situation, we recommend you start with ACPF Starter.\n\nStarter runs every two months, helping you build a foundation for systematic thinking.",
            "cta": "📝 Register Starter (RM588)",
            "upsell": "🔎 Apply for Core Review",
        },
        "recommendCore": {
            "message": "Based on your business stage, you are better suited for ACPF Core.\n\nCore runs twice a year (July and December), designed for advanced operators ready to break through bottlenecks.",
            "cta": "📝 Register Core (RM5,997)",
        },
        "upsellQuestions": {
            "q1": {
                "question": "Do you currently have a team or shop?",
                "yes": "✅ Yes",
                "no": "❌ No",
            },
            "q2": {
                "question": "Which describes you better?",
                "scale": "📈 Want to scale up",
                "foundation": "🏗️ Want to build systems",
            },
        },
        "upsellApproved": "We will arrange a Core manual review for you. Please provide your details.",
        "upsellRejected": "Based on your current stage, Starter would be more stable. We recommend starting with Starter first.",
        "backToStarter": "📝 Register Starter (RM588)",
        "gateQuestion": "Have you attended ACPF Starter before?",
        "gateYes": "✅ Yes",
        "gateNo": "❌ No",
        "gateNoResponse": "The Core program requires completing Starter as a foundation.\n\nStarter runs every two months at RM588.\n\nIf you are ready, you may register for Starter first.",
        "registerStarter": "📝 Register Starter",
        "form": {
            "askName": "Please enter your full name:",
            "askPhone": "Please enter your phone number (WhatsApp):",
            "askEmail": "Please enter your email (type 'skip' to skip):",
            "askBusinessType": "What type of beauty business are you in?",
            "invalidName": "Please enter a valid name (at least 2 characters).",
            "invalidPhone": "Please enter a valid phone number (at least 8 digits).\nExample: +60123456789",
            "invalidEmail": "Please enter a valid email address.\nExample: example@email.com",
            "invalidBusinessType": "Please enter a valid business type.",
        },
        "summary": "Please confirm your details:\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nBusiness Type: {businessType}\nProgram: {program}\nKey Pain Point: {painPoint}",
        "confirm": "✅ Confirm",
        "edit": "✏️ Edit",
        "success": """Your registration has been received.

Our team will contact you shortly to assist with the next steps.

[Payment Details]
Company Name: ACPF GROUP SDN. BHD.
Account No: 3211951736
Bank: PUBLIC BANK
Swift Code: PBBEMYKL
Amount: RM{amount}

After completing the transfer, please send your payment screenshot to the person in charge for confirmation.
Our staff will assist you with the remaining registration process.""",
        "error": "Submitted successfully, but there was a system error. Admin will follow up.",
        "sessionCleared": "Your session has been reset. Type /start to begin again.",
        "languagePrompt": "Please select your language:",
        "btnChinese": "🇨🇳 中文",
        "btnEnglish": "🇬🇧 English",
    },
}

# Pain point summaries for Google Sheets
PAIN_POINT_SUMMARY = {
    "q1": {
        "a": {"zh": "技术强但规模卡住", "en": "Strong skills but stuck at scale"},
        "b": {"zh": "有团队但无法复制放大", "en": "Have team but cannot scale"},
        "c": {"zh": "有名气但缺系统布局", "en": "Have reputation but lack systems"},
        "d": {"zh": "高位但方向不清", "en": "High level but unclear direction"},
    },
    "q2": {
        "a": {"zh": "客源不稳定", "en": "Inconsistent clients"},
        "b": {"zh": "团队无法独立", "en": "Team cannot operate independently"},
        "c": {"zh": "收入有上限", "en": "Income ceiling"},
        "d": {"zh": "资源无法整合", "en": "Cannot integrate resources"},
    },
    "q3": {
        "a": {"zh": "担心被超越", "en": "Fear of being overtaken"},
        "b": {"zh": "永远只是老板", "en": "Forever just a boss"},
        "c": {"zh": "影响力无法变现", "en": "Influence cannot monetize"},
        "d": {"zh": "精力耗尽无累积", "en": "Energy depleted no accumulation"},
    },
}


def get_text(key: str, lang: str = "en") -> str:
    """Get a text string by key and language."""
    return PROMPTS.get(lang, PROMPTS["en"]).get(key, key)


def get_nested_text(lang: str, *keys: str) -> Any:
    """Get nested text by following a path of keys."""
    result = PROMPTS.get(lang, PROMPTS["en"])
    for key in keys:
        if isinstance(result, dict):
            result = result.get(key, {})
        else:
            return ""
    return result


def build_pain_point_summary(pain_answers: dict, lang: str = "en") -> str:
    """Build a human-readable pain point summary from answers."""
    parts = []
    
    for q_key in ["q1", "q2", "q3"]:
        answer = pain_answers.get(q_key)
        if answer and q_key in PAIN_POINT_SUMMARY and answer in PAIN_POINT_SUMMARY[q_key]:
            parts.append(PAIN_POINT_SUMMARY[q_key][answer][lang])
    
    return " | ".join(parts) if parts else "-"

