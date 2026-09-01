# 受験者の登録

## ExamTools でのセッション作成

セッションの日程と時刻が決まったら、[ExamTools](https://exam.tools) 上でこれらのセッション(s)を作成する必要があります。
[ExamTools](https://exam.tools) は作成したセッションを自動的に [HamStudy](https://hamstudy.org/) に掲載します。受験者はここでセッションを見つけて登録します。

[ExamTools](https://exam.tools) では、セッションを [HamStudy](https://hamstudy.org/) にどのように表示するかをカスタマイズできる複数のオプションが用意されています。
Please make use of these options to create a smooth user experience for your applicants.

!!! warning "13歳未満の受験者"
    13歳未満の受験者は、保護者が ExamTools の COPPA 保護者同意フォームを提出するまで
    [HamStudy](https://hamstudy.org/) に登録できません。 年少の受験者の日程を組む前に、
    [未成年者と COPPA の手続き](COPPA-and-Minors.md) を参照してください。

!!! warning "既知の不具合"
    [ExamTools](https://exam.tools) では、SANDARC のセッション料金が既定で `NaN` に設定されます。 これは既知の不具合です。 Please manually reset this field to `0`.

### セッションの注記

セッションを作成する際、[ExamTools](https://exam.tools) には二つの注記欄が用意されています。 These are the primary way
applicants learn the details of your session, so take the time to fill both out well.

**一般公開される注記** は [HamStudy](https://hamstudy.org/) のセッション掲載情報に表示され、未登録の人を含む
すべての人が閲覧できます。 この欄は
[Markdown](https://www.markdownguide.org/) に対応しているため、見出し、箇条書き、リンク、画像を使用できます（画像は
外部でホストする必要があります）。 Include anything not already covered by the rest of the listing:

- セッション独自の規定（当日受付の可否、集合時刻、持ち物、電卓の取り扱いなど）
- 受験希望者がチームに連絡する手段。たとえばチームのメールアドレスなど
- リモートセッションの場合：時刻とタイムゾーンの再掲、手順書へのリンク、支払い方法

**受験者向けの注記（メール）** は、受験者がセッションに登録した際にメールで送信されます。 未登録の人には一切
表示されないため、リモートセッションのビデオ会議リンクや会場までの詳しい道順など、公開に適さない情報は
こちらに記載します。

!!! warning "メール用の注記は公開注記を置き換えます — 追加されるのではありません"
    メール用注記欄に入力がある場合、公開注記の**代わりに**その内容がメール送信されます。 Copy over anything
    from the public notes that applicants need in their registration email. メール用注記欄を空欄にした場合は、
    代わりに公開注記がメール送信されます。

以下のテンプレートは、各欄を記入する際の出発点としてご利用ください。 Copy one, paste it into the matching field
in [ExamTools](https://exam.tools), and replace the bracketed placeholders with your team's information.

??? example "テンプレート：一般公開される注記"

    `markdown     ![SANDARC](https://assets.sandarc.org/logo/current-logo.png)          Join [Your Club Name] for a ham license exam! There are no fees to test     or upgrade your license.          Walk-ins are [welcome / not accepted] - please register for an FRN in     advance (or stop by and we can help!)          Questions? [team-email@example.org]     `

??? example "テンプレート：受験者向けの注記（メール）"

    `markdown     ![SANDARC](https://assets.sandarc.org/logo/current-logo.png)          This exam session is held at [location, with any specific directions:     building, room number, parking].          Questions? [team-email@example.org]          Please review these reminders:          1. Bring a pencil / pen / marking implement of your choice.     2. Bring one legal photo ID from this list: State Driver's License,        Government-issued Passport, Military or Law Enforcement Officer        Photo ID card, Student School Photo ID card, State Photo ID card.     3. 上級資格へのアップグレードの場合は、現在の免許のコピー、または        FCC CORES システムの参照用コピーをお持ちください。     4. [Your Club Name] では電卓の貸し出しは行っていません。 Bring one if you        would prefer a physical calculator - an examiner must be able to        clear its memory. オンライン試験ソフトウェアには、デジタル電卓が        内蔵されています。     `

保存する前に、掲載内容をよく確認してください。

[ExamTools](https://exam.tools) でのセッションのスケジュール設定について詳しくは、[ExamTools ドキュメント](https://docs.exam.tools)を参照してください。

[HamStudy](https://hamstudy.org/) と連携した [ExamTools](https://exam.tools) が、受験者を登録できる唯一の公認プラットフォームです。
各チームは、クラブのウェブサイトや地域のネットなど、他の適切な手段でセッションを告知することが推奨されます。
その場合は、受験者に [HamStudy](https://hamstudy.org/) でセッションに登録するよう案内してください。

## ARRL VEC のセッション一覧

多くの受験者が、地元の試験セッションを探すために ARRL VEC のセッション一覧を利用しています。
ARRL VEC は厚意により ARRL 以外のセッションも自らのウェブサイトに掲載しています。すべてのチームがこの機会を
活用することをお勧めします。
必要なのは、ARRL VEC に[セッション登録フォーム](https://www.arrl.org/non-arrl-exam-session-form)を提出することだけです。
このフォームにはチームのメールアドレスを併せて記載するのが望ましく、受験者から連絡があった際は、登録を完了できるよう
[HamStudy](https://hamstudy.org/) 上のご自分のセッションへ案内してください。

## 当日飛び込み受験者の登録

チームが当日の飛び込み受験を認めている場合でも、その受験者は他の受験者と同様に [HamStudy](https://hamstudy.org/) から登録する必要があります。

なお、[ExamTools](https://exam.tools) には [HamStudy](https://hamstudy.org/) を経由せずに受験者を直接セッションへ追加できる機能があります。
**やむを得ない事情がある場合を除き、この機能の使用は控えてください。**
受験者は [HamStudy](https://hamstudy.org/) 上で登録手続きをすべて完了する必要があります。この手続きには、[ExamTools](https://exam.tools) の利用規約への同意、
後に NCVEC 605 フォームで使用される個人情報の入力、および重罪に関する質問への回答が含まれます。
また、申請を処理するには受験者に FRN が必要です。[FRN の取得](Getting-an-FRN.md)を参照してください。
