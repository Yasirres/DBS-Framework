# نشر DBS Framework على GitHub

هذه الحزمة جاهزة محليًا. لم يُنشأ مستودع على حسابك، ولم يُرفع أي ملف أو يُنشر إصدار.

**نسبة المصدر:** هذه نسخة طوّرها صاحب هذا المستودع انطلاقًا من
[The DBS Framework Skill — AI Foundations](https://aifoundations.io/resources/the-dbs-framework-skill).
أكد صاحب المستودع أن AI Foundations لا تمانع النشر بشرط وضع رابط موقعها
والتصريح بأن هذه النسخة مطوّرة من عملها. أُضيف الرابط والنسبة في README
والملف الأساسي وبيان المصدر؛ حافظ عليها عند النشر. سُجّل الإذن بناءً على هذا
التأكيد. MIT يخص الأدوات الجديدة فقط؛ راجع [بيان المصدر](../ATTRIBUTION.md).

## 1. فتح الحساب وإنشاء المستودع

1. افتح [github.com](https://github.com/) وسجّل الدخول بنفسك.
2. افتح [إنشاء مستودع جديد](https://github.com/new).
3. اختر حسابك في Owner، واكتب الاسم `dbs-framework`.
4. ضع هذا الوصف في Description:

   `A platform-neutral framework for building reusable AI skills and workflows with Direction, Blueprints, and Solutions.`

5. اختر **Public** ليتمكن الآخرون من الاطلاع على المشروع واستخدامه.
6. لا تضف README أو .gitignore أو License من نموذج GitHub؛ الملفات موجودة في الحزمة.
7. اضغط **Create repository**. راجع [دليل GitHub الرسمي](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).

## 2. رفع الملفات

1. فك ضغط ملف الحزمة، ثم افتح المجلد الداخلي `dbs-framework`.
2. في صفحة المستودع الفارغ، اختر **uploading an existing file**، أو **Add file → Upload files** بعد وجود ملفات.
3. اسحب **محتويات** المجلد، وليس المجلد الخارجي نفسه، إلى منطقة الرفع.
4. تحقق أن `README.md` و`SKILL.md` يظهران في الجذر، وأن المجلدات `references` و`templates` و`scripts` و`tests` و`docs` محفوظة ببنيتها.
5. تحقق من وجود `.gitignore` و`.github/workflows/ci.yml`؛ قد تخفي إعدادات جهازك الأسماء التي تبدأ بنقطة. إذا لم يُرفع ملف، استخدم **Add file → Create new file**، واكتب مساره الكامل ثم انسخ محتواه من الحزمة.
6. اكتب رسالة الحفظ `Initial release: DBS Framework v1.0.0`، ثم **Commit changes**.

لا ترفع ZIP وحده بدل ملفات المشروع؛ يمكن إرفاق ZIP لاحقًا بالإصدار. هذه الحزمة
صغيرة وتناسب الرفع عبر المتصفح. [تعليمات رفع الملفات](https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository).

## 3. الوصف وTopics

من صفحة المستودع افتح إعدادات **About** بجوار الوصف، وأضف:

`ai-agents`، `agent-skills`، `claude`، `chatgpt`، `codex`، `ai-workflows`،
`automation`، `prompt-engineering`، `mcp`.

أدخل كل Topic كوسم مستقل ثم احفظ. الوصف قابل للتعديل من المكان نفسه.
[دليل Topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics).

## 4. التحقق بعد الرفع

1. افتح README وتحقق من عرض الجدول والروابط.
2. افتح تبويب **Actions** وتحقق من نجاح مهمة **Validate** على Linux وWindows.
3. إذا كانت Actions معطلة، راجع إعدادات المستودع وشغّل الاختبارات بعد تفعيلها إن رغبت. لا تعتبر مجرد رفع ملف CI دليلًا على نجاحه.
4. راجع LICENSE وATTRIBUTION.md. MIT يشمل الأدوات الجديدة المحددة فقط؛ لا يغيّر حقوق AI Foundations في المصدر. لا توسّعه ليشمل المحتوى المعدّل إلا بناءً على إذن مناسب. [نص MIT وشروطه](https://choosealicense.com/licenses/mit/).

## 5. إنشاء الإصدار v1.0.0

1. افتح **Releases** ثم **Draft a new release** أو **Create a new release**.
2. في اختيار Tag اكتب `v1.0.0` واختر إنشاء الوسم الجديد.
3. اختر الفرع الذي يحتوي النسخة المكتملة، وغالبًا `main`، وتحقق من نجاح اختباراته.
4. عنوان الإصدار: `DBS Framework v1.0.0`.
5. نص مقترح للإصدار:

```text
First public release of DBS Framework.

Unofficial adaptation of The DBS Framework Skill by AI Foundations:
https://aifoundations.io/resources/the-dbs-framework-skill
Credit for the original DBS framework belongs to AI Foundations.
Developed by this repository's maintainer from AI Foundations' original work.
See ATTRIBUTION.md and LICENSE for the recorded redistribution permission and scope.

- Platform-neutral Direction / Blueprints / Solutions core.
- Separate Claude, ChatGPT, and Codex adapters.
- Fast and Interactive working modes.
- Execution layer covering tools, integrations, APIs, scripts, and file generation.
- Templates, structural validator, safe scaffolder, tests, and documentation.

Validation: see docs/VALIDATION.md and the repository's Actions results.
Platform adapters are guidance; tools and permissions depend on the host.
```

6. يمكن إرفاق ZIP اختياريًا، وسيتيح GitHub أيضًا أرشيفًا للمصدر المرتبط بالوسم.
7. اترك **pre-release** غير محدد للإصدار المستقر، ثم اضغط **Publish release** عندما تكون مستعدًا للنشر العام.

احتفظ برابط المصدر ونسبة التطوير في نص الإصدار عند نشره.

[دليل الإصدارات الرسمي](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository).

## المساعدة من داخل Codex

بعد فتح GitHub وتسجيل الدخول، يمكنك طلب: «ساعدني في نشر هذه الحزمة على حسابي».
يمكن للمساعد متابعة الخطوات عبر المتصفح عندما تتاح أدواته. سجّل الدخول بنفسك،
وحدّد الحساب والرغبة بالنشر صراحةً قبل إنشاء المستودع أو تغيير بياناته أو رفع الملفات.
لا تشارك كلمة المرور في المحادثة.
