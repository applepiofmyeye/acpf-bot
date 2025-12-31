const prompts = {
  zh: {
    welcome: "欢迎来到 ACPF。\n请选择您的语言：",
    languageChanged: "语言已更改为中文。",
    positioning: "ACPF 专注于协助美业高阶经营者突破瓶颈、建立系统。\n\n在推荐任何方案之前，我们会先了解你目前的阶段与需求。\n\n请回答以下问题，让我们为你提供最适合的方向。",
    startDiagnosis: "开始诊断",
    painQuestions: {
      q1: {
        question: "以下哪一个最接近你目前的状态？",
        options: {
          a: "技术很强，但生意始终卡在某个规模",
          b: "门店 / 团队有了，但无法复制与放大",
          c: "有名气，但缺乏系统与长期布局",
          d: "我已经在高位，但下一步方向不清楚"
        }
      },
      q2: {
        question: "你目前最困扰你的「不是技术」的问题是？",
        options: {
          a: "客源不稳定，靠运气",
          b: "团队无法独立运作",
          c: "收入有上限，时间被锁死",
          d: "有资源，但不会整合成体系"
        }
      },
      q3: {
        question: "如果这种状态再持续 2 年，你最担心什么？",
        options: {
          a: "生意停滞，被后来者超越",
          b: "永远只是老板，而不是平台",
          c: "影响力无法变现",
          d: "精力耗尽，却没有累积"
        }
      }
    },
    readinessQuestion: {
      question: "你目前对于解决这个问题的状态是？",
      options: {
        a: "我只是想先了解，还没准备好投入",
        b: "如果方向对，我愿意投入时间学习",
        c: "我已经在找方法，准备好采取行动",
        d: "我很清楚问题所在，需要系统化的方案"
      }
    },
    recommendStarter: {
      message: "根据你的情况，我们建议你从 ACPF Starter 开始。\n\nStarter 每两个月开班一次，帮助你建立系统思维的基础。",
      cta: "报名 Starter（RM588）",
      upsell: "申请 Core 评估"
    },
    recommendCore: {
      message: "根据你的经营阶段，你更适合进入 ACPF Core。\n\nCore 每年两次（7月与12月），专为准备突破瓶颈的高阶经营者设计。",
      cta: "报名 Core（RM5,997）"
    },
    upsellQuestions: {
      q1: {
        question: "你目前是否有团队或门店？",
        yes: "有",
        no: "没有"
      },
      q2: {
        question: "你目前更接近哪一种？",
        scale: "想复制放大（开分店/带团队）",
        foundation: "想建立系统（先打基础）"
      }
    },
    upsellApproved: "我们将为你安排 Core 人工确认，请留下资料。",
    upsellRejected: "从你目前阶段，Starter 会更稳。建议先从 Starter 开始。",
    backToStarter: "报名 Starter（RM588）",
    gateQuestion: "你是否曾参加过 ACPF Starter？",
    gateYes: "是",
    gateNo: "否",
    gateNoResponse: "Core 课程需要先完成 Starter 作为基础。\n\nStarter 每两个月开班一次，费用为 RM588。\n\n如果你准备好了，可以先报名 Starter。",
    registerStarter: "报名 Starter",
    form: {
      askName: "请输入你的全名：",
      askPhone: "请输入你的电话号码（WhatsApp）：",
      askEmail: "请输入你的电子邮箱（输入 skip 跳过）：",
      askBusinessType: "你目前从事什么类型的美业？",
      invalidName: "请输入有效的姓名。",
      invalidPhone: "请输入有效的电话号码。",
      invalidBusinessType: "请输入有效的业务类型。"
    },
    summary: "请确认你的资料：\n\n姓名：{name}\n电话：{phone}\n邮箱：{email}\n业务类型：{businessType}\n课程：{program}\n核心痛点：{painPoint}",
    confirm: "确认提交",
    edit: "重新填写",
    success: "你的报名已收到。\n\n我们的团队将尽快与你联系，协助你完成后续流程。",
    paymentInfo: `【付款资料】
公司名称： ACPF GROUP SDN. BHD.
ACC NO： 3211951736
BANK： PUBLIC BANK
Swift Code: PBBEMYKL

请完成转账后，将付款截图发送给负责人确认。
工作人员将协助你完成后续报名流程。`,
    error: "提交成功，但系统出现错误。管理员将会跟进处理。",
    sessionCleared: "你的会话已重置。输入 /start 重新开始。",
    languagePrompt: "请选择您的语言：",
    btnChinese: "中文",
    btnEnglish: "English"
  },
  en: {
    welcome: "Welcome to ACPF.\nPlease select your language:",
    languageChanged: "Language changed to English.",
    positioning: "ACPF focuses on helping high-level beauty industry operators break through bottlenecks and build systems.\n\nBefore recommending any program, we first understand your current stage and needs.\n\nPlease answer the following questions so we can provide the most suitable direction for you.",
    startDiagnosis: "Start Diagnosis",
    painQuestions: {
      q1: {
        question: "Which one best describes your current situation?",
        options: {
          a: "Strong technical skills, but business is stuck at a certain scale",
          b: "Have a shop / team, but unable to replicate and scale",
          c: "Have reputation, but lack systems and long-term structure",
          d: "Already at a high level, but unclear on the next direction"
        }
      },
      q2: {
        question: "What is the biggest non-technical problem troubling you right now?",
        options: {
          a: "Inconsistent client flow, relying on luck",
          b: "Team cannot operate independently",
          c: "Income has a ceiling, time is locked",
          d: "Have resources, but cannot integrate them into a system"
        }
      },
      q3: {
        question: "If this situation continues for another 2 years, what concerns you most?",
        options: {
          a: "Business stagnates, overtaken by newcomers",
          b: "Forever just a boss, never a platform",
          c: "Influence cannot be monetized",
          d: "Energy depleted, with no accumulation"
        }
      }
    },
    readinessQuestion: {
      question: "What is your current readiness to solve this problem?",
      options: {
        a: "I just want to understand first, not ready to commit",
        b: "If the direction is right, I am willing to invest time to learn",
        c: "I am already looking for solutions, ready to take action",
        d: "I am very clear about the problem, need a systematic solution"
      }
    },
    recommendStarter: {
      message: "Based on your situation, we recommend you start with ACPF Starter.\n\nStarter runs every two months, helping you build a foundation for systematic thinking.",
      cta: "Register Starter (RM588)",
      upsell: "Apply for Core Review"
    },
    recommendCore: {
      message: "Based on your business stage, you are better suited for ACPF Core.\n\nCore runs twice a year (July and December), designed for advanced operators ready to break through bottlenecks.",
      cta: "Register Core (RM5,997)"
    },
    upsellQuestions: {
      q1: {
        question: "Do you currently have a team or shop?",
        yes: "Yes",
        no: "No"
      },
      q2: {
        question: "Which describes you better?",
        scale: "Want to replicate and scale (open branches/lead team)",
        foundation: "Want to build systems (establish foundation first)"
      }
    },
    upsellApproved: "We will arrange a Core manual review for you. Please provide your details.",
    upsellRejected: "Based on your current stage, Starter would be more stable. We recommend starting with Starter first.",
    backToStarter: "Register Starter (RM588)",
    gateQuestion: "Have you attended ACPF Starter before?",
    gateYes: "Yes",
    gateNo: "No",
    gateNoResponse: "The Core program requires completing Starter as a foundation.\n\nStarter runs every two months at RM588.\n\nIf you are ready, you may register for Starter first.",
    registerStarter: "Register Starter",
    form: {
      askName: "Please enter your full name:",
      askPhone: "Please enter your phone number (WhatsApp):",
      askEmail: "Please enter your email (type 'skip' to skip):",
      askBusinessType: "What type of beauty business are you in?",
      invalidName: "Please enter a valid name.",
      invalidPhone: "Please enter a valid phone number.",
      invalidBusinessType: "Please enter a valid business type."
    },
    summary: "Please confirm your details:\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nBusiness Type: {businessType}\nProgram: {program}\nKey Pain Point: {painPoint}",
    confirm: "Confirm",
    edit: "Edit",
    success: `Your registration has been received.\n\nOur team will contact you shortly to assist with the next steps.
    \n\n[Payment Details]
Company Name: ACPF GROUP SDN. BHD.
Account No: 3211951736
Bank: PUBLIC BANK
Swift Code: PBBEMYKL
Amount: RM{amount}

After completing the transfer, please send your payment screenshot to the person in charge for confirmation.
Our staff will assist you with the remaining registration process.`,
    error: "Submitted successfully, but there was a system error. Admin will follow up.",
    sessionCleared: "Your session has been reset. Type /start to begin again.",
    languagePrompt: "Please select your language:",
    btnChinese: "🇨🇳 中文",
    btnEnglish: "🇬🇧 English"
  }
};
const painPointSummary = {
  q1: {
    a: { zh: "技术强但规模卡住", en: "Strong skills but stuck at scale" },
    b: { zh: "有团队但无法复制放大", en: "Have team but cannot scale" },
    c: { zh: "有名气但缺系统布局", en: "Have reputation but lack systems" },
    d: { zh: "高位但方向不清", en: "High level but unclear direction" }
  },
  q2: {
    a: { zh: "客源不稳定", en: "Inconsistent clients" },
    b: { zh: "团队无法独立", en: "Team cannot operate independently" },
    c: { zh: "收入有上限", en: "Income ceiling" },
    d: { zh: "资源无法整合", en: "Cannot integrate resources" }
  },
  q3: {
    a: { zh: "担心被超越", en: "Fear of being overtaken" },
    b: { zh: "永远只是老板", en: "Forever just a boss" },
    c: { zh: "影响力无法变现", en: "Influence cannot monetize" },
    d: { zh: "精力耗尽无累积", en: "Energy depleted no accumulation" }
  }
};

const scoringRules = {
  q1: { a: 'starter', b: 'core', c: 'core', d: 'core' },
  q2: { a: 'starter', b: 'core', c: 'core', d: 'core' },
  q3: { a: 'starter', b: 'core', c: 'core', d: 'core' },
  readiness: { a: 'starter', b: 'starter', c: 'core', d: 'core' }
};

const programLabels = {
  starter: "Starter",
  core: "Core",
  coreReview: "Core (Review)"
};

module.exports = { prompts, painPointSummary, scoringRules, programLabels };
