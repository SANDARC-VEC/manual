# 응시자 등록

## ExamTools에서 세션 만들기

세션(들)의 날짜와 시간이 확정되면 [ExamTools](https://exam.tools)에서 해당 세션을 생성해야 합니다.
[ExamTools](https://exam.tools)는 여러분의 세션을 [HamStudy](https://hamstudy.org/)에 자동으로 게시하며, 응시자는 이곳에서 세션을 찾아 등록합니다.

[ExamTools](https://exam.tools)는 세션이 [HamStudy](https://hamstudy.org/)에 표시되는 방식을 설정할 수 있는 몇 가지 옵션을 제공합니다.
Please make use of these options to create a smooth user experience for your applicants.

!!! warning "13세 미만 응시자"
    13세 미만 응시자는 부모 또는 보호자가 ExamTools COPPA 부모 동의서를 제출하기 전까지
    [HamStudy](https://hamstudy.org/)에 등록할 수 없습니다. 미성년 응시자의 세션 일정을 잡기 전에
    [미성년자와 COPPA 절차](COPPA-and-Minors.md)를 참고하십시오.

!!! warning "알려진 버그"
    [ExamTools](https://exam.tools)는 기본적으로 SANDARC 세션 응시료를 `NaN`으로 설정합니다. 이는 알려진 버그입니다. Please manually reset this field to `0`.

### 세션 안내 사항

세션을 생성할 때 [ExamTools](https://exam.tools)는 두 개의 안내 사항 입력란을 제공합니다. These are the primary way
applicants learn the details of your session, so take the time to fill both out well.

**공개 안내 사항**은 [HamStudy](https://hamstudy.org/)의 세션 목록에 함께 표시되며, 등록하지 않은 사람을 포함해
누구나 볼 수 있습니다. 이 입력란은
[마크다운](https://www.markdownguide.org/)을 지원하므로 제목, 목록, 링크, 이미지를 사용할 수 있습니다(이미지는
외부에 호스팅되어 있어야 합니다). Include anything not already covered by the rest of the listing:

- Any special rules your session has (walk-in policy, arrival time, what to bring, calculator policy, etc.)
- A way for prospective applicants to contact your team, such as your team email address
- For remote sessions: the time and time zone again, links to instructions, and how to pay

\*\*응시자 안내 사항(이메일)\*\*은 응시자가 세션에 등록할 때 이메일로 발송됩니다. 등록하지 않은 사람에게는 절대
표시되지 않으므로, 원격 세션의 화상 회의 링크나 시험장 위치에 대한 구체적인 안내처럼 공개하기 어려운 정보를
기재하기에 적합합니다.

!!! warning "이메일 안내 사항은 공개 안내 사항을 대체하며, 추가되는 것이 아닙니다"
    이메일 안내 사항 입력란을 작성하면 공개 안내 사항 **대신** 해당 내용이 이메일로 발송됩니다. Copy over anything
    from the public notes that applicants need in their registration email. 이메일 안내 사항 입력란을 비워 두면
    공개 안내 사항이 이메일로 발송됩니다.

아래 템플릿은 각 입력란 작성을 위한 출발점입니다. Copy one, paste it into the matching field
in [ExamTools](https://exam.tools), and replace the bracketed placeholders with your team's information.

??? example "템플릿: 공개 안내 사항"

    `markdown     ![SANDARC](https://assets.sandarc.org/logo/current-logo.png)          Join [Your Club Name] for a ham license exam! 시험 응시나 자격 상향에는     어떠한 비용도 들지 않습니다.          Walk-ins are [welcome / not accepted] - please register for an FRN in     advance (or stop by and we can help!)          Questions? [team-email@example.org]     `

??? example "템플릿: 응시자 안내 사항(이메일)"

    `markdown     ![SANDARC](https://assets.sandarc.org/logo/current-logo.png)          This exam session is held at [location, with any specific directions:     building, room number, parking].          Questions? [team-email@example.org]          Please review these reminders:          1. Bring a pencil / pen / marking implement of your choice.     2. 다음 중 하나의 법적 사진 신분증을 지참하십시오: 주 운전면허증,        정부 발급 여권, 군인 또는 법 집행관 사진 신분증,        학생 사진 신분증, 주 사진 신분증.     3. 자격을 상향하는 경우, 현재 면허증 사본 또는        FCC CORES 시스템의 참조용 사본을 지참하십시오.     4. [클럽 이름]에서는 계산기를 제공하지 않습니다. Bring one if you        would prefer a physical calculator - an examiner must be able to        clear its memory. 온라인 시험 소프트웨어에는 디지털 계산기가        내장되어 있습니다.     `

Review your listing carefully before saving.

Please refer to [ExamTools Documentation](https://docs.exam.tools) to learn more about scheduling your sessions on [ExamTools](https://exam.tools).

[HamStudy](https://hamstudy.org/)와 연동된 [ExamTools](https://exam.tools)는 응시자를 등록할 수 있는 유일한 승인 플랫폼입니다.
Teams are encouraged to use other appropriate means to advertise their sessions such as your club's website and local nets,
in which case you should direct applicants to [HamStudy](https://hamstudy.org/) to register for your session.

## ARRL VEC 시험 세션 목록 등재

상당히 많은 응시자가 ARRL VEC 세션 목록을 이용해 지역 내 시험 세션을 찾습니다.
ARRL VEC는 호의적 조치로 ARRL 소속이 아닌 세션도 자체 웹사이트에 등재해 주며, 모든 팀이 이 기회를
적극 활용할 것을 권장합니다.
All you need to do is submit a [session registration form](https://www.arrl.org/non-arrl-exam-session-form) to the ARRL VEC.
It is best to submit your team email along with this form and when applicants get in touch with you, please direct them to your session
on [HamStudy](https://hamstudy.org/) to complete their registration.

## 현장 접수 응시자 등록

팀에서 현장 접수를 허용하는 경우, 해당 응시자도 다른 응시자와 마찬가지로 [HamStudy](https://hamstudy.org/)를 통해 등록해야 합니다.

[ExamTools](https://exam.tools)에는 [HamStudy](https://hamstudy.org/)를 거치지 않고 응시자를 세션에 직접 추가할 수 있는 기능이 있다는 점을 알아 두시기 바랍니다.
**Please refrain from using this feature unless under extenuating circumstances.**
Applicants must complete the entirety of the registration process on [HamStudy](https://hamstudy.org/) which entails agreeing to [ExamTools](https://exam.tools) ToS,
providing personal info, which later will be used on their form NCVEC 605 and answering the felony question.
또한 응시자의 신청서를 처리하려면 FRN이 있어야 합니다 — [FRN 발급받기](Getting-an-FRN.md)를 참조하십시오.
