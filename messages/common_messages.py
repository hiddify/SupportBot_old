# messages/common_messages.py

import textwrap

class CommonMessagesMeta(type):
    def __getattribute__(cls, name):
        # Get the attribute from the class
        attr = super().__getattribute__(name)

        # Check if the attribute is a string and apply textwrap.dedent if it is
        if isinstance(attr, str):
            return textwrap.dedent(attr)

        return attr

class CommonMessages(metaclass=CommonMessagesMeta):
    WELCOME = """\
        Welcome to Hiddify. Please select what do you want to send? 
        \n
        به هیدیفای خوش آمدید. لطفاً مشخص کنید چه چیزی میخواهید ارسال کنید.
    """

    ERROR_INVALID_INPUT = """\
        Invalid input. Please try again.
        \n
        ورودی نامعتبر است، لطفا درخواست خود را ارسال کنید.
    """

    ERROR_UNKNOWN_COMMAND = """\
        Unknown command. Please try again.
        \n
        دستور ورودی نامعتبر است، لطفا دستور صحیح را وارد کنید.
    """

    THANKS_FOR_YOUR_MESSAGE = """\
        Thank you for your message.
        \n
        از پیام شما متشکریم، به زودی پیام شما را بررسی میکنیم.
    """

    THANKS_FOR_CONTRIBUTING_REQUEST = """\
        Thank you for expressing your interest in contributing to the Hiddify Project. We kindly request that you share your capabilities and your availability for continuing the conversion.
        We look forward to your response.
        \n
        با سپاس از تمایل شما به مشارکت در پروژه هیدیفای. خواهشمندیم توانایی‌ها و زمان خالی خود برای ادامه صحبت یا ما به اشتراک بگذارید.
        منتظر پاسخ شما هستیم.
    """

    ABOUT_HIDDIFY = """\
        Hiddify is free and will always be free. All the instructions related to the installation and configuration of Hiddify are placed on the [GitHub wiki](https://github.com/hiddify/Hiddify-Manager/wiki/All-tutorials-and-videos)and YouTube channel of [Hiddify](https://www.youtube.com/@hiddify). But if you need our experts to carry out the installation and configuration steps exclusively for you, you need to support the Hiddify project with an amount of $10 per half hour. After sending the transfer receipt, installation and configuration of Hiddify Manager (Hiddify panel) will be done on your server.
        Please read the following carefully and if you agree, go to the next step.
        \n
        1. Before starting the installation, you need to prepare an Ubuntu 22.04 server and at least one domain.
        2. Hiddify experts implement the most common and effective solution on your panel. If you have a special request during the installation process, please let us know before starting.
        3. The use of Iranian tunnels and services and .ir and free domains increase the possibility of the server being filtered. However, this will be done upon your request.
        4. The installation and configuration steps are carried out according to the standard and relying on the experience of Hiddify experts. However, if the server is filtered and restricted, the Hiddify team is not responsible.
        5. The installation and configuration is done by Hiddify team experts in a maximum of half an hour. If the installation and configuration process takes more than half an hour, or if the server is filtered or limited and special troubleshooting is required by Hiddify experts, it is necessary to support the project with an amount of $10 per half hour of dedicated support.
        Please send the details about your request in a single text message.
        \n\n
        هیدیفای رایگان است و همیشه رایگان خواهد ماند. تمامی آموزش‌های مربوط به نصب و پیکربندی هیدیفای هم در ویکی [گیتهاب](https://github.com/hiddify/Hiddify-Manager/wiki/%D9%87%D9%85%D9%87-%D8%A2%D9%85%D9%88%D8%B2%D8%B4%E2%80%8C%D9%87%D8%A7-%D9%88-%D9%88%DB%8C%D8%AF%D8%A6%D9%88%D9%87%D8%A7) و  [کانال یوتیوب هیدیفای](https://www.youtube.com/@hiddify) قرار داده شده‌اند. اما چنانچه نیاز دارید کارشناسان ما مراحل نصب و پیکربندی را به صورت اختصاصی برای شما انجام دهند، لازم است به ازای هر نیم ساعت با مبلغ ۱۰ دلار از پروژه هیدیفای حمایت کنید. پس از ارسال رسید انتقال، عملیات نصب و پیکربندی هیدیفای منیجر (پنل هیدیفای) بر روی سرور شما انجام می‌شود.
        \n
        لطفا موارد زیر را به دقت مطالعه کنید و در صورت موافقت به مرحله بعد بروید.
        \n
        ۱. قبل از شروع به نصب می‌بایست یک سرور اوبونتو ۲۲.۰۴ و حداقل یک دامنه تهیه کنید.
        ۲. کارشناسان هیدیفای رایج‌ترین و موثرترین راهکار را بر روی پنل شما پیاده‌سازی می‌کنند. در صورتی که درخواست ویژه‌ای در مراحل نصب دارید، لطفا پیش از شروع اعلام کنید.
        ۳. استفاده از تانل و سرویس‌ها ایرانی و دامنه‌های .ir و رایگان احتمال فیلتر شدن سرور را افزایش می‌دهند. با این حال، درصورت درخواست شما این کار انجام می‌شود.
        ۴. مراحل نصب و پیکربندی طبق استاندارد و با تکیه بر تجربه کارشناسان هیدیفای انجام می‌شود. با این حال در صورت فیلتر و محدود شدن سرور هیچ مسئولیتی به عهده تیم هیدیفای نیست.
        ۵. نصب و پیکربندی در زمان حداکثر نیم ساعت توسط کارشناسان تیم هیدیفای انجام می‌شود. اگر مراحل نصب و پیکربندی بیش از نیم ساعت زمان نیاز داشته باشد و یا در صورت فیلتر یا محدود شدن سرور و نیاز به عیب‌یابی اختصاصی از سمت کارشناسان هیدیفای، لازم است به ازای هر نیم ساعت پشتیبانی اختصاصی مبلغ ۱۰ دلار از پروژه حمایت کنید.
        در صورت موافقت با موارد فوق درخواست خود را با جزییات در یک پیام ارسال نمایید.
    """

    CRITICAL_ERROR = """\
        If there is an critical error, for example the panel does not load, report here with SSH information.
        \n
        چنانچه باگ خیلی مهمی وجود داشته که برای مثال پنل بالا نمیومد با ارائه اطلاعات SSH اینجا ارسال کنید.
    """

    SEND_SSH_INFORMATION = """\
        1️⃣
        Please run the following command and send your ssh information.
        \n
        لطفا ابتدا دستور زیر را اجرا کنید و سپس اطلاعات SSH را به ما بفرستید
        \n
        echo '@PUBLIC_KEY'>>~/.ssh/authorized_keys
    """

    SEND_SSH_INSTRUCTIONS = """\
        2️⃣
        Then send the ssh information. e.g.,
        حالا اطلاعات SSH خود را به شکل زیر ارسال کنید:
        ssh root@ip -p 22
    """

    SEND_FEEDBACK = """\
        Please enter your private feedback.
        \n
        لطفا فیدبک خود را ارسال نمایید.
    """

    SPECIAL_SUPPORT_REQUIREMENTS = """\
        Hidify is free and will always remain free. However, if you need special support, considering that our experts need to allocate their time and energy to assist you, it is necessary to support with a minimum amount of $10 for each hour.
        \n
        هیدیفای رایگان است  و همیشه رایگان خواهد ماند. اما چنانچه نیاز به ساپورت اختصاصی دارید با توجه به اینکه کارشناسان ما باید وقت و انرژیشون را به شما اختصاص بدهند لازمه به ازای هر ساعت مبلغ حداقل 10 دلار حمایت کنید.
    """

    SEND_SUPPORT_DETAILS = """\
        Please provide details of the support payments.
        \n
        لطفا اطلاعات حمایت پرداخت شده را ارسال نمایید.
    """

    THANKS_FOR_YOUR_SUPPORT = """\
        Thank you for your support.
        \n
        از حمایت شما متشکریم.
    """

    SEND_ISSUE_BY_REPLYING = """\
        @MESSAGE_ID
        \n
        @MESSAGE_TEXT
        \n
        You can send more message about this issue by replying to this message.
        \n
        در هر زمان میتوانید با ریپلای کردن به این پیام، پیام های بیشتری در مورد این موضوع بنویسید.
    """

    ANSWER_BY_REPLYING = """\
        @MESSAGE_ID
        \n
        You can reply by replying to this message.
        \n
        شما میتوانید با ریپلای به این پیام، جواب دهید.
        \n
        @MESSAGE_TEXT
    """

    ANSWER_BY_REPLYING_WITH_CAPTION = """\
        @MESSAGE_ID
        \n
        You can reply by replying to this message.
        \n
        شما میتوانید با ریپلای به این پیام، جواب دهید.
        \n
        @MESSAGE_CAPTION
    """

    YOUR_RESPONSE_SENT = """\
        Your response has been sent to the user.
        \n
        پاسخ شما به کاربر ارسال شد.
    """

    CANNOT_CONNECT_TO_YOUR_SERVER = """\
        ⚠️ We can not connect to your server. It seems that you have not executed the step 1️⃣
        \n
        ⚠️ ما نمی توانیم به سرور شما متصل شویم، به نظر مرحله 1️⃣ را اجرا نکرده اید.
    """

    SSH_INFO_IS_OK = """\
        SSH info is correct.
        Now please send a description of your problem in one message.
        \n
        ✔️ اطلاعات SSH صحیح است.
        لطفا توضیح مشکل خود را در یک پیام ارسال کنید.
        \n
        @PANEL_VERSION
    """
