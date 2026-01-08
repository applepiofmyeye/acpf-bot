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
        "positioning": "ACPF 专注协助美业老板，从靠自己撑到「有系统、有团队、能长期运转」。\n\n在推荐任何课程前，我们会先了解你现在卡在哪一个阶段。\n\n请花 2 分钟回答以下问题，我们会给你最适合的方向。",
        "startDiagnosis": "开始诊断",
        "painQuestions": {
            "q1": {
                "question": "以下哪一项，最接近你目前的状态?",
                "options": {
                    "a": "技术没问题，但生意一直卡在一个规模",
                    "b": "有门店 / 团队，但很难复制、很难放大",
                    "c": "有知名度，但缺乏系统，走不远",
                    "d": "位置已经不低，但下一步方向不清楚",
                },
            },
            "q2": {
                "question": "如果不谈技术，你现在最头痛的是？",
                "options": {
                    "a": "客源时好时坏，很难稳定",
                    "b": "团队需要你一直看，无法独立",
                    "c": "收入有上限，时间被生意绑住",
                    "d": "明明很努力，但感觉一直在原地打转",
                },
            },
            "q3": {
                "question": "如果这样的状态再持续 2 年，你最担心的是？",
                "options": {
                    "a": "生意停在原地，被后来者追上",
                    "b": "永远只是老板，而不是平台",
                    "c": "有影响力，但无法真正变现",
                    "d": "人很累，但什么都没累积下来",
                },
            },
        },
        "readinessQuestion": {
            "question": "你目前对于解决这个问题的状态是？",
            "options": {
                "a": "我只是想先了解， 还没准备好投入",
                "b": "如果方向对，我愿意花时间学习",
                "c": "我已经在找方法，准备行动",
                "d": "我很清楚问题，需要一套系统化方案",
            },
        },
        "recommendStarter": {
            "message": "根据你的情况，我们建议你从 ACPF Starter 开始。\n\nStarter 每两个月开班一次，帮助你建立系统思维的基础。",
            "cta": "📝 报名 Starter（RM588）",
            "upsell": "🔎 申请 Core 评估",
        },
        "recommendCore": {
            "message": "看了你的情况，其实你已经不是新手了。\n现在卡住，不是你不努力，而是一个人撑太久了。\n\n这个阶段，再学零散技巧已经帮不大。\n你需要的是一套可以放大、生意能跑的系统。\n\n建议你直接报名 ACPF 新美业大学生意管理核心课程（RM5,997）。\n如果你准备好走下一步，现在就完成报名和付款，锁定名额。",
            "cta": "我要踏出第一步",
        },
        "upsellQuestions": {
            "q1": {
                "question": "你目前是否有团队或门店？",
                "yes": "✅ 有",
                "no": "❌ 没有",
            },
            "q2": {
                "question": "你目前更接近哪一个？",
                "scale": "打造可复制的门店 / 团队",
                "foundation": "建立一套长期可运转的系统",
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
            "disclaimer": "Disclaimer: 你的资料将用于新美业大学生意管理课程评估与联系安排。",
            "askName": "请输入你的全名：",
            "askPhone": "请输入你的电话号码（WhatsApp）：",
            "askEmail": "请输入你的电子邮箱：",
            "askBusinessType": "你目前从事什么类型的美业？",
            "invalidName": "请输入有效的姓名（至少2个字符）。",
            "invalidPhone": "请输入有效的电话号码（至少8位数字）。\n例如：+60123456789",
            "invalidEmail": "请输入有效的电子邮箱地址。\n例如：example@email.com",
            "invalidBusinessType": "请输入有效的业务类型。",
        },
        "summary": "请确认你的资料：\n\n姓名：{name}\n电话：{phone}\n邮箱：{email}\n业务类型：{businessType}\n课程：{program}\n核心痛点：{painPoint}",
        "confirm": "✅ 确认提交",
        "edit": "✏️ 编辑",
        "editMenu": "选择要编辑的字段：",
        "editName": "✏️ 编辑姓名",
        "editPhone": "✏️ 编辑电话",
        "editEmail": "✏️ 编辑邮箱",
        "editBusiness": "✏️ 编辑业务类型",
        "back": "← 返回",
        "reviewAnswers": "请检查你的答案：\n\n",
        "reviewQ1": "Q1: {answer}",
        "reviewQ2": "Q2: {answer}",
        "reviewQ3": "Q3: {answer}",
        "reviewQ4": "Q4: {answer}",
        "proceedToRecommendation": "✅ 继续推荐",
        "editAnswer": "编辑答案",
        "success": "你的课程申请已进入下一步。完成费用确认后，我们的团队将为你安排课程与相关说明。",
        "paymentInfo": """公司名称： ACPF GROUP SDN. BHD.
ACC NO： 3211951736
BANK： PUBLIC BANK
Swift Code: PBBEMYKL

提交报名后，我们将尽快与你联系。

届时请将转账付款截图发送给负责人进行确认，

确认完成后，我们会第一时间通知你相关课程安排与详细信息。""",
        "paymentButton": "付款资料",
        "error": "提交成功，但系统出现错误。管理员将会跟进处理。",
        "sessionCleared": "你的会话已重置。输入 /start 重新开始。",
        "languagePrompt": "请选择您的语言：",
        "btnChinese": "🇨🇳 中文",
        "btnEnglish": "🇬🇧 English",
    },
    "en": {
        "welcome": "Welcome to ACPF.\nPlease select your language:",
        "languageChanged": "Language changed to English.",
        "positioning": "ACPF helps beauty business owners move from doing everything alone to building systems, teams, and sustainable operations.\n\nBefore we recommend any program, we need to understand where you're currently stuck.\n\nTake 2 minutes to answer these questions, and we'll point you in the right direction.",
        "startDiagnosis": "Start Diagnosis",
        "painQuestions": {
            "q1": {
                "question": "Which one best describes your current situation?",
                "options": {
                    "a": "Have strong skills but stuck at scale",
                    "b": "Have a team but can't scale",
                    "c": "Have scale but lack systems",
                    "d": "Just unclear on next step",
                },
            },
            "q2": {
                "question": "If we don't talk about technical skills, what's your biggest headache right now?",
                "options": {
                    "a": "Client flow is unstable, relying on luck",
                    "b": "Team can't operate independently",
                    "c": "Income has a ceiling",
                    "d": "Resources can't be integrated",
                },
            },
            "q3": {
                "question": "If this situation continues for another 2 years, what concerns you most?",
                "options": {
                    "a": "I worry about being overtaken by newcomers",
                    "b": "I worry about being just a boss, not a platform",
                    "c": "I worry my influence can't be monetized",
                    "d": "I worry about burnout with no accumulation",
                },
            },
        },
        "readinessQuestion": {
            "question": "What is your current readiness to solve this problem?",
            "options": {
                "a": "I just want to understand first, not ready to commit",
                "b": "If the direction is right, I'm willing to invest time to learn",
                "c": "I'm already looking for methods, ready to take action",
                "d": "I'm very clear on the problem, need a systematic solution",
            },
        },
        "recommendStarter": {
            "message": "Based on your situation, we recommend you start with ACPF Starter.\n\nStarter runs every two months, helping you build a foundation for systematic thinking.",
            "cta": "📝 Register Starter (RM588)",
            "upsell": "🔎 Apply for Core Review",
        },
        "recommendCore": {
            "message": "Based on your answers, you're beyond the beginner stage.\n\nThe issue isn't your effort—it's that you've been going solo for too long.\n\nScattered tips won't help now. You need a scalable system that runs without you.\n\nWe recommend ACPF's New Beauty Business Management Core Program (RM5,997).\n\nReady to move forward? Complete registration and payment to secure your spot.",
            "cta": "I Want to Take the First Step",
        },
        "upsellQuestions": {
            "q1": {
                "question": "Do you currently have a team or shop?",
                "yes": "✅ Yes",
                "no": "❌ No",
            },
            "q2": {
                "question": "Which describes you better?",
                "scale": "Build replicable shop/team",
                "foundation": "Build a long-term sustainable system",
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
            "disclaimer": "Disclaimer: Your information will be used for the New Beauty Business Management Course evaluation and contact arrangement.",
            "askName": "Please enter your full name:",
            "askPhone": "Please enter your phone number (WhatsApp):",
            "askEmail": "Please enter your email:",
            "askBusinessType": "What type of beauty business are you in?",
            "invalidName": "Please enter a valid name (at least 2 characters).",
            "invalidPhone": "Please enter a valid phone number (at least 8 digits).\nExample: +60123456789",
            "invalidEmail": "Please enter a valid email address.\nExample: example@email.com",
            "invalidBusinessType": "Please enter a valid business type.",
        },
        "summary": "Please confirm your details:\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nBusiness Type: {businessType}\nProgram: {program}\nKey Pain Point: {painPoint}",
        "confirm": "✅ Confirm",
        "edit": "✏️ Edit",
        "editMenu": "Select field to edit:",
        "editName": "✏️ Edit Name",
        "editPhone": "✏️ Edit Phone",
        "editEmail": "✏️ Edit Email",
        "editBusiness": "✏️ Edit Business Type",
        "back": "← Back",
        "reviewAnswers": "Please review your answers:\n\n",
        "reviewQ1": "Q1: {answer}",
        "reviewQ2": "Q2: {answer}",
        "reviewQ3": "Q3: {answer}",
        "reviewQ4": "Q4: {answer}",
        "proceedToRecommendation": "✅ Proceed to Recommendation",
        "editAnswer": "Edit Answer",
        "success": "Your course application has entered the next step. After payment confirmation, our team will arrange the course and related information for you.",
        "paymentInfo": """Company Name: ACPF GROUP SDN. BHD.
Account No: 3211951736
Bank: PUBLIC BANK
Swift Code: PBBEMYKL

After submitting your registration, we will contact you as soon as possible.

Please send your payment screenshot to the person in charge for confirmation.

Once confirmed, we will notify you immediately about course arrangements and detailed information.""",
        "paymentButton": "Payment Details",
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
        if (
            answer
            and q_key in PAIN_POINT_SUMMARY
            and answer in PAIN_POINT_SUMMARY[q_key]
        ):
            parts.append(PAIN_POINT_SUMMARY[q_key][answer][lang])

    return " | ".join(parts) if parts else "-"
